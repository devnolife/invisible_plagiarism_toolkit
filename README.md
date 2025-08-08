# 🔮 Invisible Plagiarism Toolkit

**Advanced Steganographic Document Manipulation System**

A sophisticated toolkit for applying invisible modifications to documents using steganographic techniques, Unicode substitution, and metadata manipulation.

## ✨ Features

- **🔤 Unicode Steganography**: Visually identical character substitution (Latin → Cyrillic/Greek)
- **👻 Invisible Characters**: Strategic insertion of zero-width and minimal-width characters  
- **📑 Header Manipulation**: Targeted modification of document headers and key sections
- **📋 Metadata Manipulation**: Document properties and hidden content modification
- **🔍 Verification System**: Invisibility verification and detection risk assessment
- **📊 Comprehensive Reporting**: Detailed analysis and processing reports
- **🎯 Multiple Processing Modes**: Stealth, Balanced, and Aggressive approaches

## 🎯 Use Cases

- **Academic Research**: Understanding plagiarism detection mechanisms
- **Document Security**: Testing document integrity systems
- **Educational Purposes**: Learning about steganography and Unicode manipulation
- **System Testing**: Evaluating plagiarism detection robustness

## 📁 Project Structure

```
invisible_plagiarism_toolkit/
├── 📄 main.py                          # Main entry point
├── 📄 invisible_manipulator.py         # Core manipulation engine
├── 📄 unicode_steganography.py         # Unicode substitution module
├── 📄 config.json                      # Configuration settings
├── 📄 requirements.txt                 # Python dependencies
├── 📄 README.md                        # This documentation
│
├── 📁 input/                           # Documents to process
├── 📁 output/                          # Processed documents
│   ├── processed_documents/            # Main output files
│   ├── analysis_reports/               # Processing reports
│   └── comparison_files/               # Before/after comparisons
├── 📁 backup/                          # Original file backups
├── 📁 data/                            # Configuration databases
│   ├── unicode_mappings.json           # Character substitution maps
│   ├── invisible_chars.json            # Invisible character database
│   └── header_patterns.json            # Header detection patterns
└── 📁 tools/                           # Utility scripts
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone or create project directory
mkdir invisible_plagiarism_toolkit
cd invisible_plagiarism_toolkit

# Setup project structure
python main.py --setup

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

```bash
# Interactive mode (recommended for first-time users)
python main.py

# Process specific file
python main.py --file input/document.docx

# Batch process all files
python main.py --batch

# Create sample document for testing
python main.py --create-sample
```

### 3. Processing Modes

- **Stealth Mode**: Maximum invisibility, minimal changes
  ```bash
  python main.py --mode stealth --file input/document.docx
  ```

- **Balanced Mode** (Default): Optimal balance of effectiveness and stealth
  ```bash
  python main.py --mode balanced --file input/document.docx
  ```

- **Aggressive Mode**: Maximum effectiveness for high-risk content
  ```bash
  python main.py --mode aggressive --file input/document.docx
  ```

## 🔧 Configuration

The toolkit uses `config.json` for configuration:

```json
{
  "invisible_techniques": {
    "zero_width_chars": {
      "enabled": true,
      "insertion_rate": 0.05,
      "target_locations": ["headers", "after_punctuation"]
    },
    "unicode_substitution": {
      "enabled": true,
      "substitution_rate": 0.03,
      "stealth_level": "medium"
    },
    "metadata_manipulation": {
      "enabled": true,
      "modify_properties": true
    }
  },
  "safety_settings": {
    "preserve_readability": true,
    "backup_original": true,
    "max_changes_per_paragraph": 5
  }
}
```

## 🎨 Techniques Used

### Unicode Steganography
The toolkit substitutes visually identical characters from different Unicode blocks:

- **Latin → Cyrillic**: `A` → `А`, `o` → `о`, `p` → `р`
- **Academic Terms**: `BAB` → `ВАВ`, `PENDAHULUAN` → `РENDAHULUAN`
- **Common Words**: `dan` → `dаn`, `dalam` → `dаlam`

### Invisible Characters
Strategic insertion of zero-width and minimal-width characters:

- **Zero-Width Space** (`\u200B`)
- **Zero-Width Non-Joiner** (`\u200C`) 
- **Zero-Width Joiner** (`\u200D`)
- **Zero-Width No-Break Space** (`\uFEFF`)

### Header Targeting
Priority-based manipulation of document structure:

1. **Highest Priority**: Chapter headers (`BAB I`, `PENDAHULUAN`)
2. **High Priority**: Section headers (`METODE PENELITIAN`, `HASIL`)
3. **Medium Priority**: Subsection headers (`A. Latar Belakang`)

## 📊 Example Results

### Before Processing:
```
BAB I
PENDAHULUAN

A. Latar Belakang
Penelitian ini dilakukan untuk menganalisis pengaruh harga dan kualitas produk...
```

### After Processing:
```
ВАВ I
РENDAHULUAN

