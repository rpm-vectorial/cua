# Computer Use Agent (CUA)

A web interface for AI-powered browser automation.

## Overview

CUA provides a Gradio-based web UI for controlling AI agents that can interact with web browsers. It's built with modularity, scalability, and ease of use in mind.

## Features

- 🌐 **Browser Automation**: Control Chrome/Chromium browsers with AI
- 🧠 **Multiple LLM Providers**: Support for OpenAI, Anthropic, Google, and more
- 🎨 **Customizable UI**: Multiple themes and layouts
- 📊 **Recording & History**: Save agent sessions and browser recordings
- 🛠️ **Extensible**: Modular design for adding new features

## Architecture

### System Overview

CUA is an AI-powered browser automation system that allows intelligent agents to control a web browser to complete tasks. The architecture follows a modular design with clear separation of concerns across multiple components.

The system consists of these main parts:
- **User Interface (UI)**: A Gradio-based web interface for user interaction
- **Agent System**: Manages AI agents that perform tasks
- **Browser Control**: Handles browser automation
- **LLM Integration**: Connects to various language models

### Key Components

#### Entry Points
- **run.py**: Wrapper script that sets up the environment and runs the application
- **browser_use_app.py**: Main entry point that initializes and launches the UI

#### Core Components
- **Agent**: Executes tasks by controlling the browser using an LLM
- **AgentManager**: Manages agent lifecycle and provides a clean interface for the UI
- **BrowserManager**: Handles browser initialization and lifecycle

#### UI Components
- **UIBuilder**: Constructs the Gradio web interface
- **UIHandlers**: Handles UI events and coordinates with backend components
- **ComponentManager**: Manages UI components and their registration

#### Utility Components
- **LLMUtils**: Provides access to various language models (OpenAI, Anthropic, etc.)
- **FileUtils**: Handles file operations like saving recordings
- **EnvUtils**: Manages environment variables and sensitive information

### Flow Overview

1. **Startup Flow**: User runs the application → Environment setup → UI initialization → Web interface display
2. **Agent Execution**: User submits task → Agent creation → Browser initialization → Task execution → Results display

For more detailed architecture information, including diagrams, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Directory Structure

```
cua/
├── browser_use_app.py           # Main application entry point
├── run.py                       # Wrapper script to run the application
├── browser_use_ui/              # Main package
│   ├── agent/                   # Agent core components
│   ├── agents/                  # Agent management
│   ├── browser/                 # Browser control
│   ├── controller/              # Control logic
│   ├── ui/                      # Web interface
│   └── utils/                   # Utilities
├── scripts/                     # Helper scripts
└── docs/                        # Documentation
```

## Installation

### Prerequisites

- Python 3.9+
- Chrome or Chromium browser
- An API key for at least one LLM provider

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rpm-vectorial/cua.git
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

### Using the Direct Run Script

The easiest way to run the application is using:

```bash
./scripts/direct_run.sh
```

This script will set up your API keys and start the application.

### Using the Regular Script

```bash
./scripts/run_app.sh
```

### Using Python Directly

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