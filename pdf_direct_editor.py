# pdf_direct_editor.py
"""
PDF Direct Editor with Invisible Character Injection
Sistem untuk mengedit langsung PDF dengan teknik steganografi
Dapat mengaplikasikan invisible characters dan Unicode substitution pada PDF
"""

import os
import re
import json
import random
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
from dataclasses import dataclass
import logging

try:
    import fitz  # PyMuPDF - for direct PDF editing
    import pdfplumber
except ImportError as e:
    print(f"Missing PDF libraries. Install with: pip install PyMuPDF pdfplumber")
    raise e

from unicode_steganography import UnicodeSteg
from pdf_turnitin_analyzer import PDFTurnitinAnalyzer, FlaggedSection
from hybrid_paraphraser import HybridParaphraser
from contextual_paraphraser import ContextualParaphraser
from ai_quality_checker import AIQualityChecker

@dataclass
class PDFEditResult:
    original_file: str
    modified_file: str
    total_edits: int
    invisible_chars_added: int
    unicode_substitutions: int
    pages_modified: int
    invisibility_score: float
    techniques_used: List[str]
    paraphrased_sections: int = 0
    plagiarism_before: float = 0.0
    plagiarism_after: float = 0.0
    plagiarism_reduction: float = 0.0
    ai_quality_score: float = 0.0
    ai_validation_enabled: bool = False
    quality_issues: int = 0
    # Turnitin removal fields
    turnitin_traces_removed: bool = False
    turnitin_items_removed: int = 0
    turnitin_removal_stats: Dict = None

@dataclass
class TextEditTarget:
    text: str
    page_number: int
    coordinates: Tuple[float, float, float, float]  # x0, y0, x1, y1
    priority_level: int  # 1=highest, 5=lowest
    edit_type: str  # "unicode_sub", "invisible_chars", "both"

