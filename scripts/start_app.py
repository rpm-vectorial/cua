#!/usr/bin/env python3
"""
Startup wrapper script to ensure the application runs with the correct Python environment.
This script will detect whether it's running in the virtual environment and take
appropriate action.
"""

import os
import sys
import subprocess

def is_in_virtualenv():
    """Check if we're running in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def main():
    # Check if we're in the virtual environment
    if is_in_virtualenv():
        print("Running in virtual environment, launching application directly...")
        os.execv(sys.executable, [sys.executable, 'browser_use_app.py', '--ip', '127.0.0.1', '--port', '7788'])
    else:
        # We're not in the virtual environment, run the shell script instead
        print("Not in virtual environment. Running via shell script...")
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_app.sh')
        
        # Make sure the script is executable
        try:
            os.chmod(script_path, 0o755)  # rwxr-xr-x
        except Exception as e:
            print(f"Warning: couldn't set executable permission: {e}")
        
        # Use os.execv to replace the current process with the shell script
        os.execv('/bin/bash', ['/bin/bash', script_path])

if __name__ == '__main__':
    main() 