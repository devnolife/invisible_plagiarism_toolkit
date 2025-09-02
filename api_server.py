#!/usr/bin/env python3
"""
Invisible Plagiarism Toolkit - REST API Server
Advanced Multi-Layer Steganographic Document Processing API

Features:
- Complete steganography processing
- Turnitin trace removal
- Neural paraphrasing
- PDF processing
- File upload/download
- Real-time processing status

Author: DevNoLife
Version: 2.0 API Server
"""

import os
import asyncio
import uuid
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from pathlib import Path
import traceback

# FastAPI and dependencies
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
import uvicorn

# Pydantic models
from pydantic import BaseModel, Field
from enum import Enum

# Environment and configuration
from dotenv import load_dotenv

# Import our modules
from hybrid_paraphraser import HybridParaphraser
from unicode_steganography import UnicodeSteg
from invisible_manipulator import InvisibleManipulator
from ai_quality_checker import AIQualityChecker
from pdf_turnitin_analyzer import PDFTurnitinAnalyzer
from pdf_direct_editor import PDFDirectEditor

# Load environment variables
load_dotenv()

# Configure logging
log_file = os.getenv('LOG_FILE', 'logs/api.log')
Path(log_file).parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
for directory in ['uploads', 'output', 'logs']:
    Path(directory).mkdir(exist_ok=True)

