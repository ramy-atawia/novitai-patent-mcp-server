"""
LLM Client Service

Handles communication with Azure OpenAI and other LLM providers.
Provides a unified interface for text generation, summarization, and analysis.
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import openai
from openai import AzureOpenAI
import json

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for interacting with Large Language Models."""
    
    def __init__(self, azure_openai_api_key: Optional[str] = None,
                 azure_openai_endpoint: Optional[str] = None,
                 azure_openai_deployment: Optional[str] = None,
                 model_name: str = "gpt-4"):
        """
        Initialize the LLM client.
        
        Args:
            azure_openai_api_key: Azure OpenAI API key
            azure_openai_endpoint: Azure OpenAI endpoint URL
            azure_openai_deployment: Azure OpenAI deployment name
            model_name: Model name to use
        """
        self.azure_openai_api_key = azure_openai_api_key
        self.azure_openai_endpoint = azure_openai_endpoint
        self.azure_openai_deployment = azure_openai_deployment
        self.model_name = model_name
        
        # Initialize Azure OpenAI client
        if azure_openai_api_key and azure_openai_endpoint:
            try:
                self.client = AzureOpenAI(
                    api_key=azure_openai_api_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=azure_openai_endpoint,
                    timeout=300.0
                )
                self.azure_deployment = azure_openai_deployment or "gpt-4o-mini"
                self.llm_available = True
                logger.info(f"Azure OpenAI client initialized with deployment: {self.azure_deployment}")
            except Exception as e:
                logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
                self.client = None
                self.llm_available = False
        else:
            self.client = None
            self.llm_available = False
            logger.warning("Azure OpenAI not configured - LLM features disabled")
    
    def generate_text(self, prompt: str, max_tokens: int = 1000, 
                     temperature: float = 0.7, system_message: Optional[str] = None, 
                     max_retries: int = 3) -> Dict[str, Any]:
        """
        Generate text using the LLM.
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 2.0)
            system_message: Optional system message
            
        Returns:
            Dictionary containing generated text and metadata
        """
        try:
            if not self.llm_available:
                return self._create_error_result("LLM not available")
            
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # Make API call with retry logic
            last_error = None
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.azure_openai_deployment,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                    break  # Success, exit retry loop
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"LLM API call failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise e
            
            # Debug logging
            logger.info(f"Azure OpenAI response type: {type(response)}")
            logger.info(f"Response choices: {response.choices}")
            logger.info(f"First choice message content type: {type(response.choices[0].message.content)}")
            logger.info(f"First choice message content: {response.choices[0].message.content}")
            
            # Extract response
            generated_text = response.choices[0].message.content
            usage = response.usage
            
            return {
                "success": True,
                "text": generated_text,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
                },
                "model": self.azure_openai_deployment,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return self._create_error_result(f"Text generation failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if LLM is available."""
        return self.llm_available
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            "available": self.llm_available,
            "provider": "Azure OpenAI" if self.llm_available else "None",
            "model": self.azure_openai_deployment if self.llm_available else "None",
            "endpoint": self.azure_openai_endpoint if self.llm_available else "None"
        }
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error result."""
        return {
            "success": False,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        }


# Global instance for easy access
def create_llm_client():
    """Create LLM client with environment configuration."""
    try:
        from ..core.config import get_azure_openai_config, is_azure_openai_configured
    except ImportError:
        # Fallback to absolute import if relative fails
        try:
            from app.core.config import get_azure_openai_config, is_azure_openai_configured
        except ImportError:
            logger.error("Failed to import config functions")
            return LLMClient()
    
    if is_azure_openai_configured():
        config = get_azure_openai_config()
        return LLMClient(
            azure_openai_api_key=config['api_key'],
            azure_openai_endpoint=config['endpoint'],
            azure_openai_deployment=config['deployment']
        )
    else:
        logger.warning("Azure OpenAI not configured - creating LLM client without credentials")
        return LLMClient()

# Lazy-loaded global instance to avoid import errors
_llm_client_instance = None

def get_llm_client():
    """Get the LLM client instance, creating it if necessary."""
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = create_llm_client()
    return _llm_client_instance




