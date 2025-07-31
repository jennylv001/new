# Functional Equivalence Mapping

## Module Pairs and Behavioral Analysis

### utils.py

**S1 Module**: `utils.py`  
**Soldier Module**: `utils.py`  

**Similarity Metrics**:
- Intent Similarity: 0.045
- Logic Similarity: 0.889- Interface Overlap: 0.071
- Divergence Ratio: 1.500

**Complexity Comparison**:
- S1: 9 functions, 8 complexity
- Soldier: 14 functions, 9 complexity

**Compatible Functions**:
- `__init__`: Params ✓ (2 vs 2), Return ✓

**Unique Functions**:
- S1 Only: _process_dict, _process_list, validate_input, load_json_file, process_data, save_json_file, ensure_directory, calculate_file_hash
- Soldier Only: decorator, validate_config, process_directory, read_file_safely, analyze_file, calculate_checksum, validate_file_path, wrapper, create_directory, retry, validate_api_key, setup_logging, write_file_safely

---

### cli.py

**S1 Module**: `cli.py`  
**Soldier Module**: `cli.py`  

**Similarity Metrics**:
- Intent Similarity: 0.571
- Logic Similarity: 1.000- Interface Overlap: 0.571
- Divergence Ratio: 0.429

**Complexity Comparison**:
- S1: 4 functions, 3 complexity
- Soldier: 7 functions, 3 complexity

**Compatible Functions**:
- `main`: Params ✓ (0 vs 0), Return ✓
- `__init__`: Params ✓ (1 vs 1), Return ✓
- `parse_args`: Params ✓ (2 vs 2), Return ✓
- `run`: Params ✓ (2 vs 2), Return ✓

**Unique Functions**:
- Soldier Only: status_command, stop_command, start_command

---

### config.py

**S1 Module**: `config.py`  
**Soldier Module**: `config.py`  

**Similarity Metrics**:
- Intent Similarity: 0.571
- Logic Similarity: 0.400- Interface Overlap: 0.571
- Divergence Ratio: 0.429

**Complexity Comparison**:
- S1: 4 functions, 4 complexity
- Soldier: 7 functions, 10 complexity

**Compatible Functions**:
- `save_config`: Params ✓ (2 vs 2), Return ✓
- `_parse_config`: Params ✓ (2 vs 2), Return ✗
- `__init__`: Params ✓ (2 vs 2), Return ✓
- `load_config`: Params ✓ (1 vs 1), Return ✗

**Unique Functions**:
- Soldier Only: __post_init__, _apply_env_overrides, _load_config_file

---

