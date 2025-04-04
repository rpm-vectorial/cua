#!/usr/bin/env python3
"""
Browser Use App - A web interface for browser automation with AI
"""

import os
import logging
import argparse
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to load environment variables with graceful fallback
try:
    from dotenv import load_dotenv
    env_path = Path(os.path.dirname(os.path.abspath(__file__))) / '.env'
    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loading environment variables from: {env_path}")
    
    # Check if API keys are loaded
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        logger.info("OpenAI API key loaded successfully")
    else:
        logger.warning("OpenAI API key not found in environment variables")
except ImportError as e:
    print("=" * 80)
    print("ERROR: python-dotenv package is not installed.")
    print("Please run the application with the virtual environment:")
    print("    source venv/bin/activate && python browser_use_app.py")
    print("Or run the shell script directly:")
    print("    ./scripts/run_app.sh")
    print("=" * 80)
    sys.exit(1)

# Import our modules after env variables are loaded
try:
    from browser_use_ui.ui.ui_builder import UIBuilder, THEME_MAP
except ImportError as e:
    print(f"ERROR: Failed to import UI modules: {e}")
    print("Please ensure all dependencies are installed by running:")
    print("    source venv/bin/activate && pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point for the Browser Use application."""
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Gradio UI for Browser Agent")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=str, default="7788", help="Port to listen on")
    parser.add_argument(
        "--theme", 
        type=str, 
        default="Ocean", 
        choices=THEME_MAP.keys(), 
        help="Theme to use for the UI"
    )
    args = parser.parse_args()
    
    # Create and launch the UI
    ui_builder = UIBuilder(theme_name=args.theme)
    ui_builder.launch(server_name=args.ip, server_port=int(args.port))

if __name__ == '__main__':
    main() 