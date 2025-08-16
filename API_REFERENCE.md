# API_REFERENCE.md
# 📚 API Reference

## Overview
Comprehensive API reference for the Invisible Plagiarism Toolkit components.

## Core Classes

### `InvisibleManipulator`
Main engine for document manipulation using steganographic techniques.

#### Constructor
```python
InvisibleManipulator(config_file='config.json', verbose=False)
```

**Parameters:**
- `config_file` (str): Path to configuration file
- `verbose` (bool): Enable detailed logging

#### Methods

##### `apply_invisible_manipulation(file_path: str) -> Dict`
Apply steganographic techniques to a document.

**Parameters:**
- `file_path` (str): Path to input DOCX file

**Returns:**
- `Dict`: Processing results with statistics and output file path

**Example:**
```python
manipulator = InvisibleManipulator()
result = manipulator.apply_invisible_manipulation("document.docx")
print(f"Output: {result['output_file']}")
print(f"Changes: {result['stats']['chars_substituted']}")
```

##### `analyze_document_structure(file_path: str) -> Dict`
Analyze document structure and identify headers.

**Parameters:**
- `file_path` (str): Path to DOCX file

**Returns:**
- `Dict`: Document structure analysis

---

### `UnicodeSteg`
Unicode substitution and steganographic character manipulation.

#### Constructor
```python
UnicodeSteg()
```

#### Methods

##### `apply_substitution(text: str, rate: float = 0.03) -> str`
Apply Unicode character substitution.

**Parameters:**
- `text` (str): Input text
- `rate` (float): Substitution rate (0.0-1.0)

**Returns:**
- `str`: Text with Unicode substitutions

**Example:**
```python
steg = UnicodeSteg()
result = steg.apply_substitution("BAB I PENDAHULUAN", rate=0.1)
# Result might be: "ВАВ I РENDAHULUAN"
```

---

### `AdvancedAnalyzer`
Risk analysis and detection probability assessment.

#### Constructor
```python
AdvancedAnalyzer(logger=None)
```

#### Methods

##### `analyze_document_risk(original_path: str, modified_path: str) -> RiskAnalysis`
Comprehensive risk analysis between original and modified documents.

**Parameters:**
- `original_path` (str): Path to original document
- `modified_path` (str): Path to modified document

**Returns:**
- `RiskAnalysis`: Detailed risk assessment

**Example:**
```python
analyzer = AdvancedAnalyzer()
analysis = analyzer.analyze_document_risk("original.docx", "modified.docx")
print(f"Risk Level: {analysis.risk_level}")
print(f"Invisibility Score: {analysis.invisibility_score:.2%}")
```

---

## Data Structures

### `RiskAnalysis`
Dataclass containing comprehensive risk assessment results.

**Attributes:**
- `overall_risk` (float): Overall detection risk (0-1)
- `risk_level` (DetectionRisk): Categorized risk level
- `invisibility_score` (float): How invisible changes are (0-1)
- `detection_patterns` (List[str]): Suspicious patterns found
- `recommendations` (List[str]): Actionable recommendations
- `technique_breakdown` (Dict[str, float]): Per-technique risk scores

### `ProcessingStats`
Statistics from document processing.

**Attributes:**
- `total_documents` (int): Number of documents processed
- `headers_modified` (int): Number of headers modified
- `chars_substituted` (int): Unicode characters substituted
- `invisible_chars_inserted` (int): Invisible characters inserted
- `processing_time` (float): Total processing time in seconds
- `risk_score` (float): Estimated detection risk
- `invisibility_score` (float): Invisibility effectiveness

---

## Configuration Schema

### Main Configuration Structure
```json
{
  "invisible_techniques": {
    "zero_width_chars": {
      "enabled": true,
      "chars": ["\u200B", "\u200C", "\u200D", "\uFEFF"],
      "insertion_rate": 0.05,
      "target_locations": ["headers", "after_punctuation", "between_words"]
    },
    "unicode_substitution": {
      "enabled": true,
      "substitution_rate": 0.03,
      "target_chars": ["a", "e", "o", "p", "c", "x", "y"],
      "priority_words": ["BAB", "PENDAHULUAN", "METODE"]
    }
  },
  "safety_settings": {
    "preserve_readability": true,
    "maintain_formatting": true,
    "backup_original": true,
    "max_changes_per_paragraph": 5
  }
}
```

