# invisible_manipulator.py
"""
Invisible Manipulator Core - Main Engine
Sistem manipulasi dokumen menggunakan teknik steganografi dan karakter invisible
Fokus: Header manipulation, Unicode substitution, Invisible characters

Author: DevNoLife
Version: 1.0 - Steganography Edition
"""

import os
import json
import re
import random
import shutil
from datetime import datetime
from pathlib import Path
import docx
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import unicodedata
from metadata_manipulator import MetadataManipulator, MetadataOptions

class InvisibleManipulator:
    def __init__(self, config_file='config.json'):
        print("🔮 Initializing Invisible Manipulator...")
        print("✨ Steganography-based document manipulation")
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Load data files
        self.unicode_mappings = self.load_data_file('data/unicode_mappings.json')
        self.invisible_chars = self.load_data_file('data/invisible_chars.json')
        self.header_patterns = self.load_data_file('data/header_patterns.json')
        
        # Statistics tracking
        self.stats = {
            'total_documents': 0,
            'headers_modified': 0,
            'chars_substituted': 0,
            'invisible_chars_inserted': 0,
            'metadata_modified': 0,
            'processing_time': 0
        }
        
        print("✅ Configuration loaded")
        print("✅ Unicode mappings ready")
        print("✅ Invisible characters database loaded")
        print("✅ Header patterns configured")
        print("🎯 Ready for invisible manipulation!")
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"📋 Configuration loaded from {config_file}")
            return config
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found, using defaults")
            return self.get_default_config()
    
    def load_data_file(self, file_path):
        """Load data files (mappings, patterns, etc.)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"⚠️ Data file {file_path} not found, using defaults")
            return {}
    
    def get_default_config(self):
        """Default configuration if config file is missing"""
        return {
            "invisible_techniques": {
                "zero_width_chars": {
                    "enabled": True,
                    "insertion_rate": 0.05,
                    "target_locations": ["headers", "after_punctuation"]
                },
                "unicode_substitution": {
                    "enabled": True,
                    "substitution_rate": 0.03
                },
                "metadata_manipulation": {
                    "enabled": True
                }
            },
            "safety_settings": {
                "preserve_readability": True,
                "backup_original": True,
                "max_changes_per_paragraph": 5
            }
        }
    
    def analyze_document_structure(self, doc_path):
        """Analyze document to identify headers, key sections, etc."""
        print("🔍 Analyzing document structure...")
        
        doc = docx.Document(doc_path)
        analysis = {
            'total_paragraphs': len(doc.paragraphs),
            'headers': [],
            'key_sections': [],
            'citations': [],
            'metadata': {}
        }
        
        for i, paragraph in enumerate(doc.paragraphs):
            text = paragraph.text.strip()
            
            if not text:
                continue
            
            # Detect headers
            if self.is_header(text, paragraph):
                analysis['headers'].append({
                    'index': i,
                    'text': text,
                    'type': self.classify_header(text),
                    'priority': self.get_header_priority(text)
                })
            
            # Detect key sections
            if self.is_key_section(text):
                analysis['key_sections'].append({
                    'index': i,
                    'text': text,
                    'section_type': self.classify_section(text)
                })
            
            # Detect citations (simple pattern)
            if self.contains_citation(text):
                analysis['citations'].append({
                    'index': i,
                    'text': text[:100] + '...' if len(text) > 100 else text
                })
        
        print(f"📊 Analysis complete:")
        print(f"   📄 Total paragraphs: {analysis['total_paragraphs']}")
        print(f"   📑 Headers found: {len(analysis['headers'])}")
        print(f"   🎯 Key sections: {len(analysis['key_sections'])}")
        print(f"   📚 Citations: {len(analysis['citations'])}")
        
        return analysis
    
    def is_header(self, text, paragraph):
        """Determine if text is a header"""
        # Check formatting clues
        if hasattr(paragraph, 'style') and paragraph.style:
            style_name = paragraph.style.name.lower()
            if 'heading' in style_name or 'title' in style_name:
                return True
        
        # Check text patterns
        text_upper = text.upper()
        
        # Common header patterns
        header_indicators = [
            r'^BAB\s+[IVX]+',           # BAB I, BAB II, etc.
            r'^CHAPTER\s+\d+',         # CHAPTER 1, etc.
            r'^[A-Z]\.\s+[A-Z]',       # A. SOMETHING
            r'^PENDAHULUAN$',          # Exact matches
            r'^METODE\s+PENELITIAN$',
            r'^HASIL\s+DAN\s+PEMBAHASAN$',
            r'^KESIMPULAN$',
            r'^DAFTAR\s+PUSTAKA$'
        ]
        
        for pattern in header_indicators:
            if re.match(pattern, text_upper):
                return True
        
        # Additional checks
        conditions = [
            len(text.split()) <= 6,     # Short
            text.isupper(),             # All caps
            len(text) < 50,             # Not too long
            not text.endswith('.')      # Usually no period
        ]
        
        return sum(conditions) >= 2
    
    def classify_header(self, text):
        """Classify header type"""
        text_upper = text.upper()
        
        if re.match(r'^BAB\s+[IVX]+', text_upper):
            return 'chapter'
        elif text_upper in ['PENDAHULUAN', 'METODE PENELITIAN', 'HASIL DAN PEMBAHASAN', 'KESIMPULAN']:
            return 'major_section'
        elif re.match(r'^[A-Z]\.\s+', text_upper):
            return 'subsection'
        else:
            return 'minor_header'
    
    def get_header_priority(self, text):
        """Get manipulation priority for header"""
        text_upper = text.upper()
        
        if 'BAB' in text_upper or text_upper in ['PENDAHULUAN', 'KESIMPULAN']:
            return 'highest'
        elif text_upper in ['METODE PENELITIAN', 'HASIL DAN PEMBAHASAN']:
            return 'high'
        elif re.match(r'^[A-Z]\.\s+', text_upper):
            return 'medium'
        else:
            return 'low'
    
    def is_key_section(self, text):
        """Identify key sections that need attention"""
        key_phrases = [
            'latar belakang', 'rumusan masalah', 'tujuan penelitian',
            'metode penelitian', 'hasil penelitian', 'analisis data',
            'kesimpulan', 'saran', 'daftar pustaka'
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in key_phrases)
    
    def classify_section(self, text):
        """Classify section type"""
        text_lower = text.lower()
        
        if 'latar belakang' in text_lower:
            return 'background'
        elif 'rumusan masalah' in text_lower:
            return 'problem_statement'
        elif 'tujuan' in text_lower:
            return 'objectives'
        elif 'metode' in text_lower:
            return 'methodology'
        elif 'hasil' in text_lower:
            return 'results'
        elif 'kesimpulan' in text_lower:
            return 'conclusion'
        else:
            return 'general'
    
    def contains_citation(self, text):
        """Simple citation detection"""
        citation_patterns = [
            r'\(\d{4}\)',               # (2020)
            r'\([^)]*\d{4}[^)]*\)',    # (Smith, 2020)
            r'et\s+al\.',              # et al.
            r'\w+\s+\(\d{4}\)'         # Author (2020)
        ]
        
        return any(re.search(pattern, text) for pattern in citation_patterns)
    
    def apply_invisible_manipulation(self, doc_path, output_path=None):
        """Apply invisible manipulation techniques to document"""
        print("🔮 Starting invisible manipulation...")
        
        start_time = datetime.now()
        
        # Create backup
        if self.config['safety_settings']['backup_original']:
            backup_path = self.create_backup(doc_path)
            print(f"💾 Backup created: {backup_path}")
        
        # Analyze document
        analysis = self.analyze_document_structure(doc_path)
        
        # Load document
        doc = docx.Document(doc_path)
        
        # Apply techniques based on priority
        self.apply_header_manipulation(doc, analysis)
        self.apply_unicode_substitution(doc, analysis)
        self.apply_invisible_characters(doc, analysis)
        self.apply_metadata_manipulation(doc)
        
        # Save processed document
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = Path(doc_path).stem
            output_path = f"output/processed_documents/{base_name}_invisible_{timestamp}.docx"
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        doc.save(output_path)
        
        # Calculate statistics
        end_time = datetime.now()
        self.stats['processing_time'] = (end_time - start_time).total_seconds()
        self.stats['total_documents'] += 1
        
        print(f"✅ Invisible manipulation completed!")
        print(f"💾 Output saved: {output_path}")
        self.print_manipulation_stats()
        
        return {
            'input_file': doc_path,
            'output_file': output_path,
            'backup_file': backup_path if self.config['safety_settings']['backup_original'] else None,
            'analysis': analysis,
            'stats': self.stats.copy(),
            'processing_time': self.stats['processing_time']
        }
    
    def apply_header_manipulation(self, doc, analysis):
        """Apply manipulation specifically to headers"""
        print("📑 Manipulating headers...")
        
        if not self.config['invisible_techniques']['unicode_substitution']['enabled']:
            return
        
        headers = analysis['headers']
        high_priority_headers = [h for h in headers if h['priority'] in ['highest', 'high']]
        
        for header_info in high_priority_headers:
            paragraph = doc.paragraphs[header_info['index']]
            original_text = paragraph.text
            
            # Apply Unicode substitution for headers
            manipulated_text = self.apply_unicode_substitution_to_text(original_text)
            
            if manipulated_text != original_text:
                paragraph.text = manipulated_text
                self.stats['headers_modified'] += 1
                
                print(f"   🔀 Header modified: '{original_text}' → '{manipulated_text}'")
    
    def apply_unicode_substitution_to_text(self, text):
        """Apply Unicode character substitution"""
        if not self.unicode_mappings:
            return text
        
        substitution_rate = self.config['invisible_techniques']['unicode_substitution']['substitution_rate']
        latin_to_cyrillic = self.unicode_mappings.get('latin_to_cyrillic', {})
        special_subs = self.unicode_mappings.get('special_substitutions', {})
        
        result = text
        
        # Apply special substitutions first (whole words)
        for original, replacement in special_subs.items():
            if original in result:
                if random.random() < substitution_rate * 3:  # Higher rate for special words
                    result = result.replace(original, replacement)
                    self.stats['chars_substituted'] += len(original)
        
        # Apply individual character substitutions
        new_result = ""
        for char in result:
            if char in latin_to_cyrillic and random.random() < substitution_rate:
                new_result += latin_to_cyrillic[char]
                self.stats['chars_substituted'] += 1
            else:
                new_result += char
        
        return new_result
    
    def apply_unicode_substitution(self, doc, analysis):
        """Apply Unicode substitution to key sections"""
        print("🔤 Applying Unicode substitutions...")
        
        if not self.config['invisible_techniques']['unicode_substitution']['enabled']:
            return
        
        key_sections = analysis['key_sections']
        
        for section_info in key_sections:
            paragraph = doc.paragraphs[section_info['index']]
            original_text = paragraph.text
            
            # Apply substitution with lower rate for content
            manipulated_text = self.apply_unicode_substitution_to_text(original_text)
            
            if manipulated_text != original_text:
                paragraph.text = manipulated_text
    
    def apply_invisible_characters(self, doc, analysis):
        """Insert invisible characters strategically"""
        print("👻 Inserting invisible characters...")
        
        if not self.config['invisible_techniques']['zero_width_chars']['enabled']:
            return
        
        if not self.invisible_chars:
            return
        
        insertion_rate = self.config['invisible_techniques']['zero_width_chars']['insertion_rate']
        zero_width_chars = list(self.invisible_chars.get('zero_width', {}).values())
        
        if not zero_width_chars:
            return
        
        # Focus on headers and key sections
        target_paragraphs = []
        
        # Add headers
        for header_info in analysis['headers']:
            target_paragraphs.append(header_info['index'])
        
        # Add key sections  
        for section_info in analysis['key_sections']:
            target_paragraphs.append(section_info['index'])
        
        for para_index in target_paragraphs:
            if para_index < len(doc.paragraphs):
                paragraph = doc.paragraphs[para_index]
                original_text = paragraph.text
                
                # Insert invisible characters
                new_text = self.insert_invisible_chars(original_text, zero_width_chars, insertion_rate)
                
                if new_text != original_text:
                    paragraph.text = new_text
                    self.stats['invisible_chars_inserted'] += new_text.count('\u200B') + new_text.count('\u200C')
    
    def insert_invisible_chars(self, text, invisible_chars, insertion_rate):
        """Insert invisible characters into text"""
        result = ""
        
        for i, char in enumerate(text):
            result += char
            
            # Insert after punctuation or spaces
            if char in '.,:;! ' and random.random() < insertion_rate:
                invisible_char = random.choice(invisible_chars)
                result += invisible_char
        
        return result
    
    def apply_metadata_manipulation(self, doc):
        """Manipulate document metadata"""
        print("📋 Manipulating metadata...")
        if not self.config['invisible_techniques']['metadata_manipulation']['enabled']:
            return

        try:
            options = MetadataOptions(
                modify_properties=self.config['invisible_techniques']['metadata_manipulation'].get('modify_properties', True),
                add_invisible_content=self.config['invisible_techniques']['metadata_manipulation'].get('add_invisible_content', True),
            )
            manip = MetadataManipulator(options)
            changes = manip.apply(doc)
            self.stats['metadata_modified'] += int(changes > 0)
        except Exception as e:
            print(f"⚠️ Could not modify metadata: {e}")
    
    def create_backup(self, file_path):
        """Create backup of original file"""
        backup_dir = Path("backup")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(file_path).stem
        extension = Path(file_path).suffix
        
        backup_path = backup_dir / f"{original_name}_backup_{timestamp}{extension}"
        
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    
    def print_manipulation_stats(self):
        """Print manipulation statistics"""
        print("\n📊 MANIPULATION STATISTICS:")
        print("=" * 50)
        print(f"📄 Documents processed: {self.stats['total_documents']}")
        print(f"📑 Headers modified: {self.stats['headers_modified']}")
        print(f"🔤 Characters substituted: {self.stats['chars_substituted']}")
        print(f"👻 Invisible chars inserted: {self.stats['invisible_chars_inserted']}")
        print(f"📋 Metadata modifications: {self.stats['metadata_modified']}")
        print(f"⏱️ Processing time: {self.stats['processing_time']:.2f}s")
        print("=" * 50)
    
    def verify_invisibility(self, original_path, modified_path):
        """Verify that changes are visually invisible"""
        print("🔍 Verifying invisibility of changes...")
        
        try:
            original_doc = docx.Document(original_path)
            modified_doc = docx.Document(modified_path)
            
            differences = {
                'visible_changes': 0,
                'invisible_changes': 0,
                'total_chars_changed': 0
            }
            
            # Compare paragraph by paragraph
            for i, (orig_para, mod_para) in enumerate(zip(original_doc.paragraphs, modified_doc.paragraphs)):
                orig_text = orig_para.text
                mod_text = mod_para.text
                
                if orig_text != mod_text:
                    # Check if the difference is only invisible characters
                    orig_visible = ''.join(c for c in orig_text if unicodedata.category(c) != 'Cf')
                    mod_visible = ''.join(c for c in mod_text if unicodedata.category(c) != 'Cf')
                    
                    if orig_visible == mod_visible:
                        differences['invisible_changes'] += 1
                    else:
                        differences['visible_changes'] += 1
                    
                    differences['total_chars_changed'] += abs(len(mod_text) - len(orig_text))
            
            print(f"   👻 Invisible changes: {differences['invisible_changes']}")
            print(f"   👁️ Visible changes: {differences['visible_changes']}")
            print(f"   📊 Total character changes: {differences['total_chars_changed']}")
            
            invisibility_score = (differences['invisible_changes'] / max(1, differences['invisible_changes'] + differences['visible_changes'])) * 100
            print(f"   🎯 Invisibility score: {invisibility_score:.1f}%")
            
            return differences
            
        except Exception as e:
            print(f"❌ Could not verify invisibility: {e}")
            return None


def create_sample_config():
    """Create sample configuration file"""
    config = {
        "invisible_techniques": {
            "zero_width_chars": {
                "enabled": True,
                "chars": ["\u200B", "\u200C", "\u200D", "\uFEFF"],
                "insertion_rate": 0.05,
                "target_locations": ["headers", "after_punctuation", "between_words"]
            },
            "unicode_substitution": {
                "enabled": True,
                "confidence_level": "high",
                "target_chars": ["a", "e", "o", "p", "c", "x", "y"],
                "substitution_rate": 0.03
            },
            "spacing_manipulation": {
                "enabled": False,
                "micro_adjustments": True,
                "spacing_variance": 0.1
            },
            "metadata_manipulation": {
                "enabled": True,
                "modify_properties": True,
                "add_invisible_content": True
            }
        },
        "safety_settings": {
            "preserve_readability": True,
            "maintain_formatting": True,
            "backup_original": True,
            "max_changes_per_paragraph": 5,
            "avoid_obvious_patterns": True
        },
        "target_elements": {
            "headers": {
                "priority": "highest",
                "techniques": ["unicode_substitution", "invisible_chars"]
            },
            "first_sentences": {
                "priority": "high",
                "techniques": ["spacing_manipulation"]
            },
            "citations": {
                "priority": "medium",
                "techniques": ["invisible_chars"]
            },
            "conclusion_paragraphs": {
                "priority": "high",
                "techniques": ["unicode_substitution"]
            }
        }
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Sample config.json created")


def main():
    """Main function for testing"""
    print("🔮 INVISIBLE MANIPULATOR - TEST MODE")
    print("=" * 50)
    
    # Create sample config if it doesn't exist
    if not os.path.exists('config.json'):
        create_sample_config()
    
    # Initialize manipulator
    manipulator = InvisibleManipulator()
    
    # Test with sample document
    input_file = "input/sample_thesis.docx"
    
    if os.path.exists(input_file):
        print(f"🎯 Processing: {input_file}")
        
        result = manipulator.apply_invisible_manipulation(input_file)
        
        if result:
            print("\n🎉 Processing completed successfully!")
            print(f"📥 Input: {result['input_file']}")
            print(f"📤 Output: {result['output_file']}")
            
            if result['backup_file']:
                print(f"💾 Backup: {result['backup_file']}")
            
            # Verify invisibility
            if result['backup_file']:
                manipulator.verify_invisibility(result['backup_file'], result['output_file'])
        
    else:
        print(f"❌ Input file not found: {input_file}")
        print("💡 Please create the input directory and add a sample document")


if __name__ == "__main__":
    main()
