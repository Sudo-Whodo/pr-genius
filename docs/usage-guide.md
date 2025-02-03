# Usage Guide

This guide explains how to use PR Genius in different environments and with different LLM providers.

## Table of Contents

- [GitHub Action](#github-action)
- [Local Testing](#local-testing)
  - [Using test-local.sh](#using-test-localsh)
  - [Using test-action-local.sh](#using-test-action-localsh)
- [LLM Providers](#llm-providers)
  - [OpenRouter](#openrouter)
  - [AWS Bedrock](#aws-bedrock)
  - [Ollama](#ollama)
- [Customization](#customization)
  - [Review Prompts](#review-prompts)
  - [Models](#models)

## GitHub Action

To use PR Genius as a GitHub Action, add the following to your workflow:

```yaml
name: PR Analysis
on:
  pull_request:
    types: [opened, synchronize]
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    name: Analyze PR
    steps:
      - name: PR Analysis
        uses: sudo-whodo/pr-genius@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          provider: openrouter # or ollama, bedrock
          openrouter_api_key: ${{ secrets.OPENROUTER_API_KEY }} # if using OpenRouter
          model: anthropic/claude-3-sonnet # optional
          system_content: "Your custom review instructions" # optional
          docs_system_content: "Your custom docs review instructions" # optional
```

## Local Testing

### Using test-local.sh

For quick local testing with Docker:

```bash
# Test with OpenRouter
export GITHUB_TOKEN=your_token
export OPENROUTER_API_KEY=your_key
./examples/test-local.sh --provider openrouter --pr 3

# Test with Ollama
export GITHUB_TOKEN=your_token
./examples/test-local.sh --provider ollama --model deepseek-r1:1.5b --pr 3
```

### Testing Options

There are two ways to test the action:

#### 1. Using test-action-local.sh (Local Testing)

For testing the action locally using act:

1. Install act:

```bash
brew install act  # macOS
```

2. Run the action:

```bash
# Test with OpenRouter
export GITHUB_TOKEN=your_token
export OPENROUTER_API_KEY=your_key
./examples/test-action-local.sh --provider openrouter --pr 3

# Test with custom review prompts
export GITHUB_TOKEN=your_token
export OPENROUTER_API_KEY=your_key
export PR_REVIEW_SYSTEM_CONTENT="Focus on security issues"
export PR_REVIEW_DOCS_SYSTEM_CONTENT="Focus on API documentation"
./examples/test-action-local.sh --provider openrouter --pr 3

# Test with Ollama
export GITHUB_TOKEN=your_token
./examples/test-action-local.sh --provider ollama --model deepseek-r1:1.5b --pr 3

# Test with AWS Bedrock
export GITHUB_TOKEN=your_token
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
./examples/test-action-local.sh --provider bedrock --model anthropic.claude-3-sonnet --pr 3
```

The script will:

- Create a temporary workflow file
- Set up secrets securely
- Run the action in a Docker container
- Clean up temporary files

Note for M-series Mac users: The script automatically handles architecture differences by using `--container-architecture linux/amd64`.

#### 2. Using Manual Workflow (GitHub UI)

You can also trigger tests directly from GitHub's UI:

1. Go to your repository's "Actions" tab
2. Select "Test PR Analysis" workflow from the left sidebar
3. Click "Run workflow" button
4. Fill in the form:
   - PR number (required, defaults to "1")
   - Provider (optional, defaults to "openrouter")
   - Model (optional)
5. Click "Run workflow" to start the analysis

This method is useful when you want to:

- Test without local setup
- Run multiple tests with different configurations
- Share test results with team members
- Debug issues in the GitHub Actions environment

The workflow uses your repository's secrets (PAT_TOKEN and OPENROUTER_API_KEY) and provides the same functionality as local testing.

## LLM Providers

### OpenRouter

OpenRouter provides access to various LLMs through a single API:

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Set the environment variable:

```bash
export OPENROUTER_API_KEY=your_key
```

### AWS Bedrock

For AWS Bedrock:

1. Set up AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

2. Available models:

- anthropic.claude-3-sonnet
- anthropic.claude-3-haiku
- anthropic.claude-2.1
- anthropic.claude-2.0

### Ollama

For local LLM inference using Ollama:

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model:

```bash
ollama pull deepseek-r1:1.5b
```

3. Run with Ollama provider:

```bash
./examples/test-local.sh --provider ollama --model deepseek-r1:1.5b
```

## Customization

### Review Prompts

You can customize the review prompts using environment variables:

```bash
# Customize code review focus
export PR_REVIEW_SYSTEM_CONTENT="Focus on:
1. Security vulnerabilities
2. Performance implications
3. Error handling
4. Testing coverage"

# Customize documentation review focus
export PR_REVIEW_DOCS_SYSTEM_CONTENT="Focus on:
1. API documentation
2. Configuration examples
3. Deployment instructions
4. Breaking changes"
```

### Models

Each provider has different available models:

- OpenRouter: anthropic/claude-3-sonnet, anthropic/claude-3-haiku, etc.
- AWS Bedrock: anthropic.claude-3-sonnet, anthropic.claude-2.1, etc.
- Ollama: deepseek-r1:1.5b, llama2, codellama, etc.

Specify a model using the `--model` flag:

```bash
./examples/test-local.sh --provider openrouter --model anthropic/claude-3-sonnet
```
