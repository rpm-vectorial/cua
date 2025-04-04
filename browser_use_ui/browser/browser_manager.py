import os
import logging
import asyncio
from typing import Optional, List, Dict, Any

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import (
    BrowserContextConfig,
    BrowserContextWindowSize
)
from browser_use_ui.browser.custom_browser import CustomBrowser
from browser_use_ui.browser.custom_context import CustomBrowserContext

logger = logging.getLogger(__name__)

class BrowserManager:
    """
    Manages browser instances and contexts to avoid global state
    and provide cleaner lifecycle management.
    """
    
    def __init__(self):
        self.browser = None
        self.browser_context = None
        
    async def initialize_browser(
        self, 
        headless: bool, 
        disable_security: bool, 
        cdp_url: str = None, 
        extra_chromium_args: List[str] = None,
        use_own_browser: bool = False,
        browser_type: str = "default"
    ) -> None:
        """
        Initialize a browser instance if one doesn't exist or if configuration has changed.
        
        Args:
            headless: Whether to run browser in headless mode
            disable_security: Whether to disable browser security features
            cdp_url: URL for Chrome DevTools Protocol
            extra_chromium_args: Additional Chrome command line arguments
            use_own_browser: Whether to use an existing browser instance
            browser_type: Type of browser to use ("default" or "custom")
        """
        # Default extra args
        if extra_chromium_args is None:
            extra_chromium_args = []
            
        # Handle Chrome path for own browser
        chrome_path = None
        if use_own_browser:
            chrome_path = os.getenv("CHROME_PATH", None)
            if chrome_path == "":
                chrome_path = None
                
            chrome_user_data = os.getenv("CHROME_USER_DATA", None)
            if chrome_user_data:
                extra_chromium_args += [f"--user-data-dir={chrome_user_data}"]
                
        # Initialize browser based on type
        if browser_type == "custom":
            self.browser = CustomBrowser(
                config=BrowserConfig(
                    headless=headless,
                    disable_security=disable_security,
                    cdp_url=cdp_url,
                    chrome_instance_path=chrome_path,
                    extra_chromium_args=extra_chromium_args,
                )
            )
        else:
            self.browser = Browser(
                config=BrowserConfig(
                    headless=headless,
                    disable_security=disable_security,
                    cdp_url=cdp_url,
                    chrome_instance_path=chrome_path,
                    extra_chromium_args=extra_chromium_args,
                )
            )
        
        logger.info(f"Initialized {browser_type} browser with headless={headless}")
        
    async def initialize_context(
        self,
        window_width: int,
        window_height: int,
        save_trace_path: Optional[str] = None,
        save_recording_path: Optional[str] = None
    ) -> None:
        """
        Initialize a browser context with specified configuration.
        
        Args:
            window_width: Browser window width
            window_height: Browser window height
            save_trace_path: Path to save traces (None to disable)
            save_recording_path: Path to save recordings (None to disable)
        """
        if self.browser is None:
            raise ValueError("Browser must be initialized before creating a context")
            
        self.browser_context = await self.browser.new_context(
            config=BrowserContextConfig(
                trace_path=save_trace_path,
                save_recording_path=save_recording_path,
                no_viewport=False,
                browser_window_size=BrowserContextWindowSize(
                    width=window_width, 
                    height=window_height
                ),
            )
        )
        
        logger.info(f"Initialized browser context with window size {window_width}x{window_height}")
        
    async def close_browser(self) -> None:
        """Close the browser and context if they exist."""
        if self.browser_context:
            await self.browser_context.close()
            self.browser_context = None
            logger.info("Closed browser context")
            
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("Closed browser")
            
    async def capture_screenshot(self) -> Optional[str]:
        """
        Capture a screenshot of the current browser window.
        
        Returns:
            Base64-encoded screenshot or None if unable to capture
        """
        if not self.browser_context:
            return None
            
        try:
            pages = await self.browser_context.get_pages()
            if not pages:
                return None
                
            # Get the first page
            page = pages[0]
            screenshot_bytes = await page.screenshot(type="jpeg", quality=80)
            
            import base64
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"Error capturing screenshot: {e}")
            return None 