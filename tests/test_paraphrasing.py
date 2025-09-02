#!/usr/bin/env python3
"""
Test paraphrasing functionality with known flagged content
"""

from intelligent_paraphraser import IntelligentParaphraser
from pdf_turnitin_analyzer import PDFTurnitinAnalyzer

def main():
    # Initialize modules
    paraphraser = IntelligentParaphraser(verbose=True)
    analyzer = PDFTurnitinAnalyzer(verbose=True)
    
    # Analyze the PDF to get actual flagged sections
    print("🔍 Analyzing Turnitin PDF for flagged sections...")
    analysis_result = analyzer.analyze_turnitin_pdf("output/turnitin_result/example-2.pdf")
    
    print(f"\n📊 Found {len(analysis_result.flagged_sections)} flagged sections")
    print(f"💯 Overall similarity: {analysis_result.overall_similarity}%")
    
    # Test paraphrasing on actual flagged content
    paraphrase_results = []
    print("\n🔄 TESTING PARAPHRASING ON FLAGGED CONTENT:")
    print("=" * 60)
    
    for i, section in enumerate(analysis_result.flagged_sections[:10], 1):  # Test first 10
        if section.flagged_type in ['academic_pattern', 'academic_phrase'] and len(section.text.strip()) > 15:
            print(f"\n📝 Test {i}: {section.flagged_type}")
            print(f"📄 Page {section.page_number}")
            print(f"🔴 Original: {section.text}")
            
            # Apply paraphrasing
            result = paraphraser.paraphrase_text(section.text, "high")
            paraphrase_results.append(result)
            
            print(f"🟢 Paraphrased: {result.paraphrased_text}")
            print(f"📉 Similarity Reduction: {result.similarity_reduction:.1f}%")
            print(f"🔧 Techniques: {', '.join(result.techniques_used)}")
            print("-" * 40)
    
    # Summary statistics
    if paraphrase_results:
        avg_reduction = sum(r.similarity_reduction for r in paraphrase_results) / len(paraphrase_results)
        print(f"\n📊 PARAPHRASING SUMMARY:")
        print(f"✨ Sections processed: {len(paraphrase_results)}")
        print(f"📉 Average similarity reduction: {avg_reduction:.1f}%")
        print(f"🎯 Estimated plagiarism reduction: {len(paraphrase_results) * 3.5:.1f}%")
        
        # Show most effective techniques
        all_techniques = []
        for result in paraphrase_results:
            all_techniques.extend(result.techniques_used)
        
        technique_counts = {}
        for tech in all_techniques:
            technique_counts[tech] = technique_counts.get(tech, 0) + 1
        
        print(f"\n🔧 Most used techniques:")
        for tech, count in sorted(technique_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {tech}: {count} times")

if __name__ == "__main__":
    main()