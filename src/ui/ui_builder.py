import os
import logging
import gradio as gr
from typing import Dict, Any, Optional

from src.ui.component_manager import ComponentManager, scan_and_register_components
from src.ui.handlers import UIHandlers
from src.utils.llm_utils import MODEL_NAMES, update_model_dropdown
from src.utils.file_utils import list_recordings

logger = logging.getLogger(__name__)

# Define theme mapping
THEME_MAP = {
    "Default": gr.themes.Default(),
    "Soft": gr.themes.Soft(),
    "Monochrome": gr.themes.Monochrome(),
    "Glass": gr.themes.Glass(),
    "Origin": gr.themes.Origin(),
    "Citrus": gr.themes.Citrus(),
    "Ocean": gr.themes.Ocean(),
    "Base": gr.themes.Base()
}

class UIBuilder:
    """
    Builds and configures the Gradio UI.
    """
    
    def __init__(self, theme_name: str = "Ocean"):
        self.theme_name = theme_name
        self.component_manager = ComponentManager()
        self.ui_handlers = UIHandlers()
        self.demo = None
        
    def build_ui(self) -> gr.Blocks:
        """
        Build the complete UI.
        
        Returns:
            Configured Gradio Blocks interface
        """
        css = """
        .gradio-container {
            width: 60vw !important; 
            max-width: 60% !important; 
            margin-left: auto !important;
            margin-right: auto !important;
            padding-top: 20px !important;
        }
        .header-text {
            text-align: center;
            margin-bottom: 30px;
        }
        .theme-section {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
        }
        """

        with gr.Blocks(
                title="Browser Use WebUI", 
                theme=THEME_MAP[self.theme_name], 
                css=css
        ) as self.demo:
            with gr.Row():
                gr.Markdown(
                    """
                    # 🌐 Browser Use WebUI
                    ### Control your browser with AI assistance
                    """,
                    elem_classes=["header-text"],
                )

            with gr.Tabs() as tabs:
                # Tab 1: Agent Settings
                with gr.TabItem("⚙️ Agent Settings", id=1):
                    with gr.Group():
                        agent_type = gr.Radio(
                            ["org", "custom"],
                            label="Agent Type",
                            value="custom",
                            info="Select the type of agent to use",
                            interactive=True
                        )
                        with gr.Column():
                            max_steps = gr.Slider(
                                minimum=1,
                                maximum=200,
                                value=100,
                                step=1,
                                label="Max Run Steps",
                                info="Maximum number of steps the agent will take",
                                interactive=True
                            )
                            max_actions_per_step = gr.Slider(
                                minimum=1,
                                maximum=100,
                                value=10,
                                step=1,
                                label="Max Actions per Step",
                                info="Maximum number of actions the agent will take per step",
                                interactive=True
                            )
                        with gr.Column():
                            use_vision = gr.Checkbox(
                                label="Use Vision",
                                value=True,
                                info="Enable visual processing capabilities",
                                interactive=True
                            )
                            max_input_tokens = gr.Number(
                                label="Max Input Tokens",
                                value=128000,
                                precision=0,
                                interactive=True
                            )
                            tool_calling_method = gr.Dropdown(
                                label="Tool Calling Method",
                                value="auto",
                                interactive=True,
                                allow_custom_value=True,
                                choices=["auto", "json_schema", "function_calling"],
                                info="Tool Calls Function Name",
                                visible=False
                            )

                # Tab 2: LLM Settings
                with gr.TabItem("🔧 LLM Settings", id=2):
                    with gr.Group():
                        llm_provider = gr.Dropdown(
                            choices=[provider for provider in MODEL_NAMES.keys()],
                            label="LLM Provider",
                            value="openai",
                            info="Select your preferred language model provider",
                            interactive=True
                        )
                        llm_model_name = gr.Dropdown(
                            label="Model Name",
                            choices=MODEL_NAMES['openai'],
                            value="gpt-4o",
                            interactive=True,
                            allow_custom_value=True,
                            info="Select a model in the dropdown options or directly type a custom model name"
                        )
                        ollama_num_ctx = gr.Slider(
                            minimum=2 ** 8,
                            maximum=2 ** 16,
                            value=16000,
                            step=1,
                            label="Ollama Context Length",
                            info="Controls max context length model needs to handle (less = faster)",
                            visible=False,
                            interactive=True
                        )
                        llm_temperature = gr.Slider(
                            minimum=0.0,
                            maximum=2.0,
                            value=0.6,
                            step=0.1,
                            label="Temperature",
                            info="Controls randomness in model outputs",
                            interactive=True
                        )
                        with gr.Row():
                            llm_base_url = gr.Textbox(
                                label="Base URL",
                                value="",
                                info="API endpoint URL (if required)"
                            )
                            llm_api_key = gr.Textbox(
                                label="API Key",
                                type="password",
                                value="",
                                info="Your API key (leave blank to use .env)"
                            )

                # Tab 3: Browser Settings
                with gr.TabItem("🌐 Browser Settings", id=3):
                    with gr.Group():
                        with gr.Row():
                            use_own_browser = gr.Checkbox(
                                label="Use Own Browser",
                                value=False,
                                info="Use your existing browser instance",
                                interactive=True
                            )
                            keep_browser_open = gr.Checkbox(
                                label="Keep Browser Open",
                                value=False,
                                info="Keep Browser Open between Tasks",
                                interactive=True
                            )
                            headless = gr.Checkbox(
                                label="Headless Mode",
                                value=False,
                                info="Run browser without GUI",
                                interactive=True
                            )
                            disable_security = gr.Checkbox(
                                label="Disable Security",
                                value=True,
                                info="Disable browser security features",
                                interactive=True
                            )
                            enable_recording = gr.Checkbox(
                                label="Enable Recording",
                                value=True,
                                info="Enable saving browser recordings",
                                interactive=True
                            )

                        with gr.Row():
                            window_w = gr.Number(
                                label="Window Width",
                                value=1280,
                                info="Browser window width",
                                interactive=True
                            )
                            window_h = gr.Number(
                                label="Window Height",
                                value=1100,
                                info="Browser window height",
                                interactive=True
                            )

                        chrome_cdp = gr.Textbox(
                            label="CDP URL",
                            placeholder="http://localhost:9222",
                            value="",
                            info="CDP for Google remote debugging",
                            interactive=True,
                        )

                        save_recording_path = gr.Textbox(
                            label="Recording Path",
                            placeholder="e.g. ./tmp/record_videos",
                            value="./tmp/record_videos",
                            info="Path to save browser recordings",
                            interactive=True,
                        )

                        save_trace_path = gr.Textbox(
                            label="Trace Path",
                            placeholder="e.g. ./tmp/traces",
                            value="./tmp/traces",
                            info="Path to save Agent traces",
                            interactive=True,
                        )

                        save_agent_history_path = gr.Textbox(
                            label="Agent History Save Path",
                            placeholder="e.g., ./tmp/agent_history",
                            value="./tmp/agent_history",
                            info="Specify the directory where agent history should be saved.",
                            interactive=True,
                        )

                # Tab 4: Run Agent
                with gr.TabItem("🤖 Run Agent", id=4):
                    task = gr.Textbox(
                        label="Task Description",
                        lines=4,
                        placeholder="Enter your task here...",
                        value="go to google.com and type 'OpenAI' click search and give me the first url",
                        info="Describe what you want the agent to do",
                        interactive=True
                    )
                    add_infos = gr.Textbox(
                        label="Additional Information",
                        lines=3,
                        placeholder="Add any helpful context or instructions...",
                        info="Optional hints to help the LLM complete the task",
                        value="",
                        interactive=True
                    )

                    with gr.Row():
                        run_button = gr.Button("▶️ Run Agent", variant="primary", scale=2)
                        stop_button = gr.Button("⏹️ Stop", variant="stop", scale=1)

                    with gr.Row():
                        browser_view = gr.HTML(
                            value="<h1 style='width:80vw; height:50vh'>Waiting for browser session...</h1>",
                            label="Live Browser View",
                            visible=False
                        )

                    gr.Markdown("### Results")
                    with gr.Row():
                        with gr.Column():
                            final_result_output = gr.Textbox(
                                label="Final Result", lines=3, show_label=True
                            )
                        with gr.Column():
                            errors_output = gr.Textbox(
                                label="Errors", lines=3, show_label=True
                            )
                    with gr.Row():
                        with gr.Column():
                            model_actions_output = gr.Textbox(
                                label="Model Actions", lines=3, show_label=True, visible=False
                            )
                        with gr.Column():
                            model_thoughts_output = gr.Textbox(
                                label="Model Thoughts", lines=3, show_label=True, visible=False
                            )
                    recording_gif = gr.Image(label="Result GIF", format="gif")
                    trace_file = gr.File(label="Trace File")
                    agent_history_file = gr.File(label="Agent History")

                # Tab 5: Recordings
                with gr.TabItem("🎥 Recordings", id=7, visible=True):
                    recordings_gallery = gr.Gallery(
                        label="Recordings",
                        columns=3,
                        height="auto",
                        object_fit="contain"
                    )

                    refresh_button = gr.Button("🔄 Refresh Recordings", variant="secondary")

                # Tab 6: UI Configuration
                with gr.TabItem("📁 UI Configuration", id=8):
                    config_file_input = gr.File(
                        label="Load UI Settings from Config File",
                        file_types=[".json"],
                        interactive=True
                    )
                    with gr.Row():
                        load_config_button = gr.Button("Load Config", variant="primary")
                        save_config_button = gr.Button("Save UI Settings", variant="primary")

                    config_status = gr.Textbox(
                        label="Status",
                        lines=2,
                        interactive=False
                    )

            # Event handlers
            def update_ctx_visibility(provider):
                return gr.update(visible=provider == "ollama")

            # Bind the change event of llm_provider
            llm_provider.change(
                fn=update_ctx_visibility,
                inputs=llm_provider,
                outputs=ollama_num_ctx
            )

            # Update models when provider changes
            llm_provider.change(
                fn=lambda provider, api_key, base_url: update_model_dropdown(
                    provider=provider, 
                    api_key=api_key, 
                    base_url=base_url
                ),
                inputs=[llm_provider, llm_api_key, llm_base_url],
                outputs=llm_model_name
            )

            # Enable/disable recording path based on recording checkbox
            enable_recording.change(
                fn=lambda enabled: gr.update(interactive=enabled),
                inputs=enable_recording,
                outputs=save_recording_path
            )

            # Browser management
            use_own_browser.change(fn=self.ui_handlers.close_browser)
            keep_browser_open.change(fn=self.ui_handlers.close_browser)

            # Run and stop buttons
            run_button.click(
                fn=self.ui_handlers.run_with_stream,
                inputs=[
                    agent_type, llm_provider, llm_model_name, ollama_num_ctx, llm_temperature, llm_base_url,
                    llm_api_key, use_own_browser, keep_browser_open, headless, disable_security, window_w, window_h,
                    save_recording_path, save_agent_history_path, save_trace_path, enable_recording, task, add_infos, 
                    max_steps, use_vision, max_actions_per_step, tool_calling_method, chrome_cdp, max_input_tokens
                ],
                outputs=[
                    browser_view, final_result_output, errors_output, model_actions_output, model_thoughts_output,
                    recording_gif, trace_file, agent_history_file, stop_button, run_button
                ],
            )

            stop_button.click(
                fn=self.ui_handlers.stop_agent,
                inputs=[],
                outputs=[stop_button, run_button],
            )

            # Recordings gallery
            refresh_button.click(
                fn=list_recordings,
                inputs=save_recording_path,
                outputs=recordings_gallery
            )

            # Config management
            save_config_button.click(
                fn=self.component_manager.save_current_config,
                inputs=[],
                outputs=[config_status]
            )

            load_config_button.click(
                fn=self.component_manager.update_ui_from_config,
                inputs=[config_file_input],
                outputs=[config_status]
            )

            # Register components for configuration management
            scan_and_register_components(self.demo, self.component_manager)

        return self.demo
        
    def launch(self, server_name: str = "127.0.0.1", server_port: int = 7788) -> None:
        """
        Launch the UI server.
        
        Args:
            server_name: Server hostname
            server_port: Server port
        """
        if self.demo is None:
            self.build_ui()
            
        self.demo.launch(server_name=server_name, server_port=server_port) 