#!/usr/bin/env python3
"""
Interactive Main Interface - Complete Steganography System
Advanced Multi-Layer Document Manipulation and Plagiarism Detection Evasion

Features:
- File selection and browsing
- Multiple technique selection
- Interactive configuration
- Real-time progress monitoring
- Comprehensive result display

Author: DevNoLife
Version: 2.0 Complete System
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Import all system modules
from hybrid_paraphraser import HybridParaphraser, HybridParaphraseResult
from unicode_steganography import UnicodeSteg
from invisible_manipulator import InvisibleManipulator
from ai_quality_checker import AIQualityChecker, QualityAssessment
from pdf_turnitin_analyzer import PDFTurnitinAnalyzer
from pdf_direct_editor import PDFDirectEditor

class InteractiveSystem:
    def __init__(self):
        self.version = "2.0 Complete System"
        self.current_file = None
        self.current_technique = None
        self.configuration = self.load_default_config()
        
        # System components (lazy loading)
        self.paraphraser = None
        self.unicode_steg = None
        self.invisible_manipulator = None
        self.ai_checker = None
        self.pdf_analyzer = None
        self.pdf_editor = None
        
        # Results storage
        self.last_result = None
        
    def load_default_config(self) -> Dict:
        """Load default system configuration"""
        return {
            "paraphrasing": {
                "t5_model": "Wikidepia/IndoT5-base-paraphrase",
                "enable_contextual": True,
                "synonym_database": "data/sinonim.json",
                "quality_threshold": 0.7
            },
            "steganography": {
                "unicode_substitution": {
                    "enabled": True,
                    "aggressiveness": 0.15,
                    "target_academic_words": True
                },
                "invisible_characters": {
                    "enabled": True,
                    "injection_rate": 0.3,
                    "character_types": ["zwsp", "zwnj", "zwj", "mongolian"]
                }
            },
            "ai_validation": {
                "use_gemini": True,
                "fallback_heuristics": True,
                "confidence_threshold": "medium"
            },
            "pdf_processing": {
                "coordinate_precision": "high",
                "preserve_formatting": True,
                "max_text_changes": 50
            }
        }
    
    def print_banner(self):
        """Display system banner"""
        print("=" * 70)
        print("🕵️  INVISIBLE PLAGIARISM TOOLKIT - COMPLETE SYSTEM")
        print("   Advanced Multi-Layer Steganographic Document Manipulation")
        print("=" * 70)
        print(f"📊 Version: {self.version}")
        print(f"📅 System Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Features: T5 Neural + 20,139 Synonyms + Unicode + Invisible + AI")
        print("=" * 70)
        print()
    
    def display_main_menu(self):
        """Display main menu options"""
        print("🎛️  MAIN MENU - Choose an option:")
        print()
        print("📄 FILE OPERATIONS:")
        print("   1. Select Text File (.txt, .md)")
        print("   2. Select PDF File (.pdf)")
        print("   3. Browse Input Directory")
        print("   4. View Current File Info")
        print()
        print("🔧 PROCESSING TECHNIQUES:")
        print("   5. Complete Steganography System (Recommended)")
        print("   6. Neural Paraphrasing Only")
        print("   7. Steganography Only (Unicode + Invisible)")
        print("   8. PDF Processing (Turnitin Analysis + Direct Edit)")
        print()
        print("⚙️  CONFIGURATION:")
        print("   9. Adjust Processing Parameters")
        print("   10. View System Status")
        print("   11. Run System Diagnostics")
        print()
        print("📊 DEMONSTRATIONS:")
        print("   12. Run Complete System Demo")
        print("   13. Compare Techniques")
        print("   14. View Previous Results")
        print()
        print("❓ HELP & INFO:")
        print("   15. Help & Usage Guide")
        print("   16. About & Credits")
        print("   0. Exit")
        print()
    
    def select_file(self, file_type: str = "text") -> Optional[str]:
        """File selection interface"""
        print(f"📁 SELECT {file_type.upper()} FILE:")
        print()
        
        # Check input directory
        input_dir = Path("input")
        if not input_dir.exists():
            input_dir.mkdir(exist_ok=True)
            print("📁 Created input/ directory")
        
        # Get file extensions based on type
        if file_type == "text":
            extensions = ["*.txt", "*.md"]
        elif file_type == "pdf":
            extensions = ["*.pdf"]
        else:
            extensions = ["*.*"]
        
        # Find files
        files = []
        for ext in extensions:
            files.extend(list(input_dir.glob(ext)))
        
        if not files:
            print(f"❌ No {file_type} files found in input/ directory")
            print("💡 Please copy your files to the input/ folder")
            return None
        
        # Display files
        print(f"📋 Available {file_type} files:")
        for i, file_path in enumerate(files, 1):
            file_size = file_path.stat().st_size / 1024  # KB
            modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            print(f"   {i}. {file_path.name} ({file_size:.1f} KB, {modified.strftime('%Y-%m-%d %H:%M')})")
        
        print()
        try:
            choice = int(input("🔢 Enter file number (0 to cancel): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(files):
                selected_file = str(files[choice - 1])
                self.current_file = selected_file
                print(f"✅ Selected: {Path(selected_file).name}")
                return selected_file
            else:
                print("❌ Invalid file number")
                return None
        except ValueError:
            print("❌ Please enter a valid number")
            return None
    
    def show_file_info(self):
        """Display current file information"""
        if not self.current_file:
            print("❌ No file selected")
            return
        
        file_path = Path(self.current_file)
        if not file_path.exists():
            print("❌ Selected file no longer exists")
            self.current_file = None
            return
        
        print(f"📄 CURRENT FILE INFORMATION:")
        print(f"   📁 Name: {file_path.name}")
        print(f"   📍 Path: {file_path}")
        print(f"   📊 Size: {file_path.stat().st_size / 1024:.1f} KB")
        print(f"   📅 Modified: {datetime.fromtimestamp(file_path.stat().st_mtime)}")
        
        # Preview content for text files
        if file_path.suffix.lower() in ['.txt', '.md']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"   📝 Preview: {preview}")
                    print(f"   📏 Total Characters: {len(content)}")
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        
        print()
    
    def initialize_system_components(self, technique: str):
        """Initialize required system components based on technique"""
        print("🔧 Initializing system components...")
        
        if technique in ["complete", "paraphrase"]:
            if not self.paraphraser:
                print("🧠 Loading Neural Paraphrasing System...")
                self.paraphraser = HybridParaphraser(enable_t5=True, verbose=False)
        
        if technique in ["complete", "steganography"]:
            if not self.unicode_steg:
                print("🔤 Loading Unicode Steganography...")
                self.unicode_steg = UnicodeSteg()
            if not self.invisible_manipulator:
                print("👻 Loading Invisible Characters System...")
                self.invisible_manipulator = InvisibleManipulator(verbose=False)
        
        if technique in ["complete", "paraphrase"]:
            if not self.ai_checker:
                print("🤖 Loading AI Quality Checker...")
                self.ai_checker = AIQualityChecker(verbose=False)
        
        if technique == "pdf":
            if not self.pdf_analyzer:
                print("📄 Loading PDF Turnitin Analyzer...")
                self.pdf_analyzer = PDFTurnitinAnalyzer()
            if not self.pdf_editor:
                print("✏️ Loading PDF Direct Editor...")
                self.pdf_editor = PDFDirectEditor()
        
        print("✅ System components loaded!")
        print()
    
    def process_complete_system(self, text: str) -> Dict:
        """Run complete steganography system pipeline"""
        print("🕵️ RUNNING COMPLETE STEGANOGRAPHY SYSTEM")
        print("=" * 50)
        
        results = {
            "original_text": text,
            "processing_steps": [],
            "final_text": text,
            "metrics": {},
            "effectiveness_score": 0
        }
        
        current_text = text
        
        # Step 1: Neural + Contextual Paraphrasing
        print("🧠 STEP 1: Advanced Paraphrasing (T5 + 20,139 Synonyms)")
        print("-" * 40)
        start_time = time.time()
        
        paraphrase_result = self.paraphraser.paraphrase_hybrid(current_text, "parallel")
        paraphrase_time = time.time() - start_time
        
        current_text = paraphrase_result.hybrid_paraphrase
        
        print(f"✨ Method Used: {paraphrase_result.best_method}")
        print(f"📊 Quality Score: {max(paraphrase_result.quality_scores.values()) if paraphrase_result.quality_scores else 'N/A'}")
        print(f"⏱️ Processing Time: {paraphrase_time:.2f}s")
        print()
        
        results["processing_steps"].append({
            "step": "paraphrasing",
            "method": paraphrase_result.best_method,
            "quality_scores": paraphrase_result.quality_scores,
            "processing_time": paraphrase_time
        })
        
        # Step 2: Unicode Steganography
        print("🔤 STEP 2: Unicode Steganography (Latin→Cyrillic)")
        print("-" * 40)
        start_time = time.time()
        
        unicode_text, unicode_log = self.unicode_steg.apply_strategic_substitution(
            current_text, aggressiveness=self.configuration["steganography"]["unicode_substitution"]["aggressiveness"]
        )
        unicode_time = time.time() - start_time
        
        current_text = unicode_text
        
        print(f"🔄 Substitutions Made: {unicode_log['total_changes']}")
        print(f"📈 Steganography Ratio: {(unicode_log['total_changes'] / len(current_text.split())) * 100:.1f}%")
        print(f"⏱️ Processing Time: {unicode_time:.2f}s")
        print()
        
        results["processing_steps"].append({
            "step": "unicode_steganography",
            "substitutions_made": unicode_log['total_changes'],
            "processing_time": unicode_time
        })
        
        # Step 3: Invisible Character Injection
        print("👻 STEP 3: Invisible Character Injection")
        print("-" * 40)
        start_time = time.time()
        
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
        final_text = self.invisible_manipulator.insert_invisible_chars(
            current_text, invisible_chars, self.configuration["steganography"]["invisible_characters"]["injection_rate"]
        )
        invisible_time = time.time() - start_time
        
        invisible_count = len(final_text) - len(current_text)
        current_text = final_text
        
        print(f"👻 Invisible Characters Added: {invisible_count}")
        print(f"📍 Injection Rate: {self.configuration['steganography']['invisible_characters']['injection_rate'] * 100}%")
        print(f"⏱️ Processing Time: {invisible_time:.2f}s")
        print()
        
        results["processing_steps"].append({
            "step": "invisible_characters",
            "chars_added": invisible_count,
            "processing_time": invisible_time
        })
        
        # Step 4: AI Quality Assessment
        print("🤖 STEP 4: AI Quality Validation")
        print("-" * 40)
        start_time = time.time()
        
        final_assessment = self.ai_checker.assess_paraphrase_quality(
            text, current_text, "Academic research with steganographic modifications"
        )
        validation_time = time.time() - start_time
        
        print(f"📊 Overall Score: {final_assessment.overall_score:.2f}/1.0")
        print(f"🎯 Naturalness: {final_assessment.naturalness_score:.2f}/1.0")
        print(f"🎓 Academic Fit: {final_assessment.academic_appropriateness:.2f}/1.0")
        print(f"💬 Meaning Preserved: {final_assessment.meaning_preservation:.2f}/1.0")
        print(f"📝 Grammar Quality: {final_assessment.grammar_quality:.2f}/1.0")
        print(f"🔒 Confidence: {final_assessment.confidence_level}")
        print(f"⏱️ Processing Time: {validation_time:.2f}s")
        
        if final_assessment.flagged_issues:
            print("⚠️ Issues Detected:")
            for issue in final_assessment.flagged_issues:
                print(f"   • {issue}")
        
        print()
        
        results["processing_steps"].append({
            "step": "ai_validation",
            "overall_score": final_assessment.overall_score,
            "processing_time": validation_time
        })
        
        # Calculate Effectiveness Score
        effectiveness_score = self.calculate_evasion_score(paraphrase_result, unicode_log, final_assessment)
        
        # Final Results
        results.update({
            "final_text": current_text,
            "metrics": {
                "total_processing_time": paraphrase_time + unicode_time + invisible_time + validation_time,
                "length_change": len(current_text) - len(text),
                "character_changes": unicode_log['total_changes'] + invisible_count,
                "final_quality": final_assessment.overall_score
            },
            "effectiveness_score": effectiveness_score
        })
        
        return results
    
    def calculate_evasion_score(self, paraphrase_result, unicode_log: Dict, assessment: QualityAssessment) -> int:
        """Calculate overall evasion effectiveness score"""
        score = 0
        
        # Paraphrasing effectiveness (25 points max)
        if paraphrase_result and paraphrase_result.quality_scores:
            max_quality = max(paraphrase_result.quality_scores.values())
            if max_quality > 0.8:
                score += 25
            elif max_quality > 0.6:
                score += 15
            else:
                score += 5
        
        # Unicode steganography (25 points max)
        unicode_changes = unicode_log.get('total_changes', 0)
        if unicode_changes > 10:
            score += 25
        elif unicode_changes > 5:
            score += 15
        elif unicode_changes > 0:
            score += 5
        
        # Invisible characters (25 points max)
        # Estimated based on typical performance
        score += 15  # Moderate invisible character injection
        
        # Quality preservation (25 points max)
        if assessment.overall_score > 0.8:
            score += 25
        elif assessment.overall_score > 0.6:
            score += 15
        else:
            score += 5
        
        return min(score, 100)
    
    def display_results_summary(self, results: Dict):
        """Display comprehensive results summary"""
        print("📊 COMPREHENSIVE RESULTS SUMMARY")
        print("=" * 60)
        print()
        
        print(f"📝 FINAL PROCESSED TEXT:")
        print(f"   {results['final_text'][:200]}{'...' if len(results['final_text']) > 200 else ''}")
        print()
        
        print(f"📈 TRANSFORMATION METRICS:")
        print(f"   Original Length: {len(results['original_text'])} characters")
        print(f"   Final Length: {len(results['final_text'])} characters") 
        print(f"   Length Change: {results['metrics']['length_change']:+d} characters")
        print(f"   Character Modifications: {results['metrics']['character_changes']}")
        print(f"   Final Quality Score: {results['metrics']['final_quality']:.2f}/1.0")
        print(f"   Total Processing Time: {results['metrics']['total_processing_time']:.2f}s")
        print()
        
        print(f"🎯 EFFECTIVENESS ASSESSMENT:")
        effectiveness = results['effectiveness_score']
        if effectiveness >= 90:
            rating = "🏆 EXCELLENT - Maximum protection"
        elif effectiveness >= 75:
            rating = "🥇 VERY GOOD - Strong evasion"
        elif effectiveness >= 60:
            rating = "🥈 GOOD - Solid implementation"
        elif effectiveness >= 45:
            rating = "🥉 ACCEPTABLE - Basic protection"
        else:
            rating = "🔴 NEEDS IMPROVEMENT"
        
        print(f"   Evasion Score: {effectiveness}/100")
        print(f"   Rating: {rating}")
        print()
        
        print(f"⏱️ PROCESSING TIME BREAKDOWN:")
        total_time = results['metrics']['total_processing_time']
        for step in results['processing_steps']:
            step_name = step['step'].replace('_', ' ').title()
            step_time = step['processing_time']
            percentage = (step_time / total_time) * 100 if total_time > 0 else 0
            print(f"   {step_name}: {step_time:.2f}s ({percentage:.1f}%)")
        
        print()
    
    def save_results(self, results: Dict) -> str:
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("output/analysis_reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"interactive_processing_{timestamp}.json"
        filepath = output_dir / filename
        
        # Add metadata
        report = {
            "timestamp": datetime.now().isoformat(),
            "processing_type": "Interactive Complete System",
            "system_version": self.version,
            **results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return str(filepath)
    
    def run_technique_selection(self):
        """Main technique selection interface"""
        if not self.current_file:
            print("❌ Please select a file first (options 1-3)")
            return
        
        print("🎛️ TECHNIQUE SELECTION:")
        print()
        print("Available techniques:")
        print("5. Complete Steganography System - Full pipeline with all techniques")
        print("6. Neural Paraphrasing Only - T5 + Contextual synonyms with AI validation")
        print("7. Steganography Only - Unicode + Invisible characters without content changes")
        print("8. PDF Processing - Turnitin analysis and direct PDF editing")
        print()
        
        try:
            choice = int(input("🔢 Select technique (5-8): "))
            
            if choice == 5:
                self.run_complete_system()
            elif choice == 6:
                self.run_paraphrasing_only()
            elif choice == 7:
                self.run_steganography_only()
            elif choice == 8:
                self.run_pdf_processing()
            else:
                print("❌ Invalid technique selection")
        
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n⏹️ Operation cancelled by user")
        except Exception as e:
            print(f"❌ Error during processing: {e}")
    
    def run_complete_system(self):
        """Execute complete steganography system"""
        self.initialize_system_components("complete")
        
        # Read file content
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
        
        if len(text) < 10:
            print("❌ Text too short for processing (minimum 10 characters)")
            return
        
        print(f"📊 Processing text: {len(text)} characters")
        print()
        
        # Run complete system
        results = self.process_complete_system(text)
        
        # Display results
        self.display_results_summary(results)
        
        # Save results
        report_path = self.save_results(results)
        print(f"📄 Detailed report saved: {report_path}")
        
        # Store for later reference
        self.last_result = results
        
        input("\n📥 Press Enter to continue...")
    
    def run_paraphrasing_only(self):
        """Execute paraphrasing-only processing"""
        self.initialize_system_components("paraphrase")
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
        
        print("🧠 NEURAL PARAPHRASING SYSTEM")
        print("=" * 40)
        
        start_time = time.time()
        result = self.paraphraser.paraphrase_hybrid(text, "parallel")
        processing_time = time.time() - start_time
        
        print(f"✨ Original Text:")
        print(f"   {text[:150]}{'...' if len(text) > 150 else ''}")
        print()
        print(f"🎯 Paraphrased Text:")
        print(f"   {result.hybrid_paraphrase[:150]}{'...' if len(result.hybrid_paraphrase) > 150 else ''}")
        print()
        print(f"🏆 Best Method: {result.best_method}")
        print(f"📊 Quality Scores:")
        for method, score in result.quality_scores.items():
            print(f"   {method}: {score:.3f}")
        print(f"⏱️ Processing Time: {processing_time:.2f}s")
        
        # AI Quality Assessment
        assessment = self.ai_checker.assess_paraphrase_quality(text, result.hybrid_paraphrase)
        print(f"🤖 AI Quality Assessment: {assessment.overall_score:.2f}/1.0")
        
        input("\n📥 Press Enter to continue...")
    
    def run_steganography_only(self):
        """Execute steganography-only processing"""
        self.initialize_system_components("steganography")
        
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
        
        print("🔤👻 STEGANOGRAPHY-ONLY PROCESSING")
        print("=" * 40)
        
        current_text = text
        
        # Unicode Steganography
        print("🔤 Applying Unicode Steganography...")
        unicode_text, unicode_log = self.unicode_steg.apply_strategic_substitution(current_text, 0.15)
        print(f"   Substitutions: {unicode_log['total_changes']}")
        
        # Invisible Characters
        print("👻 Injecting Invisible Characters...")
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
        final_text = self.invisible_manipulator.insert_invisible_chars(unicode_text, invisible_chars, 0.3)
        invisible_count = len(final_text) - len(unicode_text)
        print(f"   Invisible chars added: {invisible_count}")
        
        print()
        print(f"📊 RESULTS:")
        print(f"   Original length: {len(text)} chars")
        print(f"   Final length: {len(final_text)} chars")
        print(f"   Unicode changes: {unicode_log['total_changes']}")
        print(f"   Invisible chars: {invisible_count}")
        print(f"   Visual similarity: ~95% (estimated)")
        
        input("\n📥 Press Enter to continue...")
    
    def run_pdf_processing(self):
        """Execute PDF processing with Turnitin trace removal"""
        if not self.current_file or not self.current_file.lower().endswith('.pdf'):
            print("❌ Please select a PDF file first")
            return
        
        self.initialize_system_components("pdf")
        
        print("📄 PDF PROCESSING SYSTEM")
        print("=" * 40)
        
        print(f"🔍 Processing PDF: {Path(self.current_file).name}")
        print(f"📊 Size: {Path(self.current_file).stat().st_size / 1024:.1f} KB")
        print()
        
        # Ask user for processing options
        print("📋 PROCESSING OPTIONS:")
        print("1. Clean Turnitin traces only")
        print("2. Clean + Apply steganography")
        print("3. Full processing (Clean + Steganography + Paraphrasing)")
        print()
        
        try:
            choice = int(input("🔢 Select option (1-3): "))
            
            if choice == 1:
                # Clean Turnitin traces only
                print("\n🧹 CLEANING TURNITIN TRACES...")
                output_path = str(Path(self.current_file).with_stem(Path(self.current_file).stem + "_cleaned"))
                
                removal_stats = self.pdf_editor.remove_all_turnitin_traces(self.current_file, output_path)
                
                print("\n📊 CLEANING RESULTS:")
                if removal_stats['processing_successful']:
                    print(f"   ✅ Processing successful")
                    print(f"   📝 Text markers removed: {removal_stats['markers_removed']}")
                    print(f"   🎨 Highlights removed: {removal_stats['highlights_removed']}")
                    print(f"   💧 Watermarks removed: {removal_stats['watermarks_removed']}")
                    print(f"   🧹 Metadata fields cleaned: {removal_stats['metadata_cleaned']}")
                    print(f"   📄 Clean file: {Path(output_path).name}")
                    
                    total_removed = (removal_stats['markers_removed'] + 
                                   removal_stats['highlights_removed'] + 
                                   removal_stats['watermarks_removed'] + 
                                   removal_stats['metadata_cleaned'])
                    print(f"   🎯 Total items removed: {total_removed}")
                else:
                    print("   ❌ Processing failed")
                    if removal_stats['errors']:
                        for error in removal_stats['errors']:
                            print(f"   ⚠️ {error}")
                            
            elif choice == 2:
                # Clean + Steganography
                print("\n🕵️ CLEANING + STEGANOGRAPHY PROCESSING...")
                
                result = self.pdf_editor.edit_pdf_from_turnitin_analysis(
                    pdf_path=self.current_file,
                    turnitin_pdf_path=None,  # No Turnitin report
                    use_paraphrasing=False,
                    remove_turnitin_traces=True
                )
                
                self._display_pdf_results(result)
                
            elif choice == 3:
                # Full processing
                print("\n🚀 FULL PDF PROCESSING...")
                
                result = self.pdf_editor.edit_pdf_from_turnitin_analysis(
                    pdf_path=self.current_file,
                    turnitin_pdf_path=None,  # No Turnitin report
                    use_paraphrasing=True,
                    paraphrase_intensity="high",
                    enable_ai_validation=True,
                    remove_turnitin_traces=True
                )
                
                self._display_pdf_results(result)
                
            else:
                print("❌ Invalid option")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except Exception as e:
            print(f"❌ Error during PDF processing: {e}")
        
        input("\n📥 Press Enter to continue...")
    
    def _display_pdf_results(self, result):
        """Display PDF processing results"""
        print("\n📊 PDF PROCESSING RESULTS:")
        print("=" * 40)
        
        print(f"📄 Original: {Path(result.original_file).name}")
        print(f"📤 Modified: {Path(result.modified_file).name}")
        
        if result.turnitin_traces_removed:
            print(f"\n🧹 TURNITIN CLEANUP:")
            print(f"   ✅ Traces removed: {result.turnitin_items_removed}")
            if hasattr(result, 'turnitin_removal_stats') and result.turnitin_removal_stats:
                for doc_type, stats in result.turnitin_removal_stats.items():
                    if isinstance(stats, dict) and stats.get('processing_successful'):
                        print(f"   📝 {doc_type}: {stats.get('markers_removed', 0)} markers, "
                              f"{stats.get('highlights_removed', 0)} highlights, "
                              f"{stats.get('metadata_cleaned', 0)} metadata cleaned")
        
        print(f"\n🔧 STEGANOGRAPHY EDITS:")
        print(f"   Total edits: {result.total_edits}")
        print(f"   Unicode substitutions: {result.unicode_substitutions}")
        print(f"   Invisible chars added: {result.invisible_chars_added}")
        print(f"   Pages modified: {result.pages_modified}")
        print(f"   Invisibility score: {result.invisibility_score:.1f}%")
        
        if result.paraphrased_sections > 0:
            print(f"\n📝 PARAPHRASING:")
            print(f"   Sections paraphrased: {result.paraphrased_sections}")
            if result.ai_validation_enabled:
                print(f"   AI quality score: {result.ai_quality_score:.2f}/1.0")
                print(f"   Quality issues: {result.quality_issues}")
        
        print(f"\n🎯 EFFECTIVENESS:")
        if result.plagiarism_before > 0:
            print(f"   Similarity before: {result.plagiarism_before:.1f}%")
            print(f"   Similarity after: {result.plagiarism_after:.1f}%")
            print(f"   Reduction achieved: {result.plagiarism_reduction:.1f}%")
        
        print(f"   Techniques used: {', '.join(result.techniques_used)}")
        print(f"   Processing successful: {'✅ Yes' if result.total_edits > 0 or result.turnitin_traces_removed else '❌ No significant changes'}")
    
    def show_system_status(self):
        """Display system status and loaded components"""
        print("🔍 SYSTEM STATUS:")
        print("=" * 30)
        print()
        
        components = [
            ("Neural Paraphraser", self.paraphraser is not None),
            ("Unicode Steganography", self.unicode_steg is not None),
            ("Invisible Manipulator", self.invisible_manipulator is not None),
            ("AI Quality Checker", self.ai_checker is not None),
            ("PDF Analyzer", self.pdf_analyzer is not None),
            ("PDF Editor", self.pdf_editor is not None)
        ]
        
        print("📦 LOADED COMPONENTS:")
        for component, loaded in components:
            status = "✅ Loaded" if loaded else "⭕ Not loaded"
            print(f"   {component}: {status}")
        
        print()
        print("📁 CURRENT SESSION:")
        print(f"   Selected File: {Path(self.current_file).name if self.current_file else 'None'}")
        print(f"   Last Technique: {self.current_technique or 'None'}")
        print(f"   Last Results: {'Available' if self.last_result else 'None'}")
        
        print()
        print("💾 MEMORY USAGE:")
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            print(f"   RAM Usage: {memory_mb:.1f} MB")
        except ImportError:
            print("   RAM Usage: Not available (install psutil)")
        
        input("\n📥 Press Enter to continue...")
    
    def run_system_demo(self):
        """Run complete system demonstration"""
        print("🎬 COMPLETE SYSTEM DEMONSTRATION")
        print("=" * 40)
        
        demo_text = """
        Berdasarkan hasil penelitian dapat disimpulkan bahwa kualitas produk berpengaruh signifikan terhadap keputusan pembelian konsumen. Penelitian ini menggunakan metode kuantitatif dengan analisis statistik untuk menguji hipotesis yang diajukan.
        """.strip()
        
        print(f"📝 Demo Text ({len(demo_text)} characters):")
        print(f"   {demo_text}")
        print()
        
        self.initialize_system_components("complete")
        
        print("🚀 Running complete demonstration...")
        results = self.process_complete_system(demo_text)
        
        self.display_results_summary(results)
        
        report_path = self.save_results(results)
        print(f"📄 Demo report saved: {report_path}")
        
        input("\n📥 Press Enter to continue...")
    
    def show_help(self):
        """Display help and usage guide"""
        print("❓ HELP & USAGE GUIDE")
        print("=" * 30)
        print()
        
        print("🚀 QUICK START:")
        print("1. Select a file using options 1-3")
        print("2. Choose a processing technique (5-8)")
        print("3. Review results and saved reports")
        print()
        
        print("📄 SUPPORTED FILE TYPES:")
        print("• Text files: .txt, .md")
        print("• PDF files: .pdf")
        print()
        
        print("🔧 AVAILABLE TECHNIQUES:")
        print("• Complete System: All techniques combined")
        print("• Paraphrasing Only: T5 + Contextual synonyms")
        print("• Steganography Only: Unicode + Invisible chars")
        print("• PDF Processing: Turnitin analysis + editing")
        print()
        
        print("📊 OUTPUT LOCATIONS:")
        print("• Processed files: output/processed_documents/")
        print("• Analysis reports: output/analysis_reports/")
        print("• Comparison files: output/comparison_files/")
        print()
        
        print("⚙️ CONFIGURATION:")
        print("• Config files: config.json, data/ folder")
        print("• Synonym database: data/sinonim.json (20,139 entries)")
        print("• Unicode mappings: data/unicode_mappings.json")
        print()
        
        input("📥 Press Enter to continue...")
    
    def show_about(self):
        """Display about and credits"""
        print("ℹ️ ABOUT & CREDITS")
        print("=" * 25)
        print()
        
        print(f"🕵️ Invisible Plagiarism Toolkit")
        print(f"📊 Version: {self.version}")
        print("👨‍💻 Author: DevNoLife")
        print("📅 Last Updated: September 2025")
        print()
        
        print("🚀 SYSTEM FEATURES:")
        print("• Indonesian T5 Neural Paraphrasing")
        print("• 20,139 Contextual Synonyms Database")
        print("• Unicode Steganography (Multi-script)")
        print("• Invisible Character Injection")
        print("• PDF Analysis & Direct Editing")
        print("• AI Quality Validation (Gemini)")
        print("• Real-time Performance Monitoring")
        print()
        
        print("📚 TECHNICAL STACK:")
        print("• Transformers (Hugging Face)")
        print("• Google Gemini API")
        print("• PyPDF2, pdfplumber, PyMuPDF")
        print("• Unicode Standard Compliance")
        print()
        
        print("⚠️ IMPORTANT NOTICE:")
        print("This software is designed for educational and research")
        print("purposes only. Users must ensure compliance with all")
        print("applicable laws and institutional policies.")
        print()
        
        input("📥 Press Enter to continue...")
    
    def main_loop(self):
        """Main interactive loop"""
        self.print_banner()
        
        while True:
            try:
                self.display_main_menu()
                choice = input("🔢 Enter your choice (0-16): ").strip()
                print()
                
                if choice == "0":
                    print("👋 Thank you for using Invisible Plagiarism Toolkit!")
                    print("🔒 Remember: Use responsibly and ethically.")
                    break
                elif choice == "1":
                    self.select_file("text")
                elif choice == "2":
                    self.select_file("pdf")
                elif choice == "3":
                    print("📁 Browse input directory feature - To be implemented")
                    input("📥 Press Enter to continue...")
                elif choice == "4":
                    self.show_file_info()
                elif choice in ["5", "6", "7", "8"]:
                    self.run_technique_selection()
                elif choice == "9":
                    print("⚙️ Configuration interface - To be implemented")
                    input("📥 Press Enter to continue...")
                elif choice == "10":
                    self.show_system_status()
                elif choice == "11":
                    print("🔧 System diagnostics - To be implemented")
                    input("📥 Press Enter to continue...")
                elif choice == "12":
                    self.run_system_demo()
                elif choice == "13":
                    print("📊 Technique comparison - To be implemented")
                    input("📥 Press Enter to continue...")
                elif choice == "14":
                    print("📋 Previous results viewer - To be implemented")
                    input("📥 Press Enter to continue...")
                elif choice == "15":
                    self.show_help()
                elif choice == "16":
                    self.show_about()
                else:
                    print("❌ Invalid choice. Please select 0-16.")
                
                print()  # Add spacing between operations
                
            except KeyboardInterrupt:
                print("\n\n⏹️ Operation interrupted. Returning to main menu...")
                print()
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("🔄 Returning to main menu...")
                print()

def main():
    """Main entry point"""
    try:
        system = InteractiveSystem()
        system.main_loop()
    except KeyboardInterrupt:
        print("\n\n👋 System shutdown requested. Goodbye!")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("💡 Please check your installation and try again.")

if __name__ == "__main__":
    main()