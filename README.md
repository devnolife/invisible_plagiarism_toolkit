# 🕵️ Invisible Plagiarism Toolkit - Complete Steganography System

**Advanced Multi-Layer Steganographic Document Manipulation System**

A comprehensive toolkit combining **Indonesian T5 Neural Paraphrasing**, **20,139 Contextual Synonyms Database**, **Unicode Steganography**, **Invisible Character Injection**, **PDF Analysis & Direct Editing**, and **AI Quality Validation** for advanced document manipulation and plagiarism detection evasion.

## 🚀 Complete System Features

### 🧠 Neural Paraphrasing System
- **Indonesian T5 Model**: Advanced neural sentence restructuring using `Wikidepia/IndoT5-base-paraphrase`
- **Contextual Synonyms**: 20,139 Indonesian synonyms with academic context awareness
- **Hybrid Intelligence**: Automatic selection between T5 neural and contextual approaches
- **Quality Scoring**: Real-time assessment of paraphrase naturalness and meaning preservation

### 🔤 Unicode Steganography
- **Multi-Script Substitution**: Latin → Cyrillic, Greek, Mathematical symbols
- **Academic Term Targeting**: Strategic replacement of Indonesian academic vocabulary
- **Connector Word Processing**: Smart handling of common Indonesian connecting words
- **Invisibility Optimization**: Up to 95% visual similarity with technical differences

### 👻 Invisible Character Injection
- **6 Character Types**: Zero-width spaces, joiners, non-joiners, Mongolian separators
- **Strategic Placement**: Context-aware injection after punctuation and word boundaries
- **Rate Control**: Configurable injection density with detection avoidance

### 📄 PDF Processing Capabilities
- **Turnitin Analysis**: Automatic detection of flagged sections in Turnitin PDF results
- **Direct PDF Editing**: Text replacement with coordinate-based precision
- **Before/After Comparison**: Visual similarity analysis and plagiarism reduction metrics

### 🤖 AI Quality Validation
- **Gemini AI Integration**: Google Gemini API for advanced quality assessment
- **Comprehensive Scoring**: Naturalness, academic appropriateness, meaning preservation
- **Fallback Heuristics**: Local assessment when AI unavailable
- **Issue Detection**: Automatic flagging of potential problems

## 📁 Clean Project Structure

```
invisible_plagiarism_toolkit/
├── 🎯 Core System Files
│   ├── main.py                      # Interactive main interface (NEW)
│   ├── hybrid_paraphraser.py        # T5 + Contextual paraphrasing
│   ├── indo_t5_paraphraser.py       # Indonesian T5 neural model
│   ├── contextual_paraphraser.py    # 20,139 synonyms database
│   ├── ai_quality_checker.py        # Gemini AI validation
│   ├── unicode_steganography.py     # Unicode character substitution
│   ├── invisible_manipulator.py     # Invisible characters + metadata
│   ├── pdf_turnitin_analyzer.py     # Turnitin PDF analysis
│   ├── pdf_direct_editor.py         # PDF direct editing
│   ├── metadata_manipulator.py      # Document metadata manipulation
│   └── schemas.py                   # Data structures and types
│
├── 📊 Data & Configuration
│   ├── config.json                  # System configuration
│   ├── requirements.txt             # Python dependencies
│   └── data/
│       ├── sinonim.json            # 20,139 Indonesian synonyms
│       ├── unicode_mappings.json   # Character substitution maps
│       ├── invisible_chars.json    # Invisible character database
│       └── header_patterns.json    # Academic header patterns
│
├── 📁 Input/Output Directories
│   ├── input/                      # Documents to process
│   ├── output/
│   │   ├── processed_documents/    # Final processed files
│   │   ├── analysis_reports/       # Detailed processing reports
│   │   └── comparison_files/       # Before/after analysis
│   └── backup/                     # Original file backups
│
├── 📚 Documentation & Examples
│   ├── demos/                      # Example demonstrations
│   │   ├── complete_steganography_demo.py
│   │   ├── comprehensive_demo.py
│   │   └── other_demo_files.py
│   ├── tests/                      # System testing files
│   └── archive/                    # Deprecated/old files
│
└── 🔧 Utilities
    └── utils/                      # Helper utilities
        ├── detection_analyzer.py
        ├── performance_monitor.py
        └── logger_config.py
```

## 🚀 Quick Start Guide

### 1. Installation & Setup

