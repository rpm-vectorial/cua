# Browser Use UI

A modular UI library for browser automation with AI agents.

## Directory Structure

```
browser_use_ui/
├── __init__.py                # Package initialization
├── agents/                    # Agent-related code
│   ├── __init__.py
│   ├── agent_manager.py       # Manages agent lifecycle
│   └── custom_agent.py        # Custom agent implementation
├── browser/                   # Browser-related code
│   ├── __init__.py
│   └── browser_manager.py     # Manages browser lifecycle
├── config/                    # Configuration-related code
│   └── __init__.py
├── ui/                        # UI-related code
│   ├── __init__.py
│   ├── component_manager.py   # Manages UI components
│   ├── handlers.py            # Handles UI events
│   └── ui_builder.py          # Builds the UI
└── utils/                     # Utility functions
    ├── __init__.py
    ├── env_utils.py           # Environment variable utilities
    ├── file_utils.py          # File handling utilities
    └── llm_utils.py           # LLM-related utilities
```

## Usage

To use this package, you typically import the UIBuilder and launch the UI:

```python
from browser_use_ui.ui.ui_builder import UIBuilder

# Create and launch the UI
ui_builder = UIBuilder(theme_name="Ocean")
ui_builder.launch(server_name="127.0.0.1", server_port=7788)
```

Or use the main application:

```bash
# Run with the virtual environment
./scripts/run_app.sh

# Or directly
python browser_use_app.py
```

## Development

To add new components or modify the UI, extend the appropriate module:

- For new UI components: modify `ui/ui_builder.py`
- For new event handlers: modify `ui/handlers.py`
- For new LLM providers: modify `utils/llm_utils.py` 