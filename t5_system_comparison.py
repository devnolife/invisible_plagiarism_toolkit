#!/usr/bin/env python3
"""
T5 System Comparison Test
Membandingkan performa sistem dengan dan tanpa Indonesian T5
"""

import os
import json
import time
from datetime import datetime
from contextual_paraphraser import ContextualParaphraser
from hybrid_paraphraser import HybridParaphraser
from ai_quality_checker import AIQualityChecker

def main():
    print("🧠 T5 NEURAL PARAPHRASING SYSTEM COMPARISON")
    print("=" * 60)
    
    # Initialize systems
    print("\n🔧 INITIALIZING COMPARISON SYSTEMS...")
    
    # System 1: Contextual only (previous system)
    contextual_only = ContextualParaphraser(verbose=False)
    
    # System 2: Hybrid with T5 (new system) 
    hybrid_system = HybridParaphraser(enable_t5=True, verbose=False)
    
    # Quality checker
    quality_checker = AIQualityChecker(verbose=False)
    
    print(f"✅ Contextual System: {len(contextual_only.synonym_dict):,} synonyms")
    print(f"✅ Hybrid System: T5 + {len(contextual_only.synonym_dict):,} synonyms")
    print(f"✅ AI Quality Checker: Ready")
    
    # Test cases covering different academic contexts
    test_cases = [
        {
            "category": "Research Introduction",
            "text": "Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen",
            "complexity": "Medium"
        },
        {
            "category": "Methodology",
            "text": "Metode penelitian yang digunakan dalam studi ini adalah pendekatan kuantitatif dengan teknik pengumpulan data melalui survei",
            "complexity": "High"
        },
        {
            "category": "Data Analysis", 
            "text": "Hasil analisis statistik menunjukkan bahwa terdapat korelasi positif antara variabel independen dan dependen",
            "complexity": "High"
        },
        {
            "category": "Literature Review",
            "text": "Penelitian sebelumnya menunjukkan adanya perbedaan pendapat mengenai faktor yang mempengaruhi perilaku konsumen",
            "complexity": "Medium"
        },
        {
            "category": "Simple Statement",
            "text": "Kualitas produk sangat penting dalam kepuasan pelanggan",
            "complexity": "Low"
        }
    ]
    
    print(f"\n📊 TESTING {len(test_cases)} CASES WITH BOTH SYSTEMS")
    print("=" * 50)
    
    comparison_results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['category']} ({test_case['complexity']} complexity)")
        print(f"📝 Original: {test_case['text']}")
        
        # Test System 1: Contextual Only
        print("🔄 Testing contextual system...")
        start_time = time.time()
        contextual_result = contextual_only.batch_paraphrase_academic_text(test_case['text'], "high")
        contextual_time = time.time() - start_time
        
        contextual_paraphrase = contextual_result['paraphrased_text']
        contextual_quality = quality_checker.assess_paraphrase_quality(
            test_case['text'], contextual_paraphrase, "Academic text"
        )
        
        print(f"📚 Contextual Result: {contextual_paraphrase}")
        print(f"📊 Contextual Quality: {contextual_quality.overall_score:.2f}/1.0")
        print(f"⏱️ Contextual Time: {contextual_time:.2f}s")
        
        # Test System 2: Hybrid with T5
        print("🔄 Testing hybrid T5 system...")
        hybrid_result = hybrid_system.paraphrase_hybrid(test_case['text'], strategy="auto")
        
        print(f"🧠 T5 Result: {hybrid_result.hybrid_paraphrase}")
        print(f"📊 T5 Quality: {max(hybrid_result.quality_scores.values()) if hybrid_result.quality_scores else 0:.2f}/1.0")
        print(f"⏱️ T5 Time: {hybrid_result.processing_metrics.get('total_time', 0):.2f}s")
        print(f"🎖️ Best Method: {hybrid_result.best_method}")
        
        # Compare results
        contextual_score = contextual_quality.overall_score
        t5_score = max(hybrid_result.quality_scores.values()) if hybrid_result.quality_scores else 0
        
        winner = "🧠 T5 WINS" if t5_score > contextual_score else "📚 CONTEXTUAL WINS" if contextual_score > t5_score else "🤝 TIE"
        improvement = abs(t5_score - contextual_score)
        
        print(f"🏆 Winner: {winner} (improvement: {improvement:.2f})")
        
        # Store results
        result_data = {
            'test_case': test_case['category'],
            'complexity': test_case['complexity'],
            'original': test_case['text'],
            'contextual_result': contextual_paraphrase,
            'contextual_quality': contextual_score,
            'contextual_time': contextual_time,
            't5_result': hybrid_result.hybrid_paraphrase,
            't5_quality': t5_score,
            't5_time': hybrid_result.processing_metrics.get('total_time', 0),
            't5_method': hybrid_result.best_method,
            'winner': winner,
            'improvement': improvement
        }
        
        comparison_results.append(result_data)
        
        print("-" * 50)
    
    # Overall analysis
    print(f"\n📊 COMPREHENSIVE SYSTEM COMPARISON")
    
    # Calculate averages
    avg_contextual_quality = sum(r['contextual_quality'] for r in comparison_results) / len(comparison_results)
    avg_t5_quality = sum(r['t5_quality'] for r in comparison_results) / len(comparison_results)
    avg_contextual_time = sum(r['contextual_time'] for r in comparison_results) / len(comparison_results)
    avg_t5_time = sum(r['t5_time'] for r in comparison_results) / len(comparison_results)
    
    print(f"🎯 Average Quality Scores:")
    print(f"   📚 Contextual System: {avg_contextual_quality:.2f}/1.0")
    print(f"   🧠 T5 Hybrid System: {avg_t5_quality:.2f}/1.0")
    print(f"   📈 Quality Improvement: {(avg_t5_quality - avg_contextual_quality):.2f}")
    
    print(f"\n⏱️ Average Processing Times:")
    print(f"   📚 Contextual System: {avg_contextual_time:.2f}s")
    print(f"   🧠 T5 Hybrid System: {avg_t5_time:.2f}s")
    print(f"   ⚡ Speed Factor: {avg_contextual_time / avg_t5_time:.1f}x {'faster' if avg_contextual_time < avg_t5_time else 'slower'}")
    
    # Winner analysis
    t5_wins = sum(1 for r in comparison_results if '🧠 T5 WINS' in r['winner'])
    contextual_wins = sum(1 for r in comparison_results if '📚 CONTEXTUAL WINS' in r['winner'])
    ties = sum(1 for r in comparison_results if '🤝 TIE' in r['winner'])
    
    print(f"\n🏆 WIN/LOSS ANALYSIS:")
    print(f"   🧠 T5 Wins: {t5_wins}/{len(comparison_results)}")
    print(f"   📚 Contextual Wins: {contextual_wins}/{len(comparison_results)}")
    print(f"   🤝 Ties: {ties}/{len(comparison_results)}")
    
    # Performance by complexity
    complexity_analysis = {}
    for result in comparison_results:
        complexity = result['complexity']
        if complexity not in complexity_analysis:
            complexity_analysis[complexity] = []
        complexity_analysis[complexity].append(result)
    
    print(f"\n📈 PERFORMANCE BY COMPLEXITY:")
    for complexity, results in complexity_analysis.items():
        avg_contextual = sum(r['contextual_quality'] for r in results) / len(results)
        avg_t5 = sum(r['t5_quality'] for r in results) / len(results)
        improvement = avg_t5 - avg_contextual
        
        print(f"   {complexity} Complexity:")
        print(f"      Contextual: {avg_contextual:.2f}, T5: {avg_t5:.2f}")
        print(f"      Improvement: {improvement:+.2f}")
    
    # System recommendations
    print(f"\n💡 SYSTEM RECOMMENDATIONS:")
    
    if avg_t5_quality > avg_contextual_quality + 0.05:  # Significant improvement
        print("🧠 RECOMMENDATION: Use T5 Hybrid System")
        print("   ✅ Superior quality results")
        if t5_wins > contextual_wins:
            print("   ✅ Wins majority of test cases")
        if avg_t5_time < avg_contextual_time * 3:  # Acceptable time cost
            print("   ✅ Reasonable processing time")
        else:
            print("   ⚠️ Higher processing time (but worth it for quality)")
    
    elif avg_contextual_quality > avg_t5_quality + 0.05:
        print("📚 RECOMMENDATION: Stick with Contextual System")
        print("   ✅ Better quality with current setup")
        print("   ✅ Faster processing")
    
    else:
        print("🤝 RECOMMENDATION: Both systems perform similarly")
        print("   • Use T5 for high-quality needs")
        print("   • Use Contextual for speed needs")
    
    # Technical insights
    print(f"\n🔬 TECHNICAL INSIGHTS:")
    
    # T5 method analysis
    t5_methods = {}
    for result in comparison_results:
        method = result['t5_method']
        if method not in t5_methods:
            t5_methods[method] = 0
        t5_methods[method] += 1
    
    print("🧠 T5 Method Usage:")
    for method, count in t5_methods.items():
        print(f"   {method}: {count}/{len(comparison_results)} cases")
    
    # Save comprehensive comparison report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"output/analysis_reports/t5_system_comparison_{timestamp}.json"
    
    comparison_report = {
        "timestamp": datetime.now().isoformat(),
        "comparison_type": "T5 Neural vs Contextual Paraphrasing",
        "test_summary": {
            "total_tests": len(comparison_results),
            "avg_contextual_quality": avg_contextual_quality,
            "avg_t5_quality": avg_t5_quality,
            "avg_contextual_time": avg_contextual_time,
            "avg_t5_time": avg_t5_time,
            "quality_improvement": avg_t5_quality - avg_contextual_quality
        },
        "win_loss": {
            "t5_wins": t5_wins,
            "contextual_wins": contextual_wins,
            "ties": ties
        },
        "complexity_analysis": complexity_analysis,
        "detailed_results": comparison_results
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(comparison_report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📄 Complete comparison report saved: {report_path}")
    
    # Final system status
    print(f"\n🚀 FINAL SYSTEM STATUS:")
    print(f"🧠 Indonesian T5: {'✅ ACTIVE' if hybrid_system.t5_enabled else '❌ DISABLED'}")
    print(f"📚 Contextual Synonyms: ✅ {len(contextual_only.synonym_dict):,} entries")
    print(f"🤖 AI Validation: {'✅ GEMINI' if os.getenv('GEMINI_API_KEY') else '⚡ HEURISTIC'}")
    print(f"🎯 Overall Performance: {'🏆 ENHANCED' if avg_t5_quality > avg_contextual_quality else '📊 BASELINE'}")
    
    print(f"\n🎉 T5 SYSTEM COMPARISON COMPLETED!")

if __name__ == "__main__":
    main()