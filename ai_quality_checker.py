# ai_quality_checker.py
"""
AI Quality Checker using Google Gemini
Sistem untuk memvalidasi kualitas hasil paraphrasing menggunakan AI
"""

import os
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

try:
    import google.generativeai as genai
except ImportError:
    print("Google Generative AI not available. Install with: pip install google-generativeai")
    genai = None

@dataclass
class QualityAssessment:
    overall_score: float  # 0.0 - 1.0
    naturalness_score: float
    academic_appropriateness: float
    meaning_preservation: float
    grammar_quality: float
    recommendations: List[str]
    flagged_issues: List[str]
    confidence_level: str

class AIQualityChecker:
    def __init__(self, api_key: Optional[str] = None, verbose: bool = True):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self.setup_logging()
        
        # Initialize Gemini
        self.model = None
        if genai:
            api_key = api_key or os.getenv('GEMINI_API_KEY')
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    self.logger.info("🤖 Gemini AI initialized successfully")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize Gemini: {e}")
            else:
                self.logger.warning("⚠️ GEMINI_API_KEY not found. Set environment variable or pass api_key parameter.")
        
        # Fallback quality metrics if AI not available
        self.fallback_enabled = True
        
    def setup_logging(self):
        """Setup logging configuration"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
    
    def assess_paraphrase_quality(self, original_text: str, paraphrased_text: str, context: str = "") -> QualityAssessment:
        """
        Main function to assess paraphrase quality using AI
        """
        self.logger.info("🔍 Starting AI quality assessment...")
        
        if self.model:
            return self._gemini_assessment(original_text, paraphrased_text, context)
        elif self.fallback_enabled:
            return self._fallback_assessment(original_text, paraphrased_text, context)
        else:
            raise Exception("No AI model available and fallback disabled")
    
    def _gemini_assessment(self, original: str, paraphrased: str, context: str) -> QualityAssessment:
        """Use Gemini AI for quality assessment"""
        
        prompt = f"""
        Kamu adalah expert linguist dan academic writing specialist untuk bahasa Indonesia. 
        Evaluasi kualitas hasil parafrase berikut dengan kriteria yang ketat:

        **TEKS ASLI:**
        {original}

        **TEKS HASIL PARAFRASE:**
        {paraphrased}

        **KONTEKS:** {context if context else "Teks akademik umum"}

        Analisis dengan kriteria berikut dan berikan skor 0.0-1.0 untuk setiap aspek:

        1. **NATURALNESS (Kealamian Bahasa)**: Apakah teks terdengar natural dan tidak kaku?
        2. **ACADEMIC_APPROPRIATENESS (Kesesuaian Akademik)**: Apakah cocok untuk konteks akademik/formal?
        3. **MEANING_PRESERVATION (Preservasi Makna)**: Apakah makna original tetap terjaga?
        4. **GRAMMAR_QUALITY (Kualitas Grammar)**: Apakah grammar dan struktur kalimat benar?

        Fokus identifikasi masalah:
        - Sinonim yang aneh/tidak tepat konteks (misal: "angsal", "kata putus", "nan")
        - Kehilangan makna penting
        - Grammar errors
        - Terlalu informal untuk konteks akademik
        - Kata yang membingungkan pembaca

        Berikan output dalam format JSON EXACT ini:
        {{
            "naturalness_score": 0.85,
            "academic_appropriateness": 0.90,
            "meaning_preservation": 0.95,
            "grammar_quality": 0.88,
            "overall_score": 0.89,
            "flagged_issues": ["issue1", "issue2"],
            "recommendations": ["rec1", "rec2"],
            "confidence": "High"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_text = response_text[json_start:json_end]
            else:
                json_text = response_text
            
            # Parse AI response
            ai_result = json.loads(json_text)
            
            assessment = QualityAssessment(
                overall_score=float(ai_result.get('overall_score', 0.5)),
                naturalness_score=float(ai_result.get('naturalness_score', 0.5)),
                academic_appropriateness=float(ai_result.get('academic_appropriateness', 0.5)),
                meaning_preservation=float(ai_result.get('meaning_preservation', 0.5)),
                grammar_quality=float(ai_result.get('grammar_quality', 0.5)),
                recommendations=ai_result.get('recommendations', []),
                flagged_issues=ai_result.get('flagged_issues', []),
                confidence_level=ai_result.get('confidence', 'Medium')
            )
            
            self.logger.info(f"🤖 AI Assessment complete: Overall score {assessment.overall_score:.2f}")
            return assessment
            
        except Exception as e:
            self.logger.warning(f"AI assessment failed: {e}, falling back to heuristic")
            return self._fallback_assessment(original, paraphrased, context)
    
    def _fallback_assessment(self, original: str, paraphrased: str, context: str) -> QualityAssessment:
        """Fallback heuristic-based assessment"""
        
        # Basic heuristic scoring
        naturalness = self._assess_naturalness(paraphrased)
        academic = self._assess_academic_appropriateness(paraphrased)
        meaning = self._assess_meaning_preservation(original, paraphrased)
        grammar = self._assess_grammar_quality(paraphrased)
        
        overall = (naturalness + academic + meaning + grammar) / 4
        
        # Identify common issues
        issues = []
        recommendations = []
        
        # Check for inappropriate synonyms
        inappropriate_words = ['angsal', 'kata putus', 'nan', 'ketek', 'belalang']
        for word in inappropriate_words:
            if word.lower() in paraphrased.lower():
                issues.append(f"Inappropriate synonym: '{word}'")
                recommendations.append(f"Replace '{word}' with more appropriate academic term")
        
        # Check for meaning preservation
        if meaning < 0.7:
            issues.append("Potential meaning loss detected")
            recommendations.append("Review paraphrase to ensure original meaning is preserved")
        
        # Check academic appropriateness
        if academic < 0.6:
            issues.append("May be too informal for academic context")
            recommendations.append("Use more formal academic language")
        
        confidence = "High" if overall > 0.8 else "Medium" if overall > 0.6 else "Low"
        
        return QualityAssessment(
            overall_score=overall,
            naturalness_score=naturalness,
            academic_appropriateness=academic,
            meaning_preservation=meaning,
            grammar_quality=grammar,
            recommendations=recommendations,
            flagged_issues=issues,
            confidence_level=confidence
        )
    
    def _assess_naturalness(self, text: str) -> float:
        """Assess naturalness using heuristics"""
        score = 0.8  # Base score
        
        # Penalty for awkward constructions
        awkward_patterns = ['nan ', ' nan', 'ketek ', 'angsal']
        for pattern in awkward_patterns:
            if pattern in text.lower():
                score -= 0.2
        
        # Bonus for natural flow
        if len(text.split()) > 5 and not any(weird in text.lower() for weird in awkward_patterns):
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_academic_appropriateness(self, text: str) -> float:
        """Assess academic appropriateness"""
        score = 0.7  # Base score
        
        # Check for academic indicators
        academic_words = ['penelitian', 'analisis', 'riset', 'studi', 'kajian', 'eksplorasi']
        if any(word in text.lower() for word in academic_words):
            score += 0.2
        
        # Penalty for casual language
        casual_words = ['kayak', 'gitu', 'banget', 'oke']
        for word in casual_words:
            if word in text.lower():
                score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _assess_meaning_preservation(self, original: str, paraphrased: str) -> float:
        """Assess meaning preservation using word overlap"""
        original_words = set(original.lower().split())
        paraphrased_words = set(paraphrased.lower().split())
        
        # Calculate semantic overlap (simplified)
        common_important_words = original_words.intersection(paraphrased_words)
        important_word_ratio = len(common_important_words) / len(original_words) if original_words else 0
        
        # Length similarity factor
        length_ratio = min(len(paraphrased), len(original)) / max(len(paraphrased), len(original))
        
        # Combined score
        meaning_score = (important_word_ratio * 0.6) + (length_ratio * 0.4)
        
        return max(0.4, min(1.0, meaning_score))  # Minimum 0.4 since we're paraphrasing
    
    def _assess_grammar_quality(self, text: str) -> float:
        """Basic grammar quality assessment"""
        score = 0.9  # Assume good grammar by default
        
        # Simple checks
        if not text.strip():
            return 0.0
        
        # Check for basic sentence structure
        if not text.strip().endswith(('.', '!', '?')):
            score -= 0.1
        
        # Check for repeated words
        words = text.lower().split()
        if len(words) != len(set(words)) and len(words) > 3:
            score -= 0.1
        
        return max(0.3, min(1.0, score))
    
    def batch_assess_quality(self, paraphrase_results: List[Dict]) -> Dict:
        """Assess quality of multiple paraphrase results"""
        assessments = []
        total_scores = []
        
        for i, result in enumerate(paraphrase_results):
            self.logger.info(f"🔍 Assessing quality {i+1}/{len(paraphrase_results)}")
            
            assessment = self.assess_paraphrase_quality(
                result.get('original_text', ''),
                result.get('paraphrased_text', ''),
                result.get('context', '')
            )
            
            assessments.append(assessment)
            total_scores.append(assessment.overall_score)
            
            # Add delay to respect API rate limits
            if self.model:
                time.sleep(0.5)
        
        # Calculate aggregate metrics
        avg_score = sum(total_scores) / len(total_scores) if total_scores else 0
        high_quality_count = sum(1 for score in total_scores if score >= 0.8)
        needs_improvement = sum(1 for score in total_scores if score < 0.6)
        
        return {
            'individual_assessments': assessments,
            'summary': {
                'total_assessed': len(paraphrase_results),
                'average_quality_score': avg_score,
                'high_quality_results': high_quality_count,
                'needs_improvement': needs_improvement,
                'pass_rate': (len(total_scores) - needs_improvement) / len(total_scores) if total_scores else 0
            }
        }

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python ai_quality_checker.py <original_text> <paraphrased_text> [api_key]")
        sys.exit(1)
    
    original = sys.argv[1]
    paraphrased = sys.argv[2]
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    checker = AIQualityChecker(api_key=api_key, verbose=True)
    assessment = checker.assess_paraphrase_quality(original, paraphrased)
    
    print("\n🤖 AI QUALITY ASSESSMENT RESULTS:")
    print(f"📊 Overall Score: {assessment.overall_score:.2f}/1.0")
    print(f"🎯 Naturalness: {assessment.naturalness_score:.2f}/1.0")
    print(f"🎓 Academic Appropriateness: {assessment.academic_appropriateness:.2f}/1.0")  
    print(f"💭 Meaning Preservation: {assessment.meaning_preservation:.2f}/1.0")
    print(f"📝 Grammar Quality: {assessment.grammar_quality:.2f}/1.0")
    print(f"🔍 Confidence: {assessment.confidence_level}")
    
    if assessment.flagged_issues:
        print(f"\n⚠️ Issues Found:")
        for issue in assessment.flagged_issues:
            print(f"  • {issue}")
    
    if assessment.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in assessment.recommendations:
            print(f"  • {rec}")