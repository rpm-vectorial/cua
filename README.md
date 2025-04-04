# Browser Use App

A web interface for browser automation with AI agents.

## Overview

This application provides a Gradio-based web UI for controlling AI agents that can interact with web browsers. It's built with modularity, scalability, and ease of use in mind.

## Features

- 🌐 **Browser Automation**: Control Chrome/Chromium browsers with AI
- 🧠 **Multiple LLM Providers**: Support for OpenAI, Anthropic, Google, and more
- 🎨 **Customizable UI**: Multiple themes and layouts
- 📊 **Recording & History**: Save agent sessions and browser recordings
- 🛠️ **Extensible**: Modular design for adding new features

## Directory Structure

```
cua/
├── browser_use_ui/           # Main UI package
│   ├── agents/               # Agent handling code
│   ├── browser/              # Browser control code
│   ├── config/               # Configuration code
│   ├── ui/                   # UI components and handlers
│   └── utils/                # Utility functions
├── scripts/                  # Helper scripts
│   ├── run_app.sh            # Run the application
│   ├── start_app.py          # Environment-aware startup
│   └── fix_dropdown.py       # UI fixes
├── docs/                     # Documentation
│   └── REFACTORING_SUMMARY.md # Refactoring details
├── tests/                    # Test code
├── browser_use_app.py        # Main entry point
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.9+
- Chrome or Chromium browser
- An API key for at least one LLM provider

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cua.git
   cd cua
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Copy the example environment file and edit it:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Running the App

### Using the Script

The easiest way to run the application is using the provided script:

```bash
./scripts/run_app.sh
```

This script will activate the virtual environment and start the application.

### Using Python Directly

Alternatively, you can run the application directly:

```bash
python browser_use_app.py --ip 127.0.0.1 --port 7788
```

### Using Docker

```bash
docker-compose up -d
```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:7788`
2. Configure the agent settings and LLM provider
3. Enter a task for the agent
4. Click "Run Agent" to execute

## Development

### Adding New Features

- For new UI components: modify `browser_use_ui/ui/ui_builder.py`
- For new event handlers: modify `browser_use_ui/ui/handlers.py`
- For new LLM providers: modify `browser_use_ui/utils/llm_utils.py`

### Running Tests

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 