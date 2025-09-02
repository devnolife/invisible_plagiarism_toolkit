# 🚀 Invisible Plagiarism Toolkit API Documentation

## Overview

REST API untuk sistem steganografi dan pemrosesan dokumen tingkat lanjut. API ini menyediakan endpoint untuk memproses teks dan dokumen dengan berbagai teknik steganografi, penghapusan jejak Turnitin, dan validasi kualitas AI.

## 🔧 Setup & Installation

### 1. Environment Setup

```bash
# Clone repository
git clone <repository_url>
cd invisible_plagiarism_toolkit

# Install API requirements
pip install -r requirements_api.txt

# Setup environment variables
cp .env.example .env
# Edit .env file dan tambahkan GEMINI_API_KEY
```

### 2. Environment Variables

```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
API_HOST=localhost
API_PORT=8000
API_DEBUG=true
MAX_FILE_SIZE_MB=50
```

### 3. Start Server

```bash
# Development mode
python api_server.py

# Production mode
uvicorn api_server:app --host 0.0.0.0 --port 8000

# With Docker (optional)
docker build -t steganography-api .
docker run -p 8000:8000 steganography-api
```

## 📋 API Endpoints

### System Status

#### `GET /health`
Check server health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-09-02T10:30:00Z",
  "version": "2.0.0"
}
```

#### `GET /status`
Get comprehensive system status.

**Response:**
```json
{
  "status": "operational",
  "version": "2.0.0",
  "components_loaded": {
    "paraphraser": true,
    "unicode_steg": true,
    "invisible_manipulator": true,
    "ai_checker": true,
    "pdf_analyzer": true,
    "pdf_editor": true
  },
  "active_jobs": 2,
  "total_processed": 15,
  "system_uptime": "Running",
  "features_enabled": {
    "turnitin_removal": true,
    "t5_paraphrasing": true,
    "ai_validation": true,
    "unicode_steganography": true,
    "invisible_chars": true
  }
}
```

### Text Processing

#### `POST /process/text`
Process text with steganography techniques.

**Request Body:**
```json
{
  "text": "Your Indonesian academic text here...",
  "mode": "complete",
  "intensity": "high",
  "enable_ai_validation": true,
  "remove_turnitin_traces": true
}
```

**Parameters:**
- `text` (string, required): Text to process (10-50,000 chars)
- `mode` (enum): Processing mode
  - `complete`: Full pipeline (paraphrasing + steganography + AI validation)
  - `paraphrase_only`: Neural paraphrasing only
  - `steganography_only`: Unicode + invisible chars only
  - `pdf_processing`: PDF-specific processing
  - `turnitin_cleanup`: Remove Turnitin traces only
- `intensity` (enum): Processing intensity
  - `low`: Conservative processing
  - `medium`: Balanced approach
  - `high`: Aggressive processing
  - `extreme`: Maximum effectiveness
- `enable_ai_validation` (boolean): Use AI quality checking
- `remove_turnitin_traces` (boolean): Remove Turnitin markers

**Response:**
```json
{
  "job_id": "job_abc123def456_1693654800",
  "status": "pending",
  "mode": "complete",
  "created_at": "2024-09-02T10:30:00Z",
  "progress": 0,
  "result": null,
  "error": null
}
```

### File Processing

#### `POST /process/file`
Process uploaded file (text or PDF).

**Request:** Multipart form data
- `file` (file, required): Text file (.txt, .md) or PDF file
- `mode` (string): Processing mode (same as text processing)
- `intensity` (string): Processing intensity
- `enable_ai_validation` (boolean): Enable AI validation
- `remove_turnitin_traces` (boolean): Remove Turnitin traces

**Response:** Same as text processing

### Job Management

#### `GET /job/{job_id}`
Get job status and progress.

**Response:**
```json
{
  "job_id": "job_abc123def456_1693654800",
  "status": "processing",
  "mode": "complete",
  "created_at": "2024-09-02T10:30:00Z",
  "completed_at": null,
  "progress": 75,
  "result": null,
  "error": null,
  "original_filename": "document.pdf",
  "output_files": []
}
```

#### `GET /job/{job_id}/result`
Get detailed processing results.

**Response:**
```json
{
  "original_text": "Original text content...",
  "final_text": "Processed text with steganography...",
  "metrics": {
    "paraphrasing_method": "hybrid_parallel",
    "paraphrasing_quality": 0.89,
    "unicode_substitutions": 12,
    "invisible_chars_added": 8,
    "processing_time": 45.2,
    "length_change": 15
  },
  "effectiveness_score": 82,
  "techniques_used": [
    "neural_paraphrasing",
    "unicode_steganography", 
    "invisible_characters",
    "ai_validation"
  ],
  "turnitin_traces_removed": true,
  "ai_quality_score": 0.85
}
```

#### `GET /job/{job_id}/download`
Download processed file.

**Response:** File download

#### `GET /jobs`
List all jobs with optional filtering.

**Query Parameters:**
- `status` (optional): Filter by status (pending, processing, completed, failed)
- `limit` (optional, default: 50): Maximum results

**Response:**
```json
{
  "total": 25,
  "jobs": [
    {
      "job_id": "job_abc123def456_1693654800",
      "status": "completed",
      "mode": "complete",
      "created_at": "2024-09-02T10:30:00Z",
      "original_filename": "document.pdf"
    }
  ]
}
```

#### `DELETE /job/{job_id}`
Delete job and cleanup files.

**Response:**
```json
{
  "message": "Job job_abc123def456_1693654800 deleted successfully"
}
```

## 🔧 Processing Modes

### Complete System (`complete`)
- ✅ Indonesian T5 neural paraphrasing
- ✅ 20,139 contextual synonyms
- ✅ Unicode character substitution
- ✅ Invisible character injection
- ✅ AI quality validation
- ✅ Turnitin trace removal

**Best for:** Maximum protection and effectiveness

### Paraphrase Only (`paraphrase_only`)
- ✅ T5 neural paraphrasing
- ✅ Contextual synonym replacement
- ✅ AI quality validation
- ❌ No steganographic modifications

**Best for:** Content improvement without hidden changes

### Steganography Only (`steganography_only`)
- ❌ No content paraphrasing
- ✅ Unicode character substitution
- ✅ Invisible character injection
- ❌ Minimal AI validation

**Best for:** Hidden modifications without content changes

### Turnitin Cleanup (`turnitin_cleanup`)
- ✅ Remove similarity percentages
- ✅ Remove Turnitin watermarks
- ✅ Remove colored highlights
- ✅ Clean PDF metadata
- ✅ Remove annotations
- ❌ No steganography

**Best for:** Cleaning Turnitin-marked documents

## 🎯 Processing Intensities

| Intensity | Unicode Sub Rate | Invisible Char Rate | Description |
|-----------|-----------------|-------------------|-------------|
| **Low** | 5% | 10% | Conservative, minimal changes |
| **Medium** | 15% | 30% | Balanced approach (recommended) |
| **High** | 25% | 50% | Aggressive processing |
| **Extreme** | 35% | 70% | Maximum effectiveness |

## 📊 Response Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | Success | Request successful |
| 201 | Created | Job created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 413 | Payload Too Large | File size exceeds limit |
| 422 | Validation Error | Request validation failed |
| 500 | Server Error | Internal processing error |

## 🚀 Usage Examples

### 1. Basic Text Processing

```bash
curl -X POST "http://localhost:8000/process/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Penelitian ini menganalisis pengaruh teknologi terhadap pendidikan.",
    "mode": "complete",
    "intensity": "high",
    "enable_ai_validation": true,
    "remove_turnitin_traces": true
  }'
