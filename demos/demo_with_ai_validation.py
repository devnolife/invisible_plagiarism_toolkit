#!/usr/bin/env python3
"""
Demo with AI Validation
Demonstrasi sistem paraphrasing dengan validasi AI menggunakan Gemini
"""

import os
import json
from datetime import datetime
from contextual_paraphraser import ContextualParaphraser
from ai_quality_checker import AIQualityChecker

def main():
    print("🤖 DEMO: AI-VALIDATED CONTEXTUAL PARAPHRASING")
    print("=" * 60)
    
    # Initialize systems
    print("\n🚀 SYSTEM INITIALIZATION")
    paraphraser = ContextualParaphraser(verbose=False)
    
    # Check for Gemini API key
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ Gemini API key found")
        ai_checker = AIQualityChecker(api_key=api_key, verbose=False)
    else:
        print("⚠️  Gemini API key not found - using fallback heuristics")
        print("   To use AI validation, set GEMINI_API_KEY environment variable")
        ai_checker = AIQualityChecker(verbose=False)
    
    print(f"✅ Loaded {len(paraphraser.synonym_dict)} synonyms")
    print("✅ AI quality checker ready")
    
    # Test cases - including some that should be flagged
    test_cases = [
        {
            "name": "Good Academic Text",
            "text": "Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen",
            "expected_quality": "High"
        },
        {
            "name": "Business Analysis", 
            "text": "Analisis data menunjukkan bahwa faktor harga dan kualitas memiliki korelasi positif dengan kepuasan pelanggan",
            "expected_quality": "High"
        },
        {
            "name": "Research Methodology",
            "text": "Metode penelitian yang digunakan adalah pendekatan kuantitatif dengan teknik survei dan wawancara mendalam",
            "expected_quality": "High"
        }
    ]
    
    print(f"\n📊 TESTING {len(test_cases)} CASES WITH AI VALIDATION")
    print("=" * 50)
    
    all_results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['name']}")
        print(f"📝 Original: {test_case['text']}")
        
        # Apply paraphrasing
        paraphrase_result = paraphraser.batch_paraphrase_academic_text(test_case['text'], "high")
        
        print(f"✨ Paraphrased: {paraphrase_result['paraphrased_text']}")
        print(f"📉 Similarity Reduction: {paraphrase_result['final_similarity_reduction']:.1f}%")
        
        # AI Quality Assessment
        print("🤖 Running AI quality assessment...")
        quality_assessment = ai_checker.assess_paraphrase_quality(
            test_case['text'], 
            paraphrase_result['paraphrased_text'],
            context="Academic research text"
        )
        
        # Display AI results
        print(f"📊 AI Quality Scores:")
        print(f"   Overall: {quality_assessment.overall_score:.2f}/1.0")
        print(f"   Naturalness: {quality_assessment.naturalness_score:.2f}/1.0")
        print(f"   Academic Appropriateness: {quality_assessment.academic_appropriateness:.2f}/1.0")
        print(f"   Meaning Preservation: {quality_assessment.meaning_preservation:.2f}/1.0")
        print(f"   Grammar Quality: {quality_assessment.grammar_quality:.2f}/1.0")
        print(f"   Confidence: {quality_assessment.confidence_level}")
        
        # Show issues and recommendations
        if quality_assessment.flagged_issues:
            print("⚠️  Issues Found:")
            for issue in quality_assessment.flagged_issues:
                print(f"   • {issue}")
        
        if quality_assessment.recommendations:
            print("💡 AI Recommendations:")
            for rec in quality_assessment.recommendations:
                print(f"   • {rec}")
        
        # Quality verdict
        if quality_assessment.overall_score >= 0.8:
            verdict = "🟢 EXCELLENT"
        elif quality_assessment.overall_score >= 0.7:
            verdict = "🟡 GOOD" 
        elif quality_assessment.overall_score >= 0.6:
            verdict = "🟠 ACCEPTABLE"
        else:
            verdict = "🔴 NEEDS IMPROVEMENT"
        
        print(f"🎯 AI Verdict: {verdict}")
        
        # Store results
        result_data = {
            'test_name': test_case['name'],
            'original': test_case['text'],
            'paraphrased': paraphrase_result['paraphrased_text'],
            'similarity_reduction': paraphrase_result['final_similarity_reduction'],
            'ai_scores': {
                'overall': quality_assessment.overall_score,
                'naturalness': quality_assessment.naturalness_score,
                'academic': quality_assessment.academic_appropriateness,
                'meaning': quality_assessment.meaning_preservation,
                'grammar': quality_assessment.grammar_quality,
                'confidence': quality_assessment.confidence_level
            },
            'issues': quality_assessment.flagged_issues,
            'recommendations': quality_assessment.recommendations,
            'verdict': verdict
        }
        all_results.append(result_data)
        
        print("-" * 50)
    
    # Overall analysis
    avg_ai_score = sum(r['ai_scores']['overall'] for r in all_results) / len(all_results)
    avg_similarity_reduction = sum(r['similarity_reduction'] for r in all_results) / len(all_results)
    
    high_quality_count = sum(1 for r in all_results if r['ai_scores']['overall'] >= 0.8)
    total_issues = sum(len(r['issues']) for r in all_results)
    
    print(f"\n📊 OVERALL AI VALIDATION RESULTS")
    print(f"🎯 Average AI Quality Score: {avg_ai_score:.2f}/1.0")
    print(f"📉 Average Similarity Reduction: {avg_similarity_reduction:.1f}%")
    print(f"🏆 High Quality Results: {high_quality_count}/{len(all_results)}")
    print(f"⚠️  Total Issues Found: {total_issues}")
    
    # System effectiveness rating
    if avg_ai_score >= 0.85 and total_issues <= 2:
        system_rating = "🏆 EXCELLENT SYSTEM"
        recommendation = "Ready for production use with high confidence"
    elif avg_ai_score >= 0.75 and total_issues <= 5:
        system_rating = "🥇 VERY GOOD SYSTEM"
        recommendation = "Ready for production use with regular quality checks"  
    elif avg_ai_score >= 0.65:
        system_rating = "🥈 GOOD SYSTEM"
        recommendation = "Suitable for use with manual review of results"
    else:
        system_rating = "🥉 NEEDS IMPROVEMENT"
        recommendation = "Requires further optimization before production use"
    
    print(f"\n{system_rating}")
    print(f"💭 Recommendation: {recommendation}")
    
    # Show AI validation benefits
    print(f"\n🤖 AI VALIDATION BENEFITS:")
    print("✅ Objective quality assessment")
    print("✅ Identifies inappropriate synonyms automatically")
    print("✅ Validates meaning preservation")
    print("✅ Ensures academic appropriateness")
    print("✅ Provides specific improvement recommendations")
    print("✅ Confidence scoring for reliability")
    
    # Save comprehensive report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"output/analysis_reports/ai_validated_demo_{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_version": "AI-Validated Contextual Paraphraser v1.0",
        "ai_validation_enabled": api_key is not None,
        "summary": {
            "total_tests": len(all_results),
            "avg_ai_score": avg_ai_score,
            "avg_similarity_reduction": avg_similarity_reduction,
            "high_quality_count": high_quality_count,
            "total_issues": total_issues,
            "system_rating": system_rating,
            "recommendation": recommendation
        },
        "detailed_results": all_results
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Complete AI validation report saved: {report_path}")
    
    # Instructions for API key setup
    if not api_key:
        print(f"\n🔑 TO ENABLE FULL AI VALIDATION:")
        print("1. Get Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable: export GEMINI_API_KEY='your_api_key_here'")
        print("3. Re-run this demo for full AI validation")
    
    print(f"\n🎉 AI-VALIDATED SYSTEM DEMONSTRATION COMPLETE!")

if __name__ == "__main__":
    main()