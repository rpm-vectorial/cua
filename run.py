#!/usr/bin/env python3
"""
Run script for Browser Use Application

This script is a wrapper to run the application with the appropriate environment
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a command and capture output"""
    try:
        result = subprocess.run(
            cmd, 
            shell=shell, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True
        )
        return result.returncode, result.stdout
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output

def main():
    """Run the browser use app"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the project directory
    os.chdir(current_dir)
    
    # Set up environment with API keys
    print("Setting up API keys from .env file...")
    api_key_script = os.path.join(current_dir, "scripts", "set_api_keys.py")
    if os.path.exists(api_key_script):
        # Make the script executable if it's not already
        if not os.access(api_key_script, os.X_OK):
            os.chmod(api_key_script, 0o755)
        
        # Run the API key script
        run_command([sys.executable, api_key_script])
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    # Look for the shell script first
    run_script = os.path.join(current_dir, "scripts", "run_app.sh")
    
    if os.path.exists(run_script):
        # Make the script executable if it's not already
        if not os.access(run_script, os.X_OK):
            os.chmod(run_script, 0o755)
        
        print(f"Running with script: {run_script}")
        # Forward any arguments to the shell script
        cmd = [run_script] + sys.argv[1:]
        return_code = subprocess.call(cmd)
        sys.exit(return_code)
    
    # If the shell script doesn't exist, try the app directly
    app_script = os.path.join(current_dir, "browser_use_app.py")
    
    if os.path.exists(app_script):
        if not in_venv:
            print("Using existing virtual environment.")
        
        print(f"Running application: {app_script}")
        # Default arguments for the app if none are provided
        if len(sys.argv) == 1:
            cmd = [sys.executable, app_script, "--ip", "127.0.0.1", "--port", "7788"]
        else:
            cmd = [sys.executable, app_script] + sys.argv[1:]
        
        return_code = subprocess.call(cmd)
        sys.exit(return_code)
    
    print("ERROR: Could not find application entry point.")
    print("Please ensure either 'scripts/run_app.sh' or 'browser_use_app.py' exists.")
    sys.exit(1)

if __name__ == "__main__":
    main() 