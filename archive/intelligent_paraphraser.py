# intelligent_paraphraser.py
"""
Intelligent Paraphrasing Engine
Sistem parafrase otomatis dengan fokus pada area yang ditandai Turnitin
"""

import re
import json
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

@dataclass
class ParaphraseResult:
    original_text: str
    paraphrased_text: str
    similarity_reduction: float
    techniques_used: List[str]
    word_count_change: int

class IntelligentParaphraser:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Load paraphrasing dictionaries
        self.synonym_dict = self.load_synonym_dictionary()
        self.phrase_templates = self.load_phrase_templates()
        self.academic_replacements = self.load_academic_replacements()
        
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def load_synonym_dictionary(self) -> Dict[str, List[str]]:
        """Load comprehensive synonym dictionary"""
        return {
            # Verbs - Academic context
            "mempengaruhi": ["memengaruhi", "berdampak pada", "berpengaruh terhadap", "memberikan efek pada"],
            "menunjukkan": ["memperlihatkan", "mengindikasikan", "menyiratkan", "menampilkan", "membuktikan"],
            "menggunakan": ["memanfaatkan", "memakai", "menerapkan", "mengaplikasikan"],
            "melakukan": ["menjalankan", "mengerjakan", "menyelenggarakan", "melaksanakan"],
            "menganalisis": ["meneliti", "mengkaji", "menelaah", "mengamati", "mengevaluasi"],
            "menjelaskan": ["memaparkan", "menguraikan", "mendeskripsikan", "menyajikan"],
            
            # Nouns - Business/Academic
            "penelitian": ["riset", "studi", "kajian", "analisis", "observasi"],
            "konsumen": ["pelanggan", "pembeli", "customer", "klien"],
            "keputusan": ["pilihan", "penetapan", "resolusi", "opsi", "alternatif"],
            "pembelian": ["transaksi", "akuisisi", "perolehan", "pengadaan"],
            "kualitas": ["mutu", "standar", "tingkat", "level", "derajat"],
            "produk": ["barang", "item", "komoditas", "merchandise"],
            "harga": ["tarif", "biaya", "cost", "nilai"],
            "merek": ["brand", "label", "nama dagang"],
            "citra": ["image", "reputasi", "persepsi", "gambaran"],
            "kepuasan": ["satisfaction", "pemenuhan", "gratifikasi"],
            "pengaruh": ["dampak", "efek", "imbas", "akibat", "konsekuensi"],
            
            # Adjectives
            "signifikan": ["penting", "berarti", "bermakna", "substansial", "considerable"],
            "positif": ["baik", "menguntungkan", "favorable", "konstruktif"],
            "negatif": ["buruk", "merugikan", "unfavorable", "destruktif"],
            "tinggi": ["elevasi", "besar", "substantial", "considerable"],
            "rendah": ["minim", "sedikit", "kecil", "terbatas"],
            
            # Academic phrases
            "berdasarkan": ["menurut", "sesuai dengan", "mengacu pada", "berpedoman pada"],
            "hasil": ["output", "outcome", "temuan", "capaian", "pencapaian"],
            "data": ["informasi", "fakta", "statistik", "angka"],
            "metode": ["cara", "teknik", "pendekatan", "strategi", "sistem"],
            "tujuan": ["sasaran", "target", "objektif", "maksud", "goal"],
            "faktor": ["elemen", "aspek", "komponen", "unsur", "variabel"]
        }
    
    def load_phrase_templates(self) -> Dict[str, List[str]]:
        """Load phrase restructuring templates"""
        return {
            "berdasarkan_hasil": [
                "Berdasarkan hasil {}", 
                "Mengacu pada temuan {}",
                "Sesuai dengan output {}",
                "Merujuk pada capaian {}",
                "Berpedoman pada data {}"
            ],
            "penelitian_menunjukkan": [
                "penelitian menunjukkan",
                "riset mengindikasikan", 
                "studi memperlihatkan",
                "kajian menyiratkan",
                "analisis membuktikan"
            ],
            "pengaruh_terhadap": [
                "pengaruh {} terhadap {}",
                "dampak {} pada {}",
                "efek {} atas {}",
                "imbas {} kepada {}",
                "konsekuensi {} bagi {}"
            ],
            "keputusan_pembelian": [
                "keputusan pembelian",
                "pilihan transaksi",
                "penetapan akuisisi", 
                "opsi perolehan",
                "resolusi pengadaan"
            ]
        }
    
    def load_academic_replacements(self) -> Dict[str, str]:
        """Load academic phrase replacements"""
        return {
            "Berdasarkan hasil penelitian dapat disimpulkan": "Merujuk pada temuan riset, dapat dinyatakan",
            "Penelitian ini bertujuan untuk": "Studi ini dimaksudkan untuk",
            "Metode penelitian yang digunakan": "Pendekatan riset yang diterapkan",
            "Hasil penelitian menunjukkan": "Temuan kajian mengindikasikan",
            "keputusan pembelian konsumen": "pilihan transaksi pelanggan",
            "kualitas produk dan layanan": "mutu barang serta pelayanan",
            "pengaruh signifikan terhadap": "dampak substansial pada",
            "Dari hasil penelitian": "Berdasarkan temuan studi",
            "dapat disimpulkan bahwa": "dapat dinyatakan bahwa",
            "BAB I PENDAHULUAN": "BAB 1 PENGANTAR",
            "BAB II TINJAUAN PUSTAKA": "BAB 2 LANDASAN TEORI",
            "BAB III METODE PENELITIAN": "BAB 3 METODOLOGI RISET"
        }
    
    def paraphrase_text(self, text: str, intensity: str = "medium") -> ParaphraseResult:
        """
        Main paraphrasing function
        intensity: low, medium, high, extreme
        """
        self.logger.info(f"🔄 Paraphrasing text (intensity: {intensity})")
        
        original_text = text
        paraphrased = text
        techniques_used = []
        
        # Apply different techniques based on intensity
        if intensity in ["medium", "high", "extreme"]:
            paraphrased, tech1 = self.replace_academic_phrases(paraphrased)
            techniques_used.extend(tech1)
            
        if intensity in ["high", "extreme"]:
            paraphrased, tech2 = self.synonym_replacement(paraphrased)
            techniques_used.extend(tech2)
            
        if intensity in ["extreme"]:
            paraphrased, tech3 = self.sentence_restructuring(paraphrased)
            techniques_used.extend(tech3)
            
        if intensity in ["medium", "high", "extreme"]:
            paraphrased, tech4 = self.phrase_template_replacement(paraphrased)
            techniques_used.extend(tech4)
        
        # Calculate similarity reduction (estimated)
        similarity_reduction = self.estimate_similarity_reduction(original_text, paraphrased)
        word_count_change = len(paraphrased.split()) - len(original_text.split())
        
        return ParaphraseResult(
            original_text=original_text,
            paraphrased_text=paraphrased,
            similarity_reduction=similarity_reduction,
            techniques_used=list(set(techniques_used)),
            word_count_change=word_count_change
        )
    
    def replace_academic_phrases(self, text: str) -> Tuple[str, List[str]]:
        """Replace common academic phrases"""
        modified_text = text
        techniques = []
        
        for original, replacement in self.academic_replacements.items():
            if original.lower() in modified_text.lower():
                # Case-insensitive replacement
                pattern = re.compile(re.escape(original), re.IGNORECASE)
                modified_text = pattern.sub(replacement, modified_text)
                techniques.append("academic_phrase_replacement")
                self.logger.debug(f"Replaced: {original} → {replacement}")
        
        return modified_text, techniques
    
    def synonym_replacement(self, text: str, replacement_rate: float = 0.4) -> Tuple[str, List[str]]:
        """Replace words with synonyms"""
        words = text.split()
        modified_words = []
        techniques = []
        
        for word in words:
            cleaned_word = re.sub(r'[^\w]', '', word.lower())
            
            # Check if word has synonyms
            if cleaned_word in self.synonym_dict:
                # Apply replacement based on rate
                if random.random() < replacement_rate:
                    synonyms = self.synonym_dict[cleaned_word]
                    replacement = random.choice(synonyms)
                    
                    # Preserve original case and punctuation
                    if word[0].isupper():
                        replacement = replacement.capitalize()
                    
                    # Preserve punctuation
                    punctuation = re.findall(r'[^\w]', word)
                    if punctuation:
                        replacement += ''.join(punctuation)
                    
                    modified_words.append(replacement)
                    techniques.append("synonym_replacement")
                    self.logger.debug(f"Synonym: {word} → {replacement}")
                else:
                    modified_words.append(word)
            else:
                modified_words.append(word)
        
        return ' '.join(modified_words), techniques
    
    def phrase_template_replacement(self, text: str) -> Tuple[str, List[str]]:
        """Replace phrase structures using templates"""
        modified_text = text
        techniques = []
        
        # Replace "pengaruh X terhadap Y" patterns
        pattern = r'pengaruh\s+([\w\s]+?)\s+terhadap\s+([\w\s]+?)(?=\s|$|\.|\,)'
        matches = re.finditer(pattern, modified_text, re.IGNORECASE)
        
        for match in matches:
            x_factor = match.group(1).strip()
            y_factor = match.group(2).strip()
            
            templates = self.phrase_templates["pengaruh_terhadap"]
            new_phrase = random.choice(templates).format(x_factor, y_factor)
            
            modified_text = modified_text.replace(match.group(0), new_phrase)
            techniques.append("phrase_restructuring")
            self.logger.debug(f"Restructured: {match.group(0)} → {new_phrase}")
        
        return modified_text, techniques
    
    def sentence_restructuring(self, text: str) -> Tuple[str, List[str]]:
        """Restructure sentences for variety"""
        sentences = re.split(r'\.(?=\s|$)', text)
        modified_sentences = []
        techniques = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Simple active to passive conversion patterns
            active_patterns = [
                (r'(\w+)\s+mempengaruhi\s+(.+)', r'\2 dipengaruhi oleh \1'),
                (r'(\w+)\s+menunjukkan\s+(.+)', r'\2 ditunjukkan oleh \1'),
                (r'penelitian\s+ini\s+(.+)', r'\1 dalam penelitian ini')
            ]
            
            modified_sentence = sentence
            for pattern, replacement in active_patterns:
                if re.search(pattern, sentence.lower()):
                    modified_sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
                    techniques.append("sentence_restructuring")
                    break
            
            modified_sentences.append(modified_sentence)
        
        return '. '.join(modified_sentences), techniques
    
    def estimate_similarity_reduction(self, original: str, paraphrased: str) -> float:
        """Estimate similarity reduction percentage"""
        original_words = set(original.lower().split())
        paraphrased_words = set(paraphrased.lower().split())
        
        if not original_words:
            return 0.0
        
        common_words = original_words.intersection(paraphrased_words)
        similarity = len(common_words) / len(original_words)
        reduction = (1 - similarity) * 100
        
        return min(reduction, 85.0)  # Cap at 85% reduction
    
    def batch_paraphrase_flagged_sections(self, flagged_sections: List[Dict], intensity: str = "high") -> List[ParaphraseResult]:
        """Paraphrase multiple flagged sections"""
        results = []
        
        for section in flagged_sections:
            if section.get('flagged_type') in ['academic_pattern', 'academic_phrase']:
                text = section.get('text', '')
                if len(text.strip()) > 10:  # Only paraphrase substantial text
                    result = self.paraphrase_text(text, intensity)
                    results.append(result)
                    
                    self.logger.info(f"📝 Paraphrased: {text[:50]}...")
                    self.logger.info(f"✨ Result: {result.paraphrased_text[:50]}...")
        
        return results
    
    def save_paraphrase_report(self, results: List[ParaphraseResult], output_path: str):
        """Save paraphrasing results to JSON"""
        from datetime import datetime
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_paraphrased": len(results),
            "average_similarity_reduction": sum(r.similarity_reduction for r in results) / len(results) if results else 0,
            "techniques_summary": {},
            "paraphrase_results": []
        }
        
        # Count techniques
        all_techniques = []
        for result in results:
            all_techniques.extend(result.techniques_used)
        
        technique_counts = {}
        for technique in all_techniques:
            technique_counts[technique] = technique_counts.get(technique, 0) + 1
        
        report_data["techniques_summary"] = technique_counts
        
        # Add detailed results
        for result in results:
            report_data["paraphrase_results"].append({
                "original_text": result.original_text,
                "paraphrased_text": result.paraphrased_text,
                "similarity_reduction": result.similarity_reduction,
                "techniques_used": result.techniques_used,
                "word_count_change": result.word_count_change
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"📊 Paraphrase report saved: {output_path}")

# Example usage
if __name__ == "__main__":
    import sys
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("Usage: python intelligent_paraphraser.py <text_to_paraphrase> [intensity]")
        print("Intensity options: low, medium, high, extreme")
        sys.exit(1)
    
    text = sys.argv[1]
    intensity = sys.argv[2] if len(sys.argv) > 2 else "high"
    
    paraphraser = IntelligentParaphraser(verbose=True)
    result = paraphraser.paraphrase_text(text, intensity)
    
    print("\n🔄 PARAPHRASING RESULTS:")
    print(f"📝 Original: {result.original_text}")
    print(f"✨ Paraphrased: {result.paraphrased_text}")
    print(f"📊 Similarity Reduction: {result.similarity_reduction:.2f}%")
    print(f"🔧 Techniques Used: {', '.join(result.techniques_used)}")
    print(f"📈 Word Count Change: {result.word_count_change:+d}")