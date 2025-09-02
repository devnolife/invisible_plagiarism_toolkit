# contextual_paraphraser.py
"""
Contextual Paraphraser with Smart Synonym Detection
Sistem parafrase dengan deteksi konteks untuk memastikan sinonim yang tepat
"""

import json
import re
import random
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import logging

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.tag import pos_tag
    from nltk.corpus import wordnet
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except ImportError:
    print("NLTK not available, using basic tokenization")
    nltk = None

@dataclass
class ContextualReplacement:
    original: str
    replacement: str
    context_score: float
    pos_tag: str
    context_words: List[str]

class ContextualParaphraser:
    def __init__(self, sinonim_path: str = "data/sinonim.json", verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Load comprehensive synonym dictionary
        self.synonym_dict = self.load_sinonim_json(sinonim_path)
        
        # Context awareness patterns
        self.context_patterns = self.load_context_patterns()
        
        # Academic domain keywords for better context detection
        self.academic_domains = {
            'research': ['penelitian', 'riset', 'studi', 'kajian', 'analisis'],
            'business': ['konsumen', 'pelanggan', 'produk', 'kualitas', 'pasar'],
            'statistics': ['data', 'hasil', 'signifikan', 'korelasi', 'variabel'],
            'methodology': ['metode', 'pendekatan', 'teknik', 'prosedur', 'sistem']
        }
        
        # POS tag mapping for Indonesian
        self.pos_mapping = {
            'n': ['NN', 'NNS', 'NNP', 'NNPS'],  # Nouns
            'v': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],  # Verbs
            'adj': ['JJ', 'JJR', 'JJS'],  # Adjectives
            'adv': ['RB', 'RBR', 'RBS']   # Adverbs
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def load_sinonim_json(self, file_path: str) -> Dict[str, Dict]:
        """Load comprehensive sinonim.json file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"📚 Loaded {len(data)} entries from sinonim.json")
            return data
        except Exception as e:
            self.logger.error(f"Error loading sinonim.json: {e}")
            return {}
    
    def load_context_patterns(self) -> Dict[str, List[str]]:
        """Load contextual patterns for better synonym selection"""
        return {
            'academic_research': [
                'penelitian', 'riset', 'studi', 'kajian', 'analisis', 'observasi',
                'eksperimen', 'telaah', 'investigasi', 'eksplorasi'
            ],
            'business_consumer': [
                'konsumen', 'pelanggan', 'klien', 'pembeli', 'customer', 'nasabah',
                'produk', 'barang', 'jasa', 'layanan', 'komoditas'
            ],
            'quality_measurement': [
                'kualitas', 'mutu', 'standar', 'tingkat', 'level', 'derajat',
                'taraf', 'bobot', 'nilai', 'kapasitas'
            ],
            'causal_relationship': [
                'pengaruh', 'dampak', 'efek', 'akibat', 'imbas', 'konsekuensi',
                'berpengaruh', 'berdampak', 'menyebabkan', 'mengakibatkan'
            ]
        }
    
    def get_context_domain(self, text: str) -> str:
        """Identify the domain/context of the text"""
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, keywords in self.academic_domains.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
    def get_pos_tag(self, word: str, context: str) -> str:
        """Get POS tag for a word in context"""
        if nltk is None:
            # Simple heuristic if NLTK not available
            return 'n'  # Default to noun
        
        try:
            tokens = word_tokenize(context)
            pos_tags = pos_tag(tokens)
            
            for token, tag in pos_tags:
                if token.lower() == word.lower():
                    return tag
        except:
            pass
        
        return 'NN'  # Default noun tag
    
    def calculate_context_similarity(self, original: str, synonym: str, context: str) -> float:
        """Calculate how well a synonym fits the context"""
        context_lower = context.lower()
        synonym_lower = synonym.lower()
        original_lower = original.lower()
        
        # Base score
        score = 0.5
        
        # Academic context filters - VERY IMPORTANT
        academic_indicators = ['penelitian', 'analisis', 'berdasarkan', 'menunjukkan', 'hasil', 'studi']
        is_academic_context = any(indicator in context_lower for indicator in academic_indicators)
        
        if is_academic_context:
            # Filter out inappropriate synonyms for academic context
            inappropriate_academic = [
                'angsal', 'kata putus', 'buatan', 'rakitan', 'ketek', 'kecil', 
                'belalang', 'burung', 'semut', 'macam', 'jenis', 'nan', 
                'celah', 'lantai', 'abad', 'andal', 'ajaran', 'bayaran', 'becus'
            ]
            
            if synonym_lower in inappropriate_academic:
                return 0.1  # Very low score for inappropriate matches
            
            # Prefer academic-appropriate synonyms
            academic_preferred = {
                'hasil': ['temuan', 'capaian', 'pencapaian', 'output', 'outcome'],
                'penelitian': ['riset', 'studi', 'kajian', 'investigasi', 'eksplorasi'],
                'dapat': ['mampu', 'bisa', 'sanggup'],  # Not 'angsal'
                'keputusan': ['pilihan', 'penetapan', 'resolusi', 'alternatif'],  # Not 'kata putus'
                'produk': ['barang', 'komoditas', 'item'],  # OK options
                'kualitas': ['mutu', 'standar', 'tingkat', 'derajat'],
                'konsumen': ['pelanggan', 'klien', 'customer']
            }
            
            if original_lower in academic_preferred:
                preferred_list = academic_preferred[original_lower]
                if synonym_lower in [p.lower() for p in preferred_list]:
                    score += 0.3  # Bonus for preferred academic synonyms
                else:
                    score -= 0.2  # Penalty for non-preferred in academic context
        
        # Domain consistency check
        domain = self.get_context_domain(context)
        if domain in self.context_patterns:
            domain_words = self.context_patterns[domain]
            
            # Check if synonym appears in similar contexts
            for pattern_word in domain_words:
                if pattern_word in context_lower:
                    score += 0.1
        
        # Length similarity (prefer similar length synonyms)
        length_diff = abs(len(original) - len(synonym))
        if length_diff <= 2:
            score += 0.15
        elif length_diff <= 4:
            score += 0.05
        else:
            score -= 0.1  # Penalty for very different lengths
        
        # Formality level (academic texts prefer formal synonyms)
        if is_academic_context:
            # Prefer synonyms that are formal and appropriate
            if len(synonym) >= 4 and not any(char.isdigit() for char in synonym):
                score += 0.1
        
        # Avoid overly casual replacements in formal context
        casual_words = ['kayak', 'gitu', 'banget', 'keren', 'oke', 'nggak']
        if any(casual in synonym_lower for casual in casual_words):
            score -= 0.4
        
        # Avoid archaic/uncommon words that might be confusing
        archaic_words = ['angsal', 'ketek', 'belalang', 'semut', 'burung']
        if synonym_lower in archaic_words:
            score -= 0.5
        
        # Multiword synonyms handling
        if ' ' in synonym:
            # Prefer single words in most contexts unless multiword is very appropriate
            if is_academic_context and original_lower in ['keputusan pembelian', 'hasil penelitian']:
                score += 0.1  # OK for compound terms
            else:
                score -= 0.15  # Generally prefer single words
        
        return max(0.1, min(score, 1.0))  # Ensure score is between 0.1 and 1.0
    
    def get_best_synonym(self, word: str, context: str, pos_hint: str = None) -> Optional[ContextualReplacement]:
        """Get the best contextual synonym for a word"""
        word_lower = word.lower()
        
        if word_lower not in self.synonym_dict:
            return None
        
        synonym_data = self.synonym_dict[word_lower]
        synonyms = synonym_data.get('sinonim', [])
        word_pos = synonym_data.get('tag', 'n')
        
        if not synonyms:
            return None
        
        # Calculate context scores for all synonyms
        scored_synonyms = []
        for synonym in synonyms:
            synonym = synonym.strip()
            if synonym and synonym.lower() != word_lower:
                context_score = self.calculate_context_similarity(word, synonym, context)
                
                scored_synonyms.append({
                    'synonym': synonym,
                    'score': context_score,
                    'pos': word_pos
                })
        
        if not scored_synonyms:
            return None
        
        # Sort by context score and select best match
        scored_synonyms.sort(key=lambda x: x['score'], reverse=True)
        best = scored_synonyms[0]
        
        # Only use if context score is reasonable - raised threshold for better quality
        if best['score'] >= 0.65:
            context_words = self.extract_context_words(context, word)
            
            return ContextualReplacement(
                original=word,
                replacement=best['synonym'],
                context_score=best['score'],
                pos_tag=best['pos'],
                context_words=context_words
            )
        
        return None
    
    def extract_context_words(self, context: str, target_word: str, window: int = 3) -> List[str]:
        """Extract surrounding context words"""
        words = context.split()
        target_indices = [i for i, w in enumerate(words) if target_word.lower() in w.lower()]
        
        context_words = []
        for idx in target_indices:
            start = max(0, idx - window)
            end = min(len(words), idx + window + 1)
            context_words.extend(words[start:end])
        
        return list(set(context_words))
    
    def paraphrase_with_context(self, text: str, replacement_rate: float = 0.4) -> Dict:
        """
        Paraphrase text with contextual awareness
        """
        self.logger.info(f"🎯 Starting contextual paraphrasing (rate: {replacement_rate})")
        
        words = text.split()
        replacements = []
        modified_words = []
        
        for i, word in enumerate(words):
            # Clean word for lookup
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            # Skip if word is too short or contains numbers
            if len(clean_word) < 3 or any(c.isdigit() for c in clean_word):
                modified_words.append(word)
                continue
            
            # Get context window
            context_start = max(0, i - 5)
            context_end = min(len(words), i + 6)
            context = ' '.join(words[context_start:context_end])
            
            # Try to find contextual replacement
            if random.random() < replacement_rate:
                replacement = self.get_best_synonym(clean_word, context)
                
                if replacement and replacement.context_score >= 0.65:
                    # Preserve original case and punctuation
                    new_word = self.preserve_formatting(word, replacement.replacement)
                    modified_words.append(new_word)
                    
                    replacements.append(replacement)
                    self.logger.debug(f"🔄 {word} → {new_word} (score: {replacement.context_score:.2f})")
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        paraphrased_text = ' '.join(modified_words)
        
        # Calculate similarity reduction
        original_words = set(text.lower().split())
        paraphrased_words = set(paraphrased_text.lower().split())
        common_words = original_words.intersection(paraphrased_words)
        similarity_reduction = (1 - len(common_words) / len(original_words)) * 100 if original_words else 0
        
        return {
            'original_text': text,
            'paraphrased_text': paraphrased_text,
            'replacements': replacements,
            'similarity_reduction': similarity_reduction,
            'replacement_count': len(replacements),
            'average_context_score': sum(r.context_score for r in replacements) / len(replacements) if replacements else 0
        }
    
    def preserve_formatting(self, original: str, replacement: str) -> str:
        """Preserve capitalization and punctuation from original word"""
        # Check if original starts with capital
        if original and original[0].isupper():
            replacement = replacement.capitalize()
        
        # Check if original is all uppercase
        if original.isupper():
            replacement = replacement.upper()
        
        # Preserve trailing punctuation
        punctuation = ''
        for char in reversed(original):
            if not char.isalnum():
                punctuation = char + punctuation
            else:
                break
        
        return replacement + punctuation
    
    def batch_paraphrase_academic_text(self, text: str, intensity: str = "high") -> Dict:
        """
        Specialized paraphrasing for academic text with multiple techniques
        """
        # Set replacement rate based on intensity
        rate_mapping = {
            'low': 0.2,
            'medium': 0.4, 
            'high': 0.6,
            'extreme': 0.8
        }
        
        replacement_rate = rate_mapping.get(intensity, 0.4)
        
        # Apply contextual paraphrasing
        result = self.paraphrase_with_context(text, replacement_rate)
        
        # Apply academic phrase replacements (from original system)
        academic_phrases = {
            "Berdasarkan hasil penelitian": "Merujuk pada temuan riset",
            "dapat disimpulkan bahwa": "dapat dinyatakan bahwa",
            "Penelitian ini bertujuan": "Studi ini dimaksudkan",
            "Metode penelitian yang digunakan": "Pendekatan riset yang diterapkan",
            "Hasil penelitian menunjukkan": "Temuan kajian mengindikasikan",
            "pengaruh signifikan terhadap": "dampak substansial pada",
            "keputusan pembelian konsumen": "pilihan transaksi pelanggan"
        }
        
        modified_text = result['paraphrased_text']
        phrase_replacements = 0
        
        for original_phrase, replacement_phrase in academic_phrases.items():
            if original_phrase in modified_text:
                modified_text = modified_text.replace(original_phrase, replacement_phrase)
                phrase_replacements += 1
        
        # Update result
        result['paraphrased_text'] = modified_text
        result['phrase_replacements'] = phrase_replacements
        result['total_modifications'] = len(result['replacements']) + phrase_replacements
        
        # Recalculate similarity reduction
        original_words = set(text.lower().split())
        final_words = set(modified_text.lower().split())
        common_words = original_words.intersection(final_words)
        result['final_similarity_reduction'] = (1 - len(common_words) / len(original_words)) * 100 if original_words else 0
        
        return result

# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python contextual_paraphraser.py <text_to_paraphrase> [intensity]")
        sys.exit(1)
    
    text = sys.argv[1]
    intensity = sys.argv[2] if len(sys.argv) > 2 else "high"
    
    paraphraser = ContextualParaphraser(verbose=True)
    result = paraphraser.batch_paraphrase_academic_text(text, intensity)
    
    print("\n🎯 CONTEXTUAL PARAPHRASING RESULTS:")
    print(f"📝 Original: {result['original_text']}")
    print(f"✨ Paraphrased: {result['paraphrased_text']}")
    print(f"📊 Similarity Reduction: {result['final_similarity_reduction']:.1f}%")
    print(f"🔧 Total Modifications: {result['total_modifications']}")
    print(f"📈 Context Quality: {result['average_context_score']:.2f}/1.0")
    print(f"\n🔄 Replacements Made:")
    for replacement in result['replacements']:
        print(f"  {replacement.original} → {replacement.replacement} (score: {replacement.context_score:.2f})")