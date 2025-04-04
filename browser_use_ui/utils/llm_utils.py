import os
import logging
from typing import Dict, Any, Optional, List, Union

# Import LLM providers
from langchain_ollama import ChatOllama
from langchain.schema.language_model import BaseLanguageModel
from browser_use_ui.utils.llm import DeepSeekR1ChatOllama

logger = logging.getLogger(__name__)

# Define model names per provider
MODEL_NAMES = {
    "anthropic": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"],
    "openai": ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
    "anthropic": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
    "ollama": ["llama3", "llama2", "mistral", "mixtral", "phi3"],
    "google": ["gemini-pro", "gemini-pro-vision"],
    "mistral": ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"]
}

class MissingAPIKeyError(Exception):
    """Raised when an API key is required but not provided."""
    pass

def get_llm_model(
    provider: str,
    model_name: str,
    temperature: float = 0.0,
    num_ctx: int = 16000,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> BaseLanguageModel:
    """
    Get a language model based on the provider and model name.
    
    Args:
        provider: The LLM provider (openai, anthropic, ollama, etc.)
        model_name: The name of the model
        temperature: Model temperature (randomness)
        num_ctx: Context length for Ollama models
        base_url: Base URL for API (optional)
        api_key: API key (optional, will use environment variables if not provided)
        
    Returns:
        An initialized LLM
        
    Raises:
        MissingAPIKeyError: If an API key is required but not provided
        ValueError: If the provider is not supported
    """
    # Get API key from environment if not provided
    if not api_key:
        env_var_name = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var_name, None)
        # For debugging
        logger.debug(f"Retrieving API key from environment: {env_var_name}")
        logger.debug(f"API key found in environment: {'Yes' if api_key else 'No'}")
    
    # Handle providers
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        
        if not api_key:
            raise MissingAPIKeyError(
                "OpenAI API key required. Please provide it through the UI or set OPENAI_API_KEY environment variable."
            )
        
        logger.debug(f"Initializing ChatOpenAI with model: {model_name}")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=api_key,
            openai_api_base=base_url if base_url else None
        )
    
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        
        if not api_key:
            raise MissingAPIKeyError(
                "Anthropic API key required. Please provide it through the UI or set ANTHROPIC_API_KEY environment variable."
            )
            
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            anthropic_api_key=api_key,
            anthropic_api_url=base_url if base_url else None
        )
    
    elif provider == "ollama":
        # Ollama doesn't require API keys typically
        return ChatOllama(
            model=model_name,
            temperature=temperature,
            num_ctx=num_ctx,
            base_url=base_url if base_url else "http://localhost:11434"
        )
    
    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        if not api_key:
            raise MissingAPIKeyError(
                "Google API key required. Please provide it through the UI or set GOOGLE_API_KEY environment variable."
            )
            
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key
        )
    
    elif provider == "mistral":
        from langchain_mistralai import ChatMistralAI
        
        if not api_key:
            raise MissingAPIKeyError(
                "Mistral API key required. Please provide it through the UI or set MISTRAL_API_KEY environment variable."
            )
            
        return ChatMistralAI(
            model=model_name,
            temperature=temperature,
            mistral_api_key=api_key,
            mistral_api_base=base_url if base_url else None
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

def update_model_dropdown(
    provider: str, 
    api_key: Optional[str] = None, 
    base_url: Optional[str] = None
) -> List[str]:
    """
    Update the list of models for a given provider.
    
    Args:
        provider: The LLM provider
        api_key: API key (optional)
        base_url: Base URL for API (optional)
        
    Returns:
        List of available models
    """
    # For Ollama, try to get a list of models from the server
    if provider == "ollama" and base_url:
        try:
            import requests
            response = requests.get(f"{base_url}/api/tags")
            if response.status_code == 200:
                return [model["name"] for model in response.json()["models"]]
        except Exception as e:
            logger.warning(f"Failed to get Ollama models: {e}")
    
    # Return the predefined list of models
    return MODEL_NAMES.get(provider, []) 