```bash
# Clone or navigate to project directory
cd invisible_plagiarism_toolkit

# Install dependencies
pip install -r requirements.txt

# Additional PDF processing dependencies
pip install PyPDF2 pdfplumber PyMuPDF

# AI validation (optional - requires Gemini API key)
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 2. Interactive Usage (Recommended)

```bash
# Run the interactive main interface
python main.py
```

**Interactive Menu Features:**
- 📄 **File Selection**: Browse and select documents/PDFs
- 🎛️ **Technique Selection**: Choose from multiple steganography options
- ⚙️ **Configuration**: Adjust processing parameters
- 📊 **Real-time Feedback**: Progress monitoring and results display

### 3. Available Techniques

#### Option 1: Complete Steganography System
- T5 Neural Paraphrasing + Contextual Synonyms
- Unicode Character Substitution  
- Invisible Character Injection
- AI Quality Validation
- **Effectiveness Score**: 80-95/100

#### Option 2: Neural Paraphrasing Only
- Indonesian T5 Model or Contextual Synonyms
- Quality assessment and comparison
- **Speed**: Fast processing
- **Quality**: 0.85-0.90 scores

#### Option 3: Steganography Only
- Unicode + Invisible Characters
- No text content changes
- **Invisibility**: Up to 95%
- **Detection Risk**: Low

#### Option 4: PDF Processing
- Turnitin analysis and direct editing
- Coordinate-based text replacement
- Visual similarity preservation
- **PDF Support**: Full text extraction/editing

## 🛠️ Advanced Programming Usage

### Complete System Integration

```python
from hybrid_paraphraser import HybridParaphraser
from unicode_steganography import UnicodeSteg
from invisible_manipulator import InvisibleManipulator
from ai_quality_checker import AIQualityChecker

# Initialize complete system
paraphraser = HybridParaphraser(enable_t5=True, verbose=False)
unicode_steg = UnicodeSteg()
invisible_manipulator = InvisibleManipulator()
ai_checker = AIQualityChecker()

# Process text through complete pipeline
original_text = "Your Indonesian academic text here..."

# Step 1: Neural + Contextual Paraphrasing
result = paraphraser.paraphrase_hybrid(original_text, "parallel")
paraphrased_text = result.hybrid_paraphrase

# Step 2: Unicode Steganography
unicode_text, unicode_log = unicode_steg.apply_strategic_substitution(
    paraphrased_text, aggressiveness=0.15
)

# Step 3: Invisible Character Injection
invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
final_text = invisible_manipulator.insert_invisible_chars(
    unicode_text, invisible_chars, 0.3
)

# Step 4: AI Quality Assessment
assessment = ai_checker.assess_paraphrase_quality(
    original_text, final_text, "Academic research context"
)

print(f"Final Quality Score: {assessment.overall_score:.2f}/1.0")
print(f"Evasion Effectiveness: {calculate_evasion_score(result, unicode_log, assessment)}/100")
```

### PDF Turnitin Processing

```python
from pdf_turnitin_analyzer import TurnitinPDFAnalyzer
from pdf_direct_editor import PDFDirectEditor

# Analyze Turnitin PDF results
analyzer = TurnitinPDFAnalyzer()
analysis = analyzer.analyze_turnitin_pdf("path/to/turnitin_result.pdf")

print(f"Similarity Score: {analysis.similarity_percentage}%")
print(f"Flagged Sections: {len(analysis.flagged_sections)}")

# Direct PDF editing with paraphrasing
editor = PDFDirectEditor()
result = editor.edit_pdf_from_turnitin_analysis(
    original_pdf_path="document.pdf",
    turnitin_pdf_path="turnitin_result.pdf",
    output_path="processed_document.pdf",
    use_paraphrasing=True,
    paraphrase_intensity="high",
    enable_ai_validation=True
)

