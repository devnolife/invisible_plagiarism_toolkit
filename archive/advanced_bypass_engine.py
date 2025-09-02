# advanced_bypass_engine.py
"""
Advanced Plagiarism Detection Bypass Engine
State-of-the-art techniques untuk mengatasi detector modern (2025)
"""

import re
import random
import nltk
from typing import Dict, List, Tuple, Optional
import unicodedata
from dataclasses import dataclass
import docx

# Download required NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')

from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag

@dataclass
class BypassResult:
    original_text: str
    modified_text: str
    changes_made: int
    invisibility_score: float
    bypass_techniques_used: List[str]
    risk_assessment: Dict[str, float]

class AdvancedBypassEngine:
    """Engine canggih untuk bypass plagiarism detection modern"""
    
    def __init__(self, aggression_level: str = "high"):
        self.aggression_level = aggression_level
        
        # Advanced Unicode mappings (lebih ekstensif)
        self.advanced_unicode_maps = {
            # Cyrillic yang sangat mirip
            'a': ['а', 'ɑ', 'α'], 'e': ['е', 'ε'], 'o': ['о', 'ο', 'ο'],
            'p': ['р', 'ρ'], 'c': ['с', 'ϲ'], 'x': ['х', 'χ'], 
            'y': ['у', 'γ'], 'i': ['і', 'ι'], 'A': ['А', 'Α'],
            'B': ['В', 'Β'], 'C': ['С'], 'E': ['Е', 'Ε'], 
            'H': ['Н', 'Η'], 'K': ['К', 'Κ'], 'M': ['М', 'Μ'],
            'N': ['Н', 'Ν'], 'O': ['О', 'Ο'], 'P': ['Р', 'Ρ'],
            'T': ['Т', 'Τ'], 'X': ['Х', 'Χ'], 'Y': ['У', 'Υ']
        }
        
        # Indonesian academic synonyms
        self.academic_synonyms = {
            'penelitian': ['kajian', 'studi', 'riset', 'eksplorasi'],
            'analisis': ['evaluasi', 'pengkajian', 'telaah', 'penelaahan'],
            'metode': ['cara', 'pendekatan', 'teknik', 'prosedur'],
            'hasil': ['temuan', 'outcome', 'luaran', 'capaian'],
            'data': ['informasi', 'fakta', 'keterangan'],
            'teori': ['konsep', 'gagasan', 'pemikiran'],
            'faktor': ['unsur', 'elemen', 'aspek', 'komponen'],
            'pengaruh': ['dampak', 'efek', 'imbas', 'konsekuensi'],
            'hubungan': ['relasi', 'keterkaitan', 'koneksi'],
            'perbedaan': ['disparitas', 'ketidaksamaan', 'variasi'],
            'peningkatan': ['kemajuan', 'perkembangan', 'pertumbuhan'],
            'penurunan': ['pengurangan', 'reduksi', 'degradasi'],
            'pembahasan': ['diskusi', 'uraian', 'elaborasi'],
            'kesimpulan': ['konklusi', 'inferensi', 'deduksi'],
            'rekomendasi': ['saran', 'usulan', 'anjuran'],
            'implementasi': ['penerapan', 'pelaksanaan', 'aplikasi'],
            'evaluasi': ['penilaian', 'asesmen', 'pengukuran'],
            'observasi': ['pengamatan', 'pemantauan', 'monitoring'],
            'wawancara': ['interviu', 'tanya jawab'],
            'responden': ['narasumber', 'informan', 'partisipan'],
            'sampel': ['contoh', 'specimen'],
            'populasi': ['kelompok sasaran', 'target grup'],
            'variabel': ['peubah', 'faktor'],
            'hipotesis': ['dugaan', 'asumsi', 'prediksi'],
            'signifikan': ['bermakna', 'berarti', 'penting'],
            'korelasi': ['hubungan', 'asosiasi', 'keterkaitan']
        }
        
        # Advanced invisible characters (lebih banyak)
        self.advanced_invisible_chars = [
            '\u200B',  # Zero width space
            '\u200C',  # Zero width non-joiner
            '\u200D',  # Zero width joiner
            '\uFEFF',  # Zero width no-break space
            '\u2060',  # Word joiner
            '\u180E',  # Mongolian vowel separator
            '\u034F',  # Combining grapheme joiner
            '\u061C',  # Arabic letter mark
            '\u17B4',  # Khmer vowel inherent Aq
            '\u17B5'   # Khmer vowel inherent Aa
        ]
        
        # Sentence transformation patterns
        self.sentence_patterns = [
            # Passive to active transformation patterns
            (r'(\w+) dilakukan oleh (\w+)', r'\2 melakukan \1'),
            (r'(\w+) digunakan untuk (\w+)', r'menggunakan \1 untuk \2'),
            (r'(\w+) ditunjukkan bahwa', r'menunjukkan bahwa \1'),
            # Add more patterns...
        ]
        
        print(f"🚀 Advanced Bypass Engine initialized (Level: {aggression_level})")
    
    def apply_comprehensive_bypass(self, text: str, target_detector: str = "turnitin") -> BypassResult:
        """Apply comprehensive bypass techniques"""
        
        original_text = text
        modified_text = text
        changes_made = 0
        techniques_used = []
        
        # 1. Advanced Unicode substitution (20-40% rate)
        if self.aggression_level in ["high", "extreme"]:
            modified_text, unicode_changes = self._advanced_unicode_substitution(modified_text, rate=0.25)
            changes_made += unicode_changes
            if unicode_changes > 0:
                techniques_used.append("advanced_unicode")
        
        # 2. Semantic synonym replacement (10-30% words)
        modified_text, synonym_changes = self._semantic_synonym_replacement(modified_text, rate=0.20)
        changes_made += synonym_changes
        if synonym_changes > 0:
            techniques_used.append("semantic_synonyms")
        
        # 3. Sentence structure manipulation
        modified_text, structure_changes = self._sentence_restructuring(modified_text)
        changes_made += structure_changes
        if structure_changes > 0:
            techniques_used.append("sentence_restructuring")
        
        # 4. Advanced invisible character injection (15% rate)
        modified_text, invisible_changes = self._advanced_invisible_injection(modified_text, rate=0.15)
        changes_made += invisible_changes
        if invisible_changes > 0:
            techniques_used.append("advanced_invisible")
        
        # 5. Micro-spacing manipulation
        modified_text, spacing_changes = self._micro_spacing_manipulation(modified_text)
        changes_made += spacing_changes
        if spacing_changes > 0:
            techniques_used.append("micro_spacing")
        
        # 6. Academic phrase variation
        modified_text, phrase_changes = self._academic_phrase_variation(modified_text)
        changes_made += phrase_changes
        if phrase_changes > 0:
            techniques_used.append("phrase_variation")
        
        # Calculate metrics
        invisibility_score = self._calculate_invisibility_score(original_text, modified_text)
        risk_assessment = self._assess_detection_risk(modified_text, target_detector)
        
        return BypassResult(
            original_text=original_text,
            modified_text=modified_text,
            changes_made=changes_made,
            invisibility_score=invisibility_score,
            bypass_techniques_used=techniques_used,
            risk_assessment=risk_assessment
        )
    
    def _advanced_unicode_substitution(self, text: str, rate: float = 0.25) -> Tuple[str, int]:
        """Advanced Unicode substitution dengan multiple alternatives"""
        
        modified = list(text)
        changes = 0
        
        for i, char in enumerate(modified):
            if char.lower() in self.advanced_unicode_maps and random.random() < rate:
                alternatives = self.advanced_unicode_maps[char.lower()]
                # Pilih alternatif yang paling mirip
                if char.isupper() and alternatives:
                    # Cari versi uppercase jika ada
                    upper_alternatives = [alt for alt in alternatives if alt != char.lower()]
                    if upper_alternatives:
                        modified[i] = random.choice(upper_alternatives).upper()
                        changes += 1
                elif alternatives:
                    modified[i] = random.choice(alternatives)
                    changes += 1
        
        return ''.join(modified), changes
    
    def _semantic_synonym_replacement(self, text: str, rate: float = 0.20) -> Tuple[str, int]:
        """Replace words with semantic synonyms"""
        
        words = word_tokenize(text)
        modified_words = []
        changes = 0
        
        for word in words:
            word_lower = word.lower()
            
            # Check Indonesian academic synonyms first
            if word_lower in self.academic_synonyms and random.random() < rate:
                synonyms = self.academic_synonyms[word_lower]
                replacement = random.choice(synonyms)
                
                # Preserve original case
                if word.isupper():
                    replacement = replacement.upper()
                elif word.istitle():
                    replacement = replacement.title()
                
                modified_words.append(replacement)
                changes += 1
            else:
                # Try WordNet for English words
                try:
                    synsets = wordnet.synsets(word_lower)
                    if synsets and random.random() < rate * 0.3:  # Lower rate for English
                        synonyms = []
                        for synset in synsets[:3]:  # Top 3 synsets
                            for lemma in synset.lemmas()[:2]:  # Top 2 lemmas per synset
                                synonym = lemma.name().replace('_', ' ')
                                if synonym.lower() != word_lower:
                                    synonyms.append(synonym)
                        
                        if synonyms:
                            replacement = random.choice(synonyms)
                            if word.isupper():
                                replacement = replacement.upper()
                            elif word.istitle():
                                replacement = replacement.title()
                            
                            modified_words.append(replacement)
                            changes += 1
                        else:
                            modified_words.append(word)
                    else:
                        modified_words.append(word)
                except:
                    modified_words.append(word)
        
        return ' '.join(modified_words), changes
    
    def _sentence_restructuring(self, text: str) -> Tuple[str, int]:
        """Restructure sentences to avoid pattern detection"""
        
        sentences = sent_tokenize(text)
        modified_sentences = []
        changes = 0
        
        for sentence in sentences:
            modified_sentence = sentence
            
            # Apply transformation patterns
            for pattern, replacement in self.sentence_patterns:
                if re.search(pattern, sentence):
                    new_sentence = re.sub(pattern, replacement, sentence)
                    if new_sentence != sentence:
                        modified_sentence = new_sentence
                        changes += 1
                        break
            
            # Add variety in sentence starters
            if random.random() < 0.1:  # 10% chance
                modified_sentence = self._vary_sentence_starter(modified_sentence)
                if modified_sentence != sentence:
                    changes += 1
            
            modified_sentences.append(modified_sentence)
        
        return ' '.join(modified_sentences), changes
    
    def _vary_sentence_starter(self, sentence: str) -> str:
        """Add variety to sentence starters"""
        
        starters = {
            'Hasil penelitian menunjukkan': ['Temuan penelitian mengindikasikan', 'Studi ini menemukan', 'Berdasarkan analisis'],
            'Berdasarkan hasil': ['Mengacu pada temuan', 'Sesuai dengan hasil', 'Merujuk pada data'],
            'Dapat disimpulkan': ['Dapat diinferensi', 'Dapat dinyatakan', 'Dapat dikemukakan'],
            'Penelitian ini': ['Studi ini', 'Kajian ini', 'Riset ini'],
            'Hal ini menunjukkan': ['Ini mengindikasikan', 'Kondisi ini mencerminkan', 'Fakta ini mendemonstrasikan']
        }
        
        for original, alternatives in starters.items():
            if sentence.startswith(original):
                return sentence.replace(original, random.choice(alternatives), 1)
        
        return sentence
    
    def _advanced_invisible_injection(self, text: str, rate: float = 0.15) -> Tuple[str, int]:
        """Inject advanced invisible characters strategically"""
        
        result = []
        changes = 0
        
        for i, char in enumerate(text):
            result.append(char)
            
            # Insert after punctuation, spaces, or randomly
            if (char in '.,;:!?' or char.isspace()) and random.random() < rate:
                invisible_char = random.choice(self.advanced_invisible_chars)
                result.append(invisible_char)
                changes += 1
            elif char.isalpha() and random.random() < rate * 0.3:  # Lower rate within words
                invisible_char = random.choice(self.advanced_invisible_chars[:4])  # Use safer ones
                result.append(invisible_char)
                changes += 1
        
        return ''.join(result), changes
    
    def _micro_spacing_manipulation(self, text: str) -> Tuple[str, int]:
        """Manipulate spacing at micro level"""
        
        # Replace normal spaces with various Unicode space characters
        space_variants = [
            ' ',      # Normal space
            '\u2009', # Thin space
            '\u2008', # Punctuation space
            '\u2007', # Figure space
            '\u2006', # Six-per-em space
        ]
        
        result = []
        changes = 0
        
        for char in text:
            if char == ' ' and random.random() < 0.1:  # 10% of spaces
                result.append(random.choice(space_variants[1:]))  # Avoid normal space
                changes += 1
            else:
                result.append(char)
        
        return ''.join(result), changes
    
    def _academic_phrase_variation(self, text: str) -> Tuple[str, int]:
        """Vary common academic phrases"""
        
        phrase_variations = {
            'penelitian ini bertujuan untuk': [
                'studi ini dimaksudkan untuk',
                'kajian ini diarahkan untuk',
                'riset ini didesain untuk'
            ],
            'berdasarkan hasil penelitian': [
                'mengacu pada temuan studi',
                'sesuai dengan hasil kajian',
                'merujuk pada data riset'
            ],
            'dapat disimpulkan bahwa': [
                'dapat diinferensi bahwa',
                'dapat dinyatakan bahwa',
                'dapat dikemukakan bahwa'
            ],
            'hal ini disebabkan oleh': [
                'kondisi ini diakibatkan oleh',
                'fenomena ini dipicu oleh',
                'situasi ini dipengaruhi oleh'
            ]
        }
        
        modified_text = text
        changes = 0
        
        for original_phrase, variations in phrase_variations.items():
            if original_phrase in modified_text.lower():
                replacement = random.choice(variations)
                modified_text = re.sub(
                    re.escape(original_phrase), 
                    replacement, 
                    modified_text, 
                    flags=re.IGNORECASE
                )
                changes += 1
        
        return modified_text, changes
    
    def _calculate_invisibility_score(self, original: str, modified: str) -> float:
        """Calculate how invisible the changes are"""
        
        # Visual similarity check
        original_visible = ''.join(c for c in original if unicodedata.category(c)[0] != 'C')
        modified_visible = ''.join(c for c in modified if unicodedata.category(c)[0] != 'C')
        
        # Calculate edit distance
        import difflib
        similarity = difflib.SequenceMatcher(None, original_visible, modified_visible).ratio()
        
        return similarity
    
    def _assess_detection_risk(self, text: str, detector: str) -> Dict[str, float]:
        """Assess detection risk for specific plagiarism detector"""
        
        risk_factors = {
            'unicode_density': 0,
            'invisible_char_density': 0,
            'pattern_regularity': 0,
            'semantic_coherence': 0,
            'overall_risk': 0
        }
        
        # Calculate Unicode density
        unicode_chars = sum(1 for c in text if ord(c) > 127)
        risk_factors['unicode_density'] = min(1.0, unicode_chars / len(text) * 10)
        
        # Calculate invisible character density
        invisible_chars = sum(1 for c in text if unicodedata.category(c) == 'Cf')
        risk_factors['invisible_char_density'] = min(1.0, invisible_chars / len(text) * 20)
        
        # Pattern regularity (simplified)
        risk_factors['pattern_regularity'] = 0.3  # Placeholder
        
        # Semantic coherence (simplified)
        risk_factors['semantic_coherence'] = 0.2  # Placeholder
        
        # Overall risk calculation
        weights = {'unicode_density': 0.3, 'invisible_char_density': 0.3, 
                  'pattern_regularity': 0.2, 'semantic_coherence': 0.2}
        
        risk_factors['overall_risk'] = sum(
            risk_factors[factor] * weight 
            for factor, weight in weights.items()
        )
        
        return risk_factors

