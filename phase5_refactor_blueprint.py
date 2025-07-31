#!/usr/bin/env python3
"""
PHASE 5 - REFACTOR BLUEPRINT SYNTHESIS: Complete Convergence Plan

This script implements Phase 5 of the codebase convergence analysis.
It creates a comprehensive refactor blueprint for converging the codebases.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
import re


@dataclass
class RefactorStep:
    """Represents a single atomic refactor step"""
    step_id: str
    step_type: str  # 'merge', 'adapt', 'remove', 'add', 'modify'
    source_codebase: str
    target_module: str
    source_module: str = None
    description: str = ""
    behavioral_rationale: str = ""
    risk_level: str = "medium"  # low, medium, high, critical
    dependencies: List[str] = None
    rollback_procedure: str = ""
    validation_criteria: List[str] = None
    estimated_effort: str = "medium"  # low, medium, high
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.validation_criteria is None:
            self.validation_criteria = []


class Phase5RefactorBlueprint:
    """Implements Phase 5 refactor blueprint synthesis"""
    
    def __init__(self, output_dir: str = "/home/runner/work/new/new"):
        self.output_dir = Path(output_dir)
        self.anchor_codebase = None
        self.secondary_codebase = None
        
    def load_analysis_data(self) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """Load all previous analysis data"""
        print("Phase 5: Loading analysis data...")
        
        # Load anchor selection
        with open(self.output_dir / "refactor" / "anchor_declaration.json", 'r') as f:
            anchor_data = json.load(f)
        
        self.anchor_codebase = anchor_data['anchor_selection']['selected_codebase']
        self.secondary_codebase = "soldier" if self.anchor_codebase == "s1" else "s1"
        
        print(f"Anchor codebase: {self.anchor_codebase}")
        print(f"Secondary codebase: {self.secondary_codebase}")
        
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
    
    def design_convergence_strategy(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                                  comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """Design the overall convergence strategy"""
        print("Phase 5: Designing convergence strategy...")
        
        anchor_data = s1_data if self.anchor_codebase == "s1" else soldier_data
        secondary_data = soldier_data if self.anchor_codebase == "s1" else s1_data
        
        # Identify convergence phases
        strategy = {
            "convergence_approach": "anchor_based_gradual_integration",
            "phases": [
                {
                    "phase": 1,
                    "name": "interface_alignment",
                    "description": "Align function signatures and interfaces",
                    "estimated_duration": "2-3 weeks"
                },
                {
                    "phase": 2,
                    "name": "dependency_harmonization",
                    "description": "Unify import patterns and dependencies",
                    "estimated_duration": "1-2 weeks"
                },
                {
                    "phase": 3,
                    "name": "functionality_integration",
                    "description": "Integrate unique functionality from secondary codebase",
                    "estimated_duration": "3-4 weeks"
                },
                {
                    "phase": 4,
                    "name": "optimization_consolidation",
                    "description": "Optimize and consolidate merged functionality",
                    "estimated_duration": "2-3 weeks"
                },
                {
                    "phase": 5,
                    "name": "validation_cleanup",
                    "description": "Final validation and cleanup",
                    "estimated_duration": "1-2 weeks"
                }
            ],
            "total_estimated_duration": "9-14 weeks",
            "risk_mitigation_approach": "atomic_commits_with_rollback_points"
        }
        
        return strategy
    
    def generate_atomic_refactor_steps(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                                     comparison_data: Dict[str, Any], risk_data: Dict[str, Any]) -> List[RefactorStep]:
        """Generate atomic refactor steps"""
        print("Phase 5: Generating atomic refactor steps...")
        
        refactor_steps = []
        step_counter = 1
        
        anchor_data = s1_data if self.anchor_codebase == "s1" else soldier_data
        secondary_data = soldier_data if self.anchor_codebase == "s1" else s1_data
        
        # Phase 1: Interface Alignment Steps
        refactor_steps.extend(self._generate_interface_alignment_steps(
            anchor_data, secondary_data, comparison_data, step_counter))
        step_counter += len(refactor_steps)
        
        # Phase 2: Dependency Harmonization Steps
        harmony_steps = self._generate_dependency_harmony_steps(
            anchor_data, secondary_data, step_counter)
        refactor_steps.extend(harmony_steps)
        step_counter += len(harmony_steps)
        
        # Phase 3: Functionality Integration Steps
        integration_steps = self._generate_functionality_integration_steps(
            anchor_data, secondary_data, comparison_data, step_counter)
        refactor_steps.extend(integration_steps)
        step_counter += len(integration_steps)
        
        # Phase 4: Optimization Steps
        optimization_steps = self._generate_optimization_steps(
            anchor_data, secondary_data, risk_data, step_counter)
        refactor_steps.extend(optimization_steps)
        step_counter += len(optimization_steps)
        
        # Phase 5: Validation Steps
        validation_steps = self._generate_validation_steps(step_counter)
        refactor_steps.extend(validation_steps)
        
        print(f"Generated {len(refactor_steps)} atomic refactor steps")
        return refactor_steps
    
    def _generate_interface_alignment_steps(self, anchor_data: Dict[str, Any], 
                                          secondary_data: Dict[str, Any],
                                          comparison_data: Dict[str, Any], 
                                          start_counter: int) -> List[RefactorStep]:
        """Generate interface alignment steps"""
        steps = []
        counter = start_counter
        
        for pair_id, comparison in comparison_data.items():
            anchor_module = comparison['modules'][self.anchor_codebase]
            secondary_module = comparison['modules'][self.secondary_codebase]
            
            # Check for signature incompatibilities
            interface_compat = comparison['interface_compatibility']
            
            for sig in interface_compat.get('signature_compatibility', []):
                if not sig['parameter_count_match'] or not sig['return_type_match']:
                    steps.append(RefactorStep(
                        step_id=f"STEP_{counter:03d}",
                        step_type="adapt",
                        source_codebase=self.secondary_codebase,
                        target_module=anchor_module,
                        source_module=secondary_module,
                        description=f"Align function signature for {sig['function']}",
                        behavioral_rationale=f"Parameter count mismatch ({sig['s1_params']} vs {sig['soldier_params']}) requires adaptation",
                        risk_level="medium",
                        rollback_procedure=f"Revert {anchor_module} to previous version",
                        validation_criteria=[
                            f"Function {sig['function']} accepts correct parameter count",
                            "All existing tests continue to pass",
                            "No breaking changes to public API"
                        ],
                        estimated_effort="medium"
                    ))
                    counter += 1
            
            # Handle unique functions in secondary codebase
            divergence = comparison['functional_divergence']
            for func_name in divergence['soldier_unique_functions'][:3]:  # Limit to top 3
                steps.append(RefactorStep(
                    step_id=f"STEP_{counter:03d}",
                    step_type="add",
                    source_codebase=self.secondary_codebase,
                    target_module=anchor_module,
                    source_module=secondary_module,
                    description=f"Add unique function {func_name} to anchor codebase",
                    behavioral_rationale=f"Function {func_name} provides functionality not present in anchor",
                    risk_level="high",
                    dependencies=[f"STEP_{counter-1:03d}"] if counter > start_counter else [],
                    rollback_procedure=f"Remove added function {func_name} from {anchor_module}",
                    validation_criteria=[
                        f"Function {func_name} integrates without conflicts",
                        "All dependencies are properly imported",
                        "Function passes integration tests"
                    ],
                    estimated_effort="high"
                ))
                counter += 1
        
        return steps
    
    def _generate_dependency_harmony_steps(self, anchor_data: Dict[str, Any],
                                         secondary_data: Dict[str, Any],
                                         start_counter: int) -> List[RefactorStep]:
        """Generate dependency harmonization steps"""
        steps = []
        counter = start_counter
        
        # Collect all imports from both codebases
        anchor_imports = set()
        secondary_imports = set()
        
        for behavior in anchor_data.values():
            anchor_imports.update(behavior['imports'])
        
        for behavior in secondary_data.values():
            secondary_imports.update(behavior['imports'])
        
        # Find conflicting imports
        conflicting_imports = []
        for anchor_imp in anchor_imports:
            for secondary_imp in secondary_imports:
                if (anchor_imp.split('.')[0] == secondary_imp.split('.')[0] and 
                    anchor_imp != secondary_imp):
                    conflicting_imports.append((anchor_imp, secondary_imp))
        
        # Create harmonization steps for conflicts
        for anchor_imp, secondary_imp in conflicting_imports[:5]:  # Limit to 5
            steps.append(RefactorStep(
                step_id=f"STEP_{counter:03d}",
                step_type="modify",
                source_codebase="both",
                target_module="all_affected_modules",
                description=f"Harmonize import conflict: {anchor_imp} vs {secondary_imp}",
                behavioral_rationale=f"Import version conflict may cause runtime errors",
                risk_level="high",
                rollback_procedure="Revert to original import statements",
                validation_criteria=[
                    "All modules import successfully",
                    "No version conflicts detected",
                    "All functionality remains operational"
                ],
                estimated_effort="high"
            ))
            counter += 1
        
        # Add unique imports from secondary codebase
        unique_secondary_imports = secondary_imports - anchor_imports
        for imp in list(unique_secondary_imports)[:10]:  # Limit to 10
            steps.append(RefactorStep(
                step_id=f"STEP_{counter:03d}",
                step_type="add",
                source_codebase=self.secondary_codebase,
                target_module="dependency_requirements",
                description=f"Add required import: {imp}",
                behavioral_rationale=f"Import {imp} required for secondary codebase functionality",
                risk_level="medium",
                rollback_procedure=f"Remove import {imp} from requirements",
                validation_criteria=[
                    f"Import {imp} available and functional",
                    "No conflicts with existing dependencies"
                ],
                estimated_effort="low"
            ))
            counter += 1
        
        return steps
    
    def _generate_functionality_integration_steps(self, anchor_data: Dict[str, Any],
                                                secondary_data: Dict[str, Any],
                                                comparison_data: Dict[str, Any],
                                                start_counter: int) -> List[RefactorStep]:
        """Generate functionality integration steps"""
        steps = []
        counter = start_counter
        
        # Identify modules unique to secondary codebase
        anchor_modules = set(anchor_data.keys())
        secondary_modules = set(secondary_data.keys())
        unique_secondary_modules = secondary_modules - anchor_modules
        
        # Create integration steps for unique modules
        for module in unique_secondary_modules:
            module_behavior = secondary_data[module]
            
            steps.append(RefactorStep(
                step_id=f"STEP_{counter:03d}",
                step_type="merge",
                source_codebase=self.secondary_codebase,
                target_module=f"integrated_{module}",
                source_module=module,
                description=f"Integrate unique module {module}",
                behavioral_rationale=f"Module {module} provides {len(module_behavior['functions'])} unique functions",
                risk_level="high",
                dependencies=[f"STEP_{counter-1:03d}"] if counter > start_counter else [],
                rollback_procedure=f"Remove integrated module {module}",
                validation_criteria=[
                    f"Module {module} integrates without naming conflicts",
                    "All module functions are accessible",
                    "Module passes integration tests",
                    "No circular dependencies created"
                ],
                estimated_effort="high"
            ))
            counter += 1
            
            # Create adapter steps for complex integrations
            if len(module_behavior['functions']) > 10:
                steps.append(RefactorStep(
                    step_id=f"STEP_{counter:03d}",
                    step_type="add",
                    source_codebase="new",
                    target_module=f"adapters/{module}_adapter",
                    description=f"Create adapter for complex module {module}",
                    behavioral_rationale=f"Large module ({len(module_behavior['functions'])} functions) requires adapter pattern",
                    risk_level="medium",
                    dependencies=[f"STEP_{counter-1:03d}"],
                    rollback_procedure=f"Remove adapter module",
                    validation_criteria=[
                        "Adapter correctly delegates to integrated module",
                        "Adapter maintains interface compatibility",
                        "Adapter handles error conditions properly"
                    ],
                    estimated_effort="medium"
                ))
                counter += 1
        
        return steps
    
    def _generate_optimization_steps(self, anchor_data: Dict[str, Any],
                                   secondary_data: Dict[str, Any],
                                   risk_data: Dict[str, Any],
                                   start_counter: int) -> List[RefactorStep]:
        """Generate optimization and consolidation steps"""
        steps = []
        counter = start_counter
        
        # Address high-risk areas identified in risk analysis
        high_risks = risk_data.get('high_risks', [])
        
        # Group risks by module
        risk_by_module = {}
        for risk in high_risks[:10]:  # Limit to top 10 risks
            module = risk['module']
            if module not in risk_by_module:
                risk_by_module[module] = []
            risk_by_module[module].append(risk)
        
        # Create optimization steps for high-risk modules
        for module, risks in risk_by_module.items():
            if len(risks) >= 3:  # Focus on modules with multiple risks
                steps.append(RefactorStep(
                    step_id=f"STEP_{counter:03d}",
                    step_type="modify",
                    source_codebase=self.anchor_codebase,
                    target_module=module,
                    description=f"Optimize high-risk module {module}",
                    behavioral_rationale=f"Module has {len(risks)} high risks requiring optimization",
                    risk_level="medium",
                    rollback_procedure=f"Revert {module} to pre-optimization state",
                    validation_criteria=[
                        f"Risk count for {module} reduced by at least 50%",
                        "Module functionality remains intact",
                        "Performance impact is minimal"
                    ],
                    estimated_effort="high"
                ))
                counter += 1
        
        # Consolidate duplicate functionality
        steps.append(RefactorStep(
            step_id=f"STEP_{counter:03d}",
            step_type="modify",
            source_codebase="both",
            target_module="all_modules",
            description="Consolidate duplicate functionality across modules",
            behavioral_rationale="Remove redundant code patterns identified during convergence",
            risk_level="medium",
            rollback_procedure="Restore original module implementations",
            validation_criteria=[
                "No duplicate function implementations remain",
                "All functionality accessible through unified interfaces",
                "Code coverage maintained or improved"
            ],
            estimated_effort="high"
        ))
        counter += 1
        
        return steps
    
    def _generate_validation_steps(self, start_counter: int) -> List[RefactorStep]:
        """Generate final validation steps"""
        steps = []
        counter = start_counter
        
        # Comprehensive testing
        steps.append(RefactorStep(
            step_id=f"STEP_{counter:03d}",
            step_type="add",
            source_codebase="new",
            target_module="tests/integration",
            description="Create comprehensive integration test suite",
            behavioral_rationale="Ensure convergence maintains all original functionality",
            risk_level="low",
            rollback_procedure="Remove test suite",
            validation_criteria=[
                "All original functionality tests pass",
                "New integration points tested",
                "Performance benchmarks met",
                "No regression in error handling"
            ],
            estimated_effort="medium"
        ))
        counter += 1
        
        # Documentation update
        steps.append(RefactorStep(
            step_id=f"STEP_{counter:03d}",
            step_type="add",
            source_codebase="new",
            target_module="docs/convergence",
            description="Update documentation for converged codebase",
            behavioral_rationale="Document new architecture and integration points",
            risk_level="low",
            rollback_procedure="Restore original documentation",
            validation_criteria=[
                "All new functionality documented",
                "Architecture changes explained",
                "Migration guide available"
            ],
            estimated_effort="medium"
        ))
        counter += 1
        
        # Performance validation
        steps.append(RefactorStep(
            step_id=f"STEP_{counter:03d}",
            step_type="add",
            source_codebase="new", 
            target_module="benchmarks/performance",
            description="Validate performance characteristics of converged codebase",
            behavioral_rationale="Ensure convergence doesn't degrade performance",
            risk_level="medium",
            rollback_procedure="Document performance regressions",
            validation_criteria=[
                "Performance within 10% of original codebases",
                "No memory leaks introduced",
                "Response times meet requirements"
            ],
            estimated_effort="medium"
        ))
        counter += 1
        
        return steps
    
    def generate_refactor_plan(self, convergence_strategy: Dict[str, Any], 
                             refactor_steps: List[RefactorStep]) -> None:
        """Generate complete refactor plan YAML"""
        print("Phase 5: Generating refactor plan...")
        
        # Group steps by phase
        phases = {
            1: {"name": "Interface Alignment", "steps": []},
            2: {"name": "Dependency Harmonization", "steps": []},
            3: {"name": "Functionality Integration", "steps": []},
            4: {"name": "Optimization Consolidation", "steps": []},
            5: {"name": "Validation Cleanup", "steps": []}
        }
        
        # Assign steps to phases based on type and dependencies
        for step in refactor_steps:
            step_num = int(step.step_id.split('_')[1])
            
            if step_num <= 10:
                phases[1]["steps"].append(step)
            elif step_num <= 20:
                phases[2]["steps"].append(step)
            elif step_num <= 35:
                phases[3]["steps"].append(step)
            elif step_num <= 45:
                phases[4]["steps"].append(step)
            else:
                phases[5]["steps"].append(step)
        
        # Create YAML structure
        plan = {
            "refactor_plan": {
                "metadata": {
                    "version": "1.0",
                    "created": "2025-07-31T13:00:00Z",
                    "anchor_codebase": self.anchor_codebase,
                    "secondary_codebase": self.secondary_codebase,
                    "total_steps": len(refactor_steps),
                    "estimated_duration": convergence_strategy["total_estimated_duration"]
                },
                "strategy": convergence_strategy,
                "phases": {}
            }
        }
        
        # Add phases with steps
        for phase_num, phase_data in phases.items():
            plan["refactor_plan"]["phases"][f"phase_{phase_num}"] = {
                "name": phase_data["name"],
                "description": convergence_strategy["phases"][phase_num-1]["description"],
                "estimated_duration": convergence_strategy["phases"][phase_num-1]["estimated_duration"],
                "steps": []
            }
            
            for step in phase_data["steps"]:
                step_dict = asdict(step)
                plan["refactor_plan"]["phases"][f"phase_{phase_num}"]["steps"].append(step_dict)
        
        # Save YAML plan
        plan_file = self.output_dir / "refactor" / "refactor_plan.yaml"
        with open(plan_file, 'w') as f:
            yaml.dump(plan, f, default_flow_style=False, sort_keys=False, indent=2)
        
        print(f"Refactor plan saved: {plan_file}")
    
    def generate_patchset_diffs(self, refactor_steps: List[RefactorStep]) -> None:
        """Generate specific code changes per commit"""
        print("Phase 5: Generating patchset diffs...")
        
        patchset_dir = self.output_dir / "refactor" / "patchset_diffs"
        patchset_dir.mkdir(exist_ok=True)
        
        # Generate sample diffs for key steps
        for step in refactor_steps[:10]:  # Generate for first 10 steps
            diff_content = f"""# Patch for {step.step_id}: {step.description}
