#!/usr/bin/env python3
import os
import requests
import json
import logging
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from openai import OpenAI

logger = logging.getLogger(__name__)
class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def get_completion(self, messages: List[Dict[str, str]], model: str) -> Dict[str, str]:
        """Get completion from the LLM service."""
        pass

class OpenRouterClient(BaseLLMClient):
    """Client for OpenRouter API."""

    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

    def get_completion(self, messages: List[Dict[str, str]], model: str = None) -> Dict[str, str]:
        try:
            # Makes a POST request to /v1/chat/completions
            # Use default model for OpenRouter if none specified
            openrouter_model = model or "anthropic/claude-3.5-sonnet:beta"
            response = self.client.chat.completions.create(
                model=openrouter_model,
                messages=messages
            )
            return {
                'content': response.choices[0].message.content if response.choices else "No response generated",
                'model': response.model if hasattr(response, 'model') else openrouter_model
            }
        except Exception as e:
            return {
                'content': f"Error getting OpenRouter response: {str(e)}",
                'model': "error"
            }

class BedrockClient(BaseLLMClient):
    """Client for AWS Bedrock API."""

    def __init__(self):
        import boto3
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def get_completion(self, messages: List[Dict[str, str]], model: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> Dict[str, str]:
        try:
            # Convert messages to Claude's prompt format
            prompt = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])

            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": messages,
                "temperature": 0.5
            }

            response = self.client.invoke_model(
                modelId=model,
                body=json.dumps(body)
            )

            result = json.loads(response['body'].read())
            return {
                'content': result['content'][0]['text'] if result.get('content') else "No response generated",
                'model': model
            }
        except Exception as e:
            return {
                'content': f"Error getting Bedrock response: {str(e)}",
                'model': "error"
            }

class OllamaClient(BaseLLMClient):
    """Client for Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = None):
        base_url = base_url.rstrip('/')
        self.base_url = base_url
        self.default_model = default_model or os.getenv('OLLAMA_MODEL', 'deepseek-r1:1.5b')
        self.client = OpenAI(
            base_url=f"{base_url}/v1",  # Ollama's OpenAI-compatible endpoint
            api_key="ollama"  # Ollama doesn't require an API key, but OpenAI client needs a non-empty string
        )

    def ensure_model_pulled(self, model: str) -> None:
        """Ensure the model is pulled before using it."""
        import requests
        try:
            # POST request to check if model exists
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model}
            )

            if response.status_code == 404:
                print(f"Pulling model {model}... This may take a while...")
                response = requests.post(
                    f"{self.base_url}/api/pull",
                    json={"name": model},
                    stream=True
                )
                response.raise_for_status()

                # Print progress
                for line in response.iter_lines():
                    if line:
                        print(".", end="", flush=True)
                print("\nModel pulled successfully!")
        except Exception as e:
            print(f"Warning: Could not pull model: {str(e)}")

    def get_completion(self, messages: List[Dict[str, str]], model: str = None) -> Dict[str, str]:
        model = model or self.default_model
        try:
            # Ensure model is pulled before using it
            self.ensure_model_pulled(model)

            # Makes a POST request to /v1/chat/completions
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )

            return {
                'content': response.choices[0].message.content if response.choices else "No response generated",
                'model': f"ollama/{model}"
            }
        except Exception as e:
            error_msg = str(e)
            if "not found, try pulling it first" in error_msg:
                return {
                    'content': f"Model not found. Please run 'ollama pull {model}' first to download the model.",
                    'model': "error"
                }
            return {
                'content': f"Error getting Ollama response: {error_msg}",
                'model': "error"
            }

def get_llm_client() -> BaseLLMClient:
    """
    Factory function to create an LLM client based on environment variables.

    Environment variables:
    - LLM_PROVIDER: 'openrouter', 'ollama', or 'bedrock'
    - OPENROUTER_API_KEY: Required if using OpenRouter
    - OLLAMA_BASE_URL: Optional, defaults to http://localhost:11434
    - OLLAMA_MODEL: Optional, defaults to 'deepseek-r1:1.5b'
    - AWS_ACCESS_KEY_ID: Required if using Bedrock
    - AWS_SECRET_ACCESS_KEY: Required if using Bedrock
    """
    provider = os.getenv('LLM_PROVIDER', 'openrouter').lower()

    if provider == 'openrouter':
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required for OpenRouter")
        return OpenRouterClient(api_key)

    elif provider == 'ollama':
        base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        return OllamaClient(base_url)

    elif provider == 'bedrock':
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
        if not aws_access_key or not aws_secret:
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required for Bedrock")
        return BedrockClient()

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

def main():
    """Example usage of the LLM clients."""
    try:
        # Create client based on environment variables
        client = get_llm_client()

        # Example messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]

        # Get completion
        response = client.get_completion(messages)

        print(f"Response from {response['model']}:")
        print(response['content'])

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