class PDFDirectEditor:
    def __init__(self, config_file: str = 'config.json', verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Initialize steganography modules
        self.unicode_steg = UnicodeSteg()
        self.turnitin_analyzer = PDFTurnitinAnalyzer(verbose=False)
        self.paraphraser = HybridParaphraser(enable_t5=True, verbose=False)
        self.contextual_paraphraser = ContextualParaphraser(verbose=False)
        self.ai_checker = AIQualityChecker(verbose=False)
        
        # Invisible characters for PDF injection
        self.invisible_chars = [
            '\u200B',  # Zero Width Space
            '\u200C',  # Zero Width Non-Joiner  
            '\u200D',  # Zero Width Joiner
            '\uFEFF',  # Zero Width No-Break Space
            '\u2060',  # Word Joiner
            '\u180E'   # Mongolian Vowel Separator
        ]
        
        # Statistics tracking
        self.edit_stats = {
            'total_edits': 0,
            'unicode_substitutions': 0,
            'invisible_chars_added': 0,
            'pages_modified': set()
        }
        
        self.logger.info("🔧 PDF Direct Editor initialized")
    
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(levelname)s] %(name)s: %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.logger.info(f"📋 Configuration loaded from {config_file}")
                return config
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_file}, using defaults")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "pdf_editing": {
                "unicode_substitution_rate": 0.15,
                "invisible_char_injection_rate": 0.08,
                "max_edits_per_page": 50,
                "preserve_formatting": True
            },
            "priority_targeting": {
                "headers": {"priority": 1, "techniques": ["unicode_sub", "invisible_chars"]},
                "flagged_text": {"priority": 1, "techniques": ["both"]},
                "academic_phrases": {"priority": 2, "techniques": ["unicode_sub"]},
                "normal_text": {"priority": 5, "techniques": ["invisible_chars"]}
            }
        }
    
    def edit_pdf_from_turnitin_analysis(self, pdf_path: str, turnitin_pdf_path: str = None, 
                                      output_path: str = None, 
                                      use_paraphrasing: bool = True,
                                      paraphrase_intensity: str = "high",
                                      enable_ai_validation: bool = True,
                                      remove_turnitin_traces: bool = True) -> PDFEditResult:
        """
        Edit PDF based on Turnitin analysis results with paraphrasing and Turnitin trace removal
        """
        self.logger.info(f"🎯 Starting comprehensive PDF cleaning and editing")
        
        # Step 0: Remove Turnitin traces first (if enabled)
        turnitin_removal_stats = {}
        if remove_turnitin_traces:
            self.logger.info("🧹 Removing all Turnitin traces from PDF...")
            
            # If input is Turnitin report PDF, clean it first
            if turnitin_pdf_path and os.path.exists(turnitin_pdf_path):
                temp_turnitin_path = turnitin_pdf_path.replace('.pdf', '_temp_cleaned.pdf')
                turnitin_removal_stats['turnitin_report_cleaned'] = self.remove_all_turnitin_traces(turnitin_pdf_path, temp_turnitin_path)
                turnitin_pdf_path = temp_turnitin_path
            
            # Clean the main document PDF
            temp_main_path = pdf_path.replace('.pdf', '_temp_cleaned.pdf') 
            turnitin_removal_stats['main_document_cleaned'] = self.remove_all_turnitin_traces(pdf_path, temp_main_path)
            pdf_path = temp_main_path
        
        # Step 1: Analyze Turnitin results (if available)
        analysis_result = None
        plagiarism_before = 0.0
        
        if turnitin_pdf_path and os.path.exists(turnitin_pdf_path):
            self.logger.info("🔍 Analyzing Turnitin results...")
            analysis_result = self.turnitin_analyzer.analyze_turnitin_pdf(turnitin_pdf_path)
            plagiarism_before = analysis_result.overall_similarity
        else:
            self.logger.info("📄 Processing PDF without Turnitin analysis - applying general steganography")
            # Create dummy analysis for general processing
            from pdf_turnitin_analyzer import TurnitinAnalysisResult, FlaggedSection
            analysis_result = TurnitinAnalysisResult(
                pdf_file=pdf_path,
                overall_similarity=0.0,
                flagged_sections=[],
                source_breakdown=[],
                processing_successful=True
            )
        
        # Step 2: Apply paraphrasing if requested
        paraphrased_sections = 0
        if use_paraphrasing:
            self.logger.info("📝 Applying intelligent paraphrasing...")
            paraphrased_sections = self.apply_paraphrasing_to_pdf(pdf_path, analysis_result, paraphrase_intensity)
            
            # Re-analyze after paraphrasing to estimate new score
            temp_analysis = self.turnitin_analyzer.analyze_turnitin_pdf(pdf_path)
        
        # Step 3: Create edit targets from flagged sections
        edit_targets = self.create_edit_targets_from_analysis(pdf_path, analysis_result)
        
        # Step 4: Apply invisible character edits to PDF
        result = self.apply_targeted_edits(pdf_path, edit_targets, output_path)
        
        # Update result with paraphrasing info
        result.paraphrased_sections = paraphrased_sections
        result.plagiarism_before = plagiarism_before
        result.ai_validation_enabled = enable_ai_validation
        
        # Add Turnitin removal stats to result
        if remove_turnitin_traces and turnitin_removal_stats:
            result.turnitin_traces_removed = True
            result.turnitin_removal_stats = turnitin_removal_stats
            
            # Calculate total Turnitin items removed
            total_turnitin_removed = 0
            for stats in turnitin_removal_stats.values():
                if isinstance(stats, dict):
                    total_turnitin_removed += (
                        stats.get('markers_removed', 0) + 
                        stats.get('highlights_removed', 0) + 
                        stats.get('watermarks_removed', 0) + 
                        stats.get('metadata_cleaned', 0)
                    )
            
            result.turnitin_items_removed = total_turnitin_removed
            self.logger.info(f"🧹 Total Turnitin traces removed: {total_turnitin_removed}")
        else:
            result.turnitin_traces_removed = False
            result.turnitin_items_removed = 0
        
        # AI Quality validation if enabled
        if enable_ai_validation and paraphrased_sections > 0:
            self.logger.info("🤖 Running AI quality validation...")
            result.ai_quality_score, result.quality_issues = self.validate_paraphrasing_quality(analysis_result)
        else:
            result.ai_quality_score = 0.0
            result.quality_issues = 0
        
        # Estimate final plagiarism after all edits
        plagiarism_reduction_bonus = 0
        if result.turnitin_traces_removed:
            plagiarism_reduction_bonus = min(10, result.turnitin_items_removed * 0.5)  # Bonus for removing traces
        
        result.plagiarism_after = max(0, plagiarism_before - (paraphrased_sections * 3.5) - (result.total_edits * 0.5) - plagiarism_reduction_bonus)
        result.plagiarism_reduction = result.plagiarism_before - result.plagiarism_after
        
        # Clean up temporary files if created
        if remove_turnitin_traces:
            try:
                if 'temp_main_path' in locals() and temp_main_path != pdf_path and os.path.exists(temp_main_path):
                    os.remove(temp_main_path)
                if 'temp_turnitin_path' in locals() and os.path.exists(temp_turnitin_path):
                    os.remove(temp_turnitin_path)
            except:
                pass
        
        return result
    
    def create_edit_targets_from_analysis(self, pdf_path: str, 
                                        analysis_result) -> List[TextEditTarget]:
        """
        Create edit targets from Turnitin analysis results
        """
        edit_targets = []
        
        # Load PDF for coordinate mapping
        doc = fitz.open(pdf_path)
        
        for section in analysis_result.flagged_sections:
            # Find text in PDF and get coordinates
            coordinates = self.find_text_coordinates(doc, section.text, section.page_number)
            
            if coordinates:
                # Determine edit type based on flagged type
                edit_type = self.determine_edit_type(section.flagged_type)
                priority = self.get_priority_level(section.flagged_type)
                
                target = TextEditTarget(
                    text=section.text,
                    page_number=section.page_number,
                    coordinates=coordinates,
                    priority_level=priority,
                    edit_type=edit_type
                )
                edit_targets.append(target)
        
        doc.close()
        
        # Sort by priority (highest first)
        edit_targets.sort(key=lambda x: x.priority_level)
        
        self.logger.info(f"🎯 Created {len(edit_targets)} edit targets")
        return edit_targets
    
    def find_text_coordinates(self, doc, search_text: str, 
                            page_number: int) -> Optional[Tuple[float, float, float, float]]:
        """
        Find coordinates of text in PDF
        """
        try:
            page = doc.load_page(page_number - 1)  # 0-indexed
            
            # Search for text (case insensitive, partial match)
            search_terms = search_text.split()[:5]  # First 5 words for matching
            search_query = ' '.join(search_terms)
            
            text_instances = page.search_for(search_query)
            if text_instances:
                # Return first match coordinates
                rect = text_instances[0]
                return (rect.x0, rect.y0, rect.x1, rect.y1)
            
            # Fallback: search word by word
            for word in search_terms:
                if len(word) > 3:  # Skip short words
                    instances = page.search_for(word)
                    if instances:
                        rect = instances[0]
                        return (rect.x0, rect.y0, rect.x1, rect.y1)
            
        except Exception as e:
            self.logger.warning(f"Error finding coordinates for '{search_text[:50]}...': {e}")
        
        return None
    
    def determine_edit_type(self, flagged_type: str) -> str:
        """Determine edit type based on flagged section type"""
        type_mapping = {
            "academic_pattern": "unicode_sub",
            "highlighted": "both", 
            "academic_phrase": "unicode_sub",
            "header": "both",
            "exact_match": "both"
        }
        return type_mapping.get(flagged_type, "invisible_chars")
    
    def get_priority_level(self, flagged_type: str) -> int:
        """Get priority level based on flagged type"""
        priority_mapping = {
            "highlighted": 1,
            "exact_match": 1,
            "academic_pattern": 2,
            "header": 2, 
            "academic_phrase": 3,
            "text_pattern_match": 4
        }
        return priority_mapping.get(flagged_type, 5)
    
    def apply_targeted_edits(self, pdf_path: str, edit_targets: List[TextEditTarget],
                           output_path: str = None) -> PDFEditResult:
        """
        Apply targeted edits to PDF
        """
        if output_path is None:
            name, ext = os.path.splitext(pdf_path)
            output_path = f"{name}_invisible_edited{ext}"
        
        self.logger.info(f"📝 Applying {len(edit_targets)} targeted edits to PDF")
        
        # Reset stats
        self.edit_stats = {
            'total_edits': 0,
            'unicode_substitutions': 0, 
            'invisible_chars_added': 0,
            'pages_modified': set()
        }
        
        # Open PDF for editing
        doc = fitz.open(pdf_path)
        techniques_used = []
        
        try:
            for i, target in enumerate(edit_targets):
                if i % 10 == 0:
                    self.logger.info(f"🔄 Processing edit {i+1}/{len(edit_targets)}")
                
                success = self.apply_single_edit(doc, target)
                if success:
                    self.edit_stats['total_edits'] += 1
                    self.edit_stats['pages_modified'].add(target.page_number)
                    
                    if target.edit_type not in techniques_used:
                        techniques_used.append(target.edit_type)
            
            # Save modified PDF
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            self.logger.info(f"💾 Modified PDF saved: {output_path}")
            
        finally:
            doc.close()
        
        # Calculate invisibility score
        invisibility_score = self.calculate_invisibility_score()
        
        result = PDFEditResult(
            original_file=pdf_path,
            modified_file=output_path,
            total_edits=self.edit_stats['total_edits'],
            invisible_chars_added=self.edit_stats['invisible_chars_added'],
            unicode_substitutions=self.edit_stats['unicode_substitutions'], 
            pages_modified=len(self.edit_stats['pages_modified']),
            invisibility_score=invisibility_score,
            techniques_used=techniques_used
        )
        
        self.logger.info(f"✅ PDF editing complete: {result.total_edits} edits applied")
        return result
    
    def apply_single_edit(self, doc, target: TextEditTarget) -> bool:
        """
        Apply single edit to PDF at specific coordinates
        """
        try:
            page = doc.load_page(target.page_number - 1)
            
            # Get text blocks in the area
            x0, y0, x1, y1 = target.coordinates
            
            # Expand search area slightly
            search_rect = fitz.Rect(x0-5, y0-5, x1+5, y1+5)
            text_dict = page.get_text("dict", clip=search_rect)
            
            modified_any = False
            
            for block in text_dict["blocks"]:
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"]
                        if not original_text.strip():
                            continue
                        
                        # Apply modifications based on edit type
                        modified_text = self.apply_text_modifications(
                            original_text, target.edit_type
                        )
                        
                        if modified_text != original_text:
                            # Replace text in PDF
                            success = self.replace_text_in_span(page, span, modified_text)
                            if success:
                                modified_any = True
            
            return modified_any
            
        except Exception as e:
            self.logger.warning(f"Error applying edit to target: {e}")
            return False
    
    def apply_text_modifications(self, text: str, edit_type: str) -> str:
        """
        Apply text modifications based on edit type
        """
        modified_text = text
        
        if edit_type in ["unicode_sub", "both"]:
            # Apply Unicode substitution
            modified_text = self.apply_unicode_substitution(modified_text)
        
        if edit_type in ["invisible_chars", "both"]:
            # Inject invisible characters
            modified_text = self.inject_invisible_characters(modified_text)
        
        return modified_text
    
    def apply_unicode_substitution(self, text: str) -> str:
        """Apply Unicode character substitution"""
        modified_text = text
        substitution_rate = self.config.get("pdf_editing", {}).get("unicode_substitution_rate", 0.15)
        
        # Use existing Unicode steganography
        for mapping_name, mapping in self.unicode_steg.mappings.items():
            for latin_char, unicode_char in mapping.items():
                if latin_char in modified_text and random.random() < substitution_rate:
                    # Replace some instances (not all to avoid patterns)
                    occurrences = [m.start() for m in re.finditer(re.escape(latin_char), modified_text)]
                    if occurrences:
                        # Replace random subset
                        replace_count = max(1, len(occurrences) // 3)
                        replace_positions = random.sample(occurrences, min(replace_count, len(occurrences)))
                        
                        # Replace from right to left to maintain indices
                        for pos in sorted(replace_positions, reverse=True):
                            modified_text = (modified_text[:pos] + 
                                           unicode_char + 
                                           modified_text[pos+len(latin_char):])
                            self.edit_stats['unicode_substitutions'] += 1
        
        return modified_text
    
    def inject_invisible_characters(self, text: str) -> str:
        """Inject invisible characters into text"""
        modified_text = text
        injection_rate = self.config.get("pdf_editing", {}).get("invisible_char_injection_rate", 0.08)
        
        # Strategic injection points
        injection_points = []
        
        # After punctuation
        for match in re.finditer(r'[.!?,:;]', text):
            if random.random() < injection_rate:
                injection_points.append(match.end())
        
        # Between words (spaces)
        for match in re.finditer(r'\s+', text):
            if random.random() < injection_rate * 0.5:  # Lower rate for word boundaries
                injection_points.append(match.start() + 1)
        
        # Apply injections from right to left
        for pos in sorted(injection_points, reverse=True):
            invisible_char = random.choice(self.invisible_chars)
            modified_text = modified_text[:pos] + invisible_char + modified_text[pos:]
            self.edit_stats['invisible_chars_added'] += 1
        
        return modified_text
    
    def detect_turnitin_markers(self, doc) -> List[Dict]:
        """
        Detect and locate Turnitin markers in PDF
        Mendeteksi berbagai tanda Turnitin seperti:
        - Similarity Index (e.g., "15% similarity")
        - Turnitin watermarks
        - Colored highlights/backgrounds
        - Turnitin metadata
        """
        turnitin_markers = []
        
        # Patterns untuk mendeteksi tanda Turnitin
        turnitin_patterns = [
            r'\d+%\s*(similarity|match)',
            r'turnitin',
            r'similarity\s*index',
            r'originality\s*report',
            r'grammarly',
            r'paper\s*id\s*:\s*\d+',
            r'submission\s*id\s*:\s*\d+',
            r'processed\s*on\s*\d',
            r'this\s*is\s*a\s*turnitin',
            r'generated\s*on\s*\d+/\d+/\d+',
            r'www\.turnitin\.com',
            r'©.*turnitin',
            r'similarity\s*by\s*source',
            r'publications\s*match',
            r'student\s*papers\s*match',
            r'internet\s*sources\s*match'
        ]
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get text blocks with detailed information
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].lower().strip()
                        
                        # Check for Turnitin patterns
                        for pattern in turnitin_patterns:
                            if re.search(pattern, text, re.IGNORECASE):
                                turnitin_markers.append({
                                    'page': page_num,
                                    'text': span["text"],
                                    'bbox': span["bbox"],
                                    'pattern': pattern,
                                    'type': 'text_marker',
                                    'font': span.get("font", ""),
                                    'size': span.get("size", 0)
                                })
                                self.logger.info(f"🎯 Found Turnitin marker: {text[:50]}...")
            
            # Detect colored backgrounds (often used for highlighting)
            self._detect_colored_backgrounds(page, page_num, turnitin_markers)
            
            # Detect watermarks
            self._detect_watermarks(page, page_num, turnitin_markers)
        
        return turnitin_markers
    
    def _detect_colored_backgrounds(self, page, page_num: int, markers_list: List[Dict]):
        """Detect colored backgrounds that might indicate Turnitin highlighting"""
        try:
            # Get drawing instructions
            drawings = page.get_drawings()
            
            for drawing in drawings:
                # Look for rectangles with colors (potential highlights)
                if drawing.get("type") == "re" and "fill" in drawing:
                    fill_color = drawing.get("fill")
                    
                    # Check if it's a highlight color (not white/black)
                    if fill_color and fill_color not in [0, 1, (1,1,1), (0,0,0)]:
                        markers_list.append({
                            'page': page_num,
                            'bbox': drawing.get("rect"),
                            'type': 'highlight',
                            'color': fill_color,
                            'pattern': 'colored_background'
                        })
        except Exception as e:
            self.logger.debug(f"Error detecting colored backgrounds: {e}")
    
    def _detect_watermarks(self, page, page_num: int, markers_list: List[Dict]):
        """Detect potential watermarks"""
        try:
            # Look for semi-transparent text or images
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].lower()
                        
                        # Check for watermark-like text
                        if (any(word in text for word in ['turnitin', 'similarity', 'originality']) 
                            and span.get("size", 12) > 20):  # Large text often indicates watermarks
                            
                            markers_list.append({
                                'page': page_num,
                                'text': span["text"],
                                'bbox': span["bbox"],
                                'type': 'watermark',
                                'pattern': 'large_text_watermark'
                            })
        except Exception as e:
            self.logger.debug(f"Error detecting watermarks: {e}")
    
    def remove_turnitin_markers(self, doc, markers: List[Dict]) -> int:
        """
        Remove detected Turnitin markers from PDF
        """
        removed_count = 0
        
        # Group markers by page for efficient processing
        markers_by_page = {}
        for marker in markers:
            page_num = marker['page']
            if page_num not in markers_by_page:
                markers_by_page[page_num] = []
            markers_by_page[page_num].append(marker)
        
        for page_num, page_markers in markers_by_page.items():
            page = doc[page_num]
            
            # Sort markers by position (bottom to top, right to left)
            # This ensures we don't affect positions when removing
            page_markers.sort(key=lambda x: (x['bbox'][3], x['bbox'][2]), reverse=True)
            
            for marker in page_markers:
                try:
                    success = self._remove_single_marker(page, marker)
                    if success:
                        removed_count += 1
                        self.logger.info(f"✂️ Removed Turnitin marker: {marker.get('text', marker['type'])[:30]}...")
                except Exception as e:
                    self.logger.warning(f"Failed to remove marker: {e}")
        
        return removed_count
    
    def _remove_single_marker(self, page, marker: Dict) -> bool:
        """Remove a single Turnitin marker"""
        marker_type = marker.get('type')
        bbox = fitz.Rect(marker['bbox'])
        
        if marker_type == 'text_marker':
            # Remove text by covering with white rectangle
            page.draw_rect(bbox, color=1, fill=1, width=0)
            return True
            
        elif marker_type == 'highlight':
            # Remove highlight by drawing white rectangle over it
            page.draw_rect(bbox, color=1, fill=1, width=0)
            return True
            
        elif marker_type == 'watermark':
            # Remove watermark text
            page.draw_rect(bbox, color=1, fill=1, width=0)
            return True
        
        return False
    
    def clean_pdf_metadata(self, doc) -> Dict[str, str]:
        """
        Clean Turnitin-related metadata from PDF
        """
        cleaned_metadata = {}
        original_metadata = doc.metadata
        
        # Turnitin metadata patterns to remove
        turnitin_metadata_patterns = [
            r'turnitin',
            r'similarity',
            r'originality',
            r'grammarly',
            r'plagiarism',
            r'www\.turnitin\.com'
        ]
        
        for key, value in original_metadata.items():
            if value:
                value_lower = str(value).lower()
                # Check if metadata contains Turnitin references
                contains_turnitin = any(re.search(pattern, value_lower, re.IGNORECASE) 
                                      for pattern in turnitin_metadata_patterns)
                
                if contains_turnitin:
                    cleaned_metadata[key] = ""
                    self.logger.info(f"🧹 Cleaned metadata field: {key}")
                else:
                    cleaned_metadata[key] = value
        
        # Set cleaned metadata
        doc.set_metadata(cleaned_metadata)
        
        return cleaned_metadata
    
    def remove_all_turnitin_traces(self, pdf_path: str, output_path: str = None) -> Dict:
        """
        Komprehensif menghapus semua jejak Turnitin dari PDF
        Main method untuk membersihkan PDF dari tanda-tanda Turnitin
        """
        if not output_path:
            name, ext = os.path.splitext(pdf_path)
            output_path = f"{name}_cleaned{ext}"
        
        removal_stats = {
            'markers_removed': 0,
            'highlights_removed': 0,
            'watermarks_removed': 0,
            'metadata_cleaned': 0,
            'processing_successful': False,
            'errors': []
        }
        
        try:
            # Open PDF
            doc = fitz.open(pdf_path)
            self.logger.info(f"🔍 Scanning PDF for Turnitin traces: {os.path.basename(pdf_path)}")
            
            # Step 1: Detect all Turnitin markers
            self.logger.info("🎯 Detecting Turnitin markers...")
            turnitin_markers = self.detect_turnitin_markers(doc)
            
            if turnitin_markers:
                self.logger.info(f"📍 Found {len(turnitin_markers)} Turnitin markers")
                
                # Categorize markers
                text_markers = [m for m in turnitin_markers if m['type'] == 'text_marker']
                highlights = [m for m in turnitin_markers if m['type'] == 'highlight']
                watermarks = [m for m in turnitin_markers if m['type'] == 'watermark']
                
                self.logger.info(f"   📝 Text markers: {len(text_markers)}")
                self.logger.info(f"   🎨 Highlights: {len(highlights)}")
                self.logger.info(f"   💧 Watermarks: {len(watermarks)}")
                
                # Step 2: Remove markers
                self.logger.info("✂️ Removing Turnitin markers...")
                removed_count = self.remove_turnitin_markers(doc, turnitin_markers)
                
                removal_stats['markers_removed'] = len(text_markers)
                removal_stats['highlights_removed'] = len(highlights)
                removal_stats['watermarks_removed'] = len(watermarks)
                
                self.logger.info(f"🧹 Successfully removed {removed_count} markers")
            else:
                self.logger.info("✅ No Turnitin markers detected")
            
            # Step 3: Clean metadata
            self.logger.info("🧹 Cleaning PDF metadata...")
            cleaned_metadata = self.clean_pdf_metadata(doc)
            
            # Count how many fields were cleaned
            original_metadata = doc.metadata
            cleaned_fields = sum(1 for k, v in original_metadata.items() 
                               if v and not cleaned_metadata.get(k))
            removal_stats['metadata_cleaned'] = cleaned_fields
            
            if cleaned_fields > 0:
                self.logger.info(f"🧹 Cleaned {cleaned_fields} metadata fields")
            else:
                self.logger.info("✅ No Turnitin metadata found")
            
            # Step 4: Remove annotations and comments that might contain Turnitin data
            self.logger.info("📝 Removing annotations...")
            annotations_removed = self._remove_turnitin_annotations(doc)
            
            # Step 5: Save cleaned PDF
            doc.save(output_path)
            doc.close()
            
            removal_stats['processing_successful'] = True
            self.logger.info(f"✅ Clean PDF saved: {os.path.basename(output_path)}")
            
            # Summary
            total_removed = (removal_stats['markers_removed'] + 
                           removal_stats['highlights_removed'] + 
                           removal_stats['watermarks_removed'] + 
                           removal_stats['metadata_cleaned'] + 
                           annotations_removed)
            
            self.logger.info(f"🎉 Turnitin cleanup complete! Total items removed: {total_removed}")
            
        except Exception as e:
            error_msg = f"Error cleaning PDF: {str(e)}"
            self.logger.error(error_msg)
            removal_stats['errors'].append(error_msg)
        
        return removal_stats
    
    def _remove_turnitin_annotations(self, doc) -> int:
        """Remove annotations and comments that might contain Turnitin references"""
        removed_count = 0
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            annotations = page.annots()
            for annot in annotations:
                try:
                    # Get annotation content
                    content = annot.info.get("content", "").lower()
                    title = annot.info.get("title", "").lower()
                    
                    # Check if annotation contains Turnitin references
                    turnitin_keywords = ['turnitin', 'similarity', 'originality', 'plagiarism']
                    if any(keyword in content or keyword in title for keyword in turnitin_keywords):
                        annot.delete()
                        removed_count += 1
                        self.logger.debug(f"Removed annotation: {content[:50]}...")
                        
                except Exception as e:
                    self.logger.debug(f"Error processing annotation: {e}")
        
        return removed_count
    
    def replace_text_in_span(self, page, span: dict, new_text: str) -> bool:
        """
        Replace text in specific span (advanced PDF editing)
        """
        try:
            # Get span properties
            bbox = fitz.Rect(span["bbox"])
            font = span.get("font", "Helvetica")
            fontsize = span.get("size", 12)
            color = span.get("color", 0)
            
            # Create text block to replace
            text_block = fitz.TextWriter(page.rect, color=color)
            text_block.append(bbox.tl, new_text, font=font, fontsize=fontsize)
            
            # Remove original text area (fill with white)
            page.draw_rect(bbox, color=1, fill=1, width=0)
            
            # Insert new text
            text_block.write_text(page)
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error replacing text in span: {e}")
            return False
    
    def apply_paraphrasing_to_pdf(self, pdf_path: str, analysis_result, intensity: str = "high") -> int:
        """
        Apply paraphrasing to flagged sections in PDF
        """
        paraphrased_count = 0
        doc = fitz.open(pdf_path)
        
        try:
            for section in analysis_result.flagged_sections:
                # Only paraphrase substantial academic patterns
                if (section.flagged_type in ['academic_pattern', 'academic_phrase'] 
                    and len(section.text.strip()) > 10):
                    
                    # Get paraphrased version using contextual paraphraser
                    paraphrase_result = self.contextual_paraphraser.batch_paraphrase_academic_text(section.text, intensity)
                    
                    if paraphrase_result['final_similarity_reduction'] > 15:  # Only if significant reduction
                        # Find and replace text in PDF
                        if self.replace_text_in_pdf(doc, section.text, paraphrase_result['paraphrased_text'], section.page_number):
                            paraphrased_count += 1
                            self.logger.info(f"📝 Paraphrased: {section.text[:50]}... → {paraphrase_result['paraphrased_text'][:50]}...")
            
            # Save changes
            doc.save(pdf_path)
            
        except Exception as e:
            self.logger.error(f"Error during paraphrasing: {e}")
        
        finally:
            doc.close()
        
        self.logger.info(f"✨ Paraphrased {paraphrased_count} sections")
        return paraphrased_count
    
    def validate_paraphrasing_quality(self, analysis_result) -> Tuple[float, int]:
        """
        Validate quality of paraphrased sections using AI
        Returns: (average_quality_score, total_issues)
        """
        paraphrase_results = []
        
        for section in analysis_result.flagged_sections:
            if section.flagged_type in ['academic_pattern', 'academic_phrase'] and len(section.text.strip()) > 10:
                # Get paraphrased version for comparison
                paraphrase_result = self.contextual_paraphraser.batch_paraphrase_academic_text(section.text, "high")
                paraphrase_results.append({
                    'original_text': section.text,
                    'paraphrased_text': paraphrase_result['paraphrased_text'],
                    'context': 'Academic research text'
                })
        
        if not paraphrase_results:
            return 0.0, 0
        
        # Run batch AI assessment
        assessment_results = self.ai_checker.batch_assess_quality(paraphrase_results)
        
        avg_score = assessment_results['summary']['average_quality_score']
        total_issues = sum(len(assess.flagged_issues) for assess in assessment_results['individual_assessments'])
        
        self.logger.info(f"🤖 AI validation complete: Avg score {avg_score:.2f}, {total_issues} issues found")
        
        return avg_score, total_issues
    
    def replace_text_in_pdf(self, doc, old_text: str, new_text: str, page_num: int) -> bool:
        """
        Replace specific text in PDF page
        """
        try:
            if page_num > len(doc):
                return False
            
            page = doc.load_page(page_num - 1)  # Convert to 0-based
            
            # Search for text
            text_instances = page.search_for(old_text.strip())
            
            for inst in text_instances:
                # Create new text block
                text_block = fitz.TextWriter(page.rect)
                
                # Get font info from original text (approximate)
                font = fitz.Font("helv")  # Default font
                fontsize = 11  # Default size
                
                # Clear old text area
                page.draw_rect(inst, color=1, fill=1, width=0)
                
                # Insert new text at same position
                text_block.append(inst.tl, new_text, font=font, fontsize=fontsize)
                text_block.write_text(page)
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error replacing text: {e}")
            return False
    
    def calculate_invisibility_score(self) -> float:
        """
        Calculate invisibility score based on edit statistics
        """
        total_edits = self.edit_stats['total_edits']
        if total_edits == 0:
            return 0.0
        
        # Unicode substitutions are highly invisible
        unicode_score = self.edit_stats['unicode_substitutions'] * 0.95
        
        # Invisible characters are completely invisible
        invisible_score = self.edit_stats['invisible_chars_added'] * 1.0
        
        total_score = unicode_score + invisible_score
        return min(total_score / total_edits, 1.0) * 100
    
    def create_edit_report(self, result: PDFEditResult, output_path: str):
        """Create detailed edit report"""
        from datetime import datetime
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "editing_session": {
                "original_file": result.original_file,
                "modified_file": result.modified_file,
                "total_edits": result.total_edits,
                "pages_modified": result.pages_modified,
                "techniques_used": result.techniques_used
            },
            "edit_breakdown": {
                "unicode_substitutions": result.unicode_substitutions,
                "invisible_chars_added": result.invisible_chars_added,
                "paraphrased_sections": result.paraphrased_sections,
                "invisibility_score": f"{result.invisibility_score:.2f}%"
            },
            "plagiarism_analysis": {
                "similarity_before": f"{result.plagiarism_before:.1f}%",
                "similarity_after": f"{result.plagiarism_after:.1f}%",
                "reduction_achieved": f"{result.plagiarism_reduction:.1f}%",
                "effectiveness_rating": "High" if result.plagiarism_reduction > 10 else "Medium" if result.plagiarism_reduction > 5 else "Low"
            },
            "ai_validation": {
                "enabled": result.ai_validation_enabled,
                "quality_score": f"{result.ai_quality_score:.2f}/1.0" if result.ai_validation_enabled else "N/A",
                "quality_issues": result.quality_issues,
                "quality_rating": "Excellent" if result.ai_quality_score >= 0.8 else "Good" if result.ai_quality_score >= 0.7 else "Acceptable" if result.ai_quality_score >= 0.6 else "Needs Review"
            },
            "effectiveness_metrics": {
                "edit_density": result.total_edits / result.pages_modified if result.pages_modified > 0 else 0,
                "steganography_ratio": result.unicode_substitutions / result.total_edits if result.total_edits > 0 else 0,
                "invisibility_ratio": result.invisible_chars_added / result.total_edits if result.total_edits > 0 else 0,
                "paraphrase_ratio": result.paraphrased_sections / result.total_edits if result.total_edits > 0 else 0
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📊 Edit report saved: {output_path}")

# Example usage and CLI interface
if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 3:
        print("Usage: python pdf_direct_editor.py <original_pdf> <turnitin_results_pdf> [output_pdf]")
        print("Example: python pdf_direct_editor.py input/thesis.pdf output/turnitin_result/result.pdf")
        sys.exit(1)
    
    original_pdf = sys.argv[1]
    turnitin_pdf = sys.argv[2]
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else None
    
    editor = PDFDirectEditor(verbose=True)
    
    try:
        print("\n🔧 Starting PDF Direct Editing...")
        result = editor.edit_pdf_from_turnitin_analysis(original_pdf, turnitin_pdf, output_pdf)
        
        print(f"\n✅ EDITING COMPLETE!")
        print(f"📁 Modified PDF: {result.modified_file}")
        print(f"\n📊 PLAGIARISM ANALYSIS:")
        print(f"🔴 Similarity Before: {result.plagiarism_before:.1f}%")
        print(f"🟢 Similarity After: {result.plagiarism_after:.1f}%")
        print(f"📉 Reduction Achieved: {result.plagiarism_reduction:.1f}%")
        print(f"\n🎯 EDIT SUMMARY:")
        print(f"📝 Paraphrased Sections: {result.paraphrased_sections}")
        print(f"🔤 Unicode Substitutions: {result.unicode_substitutions}")
        print(f"👻 Invisible Characters Added: {result.invisible_chars_added}")
        print(f"📄 Pages Modified: {result.pages_modified}")
        print(f"🎭 Invisibility Score: {result.invisibility_score:.2f}%")
        print(f"⚙️ Techniques Used: {', '.join(result.techniques_used)}")
        
        if result.ai_validation_enabled:
            print(f"\n🤖 AI QUALITY VALIDATION:")
            print(f"📊 Quality Score: {result.ai_quality_score:.2f}/1.0")
            print(f"⚠️ Issues Found: {result.quality_issues}")
            quality_rating = "Excellent" if result.ai_quality_score >= 0.8 else "Good" if result.ai_quality_score >= 0.7 else "Acceptable" if result.ai_quality_score >= 0.6 else "Needs Review"
            print(f"🎯 Quality Rating: {quality_rating}")
        
        # Create detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"output/analysis_reports/pdf_edit_report_{timestamp}.json"
        editor.create_edit_report(result, report_path)
        print(f"📊 Detailed report: {report_path}")
        
    except Exception as e:
        print(f"❌ Error editing PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)