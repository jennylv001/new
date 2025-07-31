#!/usr/bin/env python3
"""
GitHub Data Fetcher and Phase 1 Analysis Runner

This script fetches repository data using GitHub MCP server functions and runs Phase 1 analysis.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from phase1_traversal_mcp import Phase1TraversalMCP


def fetch_repo_files_recursively(owner: str, repo: str, path: str = "/") -> Dict[str, str]:
    """
    Recursively fetch all Python files from a GitHub repository.
    This is a placeholder that will be called with external GitHub MCP server functions.
    """
    # This will be populated externally using GitHub MCP server functions
    return {}


def save_repo_data(repo_data: Dict[str, str], filename: str) -> None:
    """Save repository data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(repo_data, f, indent=2)


def load_repo_data(filename: str) -> Dict[str, str]:
    """Load repository data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}


def create_sample_repo_data() -> Tuple[Dict[str, str], Dict[str, str]]:
    """Create sample repository data for testing when GitHub access fails"""
    
    s1_sample = {
        "cli.py": '''#!/usr/bin/env python3
"""Command-line interface for s1 system"""

import argparse
import sys
import logging
from typing import Optional, List

class S1CLI:
    """Main CLI class for s1 system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description="S1 System CLI")
        parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
        parser.add_argument("--config", "-c", type=str, help="Configuration file")
        return parser.parse_args(args)
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Main entry point"""
        try:
            parsed_args = self.parse_args(args)
            if parsed_args.verbose:
                logging.basicConfig(level=logging.DEBUG)
            
            self.logger.info("Starting S1 system")
            return 0
            
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return 1


def main():
    """Main function"""
    cli = S1CLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
''',
        
        "config.py": '''"""Configuration management for s1 system"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    username: str = "user"
    password: str = "password"
    database: str = "s1db"


@dataclass 
class S1Config:
    """Main S1 configuration"""
    debug: bool = False
    log_level: str = "INFO"
    database: DatabaseConfig = DatabaseConfig()
    api_key: Optional[str] = None


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.getenv("S1_CONFIG", "config.json")
        self._config: Optional[S1Config] = None
    
    def load_config(self) -> S1Config:
        """Load configuration from file"""
        if self._config is not None:
            return self._config
            
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                self._config = self._parse_config(data)
            except Exception as e:
                print(f"Error loading config: {e}")
                self._config = S1Config()
        else:
            self._config = S1Config()
        
        return self._config
    
    def _parse_config(self, data: Dict[str, Any]) -> S1Config:
        """Parse configuration data"""
        db_config = DatabaseConfig()
        if "database" in data:
            db_data = data["database"]
            db_config.host = db_data.get("host", db_config.host)
            db_config.port = db_data.get("port", db_config.port)
            db_config.username = db_data.get("username", db_config.username)
            db_config.password = db_data.get("password", db_config.password)
            db_config.database = db_data.get("database", db_config.database)
        
        return S1Config(
            debug=data.get("debug", False),
            log_level=data.get("log_level", "INFO"),
            database=db_config,
            api_key=data.get("api_key")
        )
    
    def save_config(self, config: S1Config) -> None:
        """Save configuration to file"""
        data = {
            "debug": config.debug,
            "log_level": config.log_level,
            "database": {
                "host": config.database.host,
                "port": config.database.port,
                "username": config.database.username,
                "password": config.database.password,
                "database": config.database.database
            },
            "api_key": config.api_key
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
''',

        "utils.py": '''"""Utility functions for s1 system"""

import os
import sys
import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


def calculate_file_hash(file_path: str) -> Optional[str]:
    """Calculate SHA256 hash of a file"""
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None


def ensure_directory(path: str) -> bool:
    """Ensure directory exists, create if needed"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False


def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """Load JSON data from file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {file_path}: {e}")  
        return None
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to JSON file"""
    try:
        ensure_directory(os.path.dirname(file_path))
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


class DataProcessor:
    """Process and validate data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data"""
        if data is None:
            return False
        
        if isinstance(data, dict):
            return len(data) > 0
        elif isinstance(data, (list, str)):
            return len(data) > 0
        else:
            return True
    
    def process_data(self, data: Any) -> Optional[Any]:
        """Process input data"""
        if not self.validate_input(data):
            return None
        
        try:
            if isinstance(data, dict):
                return self._process_dict(data)
            elif isinstance(data, list):
                return self._process_list(data)
            else:
                return data
        except Exception as e:
            print(f"Error processing data: {e}")
            return None
    
    def _process_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process dictionary data"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = value.strip()
            else:
                result[key] = value
        return result
    
    def _process_list(self, data: List[Any]) -> List[Any]:
        """Process list data"""
        return [item for item in data if item is not None]
'''
    }
    
    soldier_sample = {
        "cli.py": '''#!/usr/bin/env python3
"""Command-line interface for soldier system"""

import argparse
import sys
import logging
from typing import Optional, List, Dict, Any

class SoldierCLI:
    """Main CLI class for soldier system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.commands = {
            'start': self.start_command,
            'stop': self.stop_command,
            'status': self.status_command
        }
    
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description="Soldier System CLI")
        parser.add_argument("command", choices=self.commands.keys(), help="Command to execute")
        parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
        parser.add_argument("--config", "-c", type=str, help="Configuration file")
        parser.add_argument("--port", "-p", type=int, default=8080, help="Port number")
        return parser.parse_args(args)
    
    def start_command(self, args: argparse.Namespace) -> int:
        """Start the soldier system"""
        self.logger.info(f"Starting soldier system on port {args.port}")
        return 0
    
    def stop_command(self, args: argparse.Namespace) -> int:
        """Stop the soldier system"""
        self.logger.info("Stopping soldier system")
        return 0
    
    def status_command(self, args: argparse.Namespace) -> int:
        """Check soldier system status"""
        self.logger.info("Checking soldier system status")
        return 0
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Main entry point"""
        try:
            parsed_args = self.parse_args(args)
            if parsed_args.verbose:
                logging.basicConfig(level=logging.DEBUG)
            
            command_func = self.commands[parsed_args.command]
            return command_func(parsed_args)
            
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
            return 1
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return 1


def main():
    """Main function"""
    cli = SoldierCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
''',
        
        "config.py": '''"""Configuration management for soldier system"""

import os
import json
import yaml
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class ServerConfig:
    """Server configuration"""
    host: str = "0.0.0.0"
    port: int = 8080
    workers: int = 4
    timeout: int = 30


@dataclass 
class SoldierConfig:
    """Main Soldier configuration"""
    debug: bool = False
    log_level: str = "INFO"
    server: ServerConfig = ServerConfig()
    api_key: Optional[str] = None
    features: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = {"auth": True, "metrics": False}


class ConfigLoader:
    """Loads configuration from various sources"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.getenv("SOLDIER_CONFIG", "soldier.yaml")
        self._config: Optional[SoldierConfig] = None
    
    def load_config(self) -> SoldierConfig:
        """Load configuration from file"""
        if self._config is not None:
            return self._config
            
        if os.path.exists(self.config_file):
            try:
                data = self._load_config_file()
                self._config = self._parse_config(data)
            except Exception as e:
                print(f"Error loading config: {e}")
                self._config = SoldierConfig()
        else:
            self._config = SoldierConfig()
        
        # Override with environment variables
        self._apply_env_overrides()
        
        return self._config
    
    def _load_config_file(self) -> Dict[str, Any]:
        """Load configuration file (JSON or YAML)"""
        with open(self.config_file, 'r') as f:
            if self.config_file.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def _parse_config(self, data: Dict[str, Any]) -> SoldierConfig:
        """Parse configuration data"""
        server_config = ServerConfig()
        if "server" in data:
            server_data = data["server"]
            server_config.host = server_data.get("host", server_config.host)
            server_config.port = server_data.get("port", server_config.port)
            server_config.workers = server_data.get("workers", server_config.workers)
            server_config.timeout = server_data.get("timeout", server_config.timeout)
        
        return SoldierConfig(
            debug=data.get("debug", False),
            log_level=data.get("log_level", "INFO"),
            server=server_config,
            api_key=data.get("api_key"),
            features=data.get("features", {"auth": True, "metrics": False})
        )
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides"""
        if not self._config:
            return
            
        if os.getenv("SOLDIER_DEBUG"):
            self._config.debug = os.getenv("SOLDIER_DEBUG").lower() == "true"
            
        if os.getenv("SOLDIER_PORT"):
            try:
                self._config.server.port = int(os.getenv("SOLDIER_PORT"))
            except ValueError:
                pass
    
    def save_config(self, config: SoldierConfig) -> None:
        """Save configuration to file"""
        data = {
            "debug": config.debug,
            "log_level": config.log_level,
            "server": {
                "host": config.server.host,
                "port": config.server.port,
                "workers": config.server.workers,
                "timeout": config.server.timeout
            },
            "api_key": config.api_key,
            "features": config.features
        }
        
        if self.config_file.endswith(('.yaml', '.yml')):
            with open(self.config_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        else:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
''',

        "utils.py": '''"""Utility functions for soldier system"""

import os
import sys
import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from functools import wraps


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def retry(times: int = 3, delay: float = 1.0):
    """Retry decorator"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def calculate_checksum(data: Union[str, bytes]) -> str:
    """Calculate SHA256 checksum of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def validate_file_path(path: str) -> bool:
    """Validate file path exists and is readable"""
    try:
        return os.path.exists(path) and os.access(path, os.R_OK)
    except Exception:
        return False


def create_directory(path: str, mode: int = 0o755) -> bool:
    """Create directory with specified mode"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True, mode=mode)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False


