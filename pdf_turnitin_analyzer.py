# pdf_turnitin_analyzer.py
"""
PDF Turnitin Result Analyzer
Sistem untuk mengenali dan menganalisis area yang ditandai dalam hasil PDF Turnitin
"""

import os
import re
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass
import logging

try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
except ImportError as e:
    print(f"Missing PDF libraries. Install with: pip install PyPDF2 pdfplumber PyMuPDF")
    raise e

@dataclass
class FlaggedSection:
    text: str
    page_number: int
    similarity_score: float
    source_url: str
    coordinates: Optional[Tuple[float, float, float, float]] = None
    flagged_type: str = "unknown"  # "header", "paragraph", "citation", "exact_match"

@dataclass
class TurnitinAnalysisResult:
    overall_similarity: float
    total_flagged_sections: int
    flagged_sections: List[FlaggedSection]
    source_breakdown: Dict[str, float]
    priority_areas: List[str]

class PDFTurnitinAnalyzer:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Known Turnitin patterns
        self.turnitin_patterns = self.load_turnitin_patterns()
        
        # Academic patterns yang sering dideteksi
        self.academic_patterns = [
            r'BAB\s+[IVX]+',
            r'PENDAHULUAN',
            r'METODE\s+PENELITIAN', 
            r'HASIL\s+PENELITIAN',
            r'KESIMPULAN',
            r'DAFTAR\s+PUSTAKA',
            r'Berdasarkan\s+data\s+yang\s+diperoleh',
            r'keputusan\s+pembelian',
            r'kualitas\s+produk'
        ]
    
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
    
    def load_turnitin_patterns(self) -> Dict:
        """Load known Turnitin detection patterns"""
        return {
            "color_indicators": {
                "high_similarity": ["rgb(255,0,0)", "#ff0000", "red"],
                "medium_similarity": ["rgb(255,165,0)", "#ffa500", "orange"],
                "low_similarity": ["rgb(255,255,0)", "#ffff00", "yellow"]
            },
            "similarity_score_patterns": [
                r'(\d+)%',
                r'SIMILARITY INDEX.*?(\d+)%',
                r'INTERNET SOURCES.*?(\d+)%'
            ],
            "source_patterns": [
                r'([\w\-]+\.[\w\-]+\.[\w\-]+)',  # URLs
                r'Submitted to (.*?)Student Paper',
                r'Internet Source'
            ]
        }
    
    def analyze_turnitin_pdf(self, pdf_path: str) -> TurnitinAnalysisResult:
        """
        Analyze Turnitin PDF result to identify flagged sections
        """
        self.logger.info(f"🔍 Analyzing Turnitin PDF: {pdf_path}")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Extract basic text and metadata
        text_content = self.extract_pdf_text(pdf_path)
        similarity_score = self.extract_similarity_score(text_content)
        source_breakdown = self.extract_source_breakdown(text_content)
        
        # Analyze flagged sections using multiple methods
        flagged_sections = []
        
        # Method 1: Text-based analysis
        text_flagged = self.analyze_text_patterns(text_content)
        flagged_sections.extend(text_flagged)
        
        # Method 2: Visual analysis (if available)
        visual_flagged = self.analyze_visual_elements(pdf_path)
        flagged_sections.extend(visual_flagged)
        
        # Method 3: Academic pattern detection
        academic_flagged = self.detect_academic_patterns(text_content)
        flagged_sections.extend(academic_flagged)
        
        # Priority analysis
        priority_areas = self.identify_priority_areas(flagged_sections)
        
        result = TurnitinAnalysisResult(
            overall_similarity=similarity_score,
            total_flagged_sections=len(flagged_sections),
            flagged_sections=flagged_sections,
            source_breakdown=source_breakdown,
            priority_areas=priority_areas
        )
        
        self.logger.info(f"✅ Analysis complete: {len(flagged_sections)} flagged sections found")
        return result
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract all text from PDF"""
        text_content = ""
        
        try:
            # Method 1: pdfplumber (most reliable for text)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
        except Exception as e:
            self.logger.warning(f"pdfplumber failed: {e}, trying PyPDF2")
            
            # Method 2: PyPDF2 (fallback)
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text_content += page.extract_text() + "\n"
            except Exception as e2:
                self.logger.error(f"Both PDF readers failed: {e2}")
                
        return text_content
    
    def extract_similarity_score(self, text: str) -> float:
        """Extract overall similarity score from PDF"""
        for pattern in self.turnitin_patterns["similarity_score_patterns"]:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                try:
                    score = float(match.group(1))
                    self.logger.info(f"📊 Similarity score found: {score}%")
                    return score
                except (ValueError, IndexError):
                    continue
        
        self.logger.warning("⚠️ Could not extract similarity score")
        return 0.0
    
    def extract_source_breakdown(self, text: str) -> Dict[str, float]:
        """Extract source breakdown from PDF"""
        sources = {}
        
        # Look for source patterns with percentages
        lines = text.split('\n')
        for i, line in enumerate(lines):
            # Pattern: domain.com 24%
            domain_match = re.search(r'([\w\-]+\.[\w\-]+\.[\w\-]+)\s*(\d+)%', line)
            if domain_match:
                domain = domain_match.group(1)
                percentage = float(domain_match.group(2))
                sources[domain] = percentage
                continue
            
            # Pattern: Submitted to University Name - X%
            submitted_match = re.search(r'Submitted to (.*?)\s+(\d+)%', line)
            if submitted_match:
                institution = submitted_match.group(1).strip()
                percentage = float(submitted_match.group(2))
                sources[f"Submitted to {institution}"] = percentage
                continue
        
        self.logger.info(f"📊 Found {len(sources)} source patterns")
        return sources
    
    def analyze_text_patterns(self, text: str) -> List[FlaggedSection]:
        """Analyze text for flagged patterns"""
        flagged_sections = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for academic patterns
            for pattern in self.academic_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    section = FlaggedSection(
                        text=line,
                        page_number=self.estimate_page_number(i, len(lines)),
                        similarity_score=0.0,  # Will be updated if found
                        source_url="text_pattern_match",
                        flagged_type="academic_pattern"
                    )
                    flagged_sections.append(section)
                    break
        
        return flagged_sections
    
    def analyze_visual_elements(self, pdf_path: str) -> List[FlaggedSection]:
        """Analyze visual elements (highlighted text, colors) using PyMuPDF"""
        flagged_sections = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Extract text with formatting info
                text_dict = page.get_text("dict")
                
                for block in text_dict["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                text = span["text"].strip()
                                if not text:
                                    continue
                                
                                # Check for color indicators (highlighting)
                                color = span.get("color", 0)
                                flags = span.get("flags", 0)
                                
                                # Red/highlighted text detection
                                if self.is_highlighted_text(color, flags):
                                    section = FlaggedSection(
                                        text=text,
                                        page_number=page_num + 1,
                                        similarity_score=0.0,
                                        source_url="visual_highlight",
                                        coordinates=(
                                            span["bbox"][0], span["bbox"][1],
                                            span["bbox"][2], span["bbox"][3]
                                        ),
                                        flagged_type="highlighted"
                                    )
                                    flagged_sections.append(section)
            
            doc.close()
            
        except Exception as e:
            self.logger.warning(f"Visual analysis failed: {e}")
        
        return flagged_sections
    
    def detect_academic_patterns(self, text: str) -> List[FlaggedSection]:
        """Detect common academic text patterns that Turnitin flags"""
        flagged_sections = []
        
        # Common Indonesian academic phrases
        academic_phrases = [
            "Berdasarkan hasil penelitian",
            "Dari hasil penelitian dapat disimpulkan",
            "Penelitian ini bertujuan untuk",
            "Metode penelitian yang digunakan",
            "Hasil penelitian menunjukkan",
            "keputusan pembelian konsumen",
            "kualitas produk dan layanan",
            "pengaruh signifikan terhadap"
        ]
        
        for phrase in academic_phrases:
            pattern = re.escape(phrase).replace(r'\ ', r'\s+')
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                context_start = max(0, match.start() - 100)
                context_end = min(len(text), match.end() + 100)
                context = text[context_start:context_end]
                
                section = FlaggedSection(
                    text=match.group(),
                    page_number=self.estimate_page_from_position(match.start(), text),
                    similarity_score=0.8,  # High probability for academic phrases
                    source_url="academic_pattern",
                    flagged_type="academic_phrase"
                )
                flagged_sections.append(section)
        
        return flagged_sections
    
    def is_highlighted_text(self, color: int, flags: int) -> bool:
        """Check if text is highlighted/flagged based on color and flags"""
        # Red color detection (Turnitin uses red for high similarity)
        if color == 0xFF0000 or color == 16711680:  # Red
            return True
        
        # Check for other highlighting indicators
        if flags & 2**4:  # Bold flag, often used for flagged text
            return True
        
        return False
    
    def estimate_page_number(self, line_index: int, total_lines: int) -> int:
        """Estimate page number based on line position"""
        lines_per_page = 50  # Rough estimate
        return (line_index // lines_per_page) + 1
    
    def estimate_page_from_position(self, position: int, text: str) -> int:
        """Estimate page number from character position"""
        chars_per_page = 2000  # Rough estimate
        return (position // chars_per_page) + 1
    
    def identify_priority_areas(self, flagged_sections: List[FlaggedSection]) -> List[str]:
        """Identify priority areas that need immediate attention"""
        priority_areas = []
        
        # Count by type
        type_counts = {}
        for section in flagged_sections:
            type_counts[section.flagged_type] = type_counts.get(section.flagged_type, 0) + 1
        
        # Prioritize by frequency and importance
        if type_counts.get("academic_pattern", 0) > 5:
            priority_areas.append("Academic headers and terminology")
        
        if type_counts.get("highlighted", 0) > 10:
            priority_areas.append("Visually highlighted sections")
        
        if type_counts.get("academic_phrase", 0) > 3:
            priority_areas.append("Common academic phrases")
        
        return priority_areas
    
    def save_analysis_report(self, result: TurnitinAnalysisResult, output_path: str):
        """Save analysis result to JSON file"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "overall_similarity": result.overall_similarity,
            "total_flagged_sections": result.total_flagged_sections,
            "source_breakdown": result.source_breakdown,
            "priority_areas": result.priority_areas,
            "flagged_sections": [
                {
                    "text": section.text[:200] + "..." if len(section.text) > 200 else section.text,
                    "page_number": section.page_number,
                    "similarity_score": section.similarity_score,
                    "source_url": section.source_url,
                    "flagged_type": section.flagged_type,
                    "coordinates": section.coordinates
                }
                for section in result.flagged_sections
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📄 Analysis report saved: {output_path}")

# Example usage
if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_turnitin_analyzer.py <path_to_turnitin_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    analyzer = PDFTurnitinAnalyzer(verbose=True)
    
    try:
        result = analyzer.analyze_turnitin_pdf(pdf_path)
        
        print("\n🔍 TURNITIN ANALYSIS RESULTS:")
        print(f"📊 Overall Similarity: {result.overall_similarity}%")
        print(f"🎯 Total Flagged Sections: {result.total_flagged_sections}")
        print(f"📋 Priority Areas: {', '.join(result.priority_areas)}")
        
        print("\n📊 TOP SOURCES:")
        for source, percentage in sorted(result.source_breakdown.items(), 
                                      key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {source}: {percentage}%")
        
        print("\n🎯 FLAGGED SECTIONS (Top 10):")
        for i, section in enumerate(result.flagged_sections[:10], 1):
            print(f"  {i}. [{section.flagged_type}] Page {section.page_number}: {section.text[:100]}...")
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"output/analysis_reports/turnitin_analysis_{timestamp}.json"
        analyzer.save_analysis_report(result, report_path)
        
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")
        sys.exit(1)