# FastAPI app
app = FastAPI(
    title="Invisible Plagiarism Toolkit API",
    description="Advanced Multi-Layer Steganographic Document Processing System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global variables for system components (lazy loading)
system_components = {
    'paraphraser': None,
    'unicode_steg': None,
    'invisible_manipulator': None,
    'ai_checker': None,
    'pdf_analyzer': None,
    'pdf_editor': None
}

# Processing jobs storage (in production, use Redis/database)
processing_jobs = {}

# Pydantic Models
class ProcessingMode(str, Enum):
    COMPLETE = "complete"
    PARAPHRASE_ONLY = "paraphrase_only"
    STEGANOGRAPHY_ONLY = "steganography_only"
    PDF_PROCESSING = "pdf_processing"
    TURNITIN_CLEANUP = "turnitin_cleanup"

class ProcessingIntensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

class ProcessTextRequest(BaseModel):
    text: str = Field(..., description="Text to process", min_length=10, max_length=50000)
    mode: ProcessingMode = Field(ProcessingMode.COMPLETE, description="Processing mode")
    intensity: ProcessingIntensity = Field(ProcessingIntensity.MEDIUM, description="Processing intensity")
    enable_ai_validation: bool = Field(True, description="Enable AI quality validation")
    remove_turnitin_traces: bool = Field(True, description="Remove Turnitin traces if found")

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ProcessingJob(BaseModel):
    job_id: str
    status: JobStatus
    mode: ProcessingMode
    created_at: datetime
    completed_at: Optional[datetime] = None
    progress: int = Field(0, ge=0, le=100)
    result: Optional[Dict] = None
    error: Optional[str] = None
    original_filename: Optional[str] = None
    output_files: List[str] = []

class ProcessingResult(BaseModel):
    success: bool
    job_id: str
    processing_time: float
    original_text: Optional[str] = None
    final_text: Optional[str] = None
    metrics: Dict
    effectiveness_score: int
    techniques_used: List[str]
    turnitin_traces_removed: bool = False
    ai_quality_score: float = 0.0

class SystemStatus(BaseModel):
    status: str
    version: str
    components_loaded: Dict[str, bool]
    active_jobs: int
    total_processed: int
    system_uptime: str
    features_enabled: Dict[str, bool]

# Helper functions
def get_system_component(component_name: str):
    """Get or initialize system component"""
    if system_components[component_name] is None:
        try:
            if component_name == 'paraphraser':
                system_components[component_name] = HybridParaphraser(
                    enable_t5=os.getenv('ENABLE_T5_PARAPHRASING', 'true').lower() == 'true',
                    verbose=False
                )
            elif component_name == 'unicode_steg':
                system_components[component_name] = UnicodeSteg()
            elif component_name == 'invisible_manipulator':
                system_components[component_name] = InvisibleManipulator(verbose=False)
            elif component_name == 'ai_checker':
                api_key = os.getenv('GEMINI_API_KEY')
                system_components[component_name] = AIQualityChecker(
                    api_key=api_key if api_key else None,
                    verbose=False
                )
            elif component_name == 'pdf_analyzer':
                system_components[component_name] = PDFTurnitinAnalyzer()
            elif component_name == 'pdf_editor':
                system_components[component_name] = PDFDirectEditor()
                
            logger.info(f"✅ Initialized {component_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize {component_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize {component_name}")
    
    return system_components[component_name]

def create_job_id() -> str:
    """Generate unique job ID"""
    return f"job_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"

def update_job_progress(job_id: str, progress: int, status: JobStatus = None):
    """Update job progress"""
    if job_id in processing_jobs:
        processing_jobs[job_id]['progress'] = progress
        if status:
            processing_jobs[job_id]['status'] = status
        logger.debug(f"Job {job_id} progress: {progress}%")

# API Endpoints

@app.get("/", summary="API Root")
async def root():
    """API root endpoint"""
    return {
        "message": "Invisible Plagiarism Toolkit API v2.0",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", summary="Health Check")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.get("/status", response_model=SystemStatus, summary="System Status")
async def get_system_status():
    """Get comprehensive system status"""
    components_status = {}
    for name, component in system_components.items():
        components_status[name] = component is not None
    
    active_jobs = len([job for job in processing_jobs.values() if job['status'] in ['pending', 'processing']])
    
    features_enabled = {
        'turnitin_removal': os.getenv('ENABLE_TURNITIN_REMOVAL', 'true').lower() == 'true',
        't5_paraphrasing': os.getenv('ENABLE_T5_PARAPHRASING', 'true').lower() == 'true',
        'ai_validation': os.getenv('ENABLE_AI_VALIDATION', 'true').lower() == 'true',
        'unicode_steganography': os.getenv('ENABLE_UNICODE_STEGANOGRAPHY', 'true').lower() == 'true',
        'invisible_chars': os.getenv('ENABLE_INVISIBLE_CHARS', 'true').lower() == 'true',
    }
    
    return SystemStatus(
        status="operational",
        version="2.0.0",
        components_loaded=components_status,
        active_jobs=active_jobs,
        total_processed=len(processing_jobs),
        system_uptime="Running",
        features_enabled=features_enabled
    )

@app.post("/process/text", response_model=ProcessingJob, summary="Process Text")
async def process_text(
    request: ProcessTextRequest,
    background_tasks: BackgroundTasks
):
    """Process text with steganography techniques"""
    job_id = create_job_id()
    
    # Create job
    job = {
        'job_id': job_id,
        'status': JobStatus.PENDING,
        'mode': request.mode,
        'created_at': datetime.now(),
        'completed_at': None,
        'progress': 0,
        'result': None,
        'error': None,
        'original_filename': None,
        'output_files': []
    }
    
    processing_jobs[job_id] = job
    
    # Add background task
    background_tasks.add_task(
        process_text_background, 
        job_id, 
        request.text, 
        request.mode, 
        request.intensity,
        request.enable_ai_validation
    )
    
    return ProcessingJob(**job)

async def process_text_background(
    job_id: str, 
    text: str, 
    mode: ProcessingMode, 
    intensity: ProcessingIntensity,
    enable_ai_validation: bool
):
    """Background task for text processing"""
    try:
        update_job_progress(job_id, 5, JobStatus.PROCESSING)
        start_time = datetime.now()
        
        result = {
            'original_text': text,
            'final_text': text,
            'metrics': {},
            'effectiveness_score': 0,
            'techniques_used': [],
            'turnitin_traces_removed': False,
            'ai_quality_score': 0.0
        }
        
        current_text = text
        
        if mode in [ProcessingMode.COMPLETE, ProcessingMode.PARAPHRASE_ONLY]:
            # Paraphrasing
            update_job_progress(job_id, 20)
            paraphraser = get_system_component('paraphraser')
            
            paraphrase_result = paraphraser.paraphrase_hybrid(current_text, "parallel")
            current_text = paraphrase_result.hybrid_paraphrase
            
            result['techniques_used'].append('neural_paraphrasing')
            result['metrics']['paraphrasing_method'] = paraphrase_result.best_method
            result['metrics']['paraphrasing_quality'] = max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 0
            
            update_job_progress(job_id, 50)
        
        if mode in [ProcessingMode.COMPLETE, ProcessingMode.STEGANOGRAPHY_ONLY]:
            # Unicode Steganography
            update_job_progress(job_id, 60)
            unicode_steg = get_system_component('unicode_steg')
            
            aggressiveness_map = {
                ProcessingIntensity.LOW: 0.05,
                ProcessingIntensity.MEDIUM: 0.15,
                ProcessingIntensity.HIGH: 0.25,
                ProcessingIntensity.EXTREME: 0.35
            }
            
            unicode_text, unicode_log = unicode_steg.apply_strategic_substitution(
                current_text, 
                aggressiveness=aggressiveness_map[intensity]
            )
            current_text = unicode_text
            
            result['techniques_used'].append('unicode_steganography')
            result['metrics']['unicode_substitutions'] = unicode_log['total_changes']
            
            update_job_progress(job_id, 75)
            
            # Invisible Characters
            invisible_manipulator = get_system_component('invisible_manipulator')
            
            invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
            injection_rate_map = {
                ProcessingIntensity.LOW: 0.1,
                ProcessingIntensity.MEDIUM: 0.3,
                ProcessingIntensity.HIGH: 0.5,
                ProcessingIntensity.EXTREME: 0.7
            }
            
            final_text = invisible_manipulator.insert_invisible_chars(
                current_text, 
                invisible_chars, 
                injection_rate_map[intensity]
            )
            current_text = final_text
            
            result['techniques_used'].append('invisible_characters')
            result['metrics']['invisible_chars_added'] = len(final_text) - len(unicode_text)
            
            update_job_progress(job_id, 85)
        
        # AI Quality Validation
        if enable_ai_validation and os.getenv('GEMINI_API_KEY'):
            update_job_progress(job_id, 90)
            ai_checker = get_system_component('ai_checker')
            
            try:
                assessment = ai_checker.assess_paraphrase_quality(
                    text, current_text, "Academic text processing"
                )
                result['ai_quality_score'] = assessment.overall_score
                result['techniques_used'].append('ai_validation')
            except Exception as e:
                logger.warning(f"AI validation failed: {e}")
        
        # Calculate effectiveness
        result['final_text'] = current_text
        result['effectiveness_score'] = min(95, len(result['techniques_used']) * 20 + 15)
        result['metrics']['processing_time'] = (datetime.now() - start_time).total_seconds()
        result['metrics']['length_change'] = len(current_text) - len(text)
        
        # Update job
        processing_jobs[job_id]['result'] = result
        processing_jobs[job_id]['completed_at'] = datetime.now()
        update_job_progress(job_id, 100, JobStatus.COMPLETED)
        
        logger.info(f"✅ Job {job_id} completed successfully")
        
    except Exception as e:
        error_msg = f"Processing failed: {str(e)}"
        logger.error(f"❌ Job {job_id} failed: {error_msg}")
        
        processing_jobs[job_id]['error'] = error_msg
        processing_jobs[job_id]['status'] = JobStatus.FAILED
        processing_jobs[job_id]['completed_at'] = datetime.now()

@app.post("/process/file", response_model=ProcessingJob, summary="Process File")
async def process_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    mode: ProcessingMode = Form(ProcessingMode.COMPLETE),
    intensity: ProcessingIntensity = Form(ProcessingIntensity.MEDIUM),
    enable_ai_validation: bool = Form(True),
    remove_turnitin_traces: bool = Form(True)
):
    """Process uploaded file (text or PDF)"""
    
    # Validate file
    max_size = int(os.getenv('MAX_FILE_SIZE_MB', 50)) * 1024 * 1024
    if len(await file.read()) > max_size:
        raise HTTPException(status_code=413, detail=f"File too large (max {os.getenv('MAX_FILE_SIZE_MB', 50)}MB)")
    
    await file.seek(0)  # Reset file pointer
    
    # Create job
    job_id = create_job_id()
    
    job = {
        'job_id': job_id,
        'status': JobStatus.PENDING,
        'mode': mode,
        'created_at': datetime.now(),
        'completed_at': None,
        'progress': 0,
        'result': None,
        'error': None,
        'original_filename': file.filename,
        'output_files': []
    }
    
    processing_jobs[job_id] = job
    
    # Save uploaded file
    upload_path = Path("uploads") / f"{job_id}_{file.filename}"
    with open(upload_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Add background task
    background_tasks.add_task(
        process_file_background,
        job_id,
        str(upload_path),
        mode,
        intensity,
        enable_ai_validation,
        remove_turnitin_traces
    )
    
    return ProcessingJob(**job)

async def process_file_background(
    job_id: str,
    file_path: str,
    mode: ProcessingMode,
    intensity: ProcessingIntensity,
    enable_ai_validation: bool,
    remove_turnitin_traces: bool
):
    """Background task for file processing"""
    try:
        update_job_progress(job_id, 5, JobStatus.PROCESSING)
        
        file_path_obj = Path(file_path)
        
        if file_path_obj.suffix.lower() == '.pdf':
            # PDF processing
            pdf_editor = get_system_component('pdf_editor')
            
            output_path = f"output/{job_id}_{file_path_obj.stem}_processed.pdf"
            
            if mode == ProcessingMode.TURNITIN_CLEANUP:
                # Turnitin cleanup only
                update_job_progress(job_id, 50)
                removal_stats = pdf_editor.remove_all_turnitin_traces(file_path, output_path)
                
                result = {
                    'success': removal_stats['processing_successful'],
                    'original_file': file_path,
                    'output_file': output_path,
                    'turnitin_traces_removed': True,
                    'turnitin_removal_stats': removal_stats,
                    'techniques_used': ['turnitin_cleanup']
                }
            else:
                # Full PDF processing
                update_job_progress(job_id, 30)
                edit_result = pdf_editor.edit_pdf_from_turnitin_analysis(
                    pdf_path=file_path,
                    turnitin_pdf_path=None,
                    output_path=output_path,
                    use_paraphrasing=(mode in [ProcessingMode.COMPLETE, ProcessingMode.PARAPHRASE_ONLY]),
                    paraphrase_intensity=intensity.value,
                    enable_ai_validation=enable_ai_validation,
                    remove_turnitin_traces=remove_turnitin_traces
                )
                
                result = {
                    'success': True,
                    'original_file': edit_result.original_file,
                    'output_file': edit_result.modified_file,
                    'metrics': {
                        'total_edits': edit_result.total_edits,
                        'unicode_substitutions': edit_result.unicode_substitutions,
                        'invisible_chars_added': edit_result.invisible_chars_added,
                        'pages_modified': edit_result.pages_modified,
                        'invisibility_score': edit_result.invisibility_score
                    },
                    'techniques_used': edit_result.techniques_used,
                    'turnitin_traces_removed': edit_result.turnitin_traces_removed,
                    'ai_quality_score': edit_result.ai_quality_score
                }
                
            update_job_progress(job_id, 90)
            
        else:
            # Text file processing
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Use text processing logic
            await process_text_background(
                job_id, text_content, mode, intensity, enable_ai_validation
            )
            return
        
        # Save output file info
        processing_jobs[job_id]['output_files'].append(output_path)
        processing_jobs[job_id]['result'] = result
        processing_jobs[job_id]['completed_at'] = datetime.now()
        update_job_progress(job_id, 100, JobStatus.COMPLETED)
        
        logger.info(f"✅ File processing job {job_id} completed")
        
    except Exception as e:
        error_msg = f"File processing failed: {str(e)}"
        logger.error(f"❌ Job {job_id} failed: {error_msg}\n{traceback.format_exc()}")
        
        processing_jobs[job_id]['error'] = error_msg
        processing_jobs[job_id]['status'] = JobStatus.FAILED
        processing_jobs[job_id]['completed_at'] = datetime.now()

@app.get("/job/{job_id}", response_model=ProcessingJob, summary="Get Job Status")
async def get_job_status(job_id: str):
    """Get processing job status"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return ProcessingJob(**processing_jobs[job_id])

@app.get("/job/{job_id}/result", summary="Get Job Result")
async def get_job_result(job_id: str):
    """Get processing job result"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    if job['status'] != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Job not completed (status: {job['status']})")
    
    return job['result']

@app.get("/job/{job_id}/download", summary="Download Processed File")
async def download_processed_file(job_id: str):
    """Download processed file"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    if job['status'] != JobStatus.COMPLETED or not job['output_files']:
        raise HTTPException(status_code=400, detail="No output file available")
    
    output_file = job['output_files'][0]
    if not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_file,
        media_type='application/octet-stream',
        filename=Path(output_file).name
    )

@app.get("/jobs", summary="List All Jobs")
async def list_jobs(status: Optional[JobStatus] = None, limit: int = 50):
    """List processing jobs"""
    jobs = list(processing_jobs.values())
    
    if status:
        jobs = [job for job in jobs if job['status'] == status]
    
    # Sort by creation time (newest first)
    jobs.sort(key=lambda x: x['created_at'], reverse=True)
    
    return {
        'total': len(jobs),
        'jobs': jobs[:limit]
    }

@app.delete("/job/{job_id}", summary="Delete Job")
async def delete_job(job_id: str):
    """Delete processing job and associated files"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    # Clean up files
    try:
        # Remove uploaded file
        upload_file = f"uploads/{job_id}_{job['original_filename']}"
        if os.path.exists(upload_file):
            os.remove(upload_file)
        
        # Remove output files
        for output_file in job['output_files']:
            if os.path.exists(output_file):
                os.remove(output_file)
                
    except Exception as e:
        logger.warning(f"Error cleaning up files for job {job_id}: {e}")
    
    # Remove job
    del processing_jobs[job_id]
    
    return {"message": f"Job {job_id} deleted successfully"}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("🚀 Starting Invisible Plagiarism Toolkit API Server...")
    logger.info("🔧 System initialization will occur on first request")

# Main execution
if __name__ == "__main__":
    host = os.getenv('API_HOST', 'localhost')
    port = int(os.getenv('API_PORT', 8000))
    debug = os.getenv('API_DEBUG', 'true').lower() == 'true'
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )