#!/usr/bin/env python3
"""
Comprehensive Codebase Convergence Analysis Framework

This module implements a systematic 5-phase analysis system for comparing and converging
two full codebases based purely on observable code behavior, not naming or structure.
"""

import ast
import json
import csv
import os
import sys
import requests
import yaml
from typing import Dict, List, Any, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import networkx as nx
from collections import defaultdict
import re


@dataclass
class FunctionSignature:
    """Represents a function signature with parameters and return hints"""
    name: str
    parameters: List[str]
    return_type: Optional[str]
    decorators: List[str]
    line_number: int
    docstring: Optional[str]


@dataclass
class ModuleBehavior:
    """Captures behavioral characteristics of a module"""
    module_path: str
    exports: List[str]
    entry_points: List[str]
    functions: List[FunctionSignature]
    classes: List[str]
    imports: List[str]
    state_mutations: List[str]
    conditionals: List[Dict[str, Any]]
    error_flows: List[str]
    call_chains: List[List[str]]
    data_contracts: List[Dict[str, Any]]
    assumptions: List[str]


@dataclass
class Assumption:
    """Represents an assumption found in code"""
    module: str
    line_number: int
    type: str  # 'input_form', 'dependency_state', 'io_condition', 'external_integration', 'implicit_expectation'
    description: str
    risk_level: str  # 'low', 'medium', 'high', 'critical'


class CodeBehaviorAnalyzer:
    """Analyzes Python codebases to extract behavioral information"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        
    def fetch_github_repo(self, owner: str, repo: str, target_dir: str) -> None:
        """Download a GitHub repository to local directory"""
        if os.path.exists(target_dir):
            print(f"Repository {repo} already exists in {target_dir}")
            return
            
        # Using GitHub API to get repository content
        base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self._download_recursive(base_url, target_dir)
    
    def _download_recursive(self, url: str, target_dir: str) -> None:
        """Recursively download files from GitHub API"""
        headers = {}
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
            
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return
            
        items = response.json()
        os.makedirs(target_dir, exist_ok=True)
        
        for item in items:
            if item['type'] == 'file':
                file_path = os.path.join(target_dir, item['name'])
                file_response = requests.get(item['download_url'])
                if file_response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"Downloaded: {file_path}")
            elif item['type'] == 'dir':
                subdir = os.path.join(target_dir, item['name'])
                self._download_recursive(item['url'], subdir)
    
    def analyze_python_file(self, file_path: str) -> ModuleBehavior:
        """Analyze a single Python file for behavioral characteristics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            behavior = ModuleBehavior(
                module_path=file_path,
                exports=[],
                entry_points=[],
                functions=[],
                classes=[],
                imports=[],
                state_mutations=[],
                conditionals=[],
                error_flows=[],
                call_chains=[],
                data_contracts=[],
                assumptions=[]
            )
            
            # Analyze AST nodes
            for node in ast.walk(tree):
                self._analyze_node(node, behavior, content)
            
            return behavior
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return ModuleBehavior(
                module_path=file_path,
                exports=[], entry_points=[], functions=[], classes=[],
                imports=[], state_mutations=[], conditionals=[],
                error_flows=[], call_chains=[], data_contracts=[], assumptions=[]
            )
    
    def _analyze_node(self, node: ast.AST, behavior: ModuleBehavior, content: str) -> None:
        """Analyze individual AST nodes for behavioral patterns"""
        lines = content.split('\n')
        
        if isinstance(node, ast.FunctionDef):
            # Extract function signature and behavior
            params = [arg.arg for arg in node.args.args]
            return_type = None
            if node.returns:
                return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else None
                
            decorators = [ast.unparse(dec) if hasattr(ast, 'unparse') else str(dec) for dec in node.decorator_list]
            
            docstring = None
            if (node.body and isinstance(node.body[0], ast.Expr) and 
                isinstance(node.body[0].value, ast.Constant) and 
                isinstance(node.body[0].value.value, str)):
                docstring = node.body[0].value.value
            
            func_sig = FunctionSignature(
                name=node.name,
                parameters=params,
                return_type=return_type,
                decorators=decorators,
                line_number=node.lineno,
                docstring=docstring
            )
            behavior.functions.append(func_sig)
            
            # Check if this is an entry point
            if node.name == 'main' or any('if __name__' in line for line in lines):
                behavior.entry_points.append(node.name)
        
        elif isinstance(node, ast.ClassDef):
            behavior.classes.append(node.name)
        
        elif isinstance(node, ast.Import):
            for alias in node.names:
                behavior.imports.append(alias.name)
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                behavior.imports.append(f"{module}.{alias.name}")
        
        elif isinstance(node, ast.Assign):
            # Track state mutations
            for target in node.targets:
                if isinstance(target, ast.Name):
                    behavior.state_mutations.append(f"assign:{target.id}")
                elif isinstance(target, ast.Attribute):
                    behavior.state_mutations.append(f"attr_assign:{ast.unparse(target) if hasattr(ast, 'unparse') else str(target)}")
        
        elif isinstance(node, ast.If):
            # Track conditional logic
            test_code = ast.unparse(node.test) if hasattr(ast, 'unparse') else str(node.test)
            behavior.conditionals.append({
                'line': node.lineno,
                'condition': test_code,
                'has_else': len(node.orelse) > 0
            })
        
        elif isinstance(node, ast.Try):
            # Track error handling patterns
            for handler in node.handlers:
                exc_type = handler.type
                exc_name = ast.unparse(exc_type) if exc_type and hasattr(ast, 'unparse') else 'Exception'
                behavior.error_flows.append(f"try_except:{exc_name}:{handler.lineno}")
    
    def analyze_codebase(self, repo_path: str) -> Dict[str, ModuleBehavior]:
        """Analyze entire codebase and return module behaviors"""
        behaviors = {}
        
        for root, dirs, files in os.walk(repo_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules', '.pytest_cache']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    behaviors[relative_path] = self.analyze_python_file(file_path)
        
        return behaviors
    
    def extract_assumptions(self, behaviors: Dict[str, ModuleBehavior]) -> List[Assumption]:
        """Extract assumptions from behavioral analysis"""
        assumptions = []
        
        for module_path, behavior in behaviors.items():
            # Look for common assumption patterns
            for func in behavior.functions:
                # Parameters without type hints suggest input form assumptions
                if func.parameters and not func.return_type:
                    assumptions.append(Assumption(
                        module=module_path,
                        line_number=func.line_number,
                        type='input_form',
                        description=f"Function {func.name} assumes parameter types without validation",
                        risk_level='medium'
                    ))
                
                # Functions with external dependencies
                if any('requests' in imp or 'http' in imp for imp in behavior.imports):
                    assumptions.append(Assumption(
                        module=module_path,
                        line_number=func.line_number,
                        type='external_integration',
                        description=f"Function {func.name} assumes external service availability",
                        risk_level='high'
                    ))
            
            # Check for implicit expectations in conditionals
            for cond in behavior.conditionals:
                if 'os.' in cond['condition'] or 'sys.' in cond['condition']:
                    assumptions.append(Assumption(
                        module=module_path,
                        line_number=cond['line'],
                        type='io_condition',
                        description=f"Conditional assumes system state: {cond['condition']}",
                        risk_level='medium'
                    ))
        
        return assumptions
    
    def build_call_graph(self, behaviors: Dict[str, ModuleBehavior]) -> nx.DiGraph:
        """Build call graph from behavioral analysis"""
        graph = nx.DiGraph()
        
        for module_path, behavior in behaviors.items():
            # Add nodes for all functions
            for func in behavior.functions:
                node_id = f"{module_path}:{func.name}"
                graph.add_node(node_id, 
                              module=module_path,
                              function=func.name,
                              parameters=len(func.parameters),
                              line_number=func.line_number)
        
        # Analyze call relationships (simplified - would need more sophisticated analysis)
        for module_path, behavior in behaviors.items():
            for func in behavior.functions:
                caller_id = f"{module_path}:{func.name}"
                # This is a simplified approach - real implementation would parse function bodies
                for other_module, other_behavior in behaviors.items():
                    for other_func in other_behavior.functions:
                        if other_func.name in str(func.docstring or ''):
                            callee_id = f"{other_module}:{other_func.name}"
                            graph.add_edge(caller_id, callee_id)
        
        return graph


class ComparisonEngine:
    """Compares behavioral characteristics between codebases"""
    
    def __init__(self):
        pass
    
    def compare_modules(self, behavior1: ModuleBehavior, behavior2: ModuleBehavior) -> Dict[str, Any]:
        """Compare two module behaviors"""
        comparison = {
            'behavioral_intent_similarity': self._calculate_intent_similarity(behavior1, behavior2),
            'execution_logic_similarity': self._calculate_logic_similarity(behavior1, behavior2),
            'complexity_metrics': {
                'module1': self._calculate_complexity(behavior1),
                'module2': self._calculate_complexity(behavior2)
            },
            'efficiency_characteristics': {
                'module1': self._analyze_efficiency(behavior1),
                'module2': self._analyze_efficiency(behavior2)
            },
            'side_effect_domains': {
                'module1': self._identify_side_effects(behavior1),
                'module2': self._identify_side_effects(behavior2)
            },
            'error_handling_patterns': {
                'module1': behavior1.error_flows,
                'module2': behavior2.error_flows
            }
        }
        
        return comparison
    
    def _calculate_intent_similarity(self, b1: ModuleBehavior, b2: ModuleBehavior) -> float:
        """Calculate behavioral intent similarity (0-1)"""
        # Compare function signatures
        func_names1 = {f.name for f in b1.functions}
        func_names2 = {f.name for f in b2.functions}
        
        if not func_names1 and not func_names2:
            return 1.0
        
        intersection = len(func_names1.intersection(func_names2))
        union = len(func_names1.union(func_names2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_logic_similarity(self, b1: ModuleBehavior, b2: ModuleBehavior) -> float:
        """Calculate execution logic similarity"""
        # Compare conditional structures
        cond_count1 = len(b1.conditionals)
        cond_count2 = len(b2.conditionals)
        
        if cond_count1 == 0 and cond_count2 == 0:
            return 1.0
        
        max_cond = max(cond_count1, cond_count2)
        min_cond = min(cond_count1, cond_count2)
        
        return min_cond / max_cond if max_cond > 0 else 0.0
    
    def _calculate_complexity(self, behavior: ModuleBehavior) -> Dict[str, int]:
        """Calculate complexity metrics"""
        return {
            'function_count': len(behavior.functions),
            'class_count': len(behavior.classes),
            'conditional_count': len(behavior.conditionals),
            'state_mutation_count': len(behavior.state_mutations),
            'import_count': len(behavior.imports)
        }
    
    def _analyze_efficiency(self, behavior: ModuleBehavior) -> Dict[str, Any]:
        """Analyze efficiency characteristics"""
        return {
            'has_loops': any('for' in str(c) or 'while' in str(c) for c in behavior.conditionals),
            'recursive_potential': any('recursive' in f.docstring.lower() if f.docstring else False for f in behavior.functions),
            'io_operations': len([imp for imp in behavior.imports if any(io_mod in imp for io_mod in ['os', 'sys', 'io', 'requests'])])
        }
    
    def _identify_side_effects(self, behavior: ModuleBehavior) -> List[str]:
        """Identify potential side effects"""
        side_effects = []
        
        # File I/O side effects
        if any('os.' in mut or 'file' in mut.lower() for mut in behavior.state_mutations):
            side_effects.append('file_system')
        
        # Network side effects
        if any('requests' in imp or 'urllib' in imp for imp in behavior.imports):
            side_effects.append('network')
        
        # Global state mutations
        if any('global' in mut for mut in behavior.state_mutations):
            side_effects.append('global_state')
        
        return side_effects


if __name__ == "__main__":
    print("Comprehensive Codebase Convergence Analysis Framework")
    print("=" * 60)