import os
import glob
import logging
import base64
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

def get_latest_files(directory: Optional[str]) -> Dict[str, str]:
    """
    Get the latest files in a directory by file extension.
    
    Args:
        directory: Directory to search in
        
    Returns:
        Dictionary mapping file extensions to latest file paths
    """
    if not directory or not os.path.exists(directory):
        return {}
        
    result = {}
    
    try:
        # List all files and their modification times
        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1]
                files.append((filepath, os.path.getmtime(filepath), ext))
                
        # Group by extension and get the latest for each
        for filepath, mtime, ext in sorted(files, key=lambda x: x[1], reverse=True):
            if ext not in result:
                result[ext] = filepath
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {e}")
        
    return result

def list_recordings(save_recording_path: str) -> List[tuple]:
    """
    List all recordings in the given directory.
    
    Args:
        save_recording_path: Path to the recordings directory
        
    Returns:
        List of tuples (file_path, display_name) for all video files
    """
    if not os.path.exists(save_recording_path):
        return []

    # Get all video files
    recordings = (
        glob.glob(os.path.join(save_recording_path, "*.[mM][pP]4")) + 
        glob.glob(os.path.join(save_recording_path, "*.[wW][eE][bB][mM]"))
    )

    # Sort recordings by creation time (oldest first)
    recordings.sort(key=os.path.getctime)

    # Add numbering to the recordings
    numbered_recordings = []
    for idx, recording in enumerate(recordings, start=1):
        filename = os.path.basename(recording)
        numbered_recordings.append((recording, f"{idx}. {filename}"))

    return numbered_recordings

def ensure_directories(*paths: str) -> None:
    """
    Ensure that the specified directories exist.
    
    Args:
        *paths: Directory paths to create
    """
    for path in paths:
        if path:
            os.makedirs(path, exist_ok=True)
            logger.debug(f"Ensured directory exists: {path}")

async def capture_screenshot(browser_context) -> Optional[str]:
    """
    Capture a screenshot from the browser context.
    
    Args:
        browser_context: Browser context to capture from
        
    Returns:
        Base64-encoded screenshot or None if unable to capture
    """
    if browser_context is None:
        return None
        
    try:
        pages = await browser_context.get_pages()
        if not pages:
            return None
            
        screenshot_bytes = await pages[0].screenshot(type="jpeg", quality=80)
        return base64.b64encode(screenshot_bytes).decode('utf-8')
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
        return None 