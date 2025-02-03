#!/usr/bin/env python3
import os
import sys
from llm_clients import get_llm_client

def get_test_messages(provider: str) -> list:
    """Get test messages for a provider from environment variables"""
    system_content = os.getenv(f'{provider}_SYSTEM_CONTENT', 'You are a helpful assistant. Using anthropic/claude-3.5-sonnet by default for OpenRouter.')
    user_content = os.getenv(
        f'{provider}_USER_CONTENT',
        {
            'ollama': 'What is the difference between Python and JavaScript in one sentence?',
            'openrouter': 'Explain what a closure is in programming.',
            'bedrock': 'What are the SOLID principles in software engineering?'
        }.get(provider.lower(), 'Hello, how are you?')
    )
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def test_ollama():
    """Test the Ollama client"""
    print("\n=== Testing Ollama Client ===")
    try:
        os.environ['LLM_PROVIDER'] = 'ollama'
        client = get_llm_client()
        messages = get_test_messages('OLLAMA')
        print("Sending request to Ollama...")
        response = client.get_completion(messages)
        print(f"\nResponse from {response['model']}:")
        print(response['content'])
        return True
    except Exception as e:
        print(f"Error testing Ollama: {str(e)}")
        return False

def test_openrouter():
    """Test the OpenRouter client"""
    print("\n=== Testing OpenRouter Client ===")
    if 'OPENROUTER_API_KEY' not in os.environ:
        print("Skipping OpenRouter test: OPENROUTER_API_KEY not set")
        return False

    try:
        os.environ['LLM_PROVIDER'] = 'openrouter'
        client = get_llm_client()
        messages = get_test_messages('OPENROUTER')
        print("Sending request to OpenRouter...")
        response = client.get_completion(messages)
        print(f"\nResponse from {response['model']}:")
        print(response['content'])
        return True
    except Exception as e:
        print(f"Error testing OpenRouter: {str(e)}")
        return False

def test_bedrock():
    """Test the AWS Bedrock client"""
    print("\n=== Testing AWS Bedrock Client ===")
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    missing_vars = [var for var in required_vars if var not in os.environ]

    if missing_vars:
        print(f"Skipping Bedrock test: Missing environment variables: {', '.join(missing_vars)}")
        return False

    try:
        os.environ['LLM_PROVIDER'] = 'bedrock'
        client = get_llm_client()
        messages = get_test_messages('BEDROCK')
        print("Sending request to AWS Bedrock...")
        response = client.get_completion(messages)
        print(f"\nResponse from {response['model']}:")
        print(response['content'])
        return True
    except Exception as e:
        print(f"Error testing Bedrock: {str(e)}")
        return False

def main():
    """Run tests for all providers"""
    results = []

    # Test each provider
    results.append(("Ollama", test_ollama()))
    results.append(("OpenRouter", test_openrouter()))
    results.append(("AWS Bedrock", test_bedrock()))

    # Print summary
    print("\n=== Test Summary ===")
    for provider, success in results:
        status = "✓ Passed" if success else "✗ Failed/Skipped"
        print(f"{provider}: {status}")

    # Exit with error if all tests failed/skipped
    if not any(success for _, success in results):
        print("\nError: All tests failed or were skipped. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
