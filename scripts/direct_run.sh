#!/bin/bash
# Direct run script for the application
# This script will set the API key directly from the .env file before running

# Get the OpenAI API key from .env file
OPENAI_API_KEY=$(grep -o "OPENAI_API_KEY=.*" .env | cut -d "=" -f2)

# Print the API key setting for confirmation (masked for security)
echo "Setting OpenAI API key starting with: ${OPENAI_API_KEY:0:10}..."

# Export the key directly in the same shell
export OPENAI_API_KEY="$OPENAI_API_KEY"

# Run the application directly to avoid environment issues
echo "Running application with direct environment variables..."
venv/bin/python browser_use_app.py --ip 127.0.0.1 --port 7788 