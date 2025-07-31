#!/usr/bin/env python3
"""
Complete Codebase Convergence Analysis Runner

This script runs all 5 phases of the comprehensive codebase convergence analysis.
"""

import sys
import time
from pathlib import Path

# Import all phase modules
from github_fetcher_and_phase1 import main as run_phase1_with_sample_data
from phase2_comparison import Phase2Comparison
from phase3_stress_profiling import Phase3StressProfiling
from phase4_base_selection import Phase4BaseSelection
from phase5_refactor_blueprint import Phase5RefactorBlueprint


def main():
    """Run complete 5-phase codebase convergence analysis"""
    print("=" * 80)
    print("COMPREHENSIVE CODEBASE CONVERGENCE ANALYSIS")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    try:
        # Phase 1: Traversal and Behavioral Analysis
        print("🔍 PHASE 1: TRAVERSAL AND BEHAVIORAL ANALYSIS")
        print("-" * 60)
        phase1_start = time.time()
        
        # Run Phase 1 with sample data (or real GitHub data if available)
        s1_behaviors, soldier_behaviors = run_phase1_with_sample_data()
        
        phase1_duration = time.time() - phase1_start
        print(f"Phase 1 completed in {phase1_duration:.1f} seconds")
        print()
        
        # Phase 2: Comparative Analysis
        print("📊 PHASE 2: COMPARATIVE ANALYSIS")
        print("-" * 60)
        phase2_start = time.time()
        
        phase2 = Phase2Comparison()
        comparisons = phase2.run_phase2()
        
        phase2_duration = time.time() - phase2_start
        print(f"Phase 2 completed in {phase2_duration:.1f} seconds")
        print()
        
        # Phase 3: Stress Profiling
        print("⚠️  PHASE 3: STRESS PROFILING AND RISK ANALYSIS")
        print("-" * 60)
        phase3_start = time.time()
        
        phase3 = Phase3StressProfiling()
        risk_classification = phase3.run_phase3()
        
        phase3_duration = time.time() - phase3_start
        print(f"Phase 3 completed in {phase3_duration:.1f} seconds")
        print()
        
        # Phase 4: Base Codebase Selection
        print("🎯 PHASE 4: BASE CODEBASE SELECTION")
        print("-" * 60)
        phase4_start = time.time()
        
        phase4 = Phase4BaseSelection()
        selected_anchor = phase4.run_phase4()
        
        phase4_duration = time.time() - phase4_start
        print(f"Phase 4 completed in {phase4_duration:.1f} seconds")
        print()
        
        # Phase 5: Refactor Blueprint Synthesis
        print("🛠️  PHASE 5: REFACTOR BLUEPRINT SYNTHESIS")
        print("-" * 60)
        phase5_start = time.time()
        
        phase5 = Phase5RefactorBlueprint()
        blueprint_result = phase5.run_phase5()
        
        phase5_duration = time.time() - phase5_start
        print(f"Phase 5 completed in {phase5_duration:.1f} seconds")
        print()
        
        # Final Summary
        total_duration = time.time() - start_time
        
        print("=" * 80)
        print("ANALYSIS COMPLETE - EXECUTIVE SUMMARY")
        print("=" * 80)
        print()
        
        print("📈 ANALYSIS RESULTS:")
        print(f"  • Total Analysis Time: {total_duration:.1f} seconds")
        print(f"  • S1 Modules Analyzed: {len(s1_behaviors) if s1_behaviors else 0}")
        print(f"  • Soldier Modules Analyzed: {len(soldier_behaviors) if soldier_behaviors else 0}")
        print(f"  • Module Pairs Compared: {len(comparisons)}")
        print(f"  • Total Risks Identified: {risk_classification['risk_summary']['total_risks']}")
        print(f"  • Selected Anchor Codebase: {selected_anchor.name.upper()}")
        print(f"  • Refactor Steps Generated: {blueprint_result['total_steps']}")
        print()
        
        print("🎯 KEY FINDINGS:")
        print(f"  • Anchor Selection Score: {selected_anchor.overall_score:.3f}")
        print(f"  • Estimated Convergence Duration: {blueprint_result['strategy']['total_estimated_duration']}")
        print(f"  • Critical Risks: {risk_classification['risk_summary']['by_severity']['critical']}")
        print(f"  • High Risks: {risk_classification['risk_summary']['by_severity']['high']}")
        print()
        
        print("📁 DELIVERABLES GENERATED:")
        output_dir = Path("/home/runner/work/new/new")
        
        # List key deliverables
        deliverables = [
            "analysis/module_behavior_s1.json",
            "analysis/module_behavior_soldier.json", 
            "analysis/assumptions.csv",
            "analysis/risk_classification.json",
            "comparison/convergence_map.md",
            "refactor/anchor_declaration.json",
            "refactor/refactor_plan.yaml",
            "refactor/test_requirements.md",
            "refactor/rollback_triggers.md"
        ]
        
        for deliverable in deliverables:
            file_path = output_dir / deliverable
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                print(f"  ✅ {deliverable} ({size_kb:.1f} KB)")
            else:
                print(f"  ❌ {deliverable} (missing)")
        print()
        
        print("🚀 READY FOR CONVERGENCE EXECUTION")
        print(f"  The {selected_anchor.name.upper()} codebase has been selected as the anchor.")
        print(f"  A comprehensive {blueprint_result['total_steps']}-step refactor plan is ready.")
        print(f"  Estimated convergence time: {blueprint_result['strategy']['total_estimated_duration']}")
        print()
        
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ ANALYSIS FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    
    success = main()
    sys.exit(0 if success else 1)