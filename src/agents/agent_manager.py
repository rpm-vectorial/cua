import os
import logging
import asyncio
from typing import Dict, Any, Tuple, Optional, List, Union

from browser_use.agent.service import Agent
from src.agent.custom_agent import CustomAgent
from src.browser.browser_manager import BrowserManager
from src.controller.custom_controller import CustomController
from src.agent.custom_prompts import CustomSystemPrompt, CustomAgentMessagePrompt
from src.utils.agent_state import AgentState

logger = logging.getLogger(__name__)

class AgentManager:
    """
    Manages agent lifecycle and execution, abstracting away the complexity
    of agent initialization and operation.
    """
    
    def __init__(self):
        self.agent = None
        self.agent_state = AgentState()
        
    def get_agent_state(self) -> AgentState:
        """Get the current agent state"""
        return self.agent_state
        
    def is_agent_running(self) -> bool:
        """Check if an agent is currently running"""
        return self.agent is not None
        
    def stop_agent(self) -> None:
        """Request the agent to stop"""
        if self.agent:
            self.agent.stop()
            
        self.agent_state.request_stop()
        logger.info("Stop requested - the agent will halt at the next safe point")
        
    async def create_agent(
        self,
        agent_type: str,
        task: str,
        llm: Any,
        browser_manager: BrowserManager,
        use_vision: bool = True,
        max_actions_per_step: int = 10,
        tool_calling_method: str = "auto",
        max_input_tokens: int = 128000,
        add_infos: str = "",
    ) -> None:
        """
        Create an agent based on the specified type.
        
        Args:
            agent_type: Type of agent to create ("org" or "custom")
            task: Task for the agent to perform
            llm: Language model to use
            browser_manager: Browser manager instance
            use_vision: Whether to use vision capabilities
            max_actions_per_step: Maximum actions per step
            tool_calling_method: Method for calling tools
            max_input_tokens: Maximum input tokens
            add_infos: Additional information for the agent
        """
        if agent_type == "org":
            self.agent = Agent(
                task=task,
                llm=llm,
                use_vision=use_vision,
                browser=browser_manager.browser,
                browser_context=browser_manager.browser_context,
                max_actions_per_step=max_actions_per_step,
                tool_calling_method=tool_calling_method,
                max_input_tokens=max_input_tokens,
                generate_gif=True
            )
        elif agent_type == "custom":
            controller = CustomController()
            self.agent = CustomAgent(
                task=task,
                add_infos=add_infos,
                use_vision=use_vision,
                llm=llm,
                browser=browser_manager.browser,
                browser_context=browser_manager.browser_context,
                controller=controller,
                system_prompt_class=CustomSystemPrompt,
                agent_prompt_class=CustomAgentMessagePrompt,
                max_actions_per_step=max_actions_per_step,
                tool_calling_method=tool_calling_method,
                max_input_tokens=max_input_tokens,
                generate_gif=True
            )
        else:
            raise ValueError(f"Invalid agent type: {agent_type}")
            
        logger.info(f"Created {agent_type} agent for task: {task[:50]}...")
        
    async def run_agent(self, max_steps: int = 100) -> Dict[str, Any]:
        """
        Run the agent and return the results.
        
        Args:
            max_steps: Maximum number of steps to run
            
        Returns:
            Dictionary containing the results
        """
        if not self.agent:
            raise ValueError("Agent must be created before running")
            
        try:
            history = await self.agent.run(max_steps=max_steps)
            
            return {
                "final_result": history.final_result(),
                "errors": history.errors(),
                "model_actions": history.model_actions(),
                "model_thoughts": history.model_thoughts(),
                "agent_id": self.agent.state.agent_id
            }
        except Exception as e:
            import traceback
            error_msg = str(e) + "\n" + traceback.format_exc()
            logger.error(f"Error running agent: {error_msg}")
            return {
                "final_result": "",
                "errors": error_msg,
                "model_actions": "",
                "model_thoughts": "",
                "agent_id": self.agent.state.agent_id if self.agent and hasattr(self.agent, "state") else None
            }
            
    def save_history(self, save_path: str) -> Optional[str]:
        """
        Save the agent history to a file.
        
        Args:
            save_path: Directory to save the history to
            
        Returns:
            Path to the saved history file or None if unable to save
        """
        if not self.agent:
            return None
            
        try:
            os.makedirs(save_path, exist_ok=True)
            history_file = os.path.join(save_path, f"{self.agent.state.agent_id}.json")
            self.agent.save_history(history_file)
            return history_file
        except Exception as e:
            logger.error(f"Error saving agent history: {e}")
            return None
            
    def reset_agent(self) -> None:
        """Reset the agent state"""
        self.agent = None
        self.agent_state.clear_stop() 