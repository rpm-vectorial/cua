#!/usr/bin/env python3
"""
Script to set API keys from .env file
"""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Read API keys from .env and set them in the environment."""
    # Find the project root (location of .env file)
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / '.env'
    
    if not env_path.exists():
        logger.error(f".env file not found at {env_path}")
        sys.exit(1)
    
    logger.info(f"Reading API keys from {env_path}")
    
    # Read .env file line by line
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    # Set API keys in environment
    api_keys = [
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'GOOGLE_API_KEY',
        'MISTRAL_API_KEY'
    ]
    
    # Export keys
    for key in api_keys:
        if key in env_vars and env_vars[key]:
            os.environ[key] = env_vars[key]
            # Print masked key for security
            masked_key = f"{env_vars[key][:5]}...{env_vars[key][-5:]}" if len(env_vars[key]) > 10 else "***"
            logger.info(f"Set {key}={masked_key}")
        else:
            logger.warning(f"{key} not found or empty in .env file")
    
    logger.info("API keys set successfully")
    
if __name__ == "__main__":
    main() 