def read_file_safely(file_path: str, encoding: str = 'utf-8') -> Optional[str]:
    """Safely read file content"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def write_file_safely(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
    """Safely write content to file"""
    try:
        create_directory(os.path.dirname(file_path))
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False


class FileProcessor:
    """File processing utilities"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or setup_logging()
    
    def process_directory(self, directory: str, pattern: str = "*.py") -> List[str]:
        """Process files in directory matching pattern"""
        try:
            path = Path(directory)
            if not path.exists():
                self.logger.error(f"Directory does not exist: {directory}")
                return []
            
            files = list(path.glob(pattern))
            self.logger.info(f"Found {len(files)} files matching {pattern}")
            return [str(f) for f in files]
            
        except Exception as e:
            self.logger.error(f"Error processing directory {directory}: {e}")
            return []
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze file and return metadata"""
        try:
            stat = os.stat(file_path)
            content = read_file_safely(file_path)
            
            return {
                'path': file_path,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'lines': len(content.splitlines()) if content else 0,
                'checksum': calculate_checksum(content) if content else None
            }
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return {'path': file_path, 'error': str(e)}


class DataValidator:
    """Validate data structures and inputs"""
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        """Validate configuration structure"""
        errors = []
        
        required_fields = ['server', 'log_level']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        if 'server' in config:
            server_config = config['server']
            if not isinstance(server_config.get('port'), int):
                errors.append("Server port must be an integer")
            
            port = server_config.get('port', 0)
            if not (1 <= port <= 65535):
                errors.append("Server port must be between 1 and 65535")
        
        return errors
    
    @staticmethod
    def validate_api_key(api_key: Optional[str]) -> bool:
        """Validate API key format"""
        if not api_key:
            return False
        return len(api_key) >= 32 and api_key.isalnum()
'''
    }
    
    return s1_sample, soldier_sample


def main():
    """Main function to fetch GitHub data and run Phase 1 analysis"""
    print("GitHub Data Fetcher and Phase 1 Analysis Runner")
    print("=" * 60)
    
    # Try to load existing data or create sample data
    s1_data_file = "/tmp/s1_repo_data.json"
    soldier_data_file = "/tmp/soldier_repo_data.json"
    
    s1_data = load_repo_data(s1_data_file)
    soldier_data = load_repo_data(soldier_data_file)
    
    if not s1_data or not soldier_data:
        print("GitHub repository data not found, creating sample data for testing...")
        s1_data, soldier_data = create_sample_repo_data()
        
        # Save sample data
        save_repo_data(s1_data, s1_data_file)
        save_repo_data(soldier_data, soldier_data_file)
        
        print(f"Sample S1 data: {len(s1_data)} files")
        print(f"Sample Soldier data: {len(soldier_data)} files")
    
    # Run Phase 1 analysis
    try:
        phase1 = Phase1TraversalMCP()
        s1_behaviors, soldier_behaviors = phase1.run_phase1_with_data(s1_data, soldier_data)
        
        print(f"\nAnalysis completed successfully!")
        print(f"S1 behaviors analyzed: {len(s1_behaviors)} modules")
        print(f"Soldier behaviors analyzed: {len(soldier_behaviors)} modules")
        
        return s1_behaviors, soldier_behaviors
        
    except Exception as e:
        print(f"Error running Phase 1 analysis: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    
    main()