```

### 2. PDF File Processing

```bash
curl -X POST "http://localhost:8000/process/file" \
  -F "file=@document.pdf" \
  -F "mode=turnitin_cleanup" \
  -F "intensity=medium" \
  -F "remove_turnitin_traces=true"
```

### 3. Check Job Status

```bash
curl -X GET "http://localhost:8000/job/job_abc123def456_1693654800"
```

### 4. Download Result

```bash
curl -X GET "http://localhost:8000/job/job_abc123def456_1693654800/download" \
  -o processed_document.pdf
```

## 🔐 Security & Rate Limiting

### API Key (Future Enhancement)
```bash
curl -H "Authorization: Bearer your_api_key" \
  "http://localhost:8000/process/text"
```

### File Size Limits
- Maximum file size: 50MB (configurable via `MAX_FILE_SIZE_MB`)
- Supported formats: PDF, TXT, MD

### Processing Limits
- Maximum text length: 50,000 characters
- Concurrent jobs: No hard limit (memory dependent)
- Job retention: 24 hours (configurable)

## 📱 Postman Collection

Import the provided `Invisible_Plagiarism_Toolkit_API.postman_collection.json` file:

1. Open Postman
2. Click Import
3. Select the JSON file
4. Set environment variable: `base_url = http://localhost:8000`
5. Optionally set your `GEMINI_API_KEY` for AI validation

### Test Scenarios Included:
- ✅ System health checks
- ✅ Complete text processing workflow
- ✅ File upload and processing
- ✅ Job status monitoring
- ✅ Result retrieval and download
- ✅ Performance testing
- ✅ Error handling validation

