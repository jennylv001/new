#!/usr/bin/env python3
"""
PHASE 2 - COMPARATIVE ANALYSIS: Module Behavioral Comparison

This script implements Phase 2 of the codebase convergence analysis.
It compares shared or analogous module pairs for behavioral characteristics.
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
import pandas as pd
from analysis_framework import ComparisonEngine, ModuleBehavior


class Phase2Comparison:
    """Implements Phase 2 comparative analysis"""
    
    def __init__(self, output_dir: str = "/home/runner/work/new/new"):
        self.output_dir = Path(output_dir)
        self.comparison_engine = ComparisonEngine()
        
    def load_behavioral_data(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Load behavioral data from Phase 1"""
        s1_file = self.output_dir / "analysis" / "module_behavior_s1.json"
        soldier_file = self.output_dir / "analysis" / "module_behavior_soldier.json"
        
        with open(s1_file, 'r') as f:
            s1_data = json.load(f)
        
        with open(soldier_file, 'r') as f:
            soldier_data = json.load(f)
        
        return s1_data, soldier_data
    
    def identify_analogous_modules(self, s1_data: Dict[str, Any], 
                                 soldier_data: Dict[str, Any]) -> Dict[str, Tuple[str, str]]:
        """Identify analogous module pairs between codebases"""
        print("Phase 2: Identifying analogous modules...")
        
        s1_modules = set(s1_data.keys())
        soldier_modules = set(soldier_data.keys())
        
        # Exact name matches
        common_modules = s1_modules.intersection(soldier_modules)
        analogous_pairs = {module: (module, module) for module in common_modules}
        
        # Find modules with similar function signatures
        remaining_s1 = s1_modules - common_modules
        remaining_soldier = soldier_modules - common_modules
        
        for s1_module in remaining_s1:
            s1_funcs = {f['name'] for f in s1_data[s1_module]['functions']}
            
            best_match = None
            best_similarity = 0.0
            
            for soldier_module in remaining_soldier:
                soldier_funcs = {f['name'] for f in soldier_data[soldier_module]['functions']}
                
                if s1_funcs and soldier_funcs:
                    intersection = len(s1_funcs.intersection(soldier_funcs))
                    union = len(s1_funcs.union(soldier_funcs))
                    similarity = intersection / union if union > 0 else 0.0
                    
                    if similarity > best_similarity and similarity > 0.3:  # Minimum 30% similarity
                        best_similarity = similarity
                        best_match = soldier_module
            
            if best_match:
                analogous_pairs[f"{s1_module}<->{best_match}"] = (s1_module, best_match)
                remaining_soldier.remove(best_match)
        
        print(f"Found {len(analogous_pairs)} analogous module pairs")
        return analogous_pairs
    
    def compare_module_behaviors(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                                analogous_pairs: Dict[str, Tuple[str, str]]) -> Dict[str, Dict[str, Any]]:
        """Compare behavioral characteristics of analogous modules"""
        print("Phase 2: Comparing module behaviors...")
        
        comparisons = {}
        
        for pair_id, (s1_module, soldier_module) in analogous_pairs.items():
            s1_behavior = s1_data[s1_module]
            soldier_behavior = soldier_data[soldier_module]
            
            comparison = {
                'modules': {
                    's1': s1_module,
                    'soldier': soldier_module
                },
                'behavioral_intent_similarity': self._calculate_intent_similarity(s1_behavior, soldier_behavior),
                'execution_logic_similarity': self._calculate_logic_similarity(s1_behavior, soldier_behavior),
                'complexity_comparison': {
                    's1': s1_behavior['complexity_metrics'],
                    'soldier': soldier_behavior['complexity_metrics'],
                    'complexity_ratio': self._calculate_complexity_ratio(
                        s1_behavior['complexity_metrics'],
                        soldier_behavior['complexity_metrics']
                    )
                },
                'efficiency_analysis': {
                    's1': self._analyze_efficiency_metrics(s1_behavior),
                    'soldier': self._analyze_efficiency_metrics(soldier_behavior)
                },
                'side_effect_analysis': {
                    's1': self._identify_side_effects(s1_behavior),
                    'soldier': self._identify_side_effects(soldier_behavior)
                },
                'error_handling_comparison': {
                    's1': {
                        'error_flows': s1_behavior['error_flows'],
                        'error_coverage': len(s1_behavior['error_flows']) > 0
                    },
                    'soldier': {
                        'error_flows': soldier_behavior['error_flows'],
                        'error_coverage': len(soldier_behavior['error_flows']) > 0
                    }
                },
                'interface_compatibility': self._analyze_interface_compatibility(s1_behavior, soldier_behavior),
                'functional_divergence': self._identify_functional_divergence(s1_behavior, soldier_behavior)
            }
            
            comparisons[pair_id] = comparison
        
        return comparisons
    
    def _calculate_intent_similarity(self, s1_behavior: Dict[str, Any], 
                                   soldier_behavior: Dict[str, Any]) -> float:
        """Calculate behavioral intent similarity"""
        s1_funcs = {f['name'] for f in s1_behavior['functions']}
        soldier_funcs = {f['name'] for f in soldier_behavior['functions']}
        
        if not s1_funcs and not soldier_funcs:
            return 1.0
        
        intersection = len(s1_funcs.intersection(soldier_funcs))
        union = len(s1_funcs.union(soldier_funcs))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_logic_similarity(self, s1_behavior: Dict[str, Any], 
                                  soldier_behavior: Dict[str, Any]) -> float:
        """Calculate execution logic similarity"""
        s1_complexity = s1_behavior['complexity_metrics']['cyclomatic_complexity']
        soldier_complexity = soldier_behavior['complexity_metrics']['cyclomatic_complexity']
        
        if s1_complexity == 0 and soldier_complexity == 0:
            return 1.0
        
        max_complexity = max(s1_complexity, soldier_complexity)
        min_complexity = min(s1_complexity, soldier_complexity)
        
        return min_complexity / max_complexity if max_complexity > 0 else 0.0
    
    def _calculate_complexity_ratio(self, s1_metrics: Dict[str, Any], 
                                  soldier_metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculate complexity ratios between modules"""
        ratios = {}
        
        for metric in ['function_count', 'class_count', 'conditional_count', 'import_count']:
            s1_val = s1_metrics.get(metric, 0)
            soldier_val = soldier_metrics.get(metric, 0)
            
            if soldier_val > 0:
                ratios[f"{metric}_ratio"] = s1_val / soldier_val
            else:
                ratios[f"{metric}_ratio"] = float('inf') if s1_val > 0 else 1.0
        
        return ratios
    
    def _analyze_efficiency_metrics(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze efficiency characteristics"""
        imports = behavior['imports']
        
        return {
            'io_heavy': any(io_mod in ' '.join(imports) for io_mod in ['os', 'sys', 'io', 'requests', 'urllib']),
            'computation_heavy': any(comp_mod in ' '.join(imports) for comp_mod in ['numpy', 'pandas', 'scipy']),
            'network_dependent': any(net_mod in ' '.join(imports) for net_mod in ['requests', 'urllib', 'http', 'socket']),
            'file_operations': any(file_mod in ' '.join(imports) for file_mod in ['os', 'pathlib', 'shutil']),
            'coupling_factor': behavior['complexity_metrics']['coupling_factor']
        }
    
    def _identify_side_effects(self, behavior: Dict[str, Any]) -> List[str]:
        """Identify potential side effects"""
        side_effects = []
        imports = ' '.join(behavior['imports'])
        state_mutations = behavior['state_mutations']
        
        if any(io_mod in imports for io_mod in ['os', 'pathlib', 'shutil']):
            side_effects.append('file_system')
        
        if any(net_mod in imports for net_mod in ['requests', 'urllib', 'http']):
            side_effects.append('network')
        
        if any('global' in mut for mut in state_mutations):
            side_effects.append('global_state')
        
        if any('attr_assign' in mut for mut in state_mutations):
            side_effects.append('object_mutation')
        
        return side_effects
    
    def _analyze_interface_compatibility(self, s1_behavior: Dict[str, Any], 
                                       soldier_behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interface compatibility between modules"""
        s1_funcs = {f['name']: f for f in s1_behavior['functions']}
        soldier_funcs = {f['name']: f for f in soldier_behavior['functions']}
        
        common_funcs = set(s1_funcs.keys()).intersection(set(soldier_funcs.keys()))
        
        compatibility = {
            'common_functions': len(common_funcs),
            'total_s1_functions': len(s1_funcs),
            'total_soldier_functions': len(soldier_funcs),
            'interface_overlap': len(common_funcs) / max(len(s1_funcs), len(soldier_funcs)) if max(len(s1_funcs), len(soldier_funcs)) > 0 else 0.0,
            'signature_compatibility': []
        }
        
        for func_name in common_funcs:
            s1_func = s1_funcs[func_name]
            soldier_func = soldier_funcs[func_name]
            
            param_compatibility = len(s1_func['parameters']) == len(soldier_func['parameters'])
            type_compatibility = s1_func['return_type'] == soldier_func['return_type']
            
            compatibility['signature_compatibility'].append({
                'function': func_name,
                'parameter_count_match': param_compatibility,
                'return_type_match': type_compatibility,
                's1_params': len(s1_func['parameters']),
                'soldier_params': len(soldier_func['parameters'])
            })
        
        return compatibility
    
    def _identify_functional_divergence(self, s1_behavior: Dict[str, Any], 
                                      soldier_behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Identify functional divergences between modules"""
        s1_funcs = {f['name'] for f in s1_behavior['functions']}
        soldier_funcs = {f['name'] for f in soldier_behavior['functions']}
        
        s1_unique = s1_funcs - soldier_funcs
        soldier_unique = soldier_funcs - s1_funcs
        
        return {
            's1_unique_functions': list(s1_unique),
            'soldier_unique_functions': list(soldier_unique),
            's1_unique_count': len(s1_unique),
            'soldier_unique_count': len(soldier_unique),
            'divergence_ratio': (len(s1_unique) + len(soldier_unique)) / max(len(s1_funcs), len(soldier_funcs)) if max(len(s1_funcs), len(soldier_funcs)) > 0 else 0.0
        }
    
    def generate_comparison_tables(self, comparisons: Dict[str, Dict[str, Any]]) -> None:
        """Generate comparison tables"""
        print("Phase 2: Generating comparison tables...")
        
        tables_dir = self.output_dir / "comparison" / "comparison_tables"
        tables_dir.mkdir(exist_ok=True)
        
        # Summary comparison table
        summary_data = []
        for pair_id, comparison in comparisons.items():
            summary_data.append({
                'module_pair': pair_id,
                's1_module': comparison['modules']['s1'],
                'soldier_module': comparison['modules']['soldier'],
                'intent_similarity': comparison['behavioral_intent_similarity'],
                'logic_similarity': comparison['execution_logic_similarity'],
                'interface_overlap': comparison['interface_compatibility']['interface_overlap'],
                'divergence_ratio': comparison['functional_divergence']['divergence_ratio'],
                's1_functions': comparison['complexity_comparison']['s1']['function_count'],
                'soldier_functions': comparison['complexity_comparison']['soldier']['function_count'],
                's1_complexity': comparison['complexity_comparison']['s1']['cyclomatic_complexity'],
                'soldier_complexity': comparison['complexity_comparison']['soldier']['cyclomatic_complexity']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(tables_dir / "module_comparison_summary.csv", index=False)
        
        # Detailed comparison data
        with open(tables_dir / "detailed_comparisons.json", 'w') as f:
            json.dump(comparisons, f, indent=2)
        
        print(f"Comparison tables saved in {tables_dir}")
    
    def generate_divergence_reports(self, s1_data: Dict[str, Any], soldier_data: Dict[str, Any],
                                  analogous_pairs: Dict[str, Tuple[str, str]]) -> None:
        """Generate divergence reports for non-alignable functionality"""
        print("Phase 2: Generating divergence reports...")
        
        reports_dir = self.output_dir / "comparison" / "divergence_reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Identify orphaned modules
        s1_modules = set(s1_data.keys())
        soldier_modules = set(soldier_data.keys())
        paired_s1 = {pair[0] for pair in analogous_pairs.values()}
        paired_soldier = {pair[1] for pair in analogous_pairs.values()}
        
        s1_orphans = s1_modules - paired_s1
        soldier_orphans = soldier_modules - paired_soldier
        
        # Generate divergence report
        divergence_report = {
            'analysis_summary': {
                'total_s1_modules': len(s1_modules),
                'total_soldier_modules': len(soldier_modules),
                'paired_modules': len(analogous_pairs),
                's1_orphans': len(s1_orphans),
                'soldier_orphans': len(soldier_orphans)
            },
            's1_orphaned_modules': {},
            'soldier_orphaned_modules': {},
            'auxiliary_functionality': []
        }
        
        # Analyze orphaned S1 modules
        for module in s1_orphans:
            module_data = s1_data[module]
            divergence_report['s1_orphaned_modules'][module] = {
                'functions': [f['name'] for f in module_data['functions']],
                'classes': module_data['classes'],
                'complexity_metrics': module_data['complexity_metrics'],
                'side_effects': self._identify_side_effects(module_data),
                'primary_purpose': self._infer_module_purpose(module_data)
            }
        
        # Analyze orphaned Soldier modules
        for module in soldier_orphans:
            module_data = soldier_data[module]
            divergence_report['soldier_orphaned_modules'][module] = {
                'functions': [f['name'] for f in module_data['functions']],
                'classes': module_data['classes'],
                'complexity_metrics': module_data['complexity_metrics'],
                'side_effects': self._identify_side_effects(module_data),
                'primary_purpose': self._infer_module_purpose(module_data)
            }
        
        # Save divergence report
        with open(reports_dir / "divergence_analysis.json", 'w') as f:
            json.dump(divergence_report, f, indent=2)
        
        # Generate markdown report
        self._generate_divergence_markdown(divergence_report, reports_dir / "divergence_summary.md")
        
        print(f"Divergence reports saved in {reports_dir}")
    
    def _infer_module_purpose(self, module_data: Dict[str, Any]) -> str:
        """Infer the primary purpose of a module from its behavior"""
        imports = ' '.join(module_data['imports'])
        functions = [f['name'] for f in module_data['functions']]
        
        # Categorize based on imports and function names
        if any(web_mod in imports for web_mod in ['requests', 'urllib', 'http']):
            return 'network_communication'
        elif any(db_mod in imports for db_mod in ['sqlite', 'mysql', 'postgres', 'database']):
            return 'database_operations'
        elif any(file_mod in imports for file_mod in ['os', 'pathlib', 'shutil']):
            return 'file_operations'
        elif any(test_mod in imports for test_mod in ['unittest', 'pytest', 'test']):
            return 'testing'
        elif any(cli_func in functions for cli_func in ['main', 'parse_args', 'run']):
            return 'command_line_interface'
        elif any(config_func in functions for config_func in ['load_config', 'save_config', 'parse_config']):
            return 'configuration_management'
        else:
            return 'utility_functions'
    
    def _generate_divergence_markdown(self, divergence_report: Dict[str, Any], output_file: Path) -> None:
        """Generate markdown divergence report"""
        with open(output_file, 'w') as f:
            f.write("# Divergence Analysis Report\n\n")
            
            summary = divergence_report['analysis_summary']
            f.write("## Analysis Summary\n\n")
            f.write(f"- **Total S1 Modules**: {summary['total_s1_modules']}\n")
            f.write(f"- **Total Soldier Modules**: {summary['total_soldier_modules']}\n")
            f.write(f"- **Paired Modules**: {summary['paired_modules']}\n")
            f.write(f"- **S1 Orphaned Modules**: {summary['s1_orphans']}\n")
            f.write(f"- **Soldier Orphaned Modules**: {summary['soldier_orphans']}\n\n")
            
            if summary['s1_orphans'] > 0:
                f.write("## S1 Unique Functionality\n\n")
                for module, data in divergence_report['s1_orphaned_modules'].items():
                    f.write(f"### {module}\n")
                    f.write(f"- **Purpose**: {data['primary_purpose']}\n")
                    f.write(f"- **Functions**: {len(data['functions'])}\n")
                    f.write(f"- **Classes**: {len(data['classes'])}\n")
                    f.write(f"- **Side Effects**: {', '.join(data['side_effects']) if data['side_effects'] else 'None'}\n\n")
            
            if summary['soldier_orphans'] > 0:
                f.write("## Soldier Unique Functionality\n\n")
                for module, data in divergence_report['soldier_orphaned_modules'].items():
                    f.write(f"### {module}\n")
                    f.write(f"- **Purpose**: {data['primary_purpose']}\n")
                    f.write(f"- **Functions**: {len(data['functions'])}\n")
                    f.write(f"- **Classes**: {len(data['classes'])}\n")
                    f.write(f"- **Side Effects**: {', '.join(data['side_effects']) if data['side_effects'] else 'None'}\n\n")
    
    def generate_convergence_map(self, comparisons: Dict[str, Dict[str, Any]]) -> None:
        """Generate functional equivalence mapping"""
        print("Phase 2: Generating convergence map...")
        
        convergence_file = self.output_dir / "comparison" / "convergence_map.md"
        
        with open(convergence_file, 'w') as f:
            f.write("# Functional Equivalence Mapping\n\n")
            f.write("## Module Pairs and Behavioral Analysis\n\n")
            
            for pair_id, comparison in comparisons.items():
                f.write(f"### {pair_id}\n\n")
                f.write(f"**S1 Module**: `{comparison['modules']['s1']}`  \n")
                f.write(f"**Soldier Module**: `{comparison['modules']['soldier']}`  \n\n")
                
                f.write("**Similarity Metrics**:\n")
                f.write(f"- Intent Similarity: {comparison['behavioral_intent_similarity']:.3f}\n")
                f.write(f"- Logic Similarity: {comparison['execution_logic_similarity']:.3f}")
                f.write(f"- Interface Overlap: {comparison['interface_compatibility']['interface_overlap']:.3f}\n")
                f.write(f"- Divergence Ratio: {comparison['functional_divergence']['divergence_ratio']:.3f}\n\n")
                
                f.write("**Complexity Comparison**:\n")
                s1_complex = comparison['complexity_comparison']['s1']
                soldier_complex = comparison['complexity_comparison']['soldier']
                f.write(f"- S1: {s1_complex['function_count']} functions, {s1_complex['cyclomatic_complexity']} complexity\n")
                f.write(f"- Soldier: {soldier_complex['function_count']} functions, {soldier_complex['cyclomatic_complexity']} complexity\n\n")
                
                # Interface compatibility details
                compat = comparison['interface_compatibility']
                if compat['common_functions'] > 0:
                    f.write("**Compatible Functions**:\n")
                    for sig in compat['signature_compatibility']:
                        param_match = "✓" if sig['parameter_count_match'] else "✗"
                        type_match = "✓" if sig['return_type_match'] else "✗"
                        f.write(f"- `{sig['function']}`: Params {param_match} ({sig['s1_params']} vs {sig['soldier_params']}), Return {type_match}\n")
                    f.write("\n")
                
                # Functional divergence
                divergence = comparison['functional_divergence']
                if divergence['s1_unique_functions'] or divergence['soldier_unique_functions']:
                    f.write("**Unique Functions**:\n")
                    if divergence['s1_unique_functions']:
                        f.write(f"- S1 Only: {', '.join(divergence['s1_unique_functions'])}\n")
                    if divergence['soldier_unique_functions']:
                        f.write(f"- Soldier Only: {', '.join(divergence['soldier_unique_functions'])}\n")
                    f.write("\n")
                
                f.write("---\n\n")
        
        print(f"Convergence map saved: {convergence_file}")
    
    def run_phase2(self) -> Dict[str, Dict[str, Any]]:
        """Execute complete Phase 2 analysis"""
        print("Starting Phase 2 - Comparative Analysis")
        print("=" * 50)
        
        try:
            # Step 1: Load behavioral data
            s1_data, soldier_data = self.load_behavioral_data()
            
            # Step 2: Identify analogous modules
            analogous_pairs = self.identify_analogous_modules(s1_data, soldier_data)
            
            # Step 3: Compare module behaviors
            comparisons = self.compare_module_behaviors(s1_data, soldier_data, analogous_pairs)
            
            # Step 4: Generate comparison tables
            self.generate_comparison_tables(comparisons)
            
            # Step 5: Generate divergence reports
            self.generate_divergence_reports(s1_data, soldier_data, analogous_pairs)
            
            # Step 6: Generate convergence map
            self.generate_convergence_map(comparisons)
            
            print("\nPhase 2 Comparative Analysis Complete!")
            print("=" * 50)
            
            return comparisons
            
        except Exception as e:
            print(f"Error in Phase 2 analysis: {e}")
            import traceback
            traceback.print_exc()
            raise


if __name__ == "__main__":
    try:
        phase2 = Phase2Comparison()
        comparisons = phase2.run_phase2()
        
        print(f"Comparative analysis completed: {len(comparisons)} module pairs analyzed")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)