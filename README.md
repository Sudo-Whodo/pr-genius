# PR Genius

An AI-powered pull request analyzer that provides detailed code reviews and documentation suggestions.

## Features

- Automated PR analysis with multiple LLM providers (OpenRouter, Ollama, AWS Bedrock)
- Detailed code review with impact assessment and improvement suggestions
- Documentation update recommendations
- Support for customizable review prompts
- Docker-based testing environment

## Installation

```bash
git clone https://github.com/sudo-whodo/pr-genius.git
cd pr-genius
pip install -r pr-diff-bot/requirements.txt
```

## Usage

### Basic Usage

```bash
# Using OpenRouter (default)
export GITHUB_TOKEN=your_token
export OPENROUTER_API_KEY=your_key
./test-local.sh 123  # Analyze PR #123

# Using Ollama
./test-local.sh --provider ollama --dry-run 123

# Using AWS Bedrock
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
./test-local.sh --provider bedrock 123
```

### Customizing Review Prompts

You can customize the review focus by setting environment variables:

```bash
# Customize code review focus (e.g., security)
export PR_REVIEW_SYSTEM_CONTENT='You are a security-focused code reviewer. Focus on:
1. Security vulnerabilities
2. Authentication issues
3. Data validation
4. Error handling
Provide detailed security recommendations.'

# Customize documentation review focus (e.g., API docs)
export PR_REVIEW_DOCS_SYSTEM_CONTENT='Focus on API documentation:
1. API endpoint changes
2. Request/response formats
3. Authentication requirements
4. Rate limits and quotas
Ensure all API changes are well-documented.'

# Run with custom prompts
./test-local.sh --dry-run 123
```

### Using Ollama

PR Genius supports using Ollama as an LLM provider. When using Ollama:

1. Local Development:

```bash
# Start Ollama locally
ollama run deepseek-r1:1.5b

# Run PR Genius with local Ollama
./test-local.sh --provider ollama 123
```

2. Remote Ollama:

```bash
# Use remote Ollama instance
export OLLAMA_BASE_URL=http://your-ollama-server:11434
./test-local.sh --provider ollama 123
```

3. Docker Environment:

```bash
# The test script automatically:
# - Creates a Docker network
# - Starts Ollama container
# - Pulls required model
# - Sets up proper networking
./test-local.sh --provider ollama --dry-run 123
```

## Environment Variables

| Variable                        | Description                     | Default                 |
| ------------------------------- | ------------------------------- | ----------------------- |
| `GITHUB_TOKEN`                  | GitHub Personal Access Token    | Required                |
| `OPENROUTER_API_KEY`            | OpenRouter API Key              | Required for OpenRouter |
| `AWS_ACCESS_KEY_ID`             | AWS Access Key                  | Required for Bedrock    |
| `AWS_SECRET_ACCESS_KEY`         | AWS Secret Key                  | Required for Bedrock    |
| `OLLAMA_BASE_URL`               | Ollama API URL                  | http://localhost:11434  |
| `PR_REVIEW_SYSTEM_CONTENT`      | Custom code review instructions | Built-in prompt         |
| `PR_REVIEW_DOCS_SYSTEM_CONTENT` | Custom docs review instructions | Built-in prompt         |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -am 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
