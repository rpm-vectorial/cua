# Refactoring Plan for File Naming and Organization

## File Naming Conventions
- Python modules and packages: snake_case (e.g., `file_utils.py`)
- Shell scripts: snake_case (e.g., `run_app.sh`)
- Configuration files: snake_case (e.g., `config.json`)
- Documentation: UPPERCASE_WITH_UNDERSCORES (e.g., `README.md`, `SECURITY.md`)

## Directory Structure
```
cua/  # Root directory
├── browser_use_ui/  # Main package
│   ├── __init__.py
│   ├── config/  # Configuration-related code
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── browser/  # Browser-related code
│   │   ├── __init__.py
│   │   ├── browser_manager.py
│   │   └── custom_browser.py
│   ├── agents/  # Agent-related code
│   │   ├── __init__.py
│   │   ├── agent_manager.py
│   │   └── custom_agent.py
│   ├── ui/  # UI-related code
│   │   ├── __init__.py
│   │   ├── ui_builder.py
│   │   ├── handlers.py
│   │   └── component_manager.py
│   └── utils/  # Utility functions
│       ├── __init__.py
│       ├── env_utils.py
│       ├── file_utils.py
│       └── llm_utils.py
├── scripts/  # Helper scripts
│   ├── run_app.sh
│   └── install_dependencies.sh
├── tests/  # Tests
│   ├── __init__.py
│   ├── test_browser.py
│   └── test_llm.py
├── docs/  # Documentation
│   ├── REFACTORING_SUMMARY.md
│   └── API.md
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
├── requirements.txt
└── browser_use_app.py  # Main entry point
```

## Files to Rename
- `webui_refactored.py` → `browser_use_app.py`
- `start.py` → `scripts/start_app.py`
- `run_app.sh` → `scripts/run_app.sh`
- `fix_dropdown.py` → `scripts/fix_dropdown.py`
- `switch_to_anthropic.py` → `scripts/switch_to_anthropic.py`
- `test_anthropic.py` → `tests/test_anthropic.py`

## Implementation Steps
1. Create new directory structure
2. Move and rename files
3. Update imports to reflect new structure
4. Update paths in scripts
5. Test the restructured application
6. Update documentation with new structure 