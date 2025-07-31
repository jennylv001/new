#!/usr/bin/env python3
"""
PHASE 4 - BASE CODEBASE SELECTION: Anchor Codebase Determination

This script implements Phase 4 of the codebase convergence analysis.
It selects the canonical anchor codebase using measurable, observable scores.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
import pandas as pd
from dataclasses import dataclass
import math


@dataclass
class CodebaseMetrics:
    """Structured metrics for codebase evaluation"""
    name: str
    architectural_coherence: float  # 0-1 scale
    refactorability: float         # 0-1 scale
    functional_resilience: float   # 0-1 scale
    convergence_potential: float   # 0-1 scale
    overall_score: float          # Average of all metrics


class Phase4BaseSelection:
    """Implements Phase 4 base codebase selection"""
    
    def __init__(self, output_dir: str = "/home/runner/work/new/new"):
        self.output_dir = Path(output_dir)
        
    def load_analysis_data(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """Load all previous analysis data"""
        print("Phase 4: Loading analysis data...")
        
        # Load behavioral data
        with open(self.output_dir / "analysis" / "module_behavior_s1.json", 'r') as f:
            s1_data = json.load(f)
        
        with open(self.output_dir / "analysis" / "module_behavior_soldier.json", 'r') as f:
            soldier_data = json.load(f)
        
        # Load comparison data
        with open(self.output_dir / "comparison" / "comparison_tables" / "detailed_comparisons.json", 'r') as f:
            comparison_data = json.load(f)
        
        # Load risk classification
        with open(self.output_dir / "analysis" / "risk_classification.json", 'r') as f:
            risk_data = json.load(f)
        
        return s1_data, soldier_data, comparison_data, risk_data
    
    def calculate_architectural_coherence(self, module_data: Dict[str, Any]) -> float:
        """Calculate architectural coherence score (0-1)"""
        print("Calculating architectural coherence...")
        
        coherence_factors = []
        
        # 1. Module organization consistency
        modules = list(module_data.keys())
        similar_modules = sum(1 for i, mod1 in enumerate(modules) 
                            for mod2 in modules[i+1:] 
                            if self._modules_have_similar_structure(module_data[mod1], module_data[mod2]))
        
        total_pairs = len(modules) * (len(modules) - 1) // 2
        organization_score = similar_modules / max(total_pairs, 1)
        coherence_factors.append(organization_score)
        
        # 2. Import consistency and coupling patterns
        all_imports = []
        for behavior in module_data.values():
            all_imports.extend(behavior['imports'])
        
        import_diversity = len(set(all_imports)) / max(len(all_imports), 1)
        coupling_consistency = 1.0 - import_diversity  # Lower diversity = higher consistency
        coherence_factors.append(coupling_consistency)
        
        # 3. Error handling consistency
        modules_with_errors = sum(1 for behavior in module_data.values() if behavior['error_flows'])
        error_consistency = modules_with_errors / len(module_data)
        coherence_factors.append(error_consistency)
        
        # 4. Function naming and signature consistency
        all_functions = []
        for behavior in module_data.values():
            all_functions.extend(behavior['functions'])
        
        typed_functions = sum(1 for func in all_functions if func['return_type'])
        typing_consistency = typed_functions / max(len(all_functions), 1)
        coherence_factors.append(typing_consistency)
        
        # 5. Complexity distribution consistency
        complexities = [behavior['complexity_metrics']['cyclomatic_complexity'] 
                       for behavior in module_data.values()]
        
        if complexities:
            complexity_variance = self._calculate_variance(complexities)
            max_complexity = max(complexities)
            complexity_consistency = 1.0 - (complexity_variance / max(max_complexity**2, 1))
            coherence_factors.append(max(0.0, complexity_consistency))
        
        # Calculate overall architectural coherence
        coherence_score = sum(coherence_factors) / len(coherence_factors)
        
        print(f"Architectural coherence factors: {[f'{f:.3f}' for f in coherence_factors]}")
        print(f"Overall architectural coherence: {coherence_score:.3f}")
        
        return min(1.0, max(0.0, coherence_score))
    
    def calculate_refactorability(self, module_data: Dict[str, Any], risk_data: Dict[str, Any]) -> float:
        """Calculate refactorability score (0-1)"""
        print("Calculating refactorability...")
        
        refactorability_factors = []
        
        # 1. Code complexity - lower complexity = higher refactorability
        total_functions = sum(len(behavior['functions']) for behavior in module_data.values())
        total_complexity = sum(behavior['complexity_metrics']['cyclomatic_complexity'] 
                             for behavior in module_data.values())
        
        avg_complexity = total_complexity / max(total_functions, 1)
        complexity_factor = max(0.0, 1.0 - (avg_complexity / 20.0))  # Assuming 20 is high complexity
        refactorability_factors.append(complexity_factor)
        
        # 2. Coupling levels - lower coupling = higher refactorability
        coupling_factors = [behavior['complexity_metrics']['coupling_factor'] 
                          for behavior in module_data.values()]
        avg_coupling = sum(coupling_factors) / max(len(coupling_factors), 1)
        coupling_factor = max(0.0, 1.0 - (avg_coupling / 5.0))  # Assuming 5.0 is high coupling
        refactorability_factors.append(coupling_factor)
        
        # 3. Test coverage indicators (inferred from error handling)
        modules_with_error_handling = sum(1 for behavior in module_data.values() 
                                        if behavior['error_flows'])
        test_coverage_proxy = modules_with_error_handling / len(module_data)
        refactorability_factors.append(test_coverage_proxy)
        
        # 4. Documentation quality (inferred from docstrings)
        all_functions = []
        for behavior in module_data.values():
            all_functions.extend(behavior['functions'])
        
        documented_functions = sum(1 for func in all_functions if func['has_docstring'])
        documentation_factor = documented_functions / max(len(all_functions), 1)
        refactorability_factors.append(documentation_factor)
        
        # 5. Risk burden - lower risks = higher refactorability
        high_risks = len([risk for risk in risk_data.get('high_risks', []) 
                         if not risk['module'].startswith('soldier_')])
        critical_risks = len([risk for risk in risk_data.get('critical_risks', []) 
                            if not risk['module'].startswith('soldier_')])
        
        total_risk_weight = critical_risks * 2 + high_risks
        risk_factor = max(0.0, 1.0 - (total_risk_weight / 50.0))  # Assuming 50 is high risk
        refactorability_factors.append(risk_factor)
        
        # Calculate overall refactorability
        refactorability_score = sum(refactorability_factors) / len(refactorability_factors)
        
        print(f"Refactorability factors: {[f'{f:.3f}' for f in refactorability_factors]}")
        print(f"Overall refactorability: {refactorability_score:.3f}")
        
        return min(1.0, max(0.0, refactorability_score))
    
    def calculate_functional_resilience(self, module_data: Dict[str, Any], risk_data: Dict[str, Any]) -> float:
        """Calculate functional resilience score (0-1)"""
        print("Calculating functional resilience...")
        
        resilience_factors = []
        
        # 1. Error handling coverage
        modules_with_error_handling = sum(1 for behavior in module_data.values() 
                                        if behavior['error_flows'])
        error_coverage = modules_with_error_handling / len(module_data)
        resilience_factors.append(error_coverage)
        
        # 2. Input validation (inferred from type hints and parameter handling)
        all_functions = []
        for behavior in module_data.values():
            all_functions.extend(behavior['functions'])
        
        typed_params = sum(1 for func in all_functions 
                          if func['return_type'] and func['parameters'])
        validation_factor = typed_params / max(len(all_functions), 1)
        resilience_factors.append(validation_factor)
        
        # 3. Dependency isolation (lower external dependencies = higher resilience)
        external_deps = 0
        total_imports = 0
        
        for behavior in module_data.values():
            total_imports += len(behavior['imports'])
            external_deps += sum(1 for imp in behavior['imports'] 
                               if any(ext in imp for ext in ['requests', 'urllib', 'http', 
                                                            'database', 'sqlite', 'mysql']))
        
        dependency_factor = 1.0 - (external_deps / max(total_imports, 1))
        resilience_factors.append(dependency_factor)
        
        # 4. Fault tolerance patterns (inferred from try-except patterns)
        fault_tolerance_modules = sum(1 for behavior in module_data.values() 
                                    if any('try_except' in err for err in behavior['error_flows']))
        fault_tolerance_factor = fault_tolerance_modules / len(module_data)
        resilience_factors.append(fault_tolerance_factor)
        
        # 5. Resource management (lower resource strain = higher resilience)
        # Load strain analysis for this codebase
        strain_scores = []
        stress_profiles_dir = self.output_dir / "analysis" / "stress_profiles"
        
        for module_path in module_data.keys():
            profile_file = stress_profiles_dir / f"{module_path.replace('/', '_')}_profile.json"
            if profile_file.exists():
                with open(profile_file, 'r') as f:
                    profile = json.load(f)
                    strain_scores.append(profile.get('risk_score', 0))
        
        if strain_scores:
            avg_strain = sum(strain_scores) / len(strain_scores)
            resource_factor = max(0.0, 1.0 - (avg_strain / 10.0))  # Assuming 10 is max risk score
            resilience_factors.append(resource_factor)
        
        # Calculate overall functional resilience
        resilience_score = sum(resilience_factors) / len(resilience_factors)
        
        print(f"Resilience factors: {[f'{f:.3f}' for f in resilience_factors]}")
        print(f"Overall functional resilience: {resilience_score:.3f}")
        
        return min(1.0, max(0.0, resilience_score))
    
    def calculate_convergence_potential(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                                      comparison_data: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate convergence potential for both codebases (0-1)"""
        print("Calculating convergence potential...")
        
        # Factors that affect convergence difficulty
        s1_factors = []
        soldier_factors = []
        
        # 1. Interface compatibility
        total_interface_overlap = 0
        comparison_count = 0
        
        for comparison in comparison_data.values():
            interface_overlap = comparison['interface_compatibility']['interface_overlap']
            total_interface_overlap += interface_overlap
            comparison_count += 1
        
        avg_interface_overlap = total_interface_overlap / max(comparison_count, 1)
        s1_factors.append(avg_interface_overlap)
        soldier_factors.append(avg_interface_overlap)
        
        # 2. Function signature compatibility
        compatible_signatures = 0
        total_signatures = 0
        
        for comparison in comparison_data.values():
            for sig in comparison['interface_compatibility']['signature_compatibility']:
                total_signatures += 1
                if sig['parameter_count_match'] and sig['return_type_match']:
                    compatible_signatures += 1
        
        signature_compatibility = compatible_signatures / max(total_signatures, 1)
        s1_factors.append(signature_compatibility)
        soldier_factors.append(signature_compatibility)
        
        # 3. Module size similarity (more similar = easier convergence)
        s1_function_counts = [len(behavior['functions']) for behavior in s1_data.values()]
        soldier_function_counts = [len(behavior['functions']) for behavior in soldier_data.values()]
        
        s1_avg_functions = sum(s1_function_counts) / len(s1_function_counts)
        soldier_avg_functions = sum(soldier_function_counts) / len(soldier_function_counts)
        
        size_similarity = 1.0 - abs(s1_avg_functions - soldier_avg_functions) / max(s1_avg_functions, soldier_avg_functions)
        s1_factors.append(size_similarity)
        soldier_factors.append(size_similarity)
        
        # 4. Unique functionality burden (less unique = easier convergence)
        s1_modules = set(s1_data.keys())
        soldier_modules = set(soldier_data.keys())
        common_modules = s1_modules.intersection(soldier_modules)
        
        s1_unique_ratio = len(s1_modules - common_modules) / len(s1_modules)
        soldier_unique_ratio = len(soldier_modules - common_modules) / len(soldier_modules)
        
        s1_factors.append(1.0 - s1_unique_ratio)
        soldier_factors.append(1.0 - soldier_unique_ratio)
        
        # 5. Import compatibility
        s1_imports = set()
        soldier_imports = set()
        
        for behavior in s1_data.values():
            s1_imports.update(behavior['imports'])
        
        for behavior in soldier_data.values():
            soldier_imports.update(behavior['imports'])
        
        common_imports = s1_imports.intersection(soldier_imports)
        s1_import_compat = len(common_imports) / len(s1_imports) if s1_imports else 1.0
        soldier_import_compat = len(common_imports) / len(soldier_imports) if soldier_imports else 1.0
        
        s1_factors.append(s1_import_compat)
        soldier_factors.append(soldier_import_compat)
        
        # Calculate convergence potential scores
        s1_convergence = sum(s1_factors) / len(s1_factors)
        soldier_convergence = sum(soldier_factors) / len(soldier_factors)
        
        print(f"S1 convergence factors: {[f'{f:.3f}' for f in s1_factors]}")
        print(f"Soldier convergence factors: {[f'{f:.3f}' for f in soldier_factors]}")
        print(f"S1 convergence potential: {s1_convergence:.3f}")
        print(f"Soldier convergence potential: {soldier_convergence:.3f}")
        
        return (min(1.0, max(0.0, s1_convergence)), 
                min(1.0, max(0.0, soldier_convergence)))
    
    def _modules_have_similar_structure(self, mod1: Dict[str, Any], mod2: Dict[str, Any]) -> bool:
        """Check if two modules have similar structural patterns"""
        # Compare function count similarity
        func_count_sim = abs(len(mod1['functions']) - len(mod2['functions'])) <= 2
        
        # Compare class count similarity
        class_count_sim = abs(len(mod1['classes']) - len(mod2['classes'])) <= 1
        
        # Compare import patterns
        import_count_sim = abs(len(mod1['imports']) - len(mod2['imports'])) <= 3
        
        return func_count_sim and class_count_sim and import_count_sim
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values"""
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def select_anchor_codebase(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                              comparison_data: Dict[str, Any], risk_data: Dict[str, Any]) -> CodebaseMetrics:
        """Select the anchor codebase using measurable scores"""
        print("Phase 4: Selecting anchor codebase...")
        print("=" * 50)
        
        # Calculate metrics for S1
        s1_arch_coherence = self.calculate_architectural_coherence(s1_data)
        s1_refactorability = self.calculate_refactorability(s1_data, risk_data)
        s1_resilience = self.calculate_functional_resilience(s1_data, risk_data)
        
        # Calculate metrics for Soldier
        soldier_arch_coherence = self.calculate_architectural_coherence(soldier_data)
        soldier_refactorability = self.calculate_refactorability(soldier_data, risk_data)
        soldier_resilience = self.calculate_functional_resilience(soldier_data, risk_data)
        
        # Calculate convergence potential for both
        s1_convergence, soldier_convergence = self.calculate_convergence_potential(
            s1_data, soldier_data, comparison_data)
        
        # Create metric objects
        s1_metrics = CodebaseMetrics(
            name="s1",
            architectural_coherence=s1_arch_coherence,
            refactorability=s1_refactorability,
            functional_resilience=s1_resilience,
            convergence_potential=s1_convergence,
            overall_score=(s1_arch_coherence + s1_refactorability + s1_resilience + s1_convergence) / 4
        )
        
        soldier_metrics = CodebaseMetrics(
            name="soldier",
            architectural_coherence=soldier_arch_coherence,
            refactorability=soldier_refactorability,
            functional_resilience=soldier_resilience,
            convergence_potential=soldier_convergence,
            overall_score=(soldier_arch_coherence + soldier_refactorability + soldier_resilience + soldier_convergence) / 4
        )
        
        print("\nCODEBASE SCORING RESULTS:")
        print("=" * 50)
        print(f"S1 Codebase:")
        print(f"  Architectural Coherence: {s1_metrics.architectural_coherence:.3f}")
        print(f"  Refactorability:         {s1_metrics.refactorability:.3f}")
        print(f"  Functional Resilience:   {s1_metrics.functional_resilience:.3f}")
        print(f"  Convergence Potential:   {s1_metrics.convergence_potential:.3f}")
        print(f"  OVERALL SCORE:           {s1_metrics.overall_score:.3f}")
        print()
        print(f"Soldier Codebase:")
        print(f"  Architectural Coherence: {soldier_metrics.architectural_coherence:.3f}")
        print(f"  Refactorability:         {soldier_metrics.refactorability:.3f}")
        print(f"  Functional Resilience:   {soldier_metrics.functional_resilience:.3f}")
        print(f"  Convergence Potential:   {soldier_metrics.convergence_potential:.3f}")
        print(f"  OVERALL SCORE:           {soldier_metrics.overall_score:.3f}")
        print("=" * 50)
        
        # Select anchor based on overall score
        if s1_metrics.overall_score > soldier_metrics.overall_score:
            selected_anchor = s1_metrics
            print(f"\nANCHOR SELECTION: S1 (Score: {s1_metrics.overall_score:.3f})")
        elif soldier_metrics.overall_score > s1_metrics.overall_score:
            selected_anchor = soldier_metrics
            print(f"\nANCHOR SELECTION: Soldier (Score: {soldier_metrics.overall_score:.3f})")
        else:
            # Tie-breaker: select codebase with lower redundant complexity
            s1_redundancy = self._calculate_redundancy_metric(s1_data)
            soldier_redundancy = self._calculate_redundancy_metric(soldier_data)
            
            if s1_redundancy < soldier_redundancy:
                selected_anchor = s1_metrics
                print(f"\nANCHOR SELECTION: S1 (Tie-breaker: lower redundancy {s1_redundancy:.3f} vs {soldier_redundancy:.3f})")
            else:
                selected_anchor = soldier_metrics
                print(f"\nANCHOR SELECTION: Soldier (Tie-breaker: lower redundancy {soldier_redundancy:.3f} vs {s1_redundancy:.3f})")
        
        return selected_anchor, s1_metrics, soldier_metrics
    
    def _calculate_redundancy_metric(self, module_data: Dict[str, Any]) -> float:
        """Calculate redundant logic density"""
        total_functions = sum(len(behavior['functions']) for behavior in module_data.values())
        
        # Count function name duplications
        all_function_names = []
        for behavior in module_data.values():
            all_function_names.extend(f['name'] for f in behavior['functions'])
        
        unique_names = len(set(all_function_names))
        redundancy = 1.0 - (unique_names / max(total_functions, 1))
        
        return redundancy
    
    def generate_anchor_declaration(self, selected_anchor: CodebaseMetrics, 
                                  s1_metrics: CodebaseMetrics, soldier_metrics: CodebaseMetrics) -> None:
        """Generate anchor declaration with scoring breakdown"""
        print("Phase 4: Generating anchor declaration...")
        
        declaration = {
            "anchor_selection": {
                "selected_codebase": selected_anchor.name,
                "selection_timestamp": "2025-07-31T12:57:00Z",
                "overall_score": selected_anchor.overall_score,
                "selection_criteria": "measurable_observable_scores"
            },
            "scoring_breakdown": {
                "s1": {
                    "architectural_coherence": s1_metrics.architectural_coherence,
                    "refactorability": s1_metrics.refactorability,
                    "functional_resilience": s1_metrics.functional_resilience,
                    "convergence_potential": s1_metrics.convergence_potential,
                    "overall_score": s1_metrics.overall_score
                },
                "soldier": {
                    "architectural_coherence": soldier_metrics.architectural_coherence,
                    "refactorability": soldier_metrics.refactorability,
                    "functional_resilience": soldier_metrics.functional_resilience,
                    "convergence_potential": soldier_metrics.convergence_potential,
                    "overall_score": soldier_metrics.overall_score
                }
            },
            "score_differences": {
                "architectural_coherence": abs(s1_metrics.architectural_coherence - soldier_metrics.architectural_coherence),
                "refactorability": abs(s1_metrics.refactorability - soldier_metrics.refactorability),
                "functional_resilience": abs(s1_metrics.functional_resilience - soldier_metrics.functional_resilience),
                "convergence_potential": abs(s1_metrics.convergence_potential - soldier_metrics.convergence_potential),
                "overall": abs(s1_metrics.overall_score - soldier_metrics.overall_score)
            },
            "measurement_methodology": {
                "architectural_coherence": [
                    "Module organization consistency",
                    "Import consistency and coupling patterns", 
                    "Error handling consistency",
                    "Function naming and signature consistency",
                    "Complexity distribution consistency"
                ],
                "refactorability": [
                    "Code complexity levels",
                    "Coupling levels",
                    "Test coverage indicators",
                    "Documentation quality",
                    "Risk burden"
                ],
                "functional_resilience": [
                    "Error handling coverage",
                    "Input validation patterns",
                    "Dependency isolation",
                    "Fault tolerance patterns",
                    "Resource management"
                ],
                "convergence_potential": [
                    "Interface compatibility",
                    "Function signature compatibility",
                    "Module size similarity",
                    "Unique functionality burden",
                    "Import compatibility"
                ]
            }
        }
        
        with open(self.output_dir / "refactor" / "anchor_declaration.json", 'w') as f:
            json.dump(declaration, f, indent=2)
        
        print(f"Anchor declaration saved: {self.output_dir / 'refactor' / 'anchor_declaration.json'}")
    
    def generate_selection_rationale(self, selected_anchor: CodebaseMetrics,
                                   s1_metrics: CodebaseMetrics, soldier_metrics: CodebaseMetrics) -> None:
        """Generate evidence-based selection rationale"""
        print("Phase 4: Generating selection rationale...")
        
        rationale_file = self.output_dir / "refactor" / "selection_rationale.md"
        
        with open(rationale_file, 'w') as f:
            f.write("# Base Codebase Selection Rationale\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"**Selected Anchor Codebase: {selected_anchor.name.upper()}**\n\n")
            f.write(f"Overall Score: **{selected_anchor.overall_score:.3f}**\n\n")
            
            # Score comparison table
            f.write("## Scoring Comparison\n\n")
            f.write("| Metric | S1 | Soldier | Difference | Winner |\n")
            f.write("|--------|----|---------|-----------|---------|\n")
            
            metrics = [
                ("Architectural Coherence", s1_metrics.architectural_coherence, soldier_metrics.architectural_coherence),
                ("Refactorability", s1_metrics.refactorability, soldier_metrics.refactorability),
                ("Functional Resilience", s1_metrics.functional_resilience, soldier_metrics.functional_resilience),
                ("Convergence Potential", s1_metrics.convergence_potential, soldier_metrics.convergence_potential),
                ("**Overall Score**", s1_metrics.overall_score, soldier_metrics.overall_score)
            ]
            
            for metric_name, s1_score, soldier_score in metrics:
                diff = abs(s1_score - soldier_score)
                winner = "S1" if s1_score > soldier_score else "Soldier" if soldier_score > s1_score else "Tie"
                f.write(f"| {metric_name} | {s1_score:.3f} | {soldier_score:.3f} | {diff:.3f} | {winner} |\n")
            
            f.write("\n## Detailed Analysis\n\n")
            
            # Analysis by metric
            f.write("### Architectural Coherence\n\n")
            f.write("Measures consistency in module organization, import patterns, error handling, ")
            f.write("function signatures, and complexity distribution.\n\n")
            
            if s1_metrics.architectural_coherence > soldier_metrics.architectural_coherence:
                f.write(f"**S1 demonstrates superior architectural coherence** ({s1_metrics.architectural_coherence:.3f} vs {soldier_metrics.architectural_coherence:.3f})\n\n")
            elif soldier_metrics.architectural_coherence > s1_metrics.architectural_coherence:
                f.write(f"**Soldier demonstrates superior architectural coherence** ({soldier_metrics.architectural_coherence:.3f} vs {s1_metrics.architectural_coherence:.3f})\n\n")
            else:
                f.write("Both codebases show equivalent architectural coherence.\n\n")
            
            f.write("### Refactorability\n\n")
            f.write("Evaluates code complexity, coupling levels, test coverage, documentation quality, and risk burden.\n\n")
            
            if s1_metrics.refactorability > soldier_metrics.refactorability:
                f.write(f"**S1 shows higher refactorability** ({s1_metrics.refactorability:.3f} vs {soldier_metrics.refactorability:.3f})\n\n")
            elif soldier_metrics.refactorability > s1_metrics.refactorability:
                f.write(f"**Soldier shows higher refactorability** ({soldier_metrics.refactorability:.3f} vs {s1_metrics.refactorability:.3f})\n\n")
            else:
                f.write("Both codebases show equivalent refactorability.\n\n")
            
            f.write("### Functional Resilience\n\n")
            f.write("Assesses error handling coverage, input validation, dependency isolation, ")
            f.write("fault tolerance patterns, and resource management.\n\n")
            
            if s1_metrics.functional_resilience > soldier_metrics.functional_resilience:
                f.write(f"**S1 demonstrates superior functional resilience** ({s1_metrics.functional_resilience:.3f} vs {soldier_metrics.functional_resilience:.3f})\n\n")
            elif soldier_metrics.functional_resilience > s1_metrics.functional_resilience:
                f.write(f"**Soldier demonstrates superior functional resilience** ({soldier_metrics.functional_resilience:.3f} vs {s1_metrics.functional_resilience:.3f})\n\n")
            else:
                f.write("Both codebases show equivalent functional resilience.\n\n")
            
            f.write("### Convergence Potential\n\n")
            f.write("Evaluates interface compatibility, signature compatibility, size similarity, ")
            f.write("unique functionality burden, and import compatibility.\n\n")
            
            if s1_metrics.convergence_potential > soldier_metrics.convergence_potential:
                f.write(f"**S1 offers better convergence potential** ({s1_metrics.convergence_potential:.3f} vs {soldier_metrics.convergence_potential:.3f})\n\n")
            elif soldier_metrics.convergence_potential > s1_metrics.convergence_potential:
                f.write(f"**Soldier offers better convergence potential** ({soldier_metrics.convergence_potential:.3f} vs {s1_metrics.convergence_potential:.3f})\n\n")
            else:
                f.write("Both codebases show equivalent convergence potential.\n\n")
            
            # Conclusion
            f.write("## Selection Conclusion\n\n")
            f.write(f"Based on measurable, observable behavioral analysis, **{selected_anchor.name.upper()}** ")
            f.write(f"has been selected as the anchor codebase with an overall score of {selected_anchor.overall_score:.3f}.\n\n")
            
            # Evidence references
            f.write("## Evidence References\n\n")
            f.write("This selection is based on:\n")
            f.write("- Behavioral analysis from Phase 1 traversal\n")
            f.write("- Comparative analysis from Phase 2\n")
            f.write("- Risk profiling from Phase 3\n")
            f.write("- Quantifiable metrics derived from actual code behavior\n")
            f.write("- No assumptions based on naming, comments, or directory structure\n\n")
        
        print(f"Selection rationale saved: {rationale_file}")
    
    def generate_risks_and_limitations(self, selected_anchor: CodebaseMetrics, risk_data: Dict[str, Any]) -> None:
        """Generate selection constraints and risks documentation"""
        print("Phase 4: Generating risks and limitations...")
        
        risks_file = self.output_dir / "refactor" / "risks_and_limitations.md"
        
        with open(risks_file, 'w') as f:
            f.write("# Selection Constraints and Risks\n\n")
            
            f.write("## Selection Constraints\n\n")
            f.write("### Anchor Codebase Limitations\n\n")
            f.write(f"The selected anchor codebase (**{selected_anchor.name}**) has the following constraints:\n\n")
            
            # Analyze specific limitations based on scores
            if selected_anchor.architectural_coherence < 0.8:
                f.write(f"- **Architectural Coherence**: Score of {selected_anchor.architectural_coherence:.3f} indicates room for improvement in structural consistency\n")
            
            if selected_anchor.refactorability < 0.8:
                f.write(f"- **Refactorability**: Score of {selected_anchor.refactorability:.3f} suggests moderate complexity in code modifications\n")
            
            if selected_anchor.functional_resilience < 0.8:
                f.write(f"- **Functional Resilience**: Score of {selected_anchor.functional_resilience:.3f} indicates potential reliability concerns\n")
            
            if selected_anchor.convergence_potential < 0.8:
                f.write(f"- **Convergence Potential**: Score of {selected_anchor.convergence_potential:.3f} suggests challenges in merging codebases\n")
            
            f.write("\n### Risk Classification Impact\n\n")
            
            # Extract risks related to the selected codebase
            anchor_prefix = "" if selected_anchor.name == "s1" else "soldier_"
            anchor_risks = {
                'critical': [r for r in risk_data.get('critical_risks', []) 
                           if r['module'].startswith(anchor_prefix) or not r['module'].startswith('soldier_')],
                'high': [r for r in risk_data.get('high_risks', []) 
                        if r['module'].startswith(anchor_prefix) or not r['module'].startswith('soldier_')],
                'medium': [r for r in risk_data.get('medium_risks', []) 
                          if r['module'].startswith(anchor_prefix) or not r['module'].startswith('soldier_')]
            }
            
            f.write(f"**Critical Risks**: {len(anchor_risks['critical'])}\n")
            f.write(f"**High Risks**: {len(anchor_risks['high'])}\n")
            f.write(f"**Medium Risks**: {len(anchor_risks['medium'])}\n\n")
            
            if anchor_risks['critical']:
                f.write("#### Critical Risks in Anchor Codebase\n\n")
                for risk in anchor_risks['critical'][:5]:  # Show top 5
                    f.write(f"- **{risk['type']}** ({risk['module']}): {risk['description']}\n")
                f.write("\n")
            
            if anchor_risks['high']:
                f.write("#### High Risks in Anchor Codebase\n\n")
                for risk in anchor_risks['high'][:10]:  # Show top 10
                    f.write(f"- **{risk['type']}** ({risk['module']}): {risk['description']}\n")
                f.write("\n")
            
            f.write("## Convergence Risks\n\n")
            f.write("### Integration Challenges\n\n")
            f.write("Based on the comparative analysis, the following integration challenges are expected:\n\n")
            
            # Generic convergence risks
            f.write("1. **Interface Compatibility**: Function signature mismatches may require wrapper implementations\n")
            f.write("2. **Dependency Conflicts**: Different import patterns may create dependency resolution issues\n")
            f.write("3. **Error Handling Inconsistencies**: Different error handling patterns may need unification\n")
            f.write("4. **State Management**: Different state mutation patterns may cause integration issues\n")
            f.write("5. **Performance Variations**: Different efficiency characteristics may impact overall performance\n\n")
            
            f.write("### Mitigation Strategies\n\n")
            f.write("- **Gradual Integration**: Implement convergence in atomic, testable phases\n")
            f.write("- **Interface Adaptation**: Create adapter layers for incompatible interfaces\n")
            f.write("- **Comprehensive Testing**: Implement extensive test coverage for convergence points\n")
            f.write("- **Rollback Mechanisms**: Maintain ability to revert changes at each integration step\n")
            f.write("- **Performance Monitoring**: Track performance metrics throughout convergence process\n\n")
            
            f.write("## Limitations of Analysis\n\n")
            f.write("### Methodology Constraints\n\n")
            f.write("This analysis has the following limitations:\n\n")
            f.write("- **Static Analysis Only**: Dynamic runtime behavior not captured\n")
            f.write("- **Sample Data**: Analysis based on representative sample code, not complete repositories\n")
            f.write("- **External Dependencies**: Third-party library behavior not fully analyzed\n")
            f.write("- **Business Logic**: Domain-specific logic may have implications not captured in structural analysis\n")
            f.write("- **Performance Characteristics**: Actual runtime performance not measured\n\n")
            
            f.write("### Recommendation\n\n")
            f.write("While this analysis provides a systematic, evidence-based approach to codebase selection, ")
            f.write("the convergence process should include:\n\n")
            f.write("- **Dynamic Testing**: Runtime behavior validation\n")
            f.write("- **Performance Benchmarking**: Actual performance measurement\n")
            f.write("- **Stakeholder Review**: Business logic and domain expertise validation\n")
            f.write("- **Incremental Validation**: Step-by-step verification during convergence\n\n")
        
        print(f"Risks and limitations saved: {risks_file}")
    
    def run_phase4(self) -> CodebaseMetrics:
        """Execute complete Phase 4 base codebase selection"""
        print("Starting Phase 4 - Base Codebase Selection")
        print("=" * 60)
        
        try:
            # Ensure refactor directory exists
            refactor_dir = self.output_dir / "refactor"
            refactor_dir.mkdir(exist_ok=True)
            
            # Step 1: Load analysis data
            s1_data, soldier_data, comparison_data, risk_data = self.load_analysis_data()
            
            # Step 2: Select anchor codebase
            selected_anchor, s1_metrics, soldier_metrics = self.select_anchor_codebase(
                s1_data, soldier_data, comparison_data, risk_data)
            
            # Step 3: Generate anchor declaration
            self.generate_anchor_declaration(selected_anchor, s1_metrics, soldier_metrics)
            
            # Step 4: Generate selection rationale
            self.generate_selection_rationale(selected_anchor, s1_metrics, soldier_metrics)
            
            # Step 5: Generate risks and limitations
            self.generate_risks_and_limitations(selected_anchor, risk_data)
            
            print(f"\nPhase 4 Base Codebase Selection Complete!")
            print(f"Selected Anchor: {selected_anchor.name.upper()}")
            print(f"Overall Score: {selected_anchor.overall_score:.3f}")
            print("=" * 60)
            
            return selected_anchor
            
        except Exception as e:
            print(f"Error in Phase 4 analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    try:
        phase4 = Phase4BaseSelection()
        selected_anchor = phase4.run_phase4()
        
        print(f"Base codebase selection completed successfully!")
        print(f"Anchor: {selected_anchor.name}")
        
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.exit(1)