#!/usr/bin/env python3
"""
Test script to verify Anthropic API key functionality
"""
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Get the API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    logger.info(f"Testing Anthropic API key: {api_key[:10]}...{api_key[-4:]}")
else:
    logger.error("Anthropic API key not found in environment variables")
    exit(1)

try:
    # Only import if API key exists
    from langchain_anthropic import ChatAnthropic
    
    # Initialize the model with a valid model name
    # Use one of: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
    model = ChatAnthropic(
        model="claude-3-haiku-20240307",
        anthropic_api_key=api_key
    )
    
    # Test the model with a simple prompt
    response = model.invoke("Hello, how are you today?")
    
    # Print the response
    logger.info("Anthropic API test successful!")
    logger.info(f"Response: {response.content}")
    
except ImportError:
    logger.error("Error importing langchain_anthropic. Make sure it's installed: pip install langchain-anthropic")
except Exception as e:
    logger.error(f"Error testing Anthropic API: {e}") 