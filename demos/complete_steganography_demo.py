#!/usr/bin/env python3
"""
Complete Steganography Demo
Mendemonstrasikan SEMUA teknik steganografi:
1. Indonesian T5 Neural Paraphrasing
2. Contextual Synonym Replacement (20,139 entries)
3. Unicode Steganography (Latin → Cyrillic)
4. Invisible Characters Injection
5. AI Quality Validation
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Import all steganography modules
from unicode_steganography import UnicodeSteg
from invisible_manipulator import InvisibleManipulator
from hybrid_paraphraser import HybridParaphraser
from ai_quality_checker import AIQualityChecker

def main():
    print("🕵️ COMPLETE STEGANOGRAPHY SYSTEM DEMONSTRATION")
    print("=" * 65)
    
    # Test text - academic sample
    original_text = """
    Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen. Penelitian ini menggunakan metode kuantitatif dengan analisis statistik untuk menguji hipotesis yang diajukan.
    """
    
    print(f"📝 ORIGINAL TEXT:")
    print(f"   {original_text.strip()}")
    print(f"📊 Original Length: {len(original_text)} characters")
    
    # Initialize ALL steganography systems
    print(f"\n🔧 INITIALIZING COMPLETE STEGANOGRAPHY ARSENAL...")
    
    # 1. Unicode Steganography System
    print("🔤 Loading Unicode Steganography (Latin→Cyrillic)...")
    unicode_steg = UnicodeSteg()
    
    # 2. Invisible Characters System  
    print("👻 Loading Invisible Characters Manipulator...")
    invisible_manipulator = InvisibleManipulator()
    
    # 3. Hybrid Neural Paraphrasing System
    print("🧠 Loading T5 + Contextual Paraphrasing System...")
    hybrid_paraphraser = HybridParaphraser(enable_t5=True, verbose=False)
    
    # 4. AI Quality Checker
    print("🤖 Loading AI Quality Validation...")
    ai_checker = AIQualityChecker(verbose=False)
    
    print("✅ All steganography systems loaded!")
    
    # STEP 1: Neural + Contextual Paraphrasing
    print(f"\n🧠 STEP 1: ADVANCED PARAPHRASING (T5 + 20,139 Synonyms)")
    print("-" * 50)
    
    paraphrase_start = time.time()
    paraphrase_result = hybrid_paraphraser.paraphrase_hybrid(original_text.strip(), "parallel")
    paraphrase_time = time.time() - paraphrase_start
    
    paraphrased_text = paraphrase_result.hybrid_paraphrase
    
    print(f"✨ Paraphrased: {paraphrased_text}")
    print(f"🎖️ Method: {paraphrase_result.best_method}")
    print(f"📊 Quality Score: {max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 'N/A'}")
    print(f"⏱️ Time: {paraphrase_time:.2f}s")
    
    # STEP 2: Unicode Steganography
    print(f"\n🔤 STEP 2: UNICODE STEGANOGRAPHY (Latin→Cyrillic)")
    print("-" * 50)
    
    unicode_start = time.time()
    unicode_text, unicode_log = unicode_steg.apply_strategic_substitution(paraphrased_text, aggressiveness=0.15)
    unicode_time = time.time() - unicode_start
    
    # Create result structure for compatibility
    unicode_result = {
        'processed_text': unicode_text,
        'substitutions_made': unicode_log['total_changes'],
        'steganography_ratio': (unicode_log['total_changes'] / len(paraphrased_text.split())) * 100 if paraphrased_text else 0,
        'invisibility_score': min(95, unicode_log['total_changes'] * 8),  # Estimate
        'detailed_substitutions': unicode_log['substitutions_made']
    }
    
    print(f"🔄 Unicode Substitutions: {unicode_result['substitutions_made']}")
    print(f"📈 Steganography Ratio: {unicode_result['steganography_ratio']:.1f}%")
    print(f"🎯 Invisibility Score: {unicode_result['invisibility_score']:.1f}%")
    print(f"⏱️ Time: {unicode_time:.2f}s")
    
    # Show some examples
    if unicode_result['detailed_substitutions']:
        print("🔍 Sample Substitutions:")
        for i, sub in enumerate(unicode_result['detailed_substitutions'][:3]):
            print(f"   {sub['original']} → {sub['replacement']} ({sub['type']})")
    
    unicode_text = unicode_result['processed_text']
    
    # STEP 3: Invisible Characters Injection  
    print(f"\n👻 STEP 3: INVISIBLE CHARACTERS INJECTION")
    print("-" * 50)
    
    invisible_start = time.time()
    
    # Configure invisible manipulation
    invisible_config = {
        'zero_width_spaces': True,
        'zero_width_joiners': True,
        'word_joiners': True,
        'mongolian_vowel_separators': True,
        'injection_rate': 0.3,  # 30% of words get invisible chars
        'max_chars_per_injection': 2
    }
    
    # Use the actual method from invisible manipulator
    invisible_chars = list(invisible_manipulator.invisible_chars.get('zero_width', {}).values())
    if not invisible_chars:
        # Fallback invisible characters
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
    
    invisible_text = invisible_manipulator.insert_invisible_chars(
        unicode_text, 
        invisible_chars,
        invisible_config['injection_rate']
    )
    
    # Create result structure for compatibility
    original_len = len(unicode_text)
    processed_len = len(invisible_text)
    invisible_chars_count = processed_len - original_len
    
    invisible_result = {
        'processed_text': invisible_text,
        'invisible_chars_count': invisible_chars_count,
        'injection_points': invisible_chars_count,  # Approximate
        'invisibility_ratio': (invisible_chars_count / original_len) * 100 if original_len > 0 else 0
    }
    
    invisible_time = time.time() - invisible_start
    
    print(f"👻 Invisible Characters Added: {invisible_result['invisible_chars_count']}")
    print(f"📍 Injection Points: {invisible_result['injection_points']}")
    print(f"🎯 Invisibility Rate: {invisible_result['invisibility_ratio']:.1f}%")
    print(f"⏱️ Time: {invisible_time:.2f}s")
    
    final_steganographic_text = invisible_result['processed_text']
    
    # STEP 4: AI Quality Assessment of Final Result
    print(f"\n🤖 STEP 4: AI QUALITY VALIDATION")
    print("-" * 50)
    
    validation_start = time.time()
    final_assessment = ai_checker.assess_paraphrase_quality(
        original_text.strip(),
        final_steganographic_text,
        context="Academic research with steganographic modifications"
    )
    validation_time = time.time() - validation_start
    
    print(f"📊 Final Quality Metrics:")
    print(f"   Overall Score: {final_assessment.overall_score:.2f}/1.0")
    print(f"   Naturalness: {final_assessment.naturalness_score:.2f}/1.0") 
    print(f"   Academic Fit: {final_assessment.academic_appropriateness:.2f}/1.0")
    print(f"   Meaning Preserved: {final_assessment.meaning_preservation:.2f}/1.0")
    print(f"   Grammar Quality: {final_assessment.grammar_quality:.2f}/1.0")
    print(f"   Confidence: {final_assessment.confidence_level}")
    print(f"⏱️ Validation Time: {validation_time:.2f}s")
    
    if final_assessment.flagged_issues:
        print("⚠️ Issues Detected:")
        for issue in final_assessment.flagged_issues:
            print(f"   • {issue}")
    
    # COMPREHENSIVE RESULTS ANALYSIS
    print(f"\n📊 COMPREHENSIVE STEGANOGRAPHY RESULTS")
    print("=" * 60)
    
    # Calculate text similarity (visual)
    original_clean = original_text.strip()
    final_clean = final_steganographic_text
    
    # Character-level analysis
    original_chars = set(original_clean.lower())
    final_chars = set(final_clean.lower())
    visible_char_similarity = len(original_chars.intersection(final_chars)) / len(original_chars) * 100
    
    # Length comparison
    length_change = len(final_clean) - len(original_clean)
    length_change_pct = (length_change / len(original_clean)) * 100
    
    print(f"📝 FINAL STEGANOGRAPHIC TEXT:")
    print(f"   {final_clean}")
    print(f"")
    print(f"📈 TRANSFORMATION METRICS:")
    print(f"   Original Length: {len(original_clean)} chars")
    print(f"   Final Length: {len(final_clean)} chars")
    print(f"   Length Change: {length_change:+d} chars ({length_change_pct:+.1f}%)")
    print(f"   Visible Similarity: {visible_char_similarity:.1f}%")
    print(f"")
    print(f"🎯 STEGANOGRAPHY EFFECTIVENESS:")
    print(f"   T5 Neural Quality: {max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 0:.2f}/1.0")
    print(f"   Unicode Invisibility: {unicode_result['invisibility_score']:.1f}%")
    print(f"   Invisible Chars: {invisible_result['invisible_chars_count']} injected")
    print(f"   Final AI Quality: {final_assessment.overall_score:.2f}/1.0")
    
    # Processing time breakdown
    total_processing_time = paraphrase_time + unicode_time + invisible_time + validation_time
    
    print(f"")
    print(f"⏱️ PROCESSING TIME BREAKDOWN:")
    print(f"   T5 + Contextual: {paraphrase_time:.2f}s ({paraphrase_time/total_processing_time*100:.1f}%)")
    print(f"   Unicode Steganography: {unicode_time:.2f}s ({unicode_time/total_processing_time*100:.1f}%)")
    print(f"   Invisible Characters: {invisible_time:.2f}s ({invisible_time/total_processing_time*100:.1f}%)")
    print(f"   AI Validation: {validation_time:.2f}s ({validation_time/total_processing_time*100:.1f}%)")
    print(f"   Total: {total_processing_time:.2f}s")
    
    # Steganographic techniques summary
    print(f"\n🕵️ STEGANOGRAPHIC TECHNIQUES APPLIED:")
    print("✅ Neural sentence restructuring (Indonesian T5)")
    print("✅ Contextual synonym replacement (20,139 database)")  
    print("✅ Unicode character substitution (Latin→Cyrillic)")
    print("✅ Invisible character injection (6 types)")
    print("✅ AI quality validation (Gemini + heuristics)")
    
    # Detection evasion assessment
    print(f"\n🛡️ DETECTION EVASION ASSESSMENT:")
    evasion_score = 0
    
    # Paraphrasing effectiveness
    if max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 0 > 0.8:
        evasion_score += 25
        print("✅ High-quality paraphrasing (25 points)")
    elif max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 0 > 0.6:
        evasion_score += 15
        print("🟡 Moderate paraphrasing (15 points)")
    
    # Unicode steganography
    if unicode_result['invisibility_score'] > 80:
        evasion_score += 25
        print("✅ High Unicode invisibility (25 points)")
    elif unicode_result['invisibility_score'] > 50:
        evasion_score += 15
        print("🟡 Moderate Unicode steganography (15 points)")
    
    # Invisible characters
    if invisible_result['invisible_chars_count'] > 10:
        evasion_score += 25
        print("✅ Substantial invisible chars (25 points)")
    elif invisible_result['invisible_chars_count'] > 5:
        evasion_score += 15
        print("🟡 Moderate invisible chars (15 points)")
    
    # Quality preservation
    if final_assessment.overall_score > 0.7:
        evasion_score += 25
        print("✅ Quality preserved (25 points)")
    elif final_assessment.overall_score > 0.5:
        evasion_score += 10
        print("🟡 Quality acceptable (10 points)")
    
    print(f"")
    print(f"🎯 OVERALL EVASION SCORE: {evasion_score}/100")
    
    if evasion_score >= 90:
        rating = "🏆 EXCELLENT - Maximum steganographic protection"
    elif evasion_score >= 75:
        rating = "🥇 VERY GOOD - Strong evasion capabilities"
    elif evasion_score >= 60:
        rating = "🥈 GOOD - Solid steganographic implementation"
    elif evasion_score >= 45:
        rating = "🥉 ACCEPTABLE - Basic protection level"
    else:
        rating = "🔴 NEEDS IMPROVEMENT - Enhance steganography"
    
    print(f"🏅 RATING: {rating}")
    
    # Save comprehensive report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"output/analysis_reports/complete_steganography_demo_{timestamp}.json"
    
    comprehensive_report = {
        "timestamp": datetime.now().isoformat(),
        "demonstration_type": "Complete Steganography System",
        "original_text": original_clean,
        "final_steganographic_text": final_clean,
        "transformations": {
            "paraphrasing": {
                "method": paraphrase_result.best_method,
                "quality_scores": paraphrase_result.quality_scores,
                "processing_time": paraphrase_time
            },
            "unicode_steganography": {
                "substitutions_made": unicode_result['substitutions_made'],
                "invisibility_score": unicode_result['invisibility_score'],
                "steganography_ratio": unicode_result['steganography_ratio'],
                "processing_time": unicode_time
            },
            "invisible_characters": {
                "chars_added": invisible_result['invisible_chars_count'],
                "injection_points": invisible_result['injection_points'],
                "invisibility_ratio": invisible_result['invisibility_ratio'],
                "processing_time": invisible_time
            }
        },
        "final_assessment": {
            "overall_score": final_assessment.overall_score,
            "naturalness": final_assessment.naturalness_score,
            "academic_appropriateness": final_assessment.academic_appropriateness,
            "meaning_preservation": final_assessment.meaning_preservation,
            "grammar_quality": final_assessment.grammar_quality,
            "confidence_level": final_assessment.confidence_level,
            "flagged_issues": final_assessment.flagged_issues,
            "processing_time": validation_time
        },
        "effectiveness_metrics": {
            "evasion_score": evasion_score,
            "rating": rating,
            "total_processing_time": total_processing_time,
            "length_change": length_change,
            "visible_similarity": visible_char_similarity
        }
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Complete demonstration report: {report_path}")
    
    # System capabilities summary
    print(f"\n🚀 COMPLETE SYSTEM CAPABILITIES:")
    print("🧠 Indonesian T5 Neural Paraphrasing")
    print("📚 20,139 Contextual Synonyms Database") 
    print("🔤 Unicode Steganography (Multiple Scripts)")
    print("👻 Invisible Characters (6 Types)")
    print("🤖 AI Quality Validation (Gemini + Heuristics)")
    print("📊 Real-time Performance Monitoring")
    print("📈 Comprehensive Effectiveness Scoring")
    print("🎯 Multi-layer Detection Evasion")
    
    print(f"\n🎉 COMPLETE STEGANOGRAPHY DEMONSTRATION FINISHED!")
    print("🕵️ All techniques working in perfect harmony!")

if __name__ == "__main__":
    main()