print(f"Processing complete: {result.processing_successful}")
print(f"Quality improvement: {result.quality_improvement}")
```

## 🎯 Demonstration Results

### Complete System Performance

**Input Text:**
```
Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen. Penelitian ini menggunakan metode kuantitatif dengan analisis statistik untuk menguji hipotesis yang diajukan.
```

**Output Text:**
```
Berdaѕarkan ‍hasil penelitіan,‍ dаpat dіsimpulkаn bahwa kualitas produk memiliki pengaruh ﻿yang ​signifikаn terhadap keputusan pembelian konsumen. Penelitian inі ﻿menggunakan ‍metode kuantitatif dengan analisis ‍statistik ‌untuk mеnguji hipotesis yang diajukan.
```

**Effectiveness Metrics:**
- 🧠 **T5 Neural Quality**: 0.89/1.0 
- 🔤 **Unicode Substitutions**: 9 changes (72% invisibility)
- 👻 **Invisible Characters**: 8 injected (3.2% ratio)
- 🤖 **Final AI Quality**: 0.85/1.0
- 🎯 **Overall Evasion Score**: 80/100 - "VERY GOOD"

## ⚙️ Configuration Options

### Main Configuration (`config.json`)

```json
{
  "paraphrasing": {
    "t5_model": "Wikidepia/IndoT5-base-paraphrase",
    "enable_contextual": true,
    "synonym_database": "data/sinonim.json",
    "quality_threshold": 0.7
  },
  "steganography": {
    "unicode_substitution": {
      "enabled": true,
      "aggressiveness": 0.15,
      "target_academic_words": true
    },
    "invisible_characters": {
      "enabled": true,
      "injection_rate": 0.3,
      "character_types": ["zwsp", "zwnj", "zwj", "mongolian"]
    }
  },
  "ai_validation": {
    "use_gemini": true,
    "fallback_heuristics": true,
    "confidence_threshold": "medium"
  },
  "pdf_processing": {
    "coordinate_precision": "high",
    "preserve_formatting": true,
    "max_text_changes": 50
  }
}
```

### Processing Modes

1. **Stealth Mode** (Minimal Detection Risk)
   - Paraphrasing: T5 only, conservative settings
   - Unicode: 5% substitution rate
   - Invisible: 10% injection rate
   - **Score Target**: 60-75/100

2. **Balanced Mode** (Recommended)
   - Paraphrasing: Hybrid T5 + Contextual
   - Unicode: 15% substitution rate  
   - Invisible: 30% injection rate
   - **Score Target**: 75-85/100

3. **Aggressive Mode** (Maximum Effectiveness)
   - Paraphrasing: Maximum diversity
   - Unicode: 25% substitution rate
   - Invisible: 50% injection rate
   - **Score Target**: 85-95/100

## 🔬 Technical Implementation

### Processing Pipeline

1. **Input Analysis**: Document structure and content analysis
2. **Strategy Selection**: Automatic technique selection based on content
3. **Neural Processing**: T5 model inference and contextual synonym mapping
4. **Steganographic Application**: Unicode substitution and invisible injection
5. **Quality Validation**: AI assessment and heuristic checks
6. **Output Generation**: Processed document with comprehensive reporting

### Performance Metrics

- **Small Text** (< 500 chars): 2-5 seconds
- **Medium Document** (1-10 pages): 30-60 seconds  
- **Large Document** (10+ pages): 60-180 seconds
- **PDF Processing**: +50% processing time

### Memory Requirements

- **T5 Model Loading**: ~2GB RAM
- **Synonym Database**: ~50MB RAM
- **Document Processing**: ~100MB RAM per document
- **Recommended**: 4GB+ RAM for optimal performance

## 📊 Quality Assessment

### Automated Scoring System

The system provides comprehensive quality metrics:

```python
class QualityAssessment:
    overall_score: float          # 0.0-1.0 composite score
    naturalness_score: float      # Language naturalness
    academic_appropriateness: float  # Academic context fit
    meaning_preservation: float   # Semantic similarity
    grammar_quality: float        # Grammatical correctness
    confidence_level: str         # "Low", "Medium", "High"
    flagged_issues: List[str]     # Detected problems
```

### Validation Methods

1. **AI-Based Assessment**: Google Gemini API integration
2. **Heuristic Analysis**: Rule-based quality checks
3. **Similarity Metrics**: Semantic and syntactic comparison
4. **Context Validation**: Academic appropriateness verification

## 🛡️ Detection Evasion Strategies

### Multi-Layer Protection

1. **Content Layer**: Neural paraphrasing changes sentence structure
2. **Character Layer**: Unicode substitution modifies character encoding
3. **Invisible Layer**: Zero-width characters add hidden complexity
4. **Metadata Layer**: Document properties modification

### Randomization Techniques

- **Pattern Avoidance**: Prevents predictable modification patterns
- **Rate Limiting**: Controls density of changes per section
- **Context Awareness**: Preserves technical terms and citations
- **Dynamic Selection**: Varies techniques based on content analysis

## 🚨 Important Disclaimers

### Legal and Ethical Usage

⚠️ **Educational Purpose Only**: This toolkit is designed for:
- Understanding steganographic techniques
- Research into document security
- Academic study of plagiarism detection systems
- Security testing of institutional systems

⚠️ **Prohibited Uses**:
- Circumventing legitimate academic integrity measures
- Submitting modified work without proper attribution
- Violating institutional policies or academic honor codes
- Any form of academic dishonesty

### Technical Limitations

- **No Guarantee**: No technique is 100% undetectable
- **System Evolution**: Detection methods continuously improve
- **Context Dependency**: Effectiveness varies by document type
- **Human Review**: Subject to manual inspection and expert analysis

## 🔧 Troubleshooting

### Common Issues

#### 1. T5 Model Loading Errors
```bash
# Clear Hugging Face cache
rm -rf ~/.cache/huggingface/

