import os
import logging
import asyncio
from typing import Dict, Any, List, Tuple, Optional

import gradio as gr

from browser_use_ui.browser.browser_manager import BrowserManager
from browser_use_ui.agents.agent_manager import AgentManager
from browser_use_ui.utils.env_utils import resolve_sensitive_env_variables
from browser_use_ui.utils.file_utils import get_latest_files, ensure_directories, capture_screenshot
from browser_use_ui.utils.llm_utils import get_llm_model, MissingAPIKeyError

logger = logging.getLogger(__name__)

class UIHandlers:
    """
    Handles UI events and coordinates actions between UI and backend components.
    """
    
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.agent_manager = AgentManager()
        
    async def stop_agent(self) -> Tuple[gr.update, gr.update]:
        """
        Stop the running agent.
        
        Returns:
            Updates for the stop and run buttons
        """
        try:
            self.agent_manager.stop_agent()
            
            # Update UI immediately
            message = "Stop requested - the agent will halt at the next safe point"
            logger.info(f"🛑 {message}")

            return (
                gr.update(value="Stopping...", interactive=False),  # stop_button
                gr.update(interactive=False),  # run_button
            )
        except Exception as e:
            error_msg = f"Error during stop: {str(e)}"
            logger.error(error_msg)
            return (
                gr.update(value="Stop", interactive=True),
                gr.update(interactive=True)
            )
            
    async def run_browser_agent(
            self,
            agent_type: str,
            llm_provider: str,
            llm_model_name: str,
            llm_num_ctx: int,
            llm_temperature: float,
            llm_base_url: str,
            llm_api_key: str,
            use_own_browser: bool,
            keep_browser_open: bool,
            headless: bool,
            disable_security: bool,
            window_w: int,
            window_h: int,
            save_recording_path: str,
            save_agent_history_path: str,
            save_trace_path: str,
            enable_recording: bool,
            task: str,
            add_infos: str,
            max_steps: int,
            use_vision: bool,
            max_actions_per_step: int,
            tool_calling_method: str,
            chrome_cdp: str,
            max_input_tokens: int
    ) -> Tuple:
        """
        Run a browser agent with the specified configuration.
        
        Returns:
            Tuple of result values for UI update
        """
        try:
            # Disable recording if not enabled
            if not enable_recording:
                save_recording_path = None

            # Ensure directories exist
            ensure_directories(
                save_recording_path,
                save_agent_history_path,
                save_trace_path
            )

            # Process sensitive environment variables in task
            task = resolve_sensitive_env_variables(task)

            # Get LLM model
            llm = get_llm_model(
                provider=llm_provider,
                model_name=llm_model_name,
                num_ctx=llm_num_ctx,
                temperature=llm_temperature,
                base_url=llm_base_url,
                api_key=llm_api_key,
            )

            # Set up browser
            extra_chromium_args = [f"--window-size={window_w},{window_h}"]
            cdp_url = chrome_cdp if chrome_cdp else None

            # Initialize browser with appropriate type
            browser_type = "custom" if agent_type == "custom" else "default"
            await self.browser_manager.initialize_browser(
                headless=headless,
                disable_security=disable_security,
                cdp_url=cdp_url,
                extra_chromium_args=extra_chromium_args,
                use_own_browser=use_own_browser,
                browser_type=browser_type
            )

            # Initialize browser context
            await self.browser_manager.initialize_context(
                window_width=window_w,
                window_height=window_h,
                save_trace_path=save_trace_path,
                save_recording_path=save_recording_path
            )

            # Create and run agent
            await self.agent_manager.create_agent(
                agent_type=agent_type,
                task=task,
                llm=llm,
                browser_manager=self.browser_manager,
                use_vision=use_vision,
                max_actions_per_step=max_actions_per_step,
                tool_calling_method=tool_calling_method,
                max_input_tokens=max_input_tokens,
                add_infos=add_infos
            )
            
            # Run the agent
            result = await self.agent_manager.run_agent(max_steps=max_steps)
            
            # Save agent history
            history_file = self.agent_manager.save_history(save_agent_history_path)
            
            # Get the latest trace file
            trace_file = get_latest_files(save_trace_path).get('.zip')
            
            # Get the animated GIF path
            gif_path = os.path.join(os.path.dirname(__file__), "..", "..", "agent_history.gif")
            
            # Clean up resources if needed
            if not keep_browser_open:
                await self.browser_manager.close_browser()
                
            # Reset agent state
            self.agent_manager.reset_agent()

            return (
                result["final_result"],
                result["errors"],
                result["model_actions"],
                result["model_thoughts"],
                gif_path,
                trace_file,
                history_file,
                gr.update(value="Stop", interactive=True),  # Re-enable stop button
                gr.update(interactive=True)  # Re-enable run button
            )

        except MissingAPIKeyError as e:
            logger.error(str(e))
            raise gr.Error(str(e), print_exception=False)

        except Exception as e:
            import traceback
            traceback.print_exc()
            errors = str(e) + "\n" + traceback.format_exc()
            return (
                '',  # final_result
                errors,  # errors
                '',  # model_actions
                '',  # model_thoughts
                None,  # gif_path
                None,  # trace_file
                None,  # history_file
                gr.update(value="Stop", interactive=True),  # Re-enable stop button
                gr.update(interactive=True)  # Re-enable run button
            )
    
    async def run_with_stream(
            self,
            agent_type: str,
            llm_provider: str,
            llm_model_name: str,
            llm_num_ctx: int,
            llm_temperature: float,
            llm_base_url: str,
            llm_api_key: str,
            use_own_browser: bool,
            keep_browser_open: bool,
            headless: bool,
            disable_security: bool,
            window_w: int,
            window_h: int,
            save_recording_path: str,
            save_agent_history_path: str,
            save_trace_path: str,
            enable_recording: bool,
            task: str,
            add_infos: str,
            max_steps: int,
            use_vision: bool,
            max_actions_per_step: int,
            tool_calling_method: str,
            chrome_cdp: str,
            max_input_tokens: int
    ):
        """
        Run an agent with live streaming of browser view.
        
        Yields:
            UI updates at each step
        """
        stream_vw = 80
        stream_vh = int(80 * window_h // window_w)
        
        if not headless:
            # For non-headless mode, just run normally without streaming
            result = await self.run_browser_agent(
                agent_type=agent_type,
                llm_provider=llm_provider,
                llm_model_name=llm_model_name,
                llm_num_ctx=llm_num_ctx,
                llm_temperature=llm_temperature,
                llm_base_url=llm_base_url,
                llm_api_key=llm_api_key,
                use_own_browser=use_own_browser,
                keep_browser_open=keep_browser_open,
                headless=headless,
                disable_security=disable_security,
                window_w=window_w,
                window_h=window_h,
                save_recording_path=save_recording_path,
                save_agent_history_path=save_agent_history_path,
                save_trace_path=save_trace_path,
                enable_recording=enable_recording,
                task=task,
                add_infos=add_infos,
                max_steps=max_steps,
                use_vision=use_vision,
                max_actions_per_step=max_actions_per_step,
                tool_calling_method=tool_calling_method,
                chrome_cdp=chrome_cdp,
                max_input_tokens=max_input_tokens
            )
            # Add HTML content at the start of the result array
            yield [gr.update(visible=False)] + list(result)
        else:
            try:
                # Run the browser agent in the background
                agent_task = asyncio.create_task(
                    self.run_browser_agent(
                        agent_type=agent_type,
                        llm_provider=llm_provider,
                        llm_model_name=llm_model_name,
                        llm_num_ctx=llm_num_ctx,
                        llm_temperature=llm_temperature,
                        llm_base_url=llm_base_url,
                        llm_api_key=llm_api_key,
                        use_own_browser=use_own_browser,
                        keep_browser_open=keep_browser_open,
                        headless=headless,
                        disable_security=disable_security,
                        window_w=window_w,
                        window_h=window_h,
                        save_recording_path=save_recording_path,
                        save_agent_history_path=save_agent_history_path,
                        save_trace_path=save_trace_path,
                        enable_recording=enable_recording,
                        task=task,
                        add_infos=add_infos,
                        max_steps=max_steps,
                        use_vision=use_vision,
                        max_actions_per_step=max_actions_per_step,
                        tool_calling_method=tool_calling_method,
                        chrome_cdp=chrome_cdp,
                        max_input_tokens=max_input_tokens
                    )
                )

                # Initialize values for streaming
                html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Using browser...</h1>"
                final_result = errors = model_actions = model_thoughts = ""
                recording_gif = trace = history_file = None

                # Periodically update the stream while the agent task is running
                while not agent_task.done():
                    try:
                        encoded_screenshot = await capture_screenshot(self.browser_manager.browser_context)
                        if encoded_screenshot is not None:
                            html_content = f'<img src="data:image/jpeg;base64,{encoded_screenshot}" style="width:{stream_vw}vw; height:{stream_vh}vh ; border:1px solid #ccc;">'
                        else:
                            html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>"
                    except Exception as e:
                        html_content = f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>"

                    agent_state = self.agent_manager.get_agent_state()
                    if agent_state.stopped:
                        yield [
                            gr.HTML(value=html_content, visible=True),
                            final_result,
                            errors,
                            model_actions,
                            model_thoughts,
                            recording_gif,
                            trace,
                            history_file,
                            gr.update(value="Stopping...", interactive=False),  # stop_button
                            gr.update(interactive=False),  # run_button
                        ]
                        break
                    else:
                        yield [
                            gr.HTML(value=html_content, visible=True),
                            final_result,
                            errors,
                            model_actions,
                            model_thoughts,
                            recording_gif,
                            trace,
                            history_file,
                            gr.update(),  # Stop button
                            gr.update()  # Run button
                        ]
                    await asyncio.sleep(0.1)

                # Once the agent task completes, get the results
                try:
                    result = await agent_task
                    final_result, errors, model_actions, model_thoughts, recording_gif, trace, history_file, stop_button, run_button = result
                except gr.Error:
                    final_result = ""
                    model_actions = ""
                    model_thoughts = ""
                    recording_gif = trace = history_file = None
                except Exception as e:
                    errors = f"Agent error: {str(e)}"

                yield [
                    gr.HTML(value=html_content, visible=True),
                    final_result,
                    errors,
                    model_actions,
                    model_thoughts,
                    recording_gif,
                    trace,
                    history_file,
                    gr.update(value="Stop", interactive=True),  # stop_button
                    gr.update(interactive=True)  # run_button
                ]

            except Exception as e:
                import traceback
                yield [
                    gr.HTML(
                        value=f"<h1 style='width:{stream_vw}vw; height:{stream_vh}vh'>Waiting for browser session...</h1>",
                        visible=True),
                    "",
                    f"Error: {str(e)}\n{traceback.format_exc()}",
                    "",
                    "",
                    None,
                    None,
                    None,
                    gr.update(value="Stop", interactive=True),  # Re-enable stop button
                    gr.update(interactive=True)  # Re-enable run button
                ]
                
    async def close_browser(self) -> None:
        """Close the browser if it's open."""
        await self.browser_manager.close_browser() 