### Configuration Validation
All configuration values are validated on load:
- `insertion_rate`: Must be 0.0-0.5
- `substitution_rate`: Must be 0.0-0.3
- `max_changes_per_paragraph`: Must be >= 1

---

## Usage Examples

### Basic Document Processing
```python
from invisible_manipulator import InvisibleManipulator

# Initialize with default config
manipulator = InvisibleManipulator(verbose=True)

# Process single document
result = manipulator.apply_invisible_manipulation("thesis.docx")

print(f"Processed: {result['output_file']}")
print(f"Unicode substitutions: {result['stats']['chars_substituted']}")
print(f"Processing time: {result['stats']['processing_time']:.2f}s")
```

### Custom Configuration
```python
# Create custom config
config = {
    "invisible_techniques": {
        "unicode_substitution": {
            "enabled": True,
            "substitution_rate": 0.05  # Higher rate
        },
        "zero_width_chars": {
            "enabled": False  # Disable invisible chars
        }
    }
}

# Save and use custom config
import json
with open('custom_config.json', 'w') as f:
    json.dump(config, f)

manipulator = InvisibleManipulator(config_file='custom_config.json')
```

### Risk Analysis Workflow
```python
from advanced_analyzer import AdvancedAnalyzer

# Process document
manipulator = InvisibleManipulator()
result = manipulator.apply_invisible_manipulation("document.docx")

# Analyze risk
analyzer = AdvancedAnalyzer()
risk_analysis = analyzer.analyze_document_risk(
    "document.docx", 
    result['output_file']
)

# Check if safe
if risk_analysis.risk_level.value in ['minimal', 'low']:
    print("✅ Document appears safe from detection")
else:
    print("⚠️ High detection risk - consider reducing modifications")
    for rec in risk_analysis.recommendations:
        print(f"  • {rec}")
```

### Batch Processing
```python
import glob
from pathlib import Path

manipulator = InvisibleManipulator()
input_files = glob.glob("input/*.docx")

for file_path in input_files:
    print(f"Processing: {Path(file_path).name}")
    
    try:
        result = manipulator.apply_invisible_manipulation(file_path)
        print(f"  ✅ Success: {result['stats']['chars_substituted']} substitutions")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
```

---

## Error Handling

### Common Exceptions
- `FileNotFoundError`: Input file not found
- `ValueError`: Invalid configuration values
- `PermissionError`: Insufficient file permissions
- `docx.opc.exceptions.PackageNotFoundError`: Invalid DOCX file

### Best Practices
```python
try:
    result = manipulator.apply_invisible_manipulation("document.docx")
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    # Log full traceback for debugging
    import traceback
    traceback.print_exc()
```

---

## Performance Considerations

### Memory Usage
- Large documents (>10MB) may require significant memory
- Consider processing in batches for multiple large files
- Clear document objects when possible

### Processing Speed
- Unicode substitution: ~1000 chars/second
- Invisible character insertion: ~2000 chars/second
- Document analysis: ~500 chars/second

### Optimization Tips
1. Disable unused techniques in configuration
2. Lower substitution rates for faster processing
3. Use specific file processing rather than batch for large files
4. Enable verbose logging only when debugging

---

## Integration Examples

### Flask Web API
```python
from flask import Flask, request, jsonify
from invisible_manipulator import InvisibleManipulator

app = Flask(__name__)
manipulator = InvisibleManipulator()

@app.route('/process', methods=['POST'])
def process_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)
    
    try:
        result = manipulator.apply_invisible_manipulation(temp_path)
        return jsonify({
            'success': True,
            'stats': result['stats'],
            'output_file': result['output_file']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Command Line Integration
```python
import subprocess
import json

def process_via_cli(file_path: str, aggressive: bool = False) -> dict:
    """Process document via CLI interface"""
    cmd = ['python', 'main.py', '--file', file_path]
    if aggressive:
        cmd.append('--aggressive')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Parse output for statistics
        return {'success': True, 'output': result.stdout}
    else:
        return {'success': False, 'error': result.stderr}
```