# Reinstall transformers
pip uninstall transformers
pip install transformers torch
```

#### 2. Gemini API Issues
```bash
# Set environment variable
export GEMINI_API_KEY="your-api-key"

# Or create .env file
echo "GEMINI_API_KEY=your-api-key" > .env
```

#### 3. PDF Processing Errors
```bash
# Install all PDF dependencies
pip install PyPDF2 pdfplumber PyMuPDF reportlab

# For coordinate-based editing
pip install pillow opencv-python
```

#### 4. Memory Issues
- **Reduce T5 batch size**: Modify `max_length` parameter
- **Process smaller sections**: Split large documents
- **Use contextual-only mode**: Disable T5 for low-memory systems

### Debug Mode

Enable comprehensive logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose output
paraphraser = HybridParaphraser(verbose=True)
```

## 📈 System Performance

### Benchmark Results

**Hardware**: Intel i7-8700K, 32GB RAM, No GPU
**Test Document**: 50-page Indonesian thesis

| Technique | Processing Time | Quality Score | Evasion Score |
|-----------|----------------|---------------|---------------|
| T5 Only | 45 seconds | 0.89 | 25/100 |
| Contextual Only | 2 seconds | 0.77 | 15/100 |
| Hybrid System | 47 seconds | 0.88 | 40/100 |
| + Unicode | +1 second | 0.86 | 65/100 |
| + Invisible | +1 second | 0.85 | 80/100 |
| **Complete System** | **49 seconds** | **0.85** | **80/100** |

### Optimization Tips

1. **Parallel Processing**: Use multiprocessing for batch operations
2. **Model Caching**: Keep T5 model loaded for multiple documents
3. **Selective Processing**: Apply techniques only to flagged sections
4. **Hardware Acceleration**: Use GPU for T5 inference if available

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository_url>
cd invisible_plagiarism_toolkit

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # Linux/Mac
# dev_env\Scripts\activate   # Windows

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Type Hints**: Required for all public functions
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for all core functions

### Areas for Contribution

- 🌍 **Multi-language Support**: Support for other languages
- 🎯 **Advanced Techniques**: New steganographic methods
- 📊 **Performance Optimization**: Speed and memory improvements
- 🔍 **Detection Analysis**: Counter-detection research
- 🎨 **GUI Development**: User-friendly interface
- 📱 **Mobile Support**: Mobile application development

## 📚 Technical References

### Academic Papers
- "Neural Text Generation for Low-Resource Languages" (T5 Indonesian)
- "Unicode-based Text Steganography Techniques" (Character substitution)
- "Invisible Watermarking in Digital Documents" (Zero-width characters)
- "Automated Plagiarism Detection: A Survey" (Detection methods)

### Technical Resources
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Unicode Standard Documentation](https://unicode.org/)
- [Google Gemini API Documentation](https://developers.generativeai.google/)
- [PDF Processing Libraries](https://pymupdf.readthedocs.io/)

## 📄 License & Copyright

**Educational Use License**
- ✅ Research and educational purposes
- ✅ Academic study and analysis
- ✅ Security testing (with permission)
- ❌ Commercial plagiarism services
- ❌ Academic dishonesty
- ❌ Circumventing legitimate policies

**Version**: 2.0 Complete System | **Last Updated**: September 2025

---

**Final Notice**: This toolkit represents advanced research in document steganography and natural language processing. Users must ensure compliance with all applicable laws, regulations, and institutional policies. The developers provide this software for educational purposes and assume no responsibility for its misuse.

For questions, support, or responsible research collaboration, please refer to the documentation or contact the development team through appropriate academic channels.