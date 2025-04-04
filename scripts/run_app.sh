#!/bin/bash
# Run App Script

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Using existing virtual environment."
else
    echo "No virtual environment found. Using system Python."
fi

# Source the .env file to get API keys
if [ -f ".env" ]; then
    # Export the keys directly from the file
    export $(grep -v '^#' .env | xargs)
    # Confirm key is set
    echo "API keys set from .env file"
fi

# Run the app with specified or default parameters
python browser_use_app.py "$@" 