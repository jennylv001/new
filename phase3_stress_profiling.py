#!/usr/bin/env python3
"""
PHASE 3 - STRESS PROFILING: Edge Case and Failure Analysis

This script implements Phase 3 of the codebase convergence analysis.
It analyzes edge cases, failure scenarios, and risk propagation.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
import pandas as pd


class Phase3StressProfiling:
    """Implements Phase 3 stress profiling and failure analysis"""
    
    def __init__(self, output_dir: str = "/home/runner/work/new/new"):
        self.output_dir = Path(output_dir)
        
    def load_behavioral_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Load behavioral data from Phase 1"""
        s1_file = self.output_dir / "analysis" / "module_behavior_s1.json"
        soldier_file = self.output_dir / "analysis" / "module_behavior_soldier.json"
        
        with open(s1_file, 'r') as f:
            s1_data = json.load(f)
        
        with open(soldier_file, 'r') as f:
            soldier_data = json.load(f)
        
        return s1_data, soldier_data
    
    def analyze_edge_cases(self, module_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze potential edge cases for each module"""
        edge_cases = {}
        
        for module_path, behavior in module_data.items():
            module_edge_cases = []
            
            # Analyze functions for edge case potential
            for func in behavior['functions']:
                func_edge_cases = []
                
                # Parameter-based edge cases
                if func['parameters']:
                    for param in func['parameters']:
                        func_edge_cases.extend([
                            {
                                'type': 'null_parameter',
                                'description': f"Function {func['name']} receives None for parameter {param}",
                                'severity': 'medium',
                                'impact': 'function_failure'
                            },
                            {
                                'type': 'wrong_type_parameter',
                                'description': f"Function {func['name']} receives wrong type for parameter {param}",
                                'severity': 'high',
                                'impact': 'type_error'
                            }
                        ])
                
                # Return type edge cases
                if not func['return_type']:
                    func_edge_cases.append({
                        'type': 'untyped_return',
                        'description': f"Function {func['name']} has no return type annotation",
                        'severity': 'medium',
                        'impact': 'type_ambiguity'
                    })
                
                module_edge_cases.extend(func_edge_cases)
            
            # Conditional-based edge cases
            for cond in behavior['conditionals']:
                if 'os.' in cond.get('condition', ''):
                    module_edge_cases.append({
                        'type': 'system_dependency',
                        'description': f"Conditional depends on system state: {cond['condition']}",
                        'severity': 'high',
                        'impact': 'environment_failure'
                    })
                
                if not cond.get('has_else', False):
                    module_edge_cases.append({
                        'type': 'unhandled_condition',
                        'description': f"Conditional at line {cond['line']} lacks else clause",
                        'severity': 'medium',
                        'impact': 'logic_gap'
                    })
            
            # Import-based edge cases
            for imp in behavior['imports']:
                if any(external in imp for external in ['requests', 'urllib', 'http']):
                    module_edge_cases.append({
                        'type': 'network_dependency',
                        'description': f"Module depends on external network: {imp}",
                        'severity': 'critical',
                        'impact': 'service_unavailable'
                    })
                
                if any(optional in imp for optional in ['sqlite', 'mysql', 'postgres']):
                    module_edge_cases.append({
                        'type': 'database_dependency',
                        'description': f"Module depends on database: {imp}",
                        'severity': 'high',
                        'impact': 'data_unavailable'
                    })
            
            edge_cases[module_path] = module_edge_cases
        
        return edge_cases
    
    def analyze_failure_scenarios(self, module_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze expected failure scenarios from code structure"""
        failure_scenarios = {}
        
        for module_path, behavior in module_data.items():
            scenarios = []
            
            # Resource constraint failures
            if behavior['complexity_metrics']['function_count'] > 20:
                scenarios.append({
                    'type': 'high_complexity_overload',
                    'description': f"Module has {behavior['complexity_metrics']['function_count']} functions, may cause cognitive overload",
                    'probability': 'medium',
                    'impact': 'maintenance_difficulty'
                })
            
            # Coupling-based failures
            coupling_factor = behavior['complexity_metrics']['coupling_factor']
            if coupling_factor > 2.0:
                scenarios.append({
                    'type': 'high_coupling_failure',
                    'description': f"Module has high coupling factor {coupling_factor:.2f}, changes may cascade",
                    'probability': 'high',
                    'impact': 'cascading_failures'
                })
            
            # Error handling gaps
            if not behavior['error_flows']:
                scenarios.append({
                    'type': 'no_error_handling',
                    'description': "Module lacks explicit error handling mechanisms",
                    'probability': 'high',
                    'impact': 'uncontrolled_failure'
                })
            
            # State mutation risks
            if len(behavior['state_mutations']) > 10:
                scenarios.append({
                    'type': 'excessive_state_mutation',
                    'description': f"Module has {len(behavior['state_mutations'])} state mutations, may cause race conditions",
                    'probability': 'medium',
                    'impact': 'data_corruption'
                })
            
            # Concurrency risks
            if any('thread' in imp or 'async' in imp for imp in behavior['imports']):
                scenarios.append({
                    'type': 'concurrency_risk',
                    'description': "Module uses concurrency primitives without clear synchronization",
                    'probability': 'high',
                    'impact': 'race_conditions'
                })
            
            failure_scenarios[module_path] = scenarios
        
        return failure_scenarios
    
    def simulate_resource_strain(self, module_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Simulate resource strain scenarios"""
        strain_analysis = {}
        
        for module_path, behavior in module_data.items():
            analysis = {
                'memory_strain': self._analyze_memory_usage(behavior),
                'cpu_strain': self._analyze_cpu_usage(behavior),
                'io_strain': self._analyze_io_usage(behavior),
                'network_strain': self._analyze_network_usage(behavior)
            }
            
            # Overall strain score
            strain_score = sum([
                analysis['memory_strain']['risk_score'],
                analysis['cpu_strain']['risk_score'],
                analysis['io_strain']['risk_score'],
                analysis['network_strain']['risk_score']
            ]) / 4
            
            analysis['overall_strain_score'] = strain_score
            analysis['strain_level'] = self._categorize_strain_level(strain_score)
            
            strain_analysis[module_path] = analysis
        
        return strain_analysis
    
    def _analyze_memory_usage(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential memory usage patterns"""
        risk_factors = []
        risk_score = 0.0
        
        # Large data structure indicators
        if any('pandas' in imp or 'numpy' in imp for imp in behavior['imports']):
            risk_factors.append("Uses data processing libraries")
            risk_score += 0.3
        
        # File operations that may load large files
        if any('open' in mut or 'read' in mut for mut in behavior['state_mutations']):
            risk_factors.append("File operations may load large data")
            risk_score += 0.2
        
        # Class instantiation patterns
        if behavior['complexity_metrics']['class_count'] > 5:
            risk_factors.append("Multiple classes may create object hierarchies")
            risk_score += 0.1
        
        return {
            'risk_factors': risk_factors,
            'risk_score': min(risk_score, 1.0),
            'mitigation_strategies': [
                "Implement memory profiling",
                "Use generators for large datasets",
                "Implement object pooling"
            ]
        }
    
    def _analyze_cpu_usage(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential CPU usage patterns"""
        risk_factors = []
        risk_score = 0.0
        
        # Computational complexity indicators
        complexity = behavior['complexity_metrics']['cyclomatic_complexity']
        if complexity > 10:
            risk_factors.append(f"High cyclomatic complexity: {complexity}")
            risk_score += 0.4
        
        # Loop indicators
        loop_keywords = ['for', 'while', 'iter']
        if any(any(keyword in str(cond) for keyword in loop_keywords) for cond in behavior['conditionals']):
            risk_factors.append("Contains iterative operations")
            risk_score += 0.3
        
        # Recursive function patterns
        if any('recursive' in func.get('docstring', '').lower() if func.get('docstring') else False 
               for func in behavior['functions']):
            risk_factors.append("Contains recursive operations")
            risk_score += 0.2
        
        return {
            'risk_factors': risk_factors,
            'risk_score': min(risk_score, 1.0),
            'mitigation_strategies': [
                "Implement CPU profiling",
                "Use caching for expensive operations",
                "Consider algorithm optimization"
            ]
        }
    
    def _analyze_io_usage(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential I/O usage patterns"""
        risk_factors = []
        risk_score = 0.0
        
        # File I/O operations
        io_imports = [imp for imp in behavior['imports'] if any(io_mod in imp for io_mod in ['os', 'pathlib', 'shutil', 'io'])]
        if io_imports:
            risk_factors.append(f"File I/O operations: {len(io_imports)} imports")
            risk_score += 0.3
        
        # Network I/O operations
        net_imports = [imp for imp in behavior['imports'] if any(net_mod in imp for net_mod in ['requests', 'urllib', 'http'])]
        if net_imports:
            risk_factors.append(f"Network I/O operations: {len(net_imports)} imports")
            risk_score += 0.4
        
        # Database operations
        db_imports = [imp for imp in behavior['imports'] if any(db_mod in imp for db_mod in ['sqlite', 'mysql', 'postgres'])]
        if db_imports:
            risk_factors.append(f"Database I/O operations: {len(db_imports)} imports")
            risk_score += 0.3
        
        return {
            'risk_factors': risk_factors,
            'risk_score': min(risk_score, 1.0),
            'mitigation_strategies': [
                "Implement I/O timeout handling",
                "Use connection pooling",
                "Implement retry mechanisms"
            ]
        }
    
    def _analyze_network_usage(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network usage and failure patterns"""
        risk_factors = []
        risk_score = 0.0
        
        network_imports = [imp for imp in behavior['imports'] 
                          if any(net_mod in imp for net_mod in ['requests', 'urllib', 'http', 'socket'])]
        
        if network_imports:
            risk_factors.append(f"Network dependencies: {', '.join(network_imports)}")
            risk_score += 0.5
            
            # Check for timeout handling
            if not any('timeout' in err for err in behavior['error_flows']):
                risk_factors.append("No explicit timeout handling found")
                risk_score += 0.2
            
            # Check for retry mechanisms
            if not any('retry' in err for err in behavior['error_flows']):
                risk_factors.append("No retry mechanisms found")
                risk_score += 0.2
        
        return {
            'risk_factors': risk_factors,
            'risk_score': min(risk_score, 1.0),
            'mitigation_strategies': [
                "Implement circuit breakers",
                "Add network timeout handling",
                "Implement exponential backoff"
            ]
        }
    
    def _categorize_strain_level(self, strain_score: float) -> str:
        """Categorize strain level based on score"""
        if strain_score >= 0.8:
            return "critical"
        elif strain_score >= 0.6:
            return "high" 
        elif strain_score >= 0.4:
            return "medium"
        elif strain_score >= 0.2:
            return "low"
        else:
            return "minimal"
    
    def analyze_cascading_failures(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential cascading failure patterns"""
        cascading_analysis = {
            's1_cascading_risks': self._identify_cascading_risks(s1_data),
            'soldier_cascading_risks': self._identify_cascading_risks(soldier_data),
            'cross_codebase_risks': self._identify_cross_codebase_risks(s1_data, soldier_data)
        }
        
        return cascading_analysis
    
    def _identify_cascading_risks(self, module_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify cascading failure risks within a codebase"""
        risks = []
        
        # Find highly coupled modules
        high_coupling_modules = []
        for module_path, behavior in module_data.items():
            if behavior['complexity_metrics']['coupling_factor'] > 1.5:
                high_coupling_modules.append(module_path)
        
        if len(high_coupling_modules) > 1:
            risks.append({
                'type': 'coupling_cascade',
                'description': f"High coupling between modules: {', '.join(high_coupling_modules)}",
                'impact': 'Changes in one module may break others',
                'mitigation': 'Reduce coupling through dependency injection'
            })
        
        # Find modules with shared external dependencies
        external_deps = {}
        for module_path, behavior in module_data.items():
            for imp in behavior['imports']:
                if any(ext in imp for ext in ['requests', 'database', 'network']):
                    if imp not in external_deps:
                        external_deps[imp] = []
                    external_deps[imp].append(module_path)
        
        for dep, modules in external_deps.items():
            if len(modules) > 1:
                risks.append({
                    'type': 'shared_dependency_failure',
                    'description': f"Shared external dependency {dep} affects modules: {', '.join(modules)}",
                    'impact': 'External service failure affects multiple modules',
                    'mitigation': 'Implement service mesh and fallback mechanisms'
                })
        
        return risks
    
    def _identify_cross_codebase_risks(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify risks when converging the two codebases"""
        risks = []
        
        # Identify naming conflicts
        s1_functions = set()
        soldier_functions = set()
        
        for behavior in s1_data.values():
            s1_functions.update(f['name'] for f in behavior['functions'])
        
        for behavior in soldier_data.values():
            soldier_functions.update(f['name'] for f in behavior['functions'])
        
        common_names = s1_functions.intersection(soldier_functions)
        if common_names:
            risks.append({
                'type': 'naming_conflicts',
                'description': f"Function name conflicts: {', '.join(list(common_names)[:10])}{'...' if len(common_names) > 10 else ''}",
                'impact': 'Function resolution ambiguity during convergence',
                'mitigation': 'Implement namespace prefixing or function renaming'
            })
        
        # Identify import conflicts
        s1_imports = set()
        soldier_imports = set()
        
        for behavior in s1_data.values():
            s1_imports.update(behavior['imports'])
        
        for behavior in soldier_data.values():
            soldier_imports.update(behavior['imports'])
        
        conflicting_versions = []
        for s1_imp in s1_imports:
            for soldier_imp in soldier_imports:
                if s1_imp.split('.')[0] == soldier_imp.split('.')[0] and s1_imp != soldier_imp:
                    conflicting_versions.append((s1_imp, soldier_imp))
        
        if conflicting_versions:
            risks.append({
                'type': 'import_version_conflicts',
                'description': f"Import version conflicts detected: {len(conflicting_versions)} conflicts",
                'impact': 'Dependency resolution failures during convergence',
                'mitigation': 'Create unified dependency management strategy'
            })
        
        return risks
    
    def classify_risks(self, edge_cases: Dict[str, List[Dict[str, Any]]], 
                      failure_scenarios: Dict[str, List[Dict[str, Any]]],
                      strain_analysis: Dict[str, Dict[str, Any]],
                      cascading_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Classify and prioritize all identified risks"""
        risk_classification = {
            'critical_risks': [],
            'high_risks': [],
            'medium_risks': [],
            'low_risks': [],
            'risk_summary': {
                'total_risks': 0,
                'by_category': {},
                'by_severity': {}
            }
        }
        
        # Process edge cases
        for module, cases in edge_cases.items():
            for case in cases:
                risk_item = {
                    'module': module,
                    'type': case['type'],
                    'description': case['description'],
                    'category': 'edge_case',
                    'severity': case['severity']
                }
                
                if case['severity'] == 'critical':
                    risk_classification['critical_risks'].append(risk_item)
                elif case['severity'] == 'high':
                    risk_classification['high_risks'].append(risk_item)
                elif case['severity'] == 'medium':
                    risk_classification['medium_risks'].append(risk_item)
                else:
                    risk_classification['low_risks'].append(risk_item)
        
        # Process failure scenarios
        for module, scenarios in failure_scenarios.items():
            for scenario in scenarios:
                risk_item = {
                    'module': module,
                    'type': scenario['type'],
                    'description': scenario['description'],
                    'category': 'failure_scenario',
                    'severity': scenario['probability']
                }
                
                if scenario['probability'] == 'high':
                    risk_classification['high_risks'].append(risk_item)
                elif scenario['probability'] == 'medium':
                    risk_classification['medium_risks'].append(risk_item)
                else:
                    risk_classification['low_risks'].append(risk_item)
        
        # Process strain analysis
        for module, analysis in strain_analysis.items():
            if analysis['strain_level'] in ['critical', 'high']:
                risk_item = {
                    'module': module,
                    'type': 'resource_strain',
                    'description': f"High resource strain (score: {analysis['overall_strain_score']:.2f})",
                    'category': 'resource_strain',
                    'severity': analysis['strain_level']
                }
                
                if analysis['strain_level'] == 'critical':
                    risk_classification['critical_risks'].append(risk_item)
                else:
                    risk_classification['high_risks'].append(risk_item)
        
        # Process cascading analysis
        for codebase, risks in cascading_analysis.items():
            if codebase != 'cross_codebase_risks':
                for risk in risks:
                    risk_item = {
                        'module': codebase,
                        'type': risk['type'],
                        'description': risk['description'],
                        'category': 'cascading_failure',
                        'severity': 'high'  # Cascading failures are inherently high risk
                    }
                    risk_classification['high_risks'].append(risk_item)
        
        # Calculate summary statistics
        total_risks = (len(risk_classification['critical_risks']) +
                      len(risk_classification['high_risks']) +
                      len(risk_classification['medium_risks']) +
                      len(risk_classification['low_risks']))
        
        risk_classification['risk_summary']['total_risks'] = total_risks
        risk_classification['risk_summary']['by_severity'] = {
            'critical': len(risk_classification['critical_risks']),
            'high': len(risk_classification['high_risks']),
            'medium': len(risk_classification['medium_risks']),
            'low': len(risk_classification['low_risks'])
        }
        
        # Count by category
        categories = {}
        for risk_list in [risk_classification['critical_risks'], risk_classification['high_risks'],
                         risk_classification['medium_risks'], risk_classification['low_risks']]:
            for risk in risk_list:
                category = risk['category']
                categories[category] = categories.get(category, 0) + 1
        
        risk_classification['risk_summary']['by_category'] = categories
        
        return risk_classification
    
    def generate_stress_profiles(self, edge_cases: Dict[str, List[Dict[str, Any]]],
                               failure_scenarios: Dict[str, List[Dict[str, Any]]],
                               strain_analysis: Dict[str, Dict[str, Any]]) -> None:
        """Generate stress profiles for each module"""
        print("Phase 3: Generating stress profiles...")
        
        profiles_dir = self.output_dir / "analysis" / "stress_profiles"
        profiles_dir.mkdir(exist_ok=True)
        
        # Generate individual module profiles
        all_modules = set(edge_cases.keys()) | set(failure_scenarios.keys()) | set(strain_analysis.keys())
        
        for module in all_modules:
            profile = {
                'module': module,
                'edge_cases': edge_cases.get(module, []),
                'failure_scenarios': failure_scenarios.get(module, []),
                'resource_strain': strain_analysis.get(module, {}),
                'risk_score': self._calculate_module_risk_score(
                    edge_cases.get(module, []),
                    failure_scenarios.get(module, []),
                    strain_analysis.get(module, {})
                )
            }
            
            with open(profiles_dir / f"{module.replace('/', '_')}_profile.json", 'w') as f:
                json.dump(profile, f, indent=2)
        
        print(f"Generated {len(all_modules)} stress profiles in {profiles_dir}")
    
    def _calculate_module_risk_score(self, edge_cases: List[Dict[str, Any]],
                                   failure_scenarios: List[Dict[str, Any]],
                                   strain_analysis: Dict[str, Any]) -> float:
        """Calculate overall risk score for a module"""
        risk_score = 0.0
        
        # Edge case contribution
        severity_weights = {'critical': 1.0, 'high': 0.7, 'medium': 0.4, 'low': 0.1}
        for case in edge_cases:
            risk_score += severity_weights.get(case['severity'], 0.1)
        
        # Failure scenario contribution
        probability_weights = {'high': 0.8, 'medium': 0.5, 'low': 0.2}
        for scenario in failure_scenarios:
            risk_score += probability_weights.get(scenario['probability'], 0.2)
        
        # Resource strain contribution
        if strain_analysis and 'overall_strain_score' in strain_analysis:
            risk_score += strain_analysis['overall_strain_score']
        
        return min(risk_score, 10.0)  # Cap at 10.0
    
    def generate_failure_exposure_maps(self, cascading_analysis: Dict[str, Any]) -> None:
        """Generate failure exposure and risk propagation maps"""
        print("Phase 3: Generating failure exposure maps...")
        
        maps_dir = self.output_dir / "analysis" / "failure_exposure_maps"
        maps_dir.mkdir(exist_ok=True)
        
        # Generate cascading failure map
        with open(maps_dir / "cascading_failure_analysis.json", 'w') as f:
            json.dump(cascading_analysis, f, indent=2)
        
        # Generate risk propagation visualization data
        risk_propagation = {
            'nodes': [],
            'edges': [],
            'risk_levels': {}
        }
        
        # Process S1 cascading risks
        for risk in cascading_analysis.get('s1_cascading_risks', []):
            if risk['type'] == 'coupling_cascade':
                modules = risk['description'].split(': ')[1].split(', ')
                for i, module in enumerate(modules):
                    risk_propagation['nodes'].append({
                        'id': f"s1_{module}",
                        'label': module,
                        'codebase': 's1'
                    })
                    risk_propagation['risk_levels'][f"s1_{module}"] = 'high'
                    
                    # Create edges between coupled modules
                    for j, other_module in enumerate(modules):
                        if i != j:
                            risk_propagation['edges'].append({
                                'source': f"s1_{module}",
                                'target': f"s1_{other_module}",
                                'type': 'coupling'
                            })
        
        # Process Soldier cascading risks
        for risk in cascading_analysis.get('soldier_cascading_risks', []):
            if risk['type'] == 'coupling_cascade':
                modules = risk['description'].split(': ')[1].split(', ')
                for i, module in enumerate(modules):
                    risk_propagation['nodes'].append({
                        'id': f"soldier_{module}",
                        'label': module,
                        'codebase': 'soldier'
                    })
                    risk_propagation['risk_levels'][f"soldier_{module}"] = 'high'
                    
                    # Create edges between coupled modules
                    for j, other_module in enumerate(modules):
                        if i != j:
                            risk_propagation['edges'].append({
                                'source': f"soldier_{module}",
                                'target': f"soldier_{other_module}",
                                'type': 'coupling'
                            })
        
        with open(maps_dir / "risk_propagation_graph.json", 'w') as f:
            json.dump(risk_propagation, f, indent=2)
        
        print(f"Failure exposure maps saved in {maps_dir}")
    
    def save_risk_classification(self, risk_classification: Dict[str, Any]) -> None:
        """Save comprehensive risk classification"""
        print("Phase 3: Saving risk classification...")
        
        with open(self.output_dir / "analysis" / "risk_classification.json", 'w') as f:
            json.dump(risk_classification, f, indent=2)
        
        print(f"Risk classification saved: {self.output_dir / 'analysis' / 'risk_classification.json'}")
    
    def run_phase3(self) -> Dict[str, Any]:
        """Execute complete Phase 3 stress profiling analysis"""
        print("Starting Phase 3 - Stress Profiling")
        print("=" * 50)
        
        try:
            # Step 1: Load behavioral data
            s1_data, soldier_data = self.load_behavioral_data()
            
            # Step 2: Analyze edge cases
            print("Analyzing edge cases...")
            s1_edge_cases = self.analyze_edge_cases(s1_data)
            soldier_edge_cases = self.analyze_edge_cases(soldier_data)
            all_edge_cases = {**s1_edge_cases, **{f"soldier_{k}": v for k, v in soldier_edge_cases.items()}}
            
            # Step 3: Analyze failure scenarios
            print("Analyzing failure scenarios...")
            s1_failures = self.analyze_failure_scenarios(s1_data)
            soldier_failures = self.analyze_failure_scenarios(soldier_data)
            all_failures = {**s1_failures, **{f"soldier_{k}": v for k, v in soldier_failures.items()}}
            
            # Step 4: Simulate resource strain
            print("Simulating resource strain...")
            s1_strain = self.simulate_resource_strain(s1_data)
            soldier_strain = self.simulate_resource_strain(soldier_data)
            all_strain = {**s1_strain, **{f"soldier_{k}": v for k, v in soldier_strain.items()}}
            
            # Step 5: Analyze cascading failures
            print("Analyzing cascading failures...")
            cascading_analysis = self.analyze_cascading_failures(s1_data, soldier_data)
            
            # Step 6: Classify risks
            print("Classifying risks...")
            risk_classification = self.classify_risks(all_edge_cases, all_failures, all_strain, cascading_analysis)
            
            # Step 7: Generate outputs
            self.generate_stress_profiles(all_edge_cases, all_failures, all_strain)
            self.generate_failure_exposure_maps(cascading_analysis)
            self.save_risk_classification(risk_classification)
            
            print(f"\nPhase 3 Stress Profiling Complete!")
            print(f"Total risks identified: {risk_classification['risk_summary']['total_risks']}")
            print(f"Critical: {risk_classification['risk_summary']['by_severity']['critical']}")
            print(f"High: {risk_classification['risk_summary']['by_severity']['high']}")
            print(f"Medium: {risk_classification['risk_summary']['by_severity']['medium']}")
            print(f"Low: {risk_classification['risk_summary']['by_severity']['low']}")
            print("=" * 50)
            
            return risk_classification
            
        except Exception as e:
            print(f"Error in Phase 3 analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    try:
        phase3 = Phase3StressProfiling()
        risk_classification = phase3.run_phase3()
        
        print(f"Stress profiling completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.exit(1)