## 🔍 Monitoring & Logging

### Log Levels
- `DEBUG`: Detailed processing information
- `INFO`: General processing status
- `WARNING`: Non-critical issues
- `ERROR`: Processing failures

### Log Files
- API logs: `logs/api.log`
- Processing logs: Component-specific logging

### Metrics Tracking
- Job completion rates
- Processing times
- Error frequencies
- Component health status

## 🚨 Error Handling

### Common Error Responses

```json
{
  "detail": "Text too short for processing (minimum 10 characters)",
  "status_code": 400
}
```

```json
{
  "detail": "File too large (max 50MB)",
  "status_code": 413
}
```

```json
{
  "detail": "Job not found",
  "status_code": 404
}
```

### Retry Logic
- Implement exponential backoff for failed requests
- Monitor job status for completion
- Handle network timeouts gracefully

## 🎯 Best Practices

### 1. Job Monitoring
```javascript
// Poll job status until completion
async function waitForJobCompletion(jobId) {
  while (true) {
    const status = await fetch(`/job/${jobId}`).then(r => r.json());
    
    if (status.status === 'completed') {
      return await fetch(`/job/${jobId}/result`).then(r => r.json());
    } else if (status.status === 'failed') {
      throw new Error(status.error);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2s
  }
}
```

### 2. File Processing
```javascript
// Process file with progress monitoring
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('mode', 'complete');
formData.append('intensity', 'high');

const job = await fetch('/process/file', {
  method: 'POST',
  body: formData
}).then(r => r.json());

const result = await waitForJobCompletion(job.job_id);
console.log('Processing completed:', result);
```

### 3. Error Handling
```javascript
try {
  const response = await fetch('/process/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestData)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Processing failed');
  }
  
  const job = await response.json();
  // Continue with job monitoring...
  
} catch (error) {
  console.error('Processing error:', error.message);
  // Handle error appropriately
}
```

## 📚 Integration Examples

### Python Client
```python
import requests
import time
import json

class SteganographyAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def process_text(self, text, mode="complete", intensity="high"):
        response = requests.post(f"{self.base_url}/process/text", json={
            "text": text,
            "mode": mode,
            "intensity": intensity,
            "enable_ai_validation": True,
            "remove_turnitin_traces": True
        })
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, job_id, timeout=300):
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = requests.get(f"{self.base_url}/job/{job_id}").json()
            
            if status["status"] == "completed":
                result = requests.get(f"{self.base_url}/job/{job_id}/result")
                return result.json()
            elif status["status"] == "failed":
                raise Exception(status["error"])
            
            time.sleep(2)
        
        raise TimeoutError("Job did not complete within timeout")

# Usage
api = SteganographyAPI()
job = api.process_text("Your Indonesian text here...")
result = api.wait_for_completion(job["job_id"])
print("Processed text:", result["final_text"])
```

### JavaScript/Node.js Client
```javascript
const axios = require('axios');

class SteganographyAPI {
  constructor(baseURL = 'http://localhost:8000') {
    this.client = axios.create({ baseURL });
  }
  
  async processText(text, options = {}) {
    const response = await this.client.post('/process/text', {
      text,
      mode: options.mode || 'complete',
      intensity: options.intensity || 'high',
      enable_ai_validation: options.aiValidation !== false,
      remove_turnitin_traces: options.removeTurnitin !== false
    });
    return response.data;
  }
  
  async waitForCompletion(jobId, timeout = 300000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
      const { data: status } = await this.client.get(`/job/${jobId}`);
      
      if (status.status === 'completed') {
        const { data: result } = await this.client.get(`/job/${jobId}/result`);
        return result;
      } else if (status.status === 'failed') {
        throw new Error(status.error);
      }
      
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    throw new Error('Job timeout');
  }
}

// Usage
const api = new SteganographyAPI();
const job = await api.processText('Your Indonesian text here...');
const result = await api.waitForCompletion(job.job_id);
console.log('Processed text:', result.final_text);
```

## 🎉 Conclusion

API ini menyediakan akses lengkap ke sistem steganografi tingkat lanjut dengan:

- ✅ **RESTful Design**: Endpoint yang intuitif dan konsisten
- ✅ **Asynchronous Processing**: Job-based processing untuk file besar
- ✅ **Comprehensive Features**: Semua fitur sistem tersedia via API
- ✅ **Monitoring**: Real-time progress dan status tracking
- ✅ **Error Handling**: Response error yang jelas dan actionable
- ✅ **Documentation**: Dokumentasi lengkap dengan contoh
- ✅ **Testing**: Postman collection untuk testing komprehensif

**Ready for production use dengan skalabilitas dan reliability yang tinggi!**