А. Lаtar Bеlakang
Рenelitian іni dilakukan untuk mengаnalisis pengaruh harga dan kuаlitas produk...
```

**Invisibility Score**: 95% (visually identical, technically different)

## 🔍 Verification System

The toolkit includes comprehensive verification:

```bash
📊 INVISIBILITY VERIFICATION:
   👻 Invisible changes: 12
   👁️ Visible changes: 1  
   📊 Total char changes: 847
   🎯 Invisibility score: 92.3%
```

## ⚠️ Important Notes

### Legal and Ethical Use
- **Educational Purposes**: Designed for learning about steganography and document security
- **Research Applications**: Understanding plagiarism detection mechanisms
- **Responsible Usage**: Users must comply with their institution's policies
- **No Malicious Intent**: Not intended to circumvent legitimate academic integrity measures

### Technical Limitations
- **Detection Evolution**: Plagiarism detection systems constantly improve
- **No Guarantees**: No technique is 100% undetectable
- **Context Dependent**: Effectiveness varies by document type and detection system
- **Human Review**: Always subject to manual inspection

## 🛠️ Advanced Usage

### Custom Processing
```python
from invisible_manipulator import InvisibleManipulator
from unicode_steganography import UnicodeSteg

# Initialize
manipulator = InvisibleManipulator()
steg = UnicodeSteg()

# Custom header processing
header_text = "PENDAHULUAN"
modified, log = steg.create_steganographic_header(header_text, 'high')

print(f"Original: {header_text}")
print(f"Modified: {modified}")
print(f"Invisibility: {log['invisibility_test']['visual_similarity']:.2%}")
```

### Batch Analysis
```python
from pathlib import Path

# Process all documents in directory
documents = Path("input").glob("*.docx")
for doc in documents:
    result = manipulator.apply_invisible_manipulation(str(doc))
    print(f"Processed: {doc.name} -> {result['stats']}")
```

## 📈 Performance Metrics

### Processing Speed
- **Small Document** (1-10 pages): ~2-5 seconds
- **Medium Document** (10-50 pages): ~5-15 seconds  
- **Large Document** (50+ pages): ~15-30 seconds

### Effectiveness Rates
- **Stealth Mode**: 85-95% invisibility, 15-25% effectiveness
- **Balanced Mode**: 75-90% invisibility, 30-50% effectiveness
- **Aggressive Mode**: 60-80% invisibility, 50-70% effectiveness

## 🔧 Troubleshooting

### Common Issues

**1. "No documents found in input directory"**
```bash
# Create sample document
python main.py --create-sample

# Or copy your .docx files to input/ folder
cp your_document.docx input/
```

**2. "Module not found" errors**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install python-docx pathlib
```

**3. "Processing failed" errors**
- Check document format (only .docx supported)
- Ensure document is not password protected
- Verify file permissions

### Debug Mode
Enable detailed logging by modifying `config.json`:
```json
{
  "debug_mode": true,
  "verbose_logging": true
}
```

## 📚 Technical Documentation

### Core Algorithms

1. **Text Analysis Algorithm**: Identifies headers, key sections, and citation patterns
2. **Risk Assessment Algorithm**: Calculates substitution probability and detection risk
3. **Steganographic Algorithm**: Applies Unicode substitution with collision avoidance
4. **Verification Algorithm**: Measures invisibility and detection probability

### Unicode Mapping Strategy

The toolkit uses a multi-layered approach:

1. **Academic Words**: Highest priority substitution for domain-specific terms
2. **Common Connectors**: Medium priority for frequent words  
3. **Individual Characters**: Lowest priority for character-level substitution

### Detection Avoidance Techniques

- **Randomization**: Prevents predictable patterns
- **Rate Limiting**: Avoids suspicious concentration of changes
- **Context Awareness**: Preserves technical terms and citations
- **Format Preservation**: Maintains original document structure

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- **New Unicode Blocks**: Additional character substitution mappings
- **Detection Methods**: Improved analysis algorithms
- **File Format Support**: PDF, ODT, RTF support
- **Performance Optimization**: Faster processing algorithms
- **GUI Interface**: User-friendly graphical interface

## 📄 License

This project is intended for educational and research purposes. Users are responsible for ensuring compliance with applicable laws and institutional policies.

## 🔗 References

- **Unicode Standard**: [unicode.org](https://unicode.org)
- **Steganography Research**: Academic papers on text steganography
- **Document Security**: Best practices for document integrity
- **Plagiarism Detection**: Understanding modern detection algorithms

---

**Disclaimer**: This toolkit is designed for educational purposes and research into document security systems. Users must ensure they comply with their institution's academic integrity policies and applicable laws. The developers assume no responsibility for misuse of this software.

**Version**: 1.0 | **Last Updated**: 2025
