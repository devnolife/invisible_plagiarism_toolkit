# indo_t5_paraphraser.py
"""
Indonesian T5 Neural Paraphraser
Advanced neural paraphrasing using Indonesian T5 model
"""

import os
import re
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

try:
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Transformers not available. Install with: pip install transformers torch")
    TRANSFORMERS_AVAILABLE = False

@dataclass
class T5ParaphraseResult:
    original_text: str
    paraphrased_text: str
    confidence_score: float
    model_used: str
    processing_time: float
    alternatives: List[str] = None

class IndoT5Paraphraser:
    def __init__(self, model_name: str = "Wikidepia/IndoT5-base-paraphrase", verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Model loading configuration
        self.max_length = 512
        self.generation_config = {
            'max_length': 512,
            'num_beams': 4,
            'early_stopping': True,
            'do_sample': True,
            'temperature': 0.8,
            'top_k': 50,
            'top_p': 0.95,
            'no_repeat_ngram_size': 3
        }
        
        # Initialize model
        if TRANSFORMERS_AVAILABLE:
            self._load_model()
        else:
            self.logger.error("Transformers library not available")
    
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def _load_model(self):
        """Load Indonesian T5 model and tokenizer"""
        try:
            self.logger.info(f"🔄 Loading IndoT5 model: {self.model_name}")
            
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            
            self.logger.info(f"✅ IndoT5 model loaded successfully on {self.device}")
            
        except Exception as e:
            self.logger.error(f"Failed to load IndoT5 model: {e}")
            self.logger.info("💡 Trying alternative model: t5-small")
            
            try:
                # Fallback to smaller model
                self.model_name = "t5-small"
                self.tokenizer = T5Tokenizer.from_pretrained("t5-small")
                self.model = T5ForConditionalGeneration.from_pretrained("t5-small")
                self.model.to(self.device)
                self.model.eval()
                
                self.logger.info("✅ Fallback T5-small model loaded")
                
            except Exception as e2:
                self.logger.error(f"Failed to load fallback model: {e2}")
                self.model = None
                self.tokenizer = None
    
    def is_available(self) -> bool:
        """Check if T5 model is available"""
        return self.model is not None and self.tokenizer is not None
    
    def paraphrase_text(self, text: str, num_return_sequences: int = 1) -> T5ParaphraseResult:
        """
        Paraphrase text using Indonesian T5 model
        """
        if not self.is_available():
            return T5ParaphraseResult(
                original_text=text,
                paraphrased_text=text,
                confidence_score=0.0,
                model_used="None (model not available)",
                processing_time=0.0,
                alternatives=[]
            )
        
        start_time = time.time()
        
        try:
            # Prepare input for T5
            # For paraphrasing, we use the format: "paraphrase: [text]"
            input_text = f"paraphrase: {text}"
            
            self.logger.debug(f"🔄 Processing: {text[:50]}...")
            
            # Tokenize input
            inputs = self.tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=self.max_length,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Generate paraphrases
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    num_return_sequences=num_return_sequences,
                    **self.generation_config
                )
            
            # Decode results
            paraphrases = []
            for output in outputs:
                decoded = self.tokenizer.decode(output, skip_special_tokens=True)
                # Clean up the output
                cleaned = self._clean_output(decoded)
                if cleaned and cleaned.lower() != text.lower():
                    paraphrases.append(cleaned)
            
            # Select best paraphrase
            if paraphrases:
                best_paraphrase = paraphrases[0]  # First one is usually best with beam search
                alternatives = paraphrases[1:] if len(paraphrases) > 1 else []
                confidence_score = self._calculate_confidence_score(text, best_paraphrase)
            else:
                best_paraphrase = text
                alternatives = []
                confidence_score = 0.0
            
            processing_time = time.time() - start_time
            
            self.logger.debug(f"✅ Generated paraphrase in {processing_time:.2f}s")
            
            return T5ParaphraseResult(
                original_text=text,
                paraphrased_text=best_paraphrase,
                confidence_score=confidence_score,
                model_used=self.model_name,
                processing_time=processing_time,
                alternatives=alternatives
            )
            
        except Exception as e:
            self.logger.error(f"Error during paraphrasing: {e}")
            processing_time = time.time() - start_time
            
            return T5ParaphraseResult(
                original_text=text,
                paraphrased_text=text,
                confidence_score=0.0,
                model_used=f"{self.model_name} (error)",
                processing_time=processing_time,
                alternatives=[]
            )
    
    def _clean_output(self, text: str) -> str:
        """Clean and post-process T5 output"""
        # Remove common T5 artifacts
        text = re.sub(r'^(paraphrase:|translate:|summarize:)', '', text, flags=re.IGNORECASE).strip()
        
        # Fix common spacing issues
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        return text.strip()
    
    def _calculate_confidence_score(self, original: str, paraphrased: str) -> float:
        """Calculate confidence score based on quality metrics"""
        if not paraphrased or paraphrased == original:
            return 0.0
        
        # Calculate various quality metrics
        score = 0.5  # Base score
        
        # Length similarity (good paraphrases are similar length)
        length_ratio = min(len(paraphrased), len(original)) / max(len(paraphrased), len(original))
        score += length_ratio * 0.2
        
        # Word overlap (some overlap is good, too much means low paraphrasing)
        orig_words = set(original.lower().split())
        para_words = set(paraphrased.lower().split())
        
        if orig_words and para_words:
            overlap_ratio = len(orig_words.intersection(para_words)) / len(orig_words)
            # Sweet spot is around 30-70% overlap
            if 0.3 <= overlap_ratio <= 0.7:
                score += 0.2
            elif overlap_ratio < 0.3:
                score += 0.1  # Good paraphrasing but maybe too different
            else:
                score -= 0.1  # Too similar
        
        # Sentence structure check
        if len(paraphrased.split()) >= 3:  # Reasonable length
            score += 0.1
        
        return min(score, 1.0)
    
    def batch_paraphrase(self, texts: List[str], batch_size: int = 4) -> List[T5ParaphraseResult]:
        """
        Paraphrase multiple texts efficiently
        """
        self.logger.info(f"🔄 Batch paraphrasing {len(texts)} texts...")
        
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_results = []
            
            for text in batch_texts:
                result = self.paraphrase_text(text)
                batch_results.append(result)
                
                # Small delay to prevent overwhelming the GPU
                if self.device.type == 'cuda':
                    time.sleep(0.1)
            
            results.extend(batch_results)
            self.logger.debug(f"📊 Processed batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
        
        self.logger.info(f"✅ Batch paraphrasing completed")
        return results
    
    def paraphrase_with_quality_filter(self, text: str, min_confidence: float = 0.6) -> T5ParaphraseResult:
        """
        Paraphrase with quality filtering - regenerate if quality is too low
        """
        max_attempts = 3
        
        for attempt in range(max_attempts):
            result = self.paraphrase_text(text, num_return_sequences=2)
            
            if result.confidence_score >= min_confidence:
                self.logger.debug(f"✅ High quality paraphrase achieved on attempt {attempt + 1}")
                return result
            elif result.alternatives and attempt < max_attempts - 1:
                # Try with different generation parameters
                self.generation_config['temperature'] = min(1.2, self.generation_config['temperature'] + 0.2)
                self.logger.debug(f"🔄 Retrying with higher temperature (attempt {attempt + 1})")
            
        # Return best result even if below threshold
        self.logger.warning(f"⚠️ Could not achieve min confidence {min_confidence}, returning best result")
        return result
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "available": self.is_available(),
            "max_length": self.max_length,
            "generation_config": self.generation_config
        }

# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python indo_t5_paraphraser.py <text_to_paraphrase>")
        sys.exit(1)
    
    text = sys.argv[1]
    
    print("🚀 INDONESIAN T5 PARAPHRASER TEST")
    print("=" * 50)
    
    paraphraser = IndoT5Paraphraser(verbose=True)
    
    if not paraphraser.is_available():
        print("❌ T5 model not available")
        sys.exit(1)
    
    print(f"\n🔄 Model Info:")
    model_info = paraphraser.get_model_info()
    for key, value in model_info.items():
        print(f"   {key}: {value}")
    
    print(f"\n📝 Original: {text}")
    print("🔄 Generating paraphrases...")
    
    # Test single paraphrase
    result = paraphraser.paraphrase_text(text, num_return_sequences=3)
    
    print(f"\n✨ T5 PARAPHRASE RESULTS:")
    print(f"📊 Model: {result.model_used}")
    print(f"✨ Paraphrased: {result.paraphrased_text}")
    print(f"🎯 Confidence: {result.confidence_score:.2f}")
    print(f"⏱️ Processing Time: {result.processing_time:.2f}s")
    
    if result.alternatives:
        print(f"\n🔄 Alternative Paraphrases:")
        for i, alt in enumerate(result.alternatives, 1):
            print(f"   {i}. {alt}")
    
    # Test quality filter
    print(f"\n🎯 Testing Quality Filter...")
    quality_result = paraphraser.paraphrase_with_quality_filter(text, min_confidence=0.7)
    print(f"✅ High-quality result: {quality_result.paraphrased_text}")
    print(f"📊 Final confidence: {quality_result.confidence_score:.2f}")