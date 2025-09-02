# hybrid_paraphraser.py
"""
Hybrid Paraphraser System
Menggabungkan Indonesian T5 neural paraphrasing dengan contextual synonym replacement
untuk hasil terbaik dari kedua dunia: neural intelligence + comprehensive vocabulary
"""

import os
import re
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

from indo_t5_paraphraser import IndoT5Paraphraser, T5ParaphraseResult
from contextual_paraphraser import ContextualParaphraser
from ai_quality_checker import AIQualityChecker, QualityAssessment

@dataclass
class HybridParaphraseResult:
    original_text: str
    t5_paraphrase: str
    contextual_paraphrase: str
    hybrid_paraphrase: str
    best_method: str
    quality_scores: Dict[str, float]
    processing_metrics: Dict[str, float]
    recommendations: List[str]

class HybridParaphraser:
    def __init__(self, enable_t5: bool = True, verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Initialize components
        self.logger.info("🚀 Initializing Hybrid Paraphraser System...")
        
        # Always initialize contextual paraphraser (lightweight)
        self.contextual_paraphraser = ContextualParaphraser(verbose=False)
        self.logger.info(f"✅ Contextual paraphraser: {len(self.contextual_paraphraser.synonym_dict):,} synonyms")
        
        # Initialize T5 paraphraser (heavy)
        self.t5_paraphraser = None
        self.t5_enabled = enable_t5
        
        if enable_t5:
            try:
                self.t5_paraphraser = IndoT5Paraphraser(verbose=False)
                if self.t5_paraphraser.is_available():
                    self.logger.info("✅ Indonesian T5 neural paraphraser ready")
                else:
                    self.logger.warning("⚠️ T5 model not available, using contextual only")
                    self.t5_enabled = False
            except Exception as e:
                self.logger.warning(f"⚠️ Failed to initialize T5: {e}")
                self.t5_enabled = False
        else:
            self.logger.info("ℹ️ T5 paraphrasing disabled, using contextual only")
        
        # Initialize quality checker for evaluation
        self.quality_checker = AIQualityChecker(verbose=False)
        
        # Strategy configuration
        self.strategy_config = {
            'short_text_threshold': 50,  # chars
            'long_text_threshold': 200,  # chars
            't5_timeout': 60,  # seconds
            'quality_threshold': 0.6,
            'hybrid_weight_t5': 0.7,
            'hybrid_weight_contextual': 0.3
        }
        
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def paraphrase_hybrid(self, text: str, strategy: str = "auto") -> HybridParaphraseResult:
        """
        Main hybrid paraphrasing function
        Strategies: 'auto', 't5_first', 'contextual_first', 'parallel', 'best_of_both'
        """
        start_time = time.time()
        
        self.logger.info(f"🎯 Hybrid paraphrasing with strategy: {strategy}")
        
        # Step 1: Determine optimal strategy if auto
        if strategy == "auto":
            strategy = self._determine_optimal_strategy(text)
            self.logger.debug(f"🤖 Auto-selected strategy: {strategy}")
        
        # Step 2: Execute paraphrasing based on strategy
        t5_result = None
        contextual_result = None
        
        if strategy in ["t5_first", "parallel", "best_of_both"]:
            t5_result = self._run_t5_paraphrasing(text)
        
        if strategy in ["contextual_first", "parallel", "best_of_both"]:
            contextual_result = self._run_contextual_paraphrasing(text)
        
        # Handle sequential strategies
        if strategy == "t5_first" and t5_result and t5_result.confidence_score < self.strategy_config['quality_threshold']:
            self.logger.debug("🔄 T5 quality insufficient, trying contextual...")
            contextual_result = self._run_contextual_paraphrasing(text)
        
        elif strategy == "contextual_first":
            # Always run contextual first, then T5 if needed
            if not contextual_result or len(contextual_result.get('replacements', [])) < 3:
                self.logger.debug("🔄 Contextual changes minimal, trying T5...")
                t5_result = self._run_t5_paraphrasing(text)
        
        # Step 3: Quality assessment and selection
        results = self._evaluate_and_select_best(text, t5_result, contextual_result, strategy)
        
        # Step 4: Create hybrid result if both available
        if strategy == "best_of_both" and t5_result and contextual_result:
            results = self._create_hybrid_combination(text, t5_result, contextual_result, results)
        
        processing_time = time.time() - start_time
        results.processing_metrics['total_time'] = processing_time
        
        self.logger.info(f"✅ Hybrid paraphrasing completed in {processing_time:.2f}s")
        self.logger.info(f"🏆 Best method: {results.best_method}")
        
        return results
    
    def _determine_optimal_strategy(self, text: str) -> str:
        """Automatically determine the best strategy for given text"""
        text_length = len(text)
        
        # For short texts, contextual is often better (faster, more precise)
        if text_length < self.strategy_config['short_text_threshold']:
            return "contextual_first"
        
        # For medium texts, try T5 first (better restructuring)
        elif text_length < self.strategy_config['long_text_threshold']:
            return "t5_first" if self.t5_enabled else "contextual_first"
        
        # For long texts, use parallel approach for best results
        else:
            return "parallel" if self.t5_enabled else "contextual_first"
    
    def _run_t5_paraphrasing(self, text: str) -> Optional[T5ParaphraseResult]:
        """Run T5 neural paraphrasing with timeout protection"""
        if not self.t5_enabled or not self.t5_paraphraser:
            return None
        
        try:
            self.logger.debug("🧠 Running T5 neural paraphrasing...")
            result = self.t5_paraphraser.paraphrase_with_quality_filter(text, min_confidence=0.5)
            
            if result.processing_time > self.strategy_config['t5_timeout']:
                self.logger.warning(f"⏰ T5 processing took {result.processing_time:.1f}s (timeout: {self.strategy_config['t5_timeout']}s)")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ T5 paraphrasing failed: {e}")
            return None
    
    def _run_contextual_paraphrasing(self, text: str) -> Optional[Dict]:
        """Run contextual synonym-based paraphrasing"""
        try:
            self.logger.debug("📚 Running contextual paraphrasing...")
            result = self.contextual_paraphraser.batch_paraphrase_academic_text(text, "high")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Contextual paraphrasing failed: {e}")
            return None
    
    def _evaluate_and_select_best(self, original: str, t5_result: Optional[T5ParaphraseResult], 
                                 contextual_result: Optional[Dict], strategy: str) -> HybridParaphraseResult:
        """Evaluate both results and select the best approach"""
        
        # Initialize quality scores
        quality_scores = {}
        
        # Evaluate T5 result
        t5_text = ""
        if t5_result:
            t5_text = t5_result.paraphrased_text
            t5_assessment = self.quality_checker.assess_paraphrase_quality(original, t5_text, "Academic text")
            quality_scores['t5'] = t5_assessment.overall_score
            self.logger.debug(f"🧠 T5 quality score: {t5_assessment.overall_score:.2f}")
        
        # Evaluate contextual result
        contextual_text = ""
        if contextual_result:
            contextual_text = contextual_result['paraphrased_text']
            contextual_assessment = self.quality_checker.assess_paraphrase_quality(original, contextual_text, "Academic text")
            quality_scores['contextual'] = contextual_assessment.overall_score
            self.logger.debug(f"📚 Contextual quality score: {contextual_assessment.overall_score:.2f}")
        
        # Select best method
        best_method = "original"
        best_text = original
        recommendations = []
        
        if quality_scores:
            if 't5' in quality_scores and 'contextual' in quality_scores:
                if quality_scores['t5'] > quality_scores['contextual']:
                    best_method = "t5_neural"
                    best_text = t5_text
                    recommendations.append("T5 neural paraphrasing provided better results")
                else:
                    best_method = "contextual_synonyms"
                    best_text = contextual_text  
                    recommendations.append("Contextual synonym replacement was more effective")
            
            elif 't5' in quality_scores:
                if quality_scores['t5'] > 0.5:
                    best_method = "t5_neural"
                    best_text = t5_text
                    recommendations.append("T5 neural paraphrasing used (contextual not available)")
            
            elif 'contextual' in quality_scores:
                if quality_scores['contextual'] > 0.5:
                    best_method = "contextual_synonyms"
                    best_text = contextual_text
                    recommendations.append("Contextual synonyms used (T5 not available)")
        
        # Processing metrics
        processing_metrics = {
            't5_time': t5_result.processing_time if t5_result else 0,
            'contextual_time': 0.5,  # Estimate for contextual
            'strategy_used': strategy
        }
        
        return HybridParaphraseResult(
            original_text=original,
            t5_paraphrase=t5_text,
            contextual_paraphrase=contextual_text,
            hybrid_paraphrase=best_text,
            best_method=best_method,
            quality_scores=quality_scores,
            processing_metrics=processing_metrics,
            recommendations=recommendations
        )
    
    def _create_hybrid_combination(self, original: str, t5_result: T5ParaphraseResult, 
                                  contextual_result: Dict, current_result: HybridParaphraseResult) -> HybridParaphraseResult:
        """Create a hybrid combination using both T5 and contextual approaches"""
        
        self.logger.debug("🔬 Creating hybrid combination...")
        
        # Strategy: Use T5 for sentence structure, contextual for specific terms
        t5_text = t5_result.paraphrased_text
        contextual_text = contextual_result['paraphrased_text']
        
        # Smart combination: identify key academic terms and use contextual replacements
        replacements = contextual_result.get('replacements', [])
        hybrid_text = t5_text
        
        # Apply high-quality contextual replacements to T5 result
        for replacement in replacements:
            if hasattr(replacement, 'context_score') and replacement.context_score > 0.8:
                # Apply high-quality contextual replacements to T5 output
                if replacement.original.lower() in t5_text.lower():
                    hybrid_text = re.sub(
                        r'\b' + re.escape(replacement.original) + r'\b', 
                        replacement.replacement, 
                        hybrid_text, 
                        flags=re.IGNORECASE
                    )
                    self.logger.debug(f"🔄 Enhanced T5 with: {replacement.original} → {replacement.replacement}")
        
        # Evaluate hybrid result
        hybrid_assessment = self.quality_checker.assess_paraphrase_quality(original, hybrid_text, "Academic text")
        current_result.quality_scores['hybrid'] = hybrid_assessment.overall_score
        
        # Update if hybrid is better
        if hybrid_assessment.overall_score > max(current_result.quality_scores.get('t5', 0), 
                                                current_result.quality_scores.get('contextual', 0)):
            current_result.hybrid_paraphrase = hybrid_text
            current_result.best_method = "hybrid_combination"
            current_result.recommendations.append("Hybrid combination of T5 + contextual achieved best quality")
            self.logger.info("🏆 Hybrid combination selected as best result")
        
        return current_result
    
    def batch_paraphrase(self, texts: List[str], strategy: str = "auto") -> List[HybridParaphraseResult]:
        """Batch process multiple texts with hybrid paraphrasing"""
        self.logger.info(f"📊 Batch processing {len(texts)} texts with hybrid system...")
        
        results = []
        total_start = time.time()
        
        for i, text in enumerate(texts, 1):
            self.logger.debug(f"🔄 Processing text {i}/{len(texts)}")
            result = self.paraphrase_hybrid(text, strategy)
            results.append(result)
            
            # Progress update
            if i % 5 == 0 or i == len(texts):
                elapsed = time.time() - total_start
                avg_time = elapsed / i
                eta = (len(texts) - i) * avg_time
                self.logger.info(f"📈 Progress: {i}/{len(texts)}, ETA: {eta:.1f}s")
        
        total_time = time.time() - total_start
        self.logger.info(f"✅ Batch processing completed in {total_time:.1f}s")
        
        return results
    
    def get_system_info(self) -> Dict:
        """Get comprehensive system information"""
        return {
            "hybrid_paraphraser": {
                "version": "1.0",
                "t5_enabled": self.t5_enabled,
                "contextual_synonyms": len(self.contextual_paraphraser.synonym_dict),
                "t5_model": self.t5_paraphraser.model_name if self.t5_enabled else None,
                "ai_validation": self.quality_checker.model is not None
            },
            "strategy_config": self.strategy_config,
            "capabilities": [
                "Neural paraphrasing (T5)" if self.t5_enabled else "Neural paraphrasing (disabled)",
                "Contextual synonym replacement",
                "AI quality assessment", 
                "Hybrid combination strategies",
                "Automated strategy selection",
                "Batch processing"
            ]
        }

# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python hybrid_paraphraser.py <text_to_paraphrase> [strategy]")
        print("Strategies: auto, t5_first, contextual_first, parallel, best_of_both")
        sys.exit(1)
    
    text = sys.argv[1]
    strategy = sys.argv[2] if len(sys.argv) > 2 else "auto"
    
    print("🚀 HYBRID PARAPHRASER SYSTEM TEST")
    print("=" * 60)
    
    # Initialize hybrid paraphraser
    hybrid = HybridParaphraser(enable_t5=True, verbose=True)
    
    # Show system info
    print("\n🔧 SYSTEM CONFIGURATION:")
    system_info = hybrid.get_system_info()
    print(f"   T5 Neural: {'✅' if system_info['hybrid_paraphraser']['t5_enabled'] else '❌'}")
    print(f"   Contextual Synonyms: {system_info['hybrid_paraphraser']['contextual_synonyms']:,}")
    print(f"   AI Validation: {'✅' if system_info['hybrid_paraphraser']['ai_validation'] else '❌'}")
    
    print(f"\n📝 Original: {text}")
    print(f"🎯 Strategy: {strategy}")
    
    # Run hybrid paraphrasing
    result = hybrid.paraphrase_hybrid(text, strategy)
    
    print(f"\n✨ HYBRID PARAPHRASING RESULTS:")
    print(f"🧠 T5 Neural: {result.t5_paraphrase}")
    print(f"📚 Contextual: {result.contextual_paraphrase}")
    print(f"🏆 Best Result: {result.hybrid_paraphrase}")
    print(f"🎖️ Best Method: {result.best_method}")
    
    print(f"\n📊 QUALITY SCORES:")
    for method, score in result.quality_scores.items():
        print(f"   {method.title()}: {score:.2f}/1.0")
    
    print(f"\n⚡ PROCESSING METRICS:")
    for metric, value in result.processing_metrics.items():
        if 'time' in metric:
            print(f"   {metric}: {value:.2f}s")
        else:
            print(f"   {metric}: {value}")
    
    if result.recommendations:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in result.recommendations:
            print(f"   • {rec}")