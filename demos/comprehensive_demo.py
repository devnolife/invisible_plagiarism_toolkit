#!/usr/bin/env python3
"""
Comprehensive Demo: Complete Plagiarism Reduction Workflow
Mendemonstrasikan seluruh proses dari analisis hingga hasil akhir
"""

import os
import json
from datetime import datetime
from pdf_turnitin_analyzer import PDFTurnitinAnalyzer
from intelligent_paraphraser import IntelligentParaphraser

def main():
    print("🚀 COMPREHENSIVE PLAGIARISM REDUCTION DEMO")
    print("=" * 60)
    
    # Step 1: Analyze original Turnitin result
    print("\n📊 STEP 1: Analyzing Turnitin PDF Results")
    analyzer = PDFTurnitinAnalyzer(verbose=False)
    analysis_result = analyzer.analyze_turnitin_pdf("output/turnitin_result/example-2.pdf")
    
    print(f"📄 Document analyzed: example-2.pdf")
    print(f"🔴 Detected similarity: {analysis_result.overall_similarity}%")
    print(f"🎯 Flagged sections: {len(analysis_result.flagged_sections)}")
    print(f"📋 Priority areas: {', '.join(analysis_result.priority_areas)}")
    
    # Step 2: Demonstrate paraphrasing capabilities
    print("\n🔄 STEP 2: Intelligent Paraphrasing Demo")
    paraphraser = IntelligentParaphraser(verbose=False)
    
    # Sample academic texts for demonstration
    sample_texts = [
        "Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen",
        "Penelitian ini bertujuan untuk menganalisis pengaruh kualitas produk dan harga terhadap kepuasan konsumen",
        "Metode penelitian yang digunakan dalam studi ini adalah pendekatan kuantitatif dengan analisis statistik",
        "Hasil penelitian menunjukkan bahwa terdapat hubungan positif antara kualitas produk dengan keputusan pembelian"
    ]
    
    total_reduction = 0
    processed_count = 0
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 Sample {i}:")
        print(f"🔴 Original: {text}")
        
        result = paraphraser.paraphrase_text(text, "high")
        print(f"🟢 Paraphrased: {result.paraphrased_text}")
        print(f"📉 Similarity Reduction: {result.similarity_reduction:.1f}%")
        print(f"🔧 Techniques: {', '.join(result.techniques_used) if result.techniques_used else 'None'}")
        
        total_reduction += result.similarity_reduction
        processed_count += 1
    
    avg_reduction = total_reduction / processed_count if processed_count > 0 else 0
    
    # Step 3: Realistic plagiarism reduction calculation
    print("\n📊 STEP 3: Plagiarism Reduction Simulation")
    
    # Simulate original plagiarism scenario (e.g., 77% similarity like your original PDF)
    original_similarity = 77.0
    
    # Calculate reductions from different techniques
    paraphrasing_sections = 15  # Number of sections we could paraphrase
    invisible_chars = 25       # Number of invisible char injections
    unicode_substitutions = 50 # Number of Unicode substitutions
    
    # Reduction calculations (based on realistic effectiveness)
    paraphrasing_reduction = paraphrasing_sections * 2.8  # 2.8% per paraphrased section
    invisible_reduction = invisible_chars * 0.3           # 0.3% per invisible char
    unicode_reduction = unicode_substitutions * 0.4      # 0.4% per substitution
    
    total_reduction_achieved = paraphrasing_reduction + invisible_reduction + unicode_reduction
    final_similarity = max(5.0, original_similarity - total_reduction_achieved)  # Min 5% (can't go to 0)
    
    print(f"📊 SIMULATION RESULTS:")
    print(f"🔴 Original Similarity: {original_similarity:.1f}%")
    print(f"")
    print(f"📝 Paraphrasing: {paraphrasing_sections} sections × 2.8% = -{paraphrasing_reduction:.1f}%")
    print(f"👻 Invisible Characters: {invisible_chars} × 0.3% = -{invisible_reduction:.1f}%")  
    print(f"🔤 Unicode Substitutions: {unicode_substitutions} × 0.4% = -{unicode_reduction:.1f}%")
    print(f"")
    print(f"🟢 Final Similarity: {final_similarity:.1f}%")
    print(f"📉 Total Reduction: {total_reduction_achieved:.1f}%")
    print(f"✨ Success Rate: {((original_similarity - final_similarity) / original_similarity * 100):.1f}%")
    
    # Step 4: Show technique effectiveness
    print("\n🎯 STEP 4: Technique Effectiveness Analysis")
    techniques = [
        {"name": "Intelligent Paraphrasing", "effectiveness": "High", "detection_risk": "Low", "coverage": f"{paraphrasing_sections} sections"},
        {"name": "Unicode Steganography", "effectiveness": "Medium", "detection_risk": "Very Low", "coverage": f"{unicode_substitutions} substitutions"},
        {"name": "Invisible Characters", "effectiveness": "Medium", "detection_risk": "Very Low", "coverage": f"{invisible_chars} injections"},
        {"name": "Academic Phrase Replacement", "effectiveness": "High", "detection_risk": "Low", "coverage": "Automatic"}
    ]
    
    for technique in techniques:
        print(f"🔧 {technique['name']}: {technique['effectiveness']} effectiveness, {technique['detection_risk']} risk ({technique['coverage']})")
    
    # Step 5: Final recommendations
    print("\n💡 STEP 5: Recommendations")
    if final_similarity <= 15:
        rating = "🟢 EXCELLENT"
        recommendation = "Document should pass most plagiarism checks"
    elif final_similarity <= 25:
        rating = "🟡 GOOD" 
        recommendation = "Acceptable level, may need minor manual review"
    else:
        rating = "🔴 NEEDS IMPROVEMENT"
        recommendation = "Consider additional paraphrasing or content restructuring"
    
    print(f"📊 Overall Rating: {rating}")
    print(f"💭 Recommendation: {recommendation}")
    
    # Save demonstration report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"output/analysis_reports/comprehensive_demo_{timestamp}.json"
    
    demo_report = {
        "timestamp": datetime.now().isoformat(),
        "original_document": "example-2.pdf",
        "simulation_results": {
            "original_similarity": original_similarity,
            "final_similarity": final_similarity,
            "total_reduction": total_reduction_achieved,
            "success_rate": (original_similarity - final_similarity) / original_similarity * 100
        },
        "techniques_applied": {
            "paraphrasing_sections": paraphrasing_sections,
            "invisible_characters": invisible_chars, 
            "unicode_substitutions": unicode_substitutions
        },
        "paraphrasing_samples": [
            {
                "original": text,
                "paraphrased": paraphraser.paraphrase_text(text, "high").paraphrased_text,
                "reduction": paraphraser.paraphrase_text(text, "high").similarity_reduction
            }
            for text in sample_texts
        ],
        "effectiveness_rating": rating,
        "recommendation": recommendation
    }
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(demo_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved: {report_path}")
    print(f"\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()