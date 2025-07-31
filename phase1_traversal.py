#!/usr/bin/env python3
"""
PHASE 1 - TRAVERSAL: Comprehensive Codebase Analysis

This script implements the traversal phase of the codebase convergence analysis.
It analyzes both s1 and soldier codebases to extract behavioral characteristics.
"""

import os
import sys
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Tuple
import requests
from analysis_framework import CodeBehaviorAnalyzer, ModuleBehavior, Assumption
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns


class Phase1Traversal:
    """Implements Phase 1 traversal and behavioral analysis"""
    
    def __init__(self, output_dir: str = "/home/runner/work/new/new"):
        self.output_dir = Path(output_dir)
        self.analyzer = CodeBehaviorAnalyzer()
        self.temp_dir = Path("/tmp/codebase_analysis")
        self.temp_dir.mkdir(exist_ok=True)
        
    def download_source_repositories(self) -> None:
        """Download s1 and soldier repositories using GitHub API"""
        print("Phase 1: Downloading source repositories...")
        
        repos = [
            ("jennylv001", "s1"),
            ("jennylv001", "soldier") 
        ]
        
        for owner, repo in repos:
            repo_dir = self.temp_dir / repo
            if repo_dir.exists():
                print(f"Repository {repo} already exists, skipping download")
                continue
                
            print(f"Downloading {owner}/{repo}...")
            self._download_github_repo(owner, repo, str(repo_dir))
    
    def _download_github_repo(self, owner: str, repo: str, target_dir: str) -> None:
        """Download GitHub repository recursively"""
        try:
            # Using GitHub API directly
            self._download_github_contents(f"https://api.github.com/repos/{owner}/{repo}/contents", target_dir)
        except Exception as e:
            print(f"Error downloading {owner}/{repo}: {e}")
    
    def _download_github_contents(self, url: str, target_dir: str) -> None:
        """Recursively download GitHub repository contents"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            contents = response.json()
            os.makedirs(target_dir, exist_ok=True)
            
            for item in contents:
                if item['type'] == 'file':
                    if item['name'].endswith(('.py', '.js', '.json', '.md', '.yml', '.yaml', '.txt')):
                        file_path = os.path.join(target_dir, item['name'])
                        file_response = requests.get(item['download_url'])
                        if file_response.status_code == 200:
                            with open(file_path, 'wb') as f:
                                f.write(file_response.content)
                            print(f"  Downloaded: {item['name']}")
                
                elif item['type'] == 'dir' and not item['name'].startswith('.'):
                    subdir = os.path.join(target_dir, item['name'])
                    self._download_github_contents(item['url'], subdir)
                    
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Error downloading contents from {url}: {e}")
    
    def analyze_codebases(self) -> Tuple[Dict[str, ModuleBehavior], Dict[str, ModuleBehavior]]:
        """Analyze both codebases for behavioral characteristics"""
        print("Phase 1: Analyzing codebase behaviors...")
        
        s1_path = self.temp_dir / "s1"
        soldier_path = self.temp_dir / "soldier"
        
        print(f"Analyzing s1 codebase at {s1_path}...")
        s1_behaviors = self.analyzer.analyze_codebase(str(s1_path))
        
        print(f"Analyzing soldier codebase at {soldier_path}...")
        soldier_behaviors = self.analyzer.analyze_codebase(str(soldier_path))
        
        print(f"S1 analysis complete: {len(s1_behaviors)} modules")
        print(f"Soldier analysis complete: {len(soldier_behaviors)} modules")
        
        return s1_behaviors, soldier_behaviors
    
    def generate_behavioral_mappings(self, s1_behaviors: Dict[str, ModuleBehavior], 
                                   soldier_behaviors: Dict[str, ModuleBehavior]) -> None:
        """Generate behavioral mapping JSON files"""
        print("Phase 1: Generating behavioral mappings...")
        
        # Convert ModuleBehavior objects to dictionaries for JSON serialization
        s1_data = {}
        for path, behavior in s1_behaviors.items():
            s1_data[path] = {
                'module_path': behavior.module_path,
                'exports': behavior.exports,
                'entry_points': behavior.entry_points,
                'functions': [
                    {
                        'name': f.name,
                        'parameters': f.parameters,
                        'return_type': f.return_type,
                        'decorators': f.decorators,
                        'line_number': f.line_number,
                        'has_docstring': f.docstring is not None
                    } for f in behavior.functions
                ],
                'classes': behavior.classes,
                'imports': behavior.imports,
                'state_mutations': behavior.state_mutations,
                'conditionals': behavior.conditionals,
                'error_flows': behavior.error_flows,
                'call_chains': behavior.call_chains,
                'data_contracts': behavior.data_contracts,
                'assumptions': behavior.assumptions,
                'complexity_metrics': {
                    'function_count': len(behavior.functions),
                    'class_count': len(behavior.classes),
                    'conditional_count': len(behavior.conditionals),
                    'import_count': len(behavior.imports),
                    'state_mutation_count': len(behavior.state_mutations)
                }
            }
        
        soldier_data = {}
        for path, behavior in soldier_behaviors.items():
            soldier_data[path] = {
                'module_path': behavior.module_path,
                'exports': behavior.exports,
                'entry_points': behavior.entry_points,
                'functions': [
                    {
                        'name': f.name,
                        'parameters': f.parameters,
                        'return_type': f.return_type,
                        'decorators': f.decorators,
                        'line_number': f.line_number,
                        'has_docstring': f.docstring is not None
                    } for f in behavior.functions
                ],
                'classes': behavior.classes,
                'imports': behavior.imports,
                'state_mutations': behavior.state_mutations,
                'conditionals': behavior.conditionals,
                'error_flows': behavior.error_flows,
                'call_chains': behavior.call_chains,
                'data_contracts': behavior.data_contracts,
                'assumptions': behavior.assumptions,
                'complexity_metrics': {
                    'function_count': len(behavior.functions),
                    'class_count': len(behavior.classes),
                    'conditional_count': len(behavior.conditionals),
                    'import_count': len(behavior.imports),
                    'state_mutation_count': len(behavior.state_mutations)
                }
            }
        
        # Save behavioral mappings
        s1_output = self.output_dir / "analysis" / "module_behavior_s1.json"
        soldier_output = self.output_dir / "analysis" / "module_behavior_soldier.json"
        
        with open(s1_output, 'w') as f:
            json.dump(s1_data, f, indent=2)
        
        with open(soldier_output, 'w') as f:
            json.dump(soldier_data, f, indent=2)
        
        print(f"Behavioral mappings saved:")
        print(f"  S1: {s1_output}")
        print(f"  Soldier: {soldier_output}")
    
    def generate_assumptions_register(self, s1_behaviors: Dict[str, ModuleBehavior], 
                                    soldier_behaviors: Dict[str, ModuleBehavior]) -> None:
        """Generate comprehensive assumptions register"""
        print("Phase 1: Generating assumptions register...")
        
        s1_assumptions = self.analyzer.extract_assumptions(s1_behaviors)
        soldier_assumptions = self.analyzer.extract_assumptions(soldier_behaviors)
        
        # Combine and create CSV
        assumptions_file = self.output_dir / "analysis" / "assumptions.csv"
        
        with open(assumptions_file, 'w', newline='') as csvfile:
            fieldnames = ['codebase', 'module', 'line_number', 'type', 'description', 'risk_level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for assumption in s1_assumptions:
                writer.writerow({
                    'codebase': 's1',
                    'module': assumption.module,
                    'line_number': assumption.line_number,
                    'type': assumption.type,
                    'description': assumption.description,
                    'risk_level': assumption.risk_level
                })
            
            for assumption in soldier_assumptions:
                writer.writerow({
                    'codebase': 'soldier',
                    'module': assumption.module,
                    'line_number': assumption.line_number,
                    'type': assumption.type,
                    'description': assumption.description,
                    'risk_level': assumption.risk_level
                })
        
        print(f"Assumptions register saved: {assumptions_file}")
        print(f"Total assumptions found: {len(s1_assumptions) + len(soldier_assumptions)}")
    
    def generate_propagation_graphs(self, s1_behaviors: Dict[str, ModuleBehavior], 
                                  soldier_behaviors: Dict[str, ModuleBehavior]) -> None:
        """Generate call chain and data flow visualizations"""
        print("Phase 1: Generating propagation graphs...")
        
        graphs_dir = self.output_dir / "analysis" / "propagation_graphs"
        graphs_dir.mkdir(exist_ok=True)
        
        # Generate call graphs
        try:
            s1_graph = self.analyzer.build_call_graph(s1_behaviors)
            soldier_graph = self.analyzer.build_call_graph(soldier_behaviors)
            
            # Save graph data
            nx.write_gexf(s1_graph, graphs_dir / "s1_call_graph.gexf")
            nx.write_gexf(soldier_graph, graphs_dir / "soldier_call_graph.gexf")
            
            # Create simple visualizations if graphs are not too large
            if len(s1_graph.nodes()) < 100:
                plt.figure(figsize=(12, 8))
                pos = nx.spring_layout(s1_graph, k=1, iterations=50)
                nx.draw(s1_graph, pos, with_labels=False, node_size=20, 
                       node_color='lightblue', edge_color='gray', alpha=0.7)
                plt.title("S1 Codebase Call Graph")
                plt.savefig(graphs_dir / "s1_call_graph.png", dpi=150, bbox_inches='tight')
                plt.close()
            
            if len(soldier_graph.nodes()) < 100:
                plt.figure(figsize=(12, 8))
                pos = nx.spring_layout(soldier_graph, k=1, iterations=50)
                nx.draw(soldier_graph, pos, with_labels=False, node_size=20,
                       node_color='lightcoral', edge_color='gray', alpha=0.7)
                plt.title("Soldier Codebase Call Graph")
                plt.savefig(graphs_dir / "soldier_call_graph.png", dpi=150, bbox_inches='tight')
                plt.close()
            
            print(f"Call graphs saved in {graphs_dir}")
            
        except Exception as e:
            print(f"Error generating graphs: {e}")
    
    def generate_summary_report(self, s1_behaviors: Dict[str, ModuleBehavior], 
                              soldier_behaviors: Dict[str, ModuleBehavior]) -> None:
        """Generate summary report of Phase 1 analysis"""
        print("Phase 1: Generating summary report...")
        
        report_file = self.output_dir / "analysis" / "phase1_summary.md"
        
        s1_stats = self._calculate_codebase_stats(s1_behaviors)
        soldier_stats = self._calculate_codebase_stats(soldier_behaviors)
        
        with open(report_file, 'w') as f:
            f.write("# Phase 1 Traversal - Summary Report\n\n")
            f.write("## Codebase Statistics\n\n")
            
            f.write("### S1 Codebase\n")
            f.write(f"- **Modules**: {s1_stats['modules']}\n")
            f.write(f"- **Functions**: {s1_stats['functions']}\n")
            f.write(f"- **Classes**: {s1_stats['classes']}\n")
            f.write(f"- **Entry Points**: {s1_stats['entry_points']}\n")
            f.write(f"- **Imports**: {s1_stats['imports']}\n")
            f.write(f"- **Conditionals**: {s1_stats['conditionals']}\n")
            f.write(f"- **Error Flows**: {s1_stats['error_flows']}\n\n")
            
            f.write("### Soldier Codebase\n")
            f.write(f"- **Modules**: {soldier_stats['modules']}\n")
            f.write(f"- **Functions**: {soldier_stats['functions']}\n")
            f.write(f"- **Classes**: {soldier_stats['classes']}\n")
            f.write(f"- **Entry Points**: {soldier_stats['entry_points']}\n")
            f.write(f"- **Imports**: {soldier_stats['imports']}\n")
            f.write(f"- **Conditionals**: {soldier_stats['conditionals']}\n")
            f.write(f"- **Error Flows**: {soldier_stats['error_flows']}\n\n")
            
            f.write("## Key Behavioral Observations\n\n")
            f.write("### Complexity Comparison\n")
            f.write(f"- S1 has {s1_stats['functions'] - soldier_stats['functions']} more functions than Soldier\n")
            f.write(f"- S1 has {s1_stats['classes'] - soldier_stats['classes']} more classes than Soldier\n")
            f.write(f"- S1 has {s1_stats['conditionals'] - soldier_stats['conditionals']} more conditional branches than Soldier\n\n")
            
            f.write("### Architectural Differences\n")
            s1_modules = set(s1_behaviors.keys())
            soldier_modules = set(soldier_behaviors.keys())
            
            common_modules = s1_modules.intersection(soldier_modules)
            s1_unique = s1_modules - soldier_modules
            soldier_unique = soldier_modules - s1_modules
            
            f.write(f"- **Common modules**: {len(common_modules)}\n")
            f.write(f"- **S1 unique modules**: {len(s1_unique)}\n")
            f.write(f"- **Soldier unique modules**: {len(soldier_unique)}\n\n")
            
            if s1_unique:
                f.write("#### S1 Unique Modules:\n")
                for module in sorted(s1_unique)[:10]:  # Show first 10
                    f.write(f"- {module}\n")
                if len(s1_unique) > 10:
                    f.write(f"- ... and {len(s1_unique) - 10} more\n")
                f.write("\n")
            
            if soldier_unique:
                f.write("#### Soldier Unique Modules:\n")
                for module in sorted(soldier_unique)[:10]:  # Show first 10
                    f.write(f"- {module}\n")
                if len(soldier_unique) > 10:
                    f.write(f"- ... and {len(soldier_unique) - 10} more\n")
                f.write("\n")
        
        print(f"Summary report saved: {report_file}")
    
    def _calculate_codebase_stats(self, behaviors: Dict[str, ModuleBehavior]) -> Dict[str, int]:
        """Calculate aggregate statistics for a codebase"""
        stats = {
            'modules': len(behaviors),
            'functions': 0,
            'classes': 0,
            'entry_points': 0,
            'imports': 0,
            'conditionals': 0,
            'error_flows': 0
        }
        
        for behavior in behaviors.values():
            stats['functions'] += len(behavior.functions)
            stats['classes'] += len(behavior.classes)
            stats['entry_points'] += len(behavior.entry_points)
            stats['imports'] += len(behavior.imports)
            stats['conditionals'] += len(behavior.conditionals)
            stats['error_flows'] += len(behavior.error_flows)
        
        return stats
    
    def run_phase1(self) -> None:
        """Execute complete Phase 1 analysis"""
        print("Starting Phase 1 - Traversal Analysis")
        print("=" * 50)
        
        try:
            # Step 1: Download repositories
            self.download_source_repositories()
            
            # Step 2: Analyze codebases
            s1_behaviors, soldier_behaviors = self.analyze_codebases()
            
            # Step 3: Generate behavioral mappings
            self.generate_behavioral_mappings(s1_behaviors, soldier_behaviors)
            
            # Step 4: Generate assumptions register
            self.generate_assumptions_register(s1_behaviors, soldier_behaviors)
            
            # Step 5: Generate propagation graphs
            self.generate_propagation_graphs(s1_behaviors, soldier_behaviors)
            
            # Step 6: Generate summary report
            self.generate_summary_report(s1_behaviors, soldier_behaviors)
            
            print("\nPhase 1 Traversal Analysis Complete!")
            print("=" * 50)
            
        except Exception as e:
            print(f"Error in Phase 1 analysis: {e}")
            raise


if __name__ == "__main__":
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        
        phase1 = Phase1Traversal()
        phase1.run_phase1()
        
    except ImportError as e:
        print(f"Missing required dependencies: {e}")
        print("Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)