def create_ultra_aggressive_config() -> Dict:
    """Create configuration for maximum bypass effectiveness"""
    
    return {
        "invisible_techniques": {
            "unicode_substitution": {
                "enabled": True,
                "substitution_rate": 0.30,  # 30% (sangat tinggi)
                "use_advanced_mappings": True,
                "multiple_alternatives": True,
                "target_chars": ["a", "e", "o", "p", "c", "x", "y", "i", "A", "B", "C", "E", "H", "K", "M", "N", "O", "P", "T", "X", "Y"]
            },
            "zero_width_chars": {
                "enabled": True,
                "insertion_rate": 0.20,  # 20% (sangat tinggi)
                "advanced_chars": True,
                "strategic_placement": True,
                "target_locations": ["headers", "after_punctuation", "between_words", "within_words"]
            },
            "semantic_replacement": {
                "enabled": True,
                "replacement_rate": 0.25,  # 25% kata diganti
                "academic_synonyms": True,
                "wordnet_synonyms": True,
                "preserve_meaning": True
            },
            "sentence_restructuring": {
                "enabled": True,
                "restructure_rate": 0.15,  # 15% kalimat direstruktur
                "passive_active_conversion": True,
                "phrase_variation": True,
                "starter_variation": True
            },
            "micro_spacing": {
                "enabled": True,
                "spacing_variation_rate": 0.10,
                "unicode_spaces": True,
                "strategic_placement": True
            }
        },
        "detection_targets": {
            "turnitin": {
                "priority": "extreme",
                "specific_countermeasures": True,
                "semantic_analysis_bypass": True,
                "fingerprint_disruption": True
            },
            "copyscape": {
                "priority": "high",
                "text_fragmentation": True,
                "sequence_disruption": True
            },
            "plagscan": {
                "priority": "high",
                "unicode_bypass": True,
                "semantic_bypass": True
            },
            "grammarly": {
                "priority": "medium",
                "basic_substitution": True
            }
        },
        "safety_settings": {
            "preserve_readability": True,
            "maintain_academic_tone": True,
            "backup_original": True,
            "max_changes_per_paragraph": 15,  # Tingkatkan batas
            "avoid_obvious_patterns": True,
            "quality_check": True
        }
    }
