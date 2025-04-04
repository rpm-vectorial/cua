#!/usr/bin/env python3
"""
Script to modify UI configuration to use Anthropic provider
"""
import os
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Find config file locations
    config_dir = Path(os.path.expanduser("~/.browser_use"))
    os.makedirs(config_dir, exist_ok=True)
    
    config_file = config_dir / "ui_config.json"
    
    if not config_file.exists():
        # Create a new config with Anthropic settings
        config = {
            "llm_provider": "anthropic",
            "llm_model_name": "claude-3-haiku-20240307",
            "llm_temperature": 0.6,
            "llm_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "llm_base_url": os.getenv("ANTHROPIC_ENDPOINT", "https://api.anthropic.com")
        }
    else:
        # Load existing config and modify it
        with open(config_file, "r") as f:
            config = json.load(f)
        
        # Update provider settings
        config["llm_provider"] = "anthropic"
        config["llm_model_name"] = "claude-3-haiku-20240307"
        config["llm_api_key"] = os.getenv("ANTHROPIC_API_KEY", "")
        config["llm_base_url"] = os.getenv("ANTHROPIC_ENDPOINT", "https://api.anthropic.com")
    
    # Save the updated config
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Updated config file at {config_file}")
    logger.info("Next time you run the application, load the config file from:")
    logger.info("1. Go to the 'UI Configuration' tab")
    logger.info("2. Click 'Load Config'")
    logger.info("3. OR check the LLM provider in the UI - it should now be 'anthropic'")

if __name__ == "__main__":
    main() 