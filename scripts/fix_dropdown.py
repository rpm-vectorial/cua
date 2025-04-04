#!/usr/bin/env python3
"""
Script to fix the UI dropdown issue by patching model names
"""
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Path to the utils file
    utils_file = Path('src/utils/llm_utils.py')
    
    if not utils_file.exists():
        logger.error(f"Could not find file: {utils_file}")
        return
    
    # Read the file content
    with open(utils_file, 'r') as f:
        content = f.read()
    
    # Extract the MODEL_NAMES definition
    if 'MODEL_NAMES = {' not in content:
        logger.error("Could not find MODEL_NAMES dictionary in the file")
        return
    
    # Update the content to ensure anthropic models are properly defined
    updated_content = content.replace(
        'MODEL_NAMES = {',
        '''MODEL_NAMES = {
    "anthropic": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],'''
    )
    
    # Write the updated content
    with open(utils_file, 'w') as f:
        f.write(updated_content)
    
    logger.info(f"Updated {utils_file} with correct anthropic models")
    logger.info("Please restart the application for changes to take effect")

if __name__ == "__main__":
    main() 