# Step type: {step.step_type}
# Risk level: {step.risk_level}
# Behavioral rationale: {step.behavioral_rationale}
# Target module: {step.target_module}
# Source codebase: {step.source_codebase}

# This patch represents {step.step_type} operation:
# - Description: {step.description}
# - Risk Level: {step.risk_level}
# - Estimated Effort: {step.estimated_effort}

# Validation Criteria:
{chr(10).join(f'# - {criterion}' for criterion in step.validation_criteria)}

# Rollback Procedure:
# {step.rollback_procedure}

# Dependencies: {', '.join(step.dependencies) if step.dependencies else 'None'}
"""
            
            diff_file = patchset_dir / f"{step.step_id}.patch"
            with open(diff_file, 'w') as f:
                f.write(diff_content)
        
        print(f"Generated {min(10, len(refactor_steps))} patchset diffs in {patchset_dir}")
    
    def generate_test_requirements(self, refactor_steps: List[RefactorStep]) -> None:
        """Generate validation harness specifications"""
        print("Phase 5: Generating test requirements...")
        
        test_file = self.output_dir / "refactor" / "test_requirements.md"
        
        with open(test_file, 'w') as f:
            f.write("# Validation Harness Specifications\n\n")
            f.write("## Overview\n\n")
            f.write("This document specifies the testing requirements for the codebase convergence process.\n")
            f.write("Each refactor step must pass validation before proceeding to the next step.\n\n")
            
            f.write("## Global Test Requirements\n\n")
            f.write("### Pre-requisites\n")
            f.write("- All existing tests must pass before starting convergence\n")
            f.write("- Test coverage baseline established\n")
            f.write("- Performance baseline established\n")
            f.write("- Integration test environment available\n\n")
            
            f.write("### Continuous Validation\n")
            f.write("- Unit tests run after each step\n")
            f.write("- Integration tests run after each phase\n")
            f.write("- Performance tests run after major integrations\n")
            f.write("- Code coverage maintained or improved\n\n")
            
            f.write("## Step-by-Step Validation Criteria\n\n")
            
            current_phase = 0
            for step in refactor_steps:
                step_num = int(step.step_id.split('_')[1])
                
                # Determine phase
                if step_num <= 10 and current_phase != 1:
                    current_phase = 1
                    f.write(f"### Phase {current_phase}: Interface Alignment\n\n")
                elif step_num <= 20 and current_phase != 2:
                    current_phase = 2
                    f.write(f"### Phase {current_phase}: Dependency Harmonization\n\n")
                elif step_num <= 35 and current_phase != 3:
                    current_phase = 3
                    f.write(f"### Phase {current_phase}: Functionality Integration\n\n")
                elif step_num <= 45 and current_phase != 4:
                    current_phase = 4
                    f.write(f"### Phase {current_phase}: Optimization Consolidation\n\n")
                elif current_phase != 5:
                    current_phase = 5
                    f.write(f"### Phase {current_phase}: Validation Cleanup\n\n")
                
                f.write(f"#### {step.step_id}: {step.description}\n\n")
                f.write(f"**Risk Level**: {step.risk_level.upper()}\n\n")
                f.write("**Validation Criteria**:\n")
                for criterion in step.validation_criteria:
                    f.write(f"- {criterion}\n")
                f.write("\n")
                
                if step.risk_level in ['high', 'critical']:
                    f.write("**Additional High-Risk Validation**:\n")
                    f.write("- Manual code review required\n")
                    f.write("- Extended integration testing\n")
                    f.write("- Performance impact assessment\n")
                    f.write("- Rollback procedure verification\n\n")
            
            f.write("## Test Automation Framework\n\n")
            f.write("### Required Test Types\n\n")
            f.write("1. **Unit Tests**\n")
            f.write("   - Function-level testing\n")
            f.write("   - Mock external dependencies\n")
            f.write("   - Edge case coverage\n\n")
            
            f.write("2. **Integration Tests**\n")
            f.write("   - Module interaction testing\n")
            f.write("   - End-to-end workflow testing\n")
            f.write("   - Cross-module dependency testing\n\n")
            
            f.write("3. **Performance Tests**\n")
            f.write("   - Response time validation\n")
            f.write("   - Memory usage monitoring\n")
            f.write("   - Concurrent execution testing\n\n")
            
            f.write("4. **Regression Tests**\n")
            f.write("   - Existing functionality preservation\n")
            f.write("   - API compatibility verification\n")
            f.write("   - Error handling consistency\n\n")
            
            f.write("### Test Execution Pipeline\n\n")
            f.write("```yaml\n")
            f.write("test_pipeline:\n")
            f.write("  pre_step:\n")
            f.write("    - run: unit_tests\n")
            f.write("    - run: lint_check\n")
            f.write("    - run: type_check\n")
            f.write("  post_step:\n")
            f.write("    - run: unit_tests\n")
            f.write("    - run: integration_tests\n")
            f.write("    - run: performance_check\n")
            f.write("  post_phase:\n")
            f.write("    - run: full_regression_suite\n")
            f.write("    - run: performance_benchmark\n")
            f.write("    - run: security_scan\n")
            f.write("```\n\n")
        
        print(f"Test requirements saved: {test_file}")
    
    def generate_rollback_procedures(self, refactor_steps: List[RefactorStep]) -> None:
        """Generate rollback triggers and procedures"""
        print("Phase 5: Generating rollback procedures...")
        
        rollback_file = self.output_dir / "refactor" / "rollback_triggers.md"
        
        with open(rollback_file, 'w') as f:
            f.write("# Rollback Triggers and Procedures\n\n")
            f.write("## Overview\n\n")
            f.write("This document defines the conditions that trigger rollbacks and the procedures ")
            f.write("for safely reverting changes during the codebase convergence process.\n\n")
            
            f.write("## Global Rollback Triggers\n\n")
            f.write("### Automatic Rollback Conditions\n")
            f.write("- Any test failure that cannot be resolved within 2 hours\n")
            f.write("- Performance degradation >20% from baseline\n")
            f.write("- Critical security vulnerabilities introduced\n")
            f.write("- Memory leaks or resource exhaustion detected\n")
            f.write("- Data corruption or loss detected\n\n")
            
            f.write("### Manual Rollback Triggers\n")
            f.write("- Stakeholder concerns about functionality changes\n")
            f.write("- Discovery of unacceptable business logic changes\n")
            f.write("- Timeline constraints requiring scope reduction\n")
            f.write("- External dependency failures\n\n")
            
            f.write("## Step-by-Step Rollback Procedures\n\n")
            
            current_phase = 0
            for step in refactor_steps:
                step_num = int(step.step_id.split('_')[1])
                
                # Phase headers
                if step_num <= 10 and current_phase != 1:
                    current_phase = 1
                    f.write(f"### Phase {current_phase}: Interface Alignment Rollbacks\n\n")
                elif step_num <= 20 and current_phase != 2:
                    current_phase = 2
                    f.write(f"### Phase {current_phase}: Dependency Harmonization Rollbacks\n\n")
                elif step_num <= 35 and current_phase != 3:
                    current_phase = 3
                    f.write(f"### Phase {current_phase}: Functionality Integration Rollbacks\n\n")
                elif step_num <= 45 and current_phase != 4:
                    current_phase = 4
                    f.write(f"### Phase {current_phase}: Optimization Consolidation Rollbacks\n\n")
                elif current_phase != 5:
                    current_phase = 5
                    f.write(f"### Phase {current_phase}: Validation Cleanup Rollbacks\n\n")
                
                f.write(f"#### {step.step_id}: {step.description}\n\n")
                f.write(f"**Rollback Procedure**: {step.rollback_procedure}\n\n")
                
                # Add detailed rollback steps for high-risk changes
                if step.risk_level in ['high', 'critical']:
                    f.write("**Detailed Rollback Steps**:\n")
                    f.write("1. Stop all dependent processes\n")
                    f.write(f"2. {step.rollback_procedure}\n")
                    f.write("3. Verify rollback completeness\n")
                    f.write("4. Run regression tests\n")
                    f.write("5. Notify stakeholders of rollback\n")
                    f.write("6. Document rollback reason and learnings\n\n")
                
                f.write(f"**Dependencies**: {', '.join(step.dependencies) if step.dependencies else 'None'}\n")
                f.write(f"**Risk Level**: {step.risk_level.upper()}\n\n")
                
            f.write("## Recovery Procedures\n\n")
            f.write("### After Rollback\n")
            f.write("1. **Root Cause Analysis**\n")
            f.write("   - Identify why the step failed\n")
            f.write("   - Document failure mode\n")
            f.write("   - Update risk assessment\n\n")
            
            f.write("2. **Plan Adjustment**\n")
            f.write("   - Modify approach if needed\n")
            f.write("   - Add additional validation steps\n")
            f.write("   - Update risk mitigation strategies\n\n")
            
            f.write("3. **Retry Decision**\n")
            f.write("   - Assess if retry is advisable\n")
            f.write("   - Consider alternative approaches\n")
            f.write("   - Get stakeholder approval for retry\n\n")
            
            f.write("### Emergency Procedures\n")
            f.write("**Complete Rollback to Pre-Convergence State**:\n")
            f.write("1. Stop all convergence processes\n")
            f.write(f"2. Restore {self.anchor_codebase} codebase to original state\n")
            f.write("3. Verify all original functionality works\n")
            f.write("4. Run full regression test suite\n")
            f.write("5. Notify all stakeholders\n")
            f.write("6. Conduct post-mortem analysis\n\n")
        
        print(f"Rollback procedures saved: {rollback_file}")
    
    def generate_unresolved_risks(self, risk_data: Dict[str, Any], refactor_steps: List[RefactorStep]) -> None:
        """Document unresolved risks and technical debt"""
        print("Phase 5: Generating unresolved risks documentation...")
        
        # Identify risks not addressed by refactor steps
        addressed_modules = set()
        for step in refactor_steps:
            if step.target_module != "all_modules":
                addressed_modules.add(step.target_module)
        
        unresolved_risks = {
            "metadata": {
                "created": "2025-07-31T13:00:00Z",
                "total_risks": risk_data['risk_summary']['total_risks'],
                "addressed_in_refactor": len([s for s in refactor_steps if s.step_type in ['modify', 'adapt']]),
                "unresolved_count": 0
            },
            "unresolved_risks": {
                "critical": [],
                "high": [],
                "medium": []
            },
            "technical_debt": [],
            "monitoring_requirements": [],
            "future_work": []
        }
        
        # Categorize unresolved risks
        for risk in risk_data.get('critical_risks', []):
            if risk['module'] not in addressed_modules:
                unresolved_risks['unresolved_risks']['critical'].append(risk)
        
        for risk in risk_data.get('high_risks', []):
            if risk['module'] not in addressed_modules:
                unresolved_risks['unresolved_risks']['high'].append(risk)
        
        for risk in risk_data.get('medium_risks', [])[:20]:  # Limit medium risks
            if risk['module'] not in addressed_modules:
                unresolved_risks['unresolved_risks']['medium'].append(risk)
        
        # Calculate unresolved count
        unresolved_risks['metadata']['unresolved_count'] = (
            len(unresolved_risks['unresolved_risks']['critical']) +
            len(unresolved_risks['unresolved_risks']['high']) +
            len(unresolved_risks['unresolved_risks']['medium'])
        )
        
        # Add technical debt items
        unresolved_risks['technical_debt'] = [
            {
                "area": "Performance Optimization",
                "description": "Comprehensive performance tuning not included in convergence scope",
                "impact": "Potential performance degradation in high-load scenarios",
                "recommendation": "Conduct dedicated performance optimization phase post-convergence"
            },
            {
                "area": "Security Hardening",
                "description": "Security review not included in behavioral analysis",
                "impact": "Security vulnerabilities may persist from both codebases",
                "recommendation": "Conduct security audit and penetration testing"
            },
            {
                "area": "Documentation Completeness",
                "description": "Comprehensive documentation update beyond convergence scope",
                "impact": "Knowledge gaps may hinder maintenance",
                "recommendation": "Dedicated documentation sprint post-convergence"
            }
        ]
        
        # Add monitoring requirements
        unresolved_risks['monitoring_requirements'] = [
            "Performance metrics monitoring for converged functionality",
            "Error rate monitoring for integrated components",
            "Resource utilization monitoring for memory and CPU usage",
            "Dependency health monitoring for external services",
            "User experience monitoring for interface changes"
        ]
        
        # Add future work items
        unresolved_risks['future_work'] = [
            "Microservices decomposition analysis",
            "API versioning strategy implementation",
            "Automated testing framework enhancement",
            "Monitoring and observability platform integration",
            "Performance optimization and caching strategy"
        ]
        
        # Save unresolved risks
        with open(self.output_dir / "refactor" / "unresolved_risks.json", 'w') as f:
            json.dump(unresolved_risks, f, indent=2)
        
        print(f"Unresolved risks saved: {self.output_dir / 'refactor' / 'unresolved_risks.json'}")
    
    def run_phase5(self) -> Dict[str, Any]:
        """Execute complete Phase 5 refactor blueprint synthesis"""
        print("Starting Phase 5 - Refactor Blueprint Synthesis")
        print("=" * 60)
        
        try:
            # Step 1: Load analysis data
            s1_data, soldier_data, comparison_data, risk_data = self.load_analysis_data()
            
            # Step 2: Design convergence strategy
            convergence_strategy = self.design_convergence_strategy(s1_data, soldier_data, comparison_data)
            
            # Step 3: Generate atomic refactor steps
            refactor_steps = self.generate_atomic_refactor_steps(s1_data, soldier_data, comparison_data, risk_data)
            
            # Step 4: Generate refactor plan
            self.generate_refactor_plan(convergence_strategy, refactor_steps)
            
            # Step 5: Generate patchset diffs
            self.generate_patchset_diffs(refactor_steps)
            
            # Step 6: Generate test requirements
            self.generate_test_requirements(refactor_steps)
            
            # Step 7: Generate rollback procedures
            self.generate_rollback_procedures(refactor_steps)
            
            # Step 8: Generate unresolved risks
            self.generate_unresolved_risks(risk_data, refactor_steps)
            
            print(f"\nPhase 5 Refactor Blueprint Synthesis Complete!")
            print(f"Anchor Codebase: {self.anchor_codebase.upper()}")
            print(f"Total Refactor Steps: {len(refactor_steps)}")
            print(f"Estimated Duration: {convergence_strategy['total_estimated_duration']}")
            print("=" * 60)
            
            return {
                "anchor_codebase": self.anchor_codebase,
                "total_steps": len(refactor_steps),
                "strategy": convergence_strategy,
                "steps": refactor_steps
            }
            
        except Exception as e:
            print(f"Error in Phase 5 analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    try:
        phase5 = Phase5RefactorBlueprint()
        result = phase5.run_phase5()
        
        print(f"Refactor blueprint synthesis completed successfully!")
        print(f"Ready for convergence execution with {result['total_steps']} steps")
        
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.exit(1)