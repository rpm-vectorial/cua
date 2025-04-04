import os
import json
import logging
import gradio as gr
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ComponentManager:
    """
    Manages UI components for persistence and configuration.
    Allows saving and loading UI state.
    """
    
    def __init__(self):
        self.components = {}
        
    def register_component(self, name: str, component: gr.components.Component) -> None:
        """
        Register a UI component for management.
        
        Args:
            name: Unique identifier for the component
            component: Gradio component to register
        """
        if name in self.components:
            logger.warning(f"Component {name} already registered, overwriting")
            
        self.components[name] = component
        logger.debug(f"Registered component: {name}")
        
    def get_component(self, name: str) -> Optional[gr.components.Component]:
        """
        Get a registered component by name.
        
        Args:
            name: Name of the component
            
        Returns:
            The component or None if not found
        """
        return self.components.get(name)
        
    def get_all_components(self) -> List[gr.components.Component]:
        """Get all registered components"""
        return list(self.components.values())
        
    def save_current_config(self) -> Dict[str, Any]:
        """
        Save the current configuration of all components.
        
        Returns:
            Information about the saved configuration
        """
        try:
            # Create config directory if it doesn't exist
            os.makedirs("configs", exist_ok=True)
            
            # Get values from all interactive components
            config = {}
            for name, component in self.components.items():
                # Skip components without a value attribute
                if not hasattr(component, "value"):
                    continue
                    
                # Get the value if it's a supported type
                try:
                    value = component.value
                    if value is not None:
                        # Convert to JSON-compatible value if needed
                        if isinstance(value, (str, bool, int, float, list, dict)):
                            config[name] = value
                except Exception as e:
                    logger.warning(f"Could not get value from component {name}: {e}")
            
            # Save to file
            import time
            timestamp = int(time.time())
            filename = f"configs/ui_config_{timestamp}.json"
            
            with open(filename, "w") as f:
                json.dump(config, f, indent=2)
                
            return {"status": "success", "message": f"Config saved to {filename}", "config": filename}
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return {"status": "error", "message": f"Error saving configuration: {str(e)}"}
            
    def update_ui_from_config(self, config_file) -> Dict[str, Any]:
        """
        Update UI components from a configuration file.
        
        Args:
            config_file: Path to the configuration file or uploaded file object
            
        Returns:
            Dictionary with status message
        """
        try:
            # Get file path from uploaded file or direct path
            file_path = config_file.name if hasattr(config_file, "name") else config_file
            
            # Check if file exists
            if not os.path.exists(file_path):
                return {"status": "error", "message": f"Config file not found: {file_path}"}
                
            # Load config
            with open(file_path, "r") as f:
                config = json.load(f)
                
            # Update component values
            updated = 0
            for name, value in config.items():
                component = self.get_component(name)
                if component and hasattr(component, "value"):
                    try:
                        component.value = value
                        updated += 1
                    except Exception as e:
                        logger.warning(f"Could not update component {name}: {e}")
                        
            return {
                "status": "success", 
                "message": f"Updated {updated} components from {file_path}"
            }
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {"status": "error", "message": f"Error loading configuration: {str(e)}"}

def scan_and_register_components(blocks: gr.Blocks, component_manager: ComponentManager) -> int:
    """
    Scan a Gradio Blocks object and register all interactive components.
    
    Args:
        blocks: Gradio Blocks object to scan
        component_manager: ComponentManager to register components with
        
    Returns:
        Number of components registered
    """
    def traverse_blocks(block, prefix=""):
        registered = 0

        # Process block's components
        if hasattr(block, "children"):
            for i, child in enumerate(block.children):
                if isinstance(child, gr.components.Component):
                    # Skip buttons
                    if getattr(child, "interactive", False) and not isinstance(child, gr.Button):
                        name = f"{prefix}component_{i}"
                        if hasattr(child, "label") and child.label:
                            # Use label as part of the name
                            label = child.label
                            name = f"{prefix}{label}"
                        component_manager.register_component(name, child)
                        registered += 1
                elif hasattr(child, "children"):
                    # Recursively process nested Blocks
                    new_prefix = f"{prefix}block_{i}_"
                    registered += traverse_blocks(child, new_prefix)

        return registered

    total = traverse_blocks(blocks)
    logger.info(f"Total registered components: {total}")
    return total 