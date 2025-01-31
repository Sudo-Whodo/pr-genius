# PR Diff Analyzer 🤖

<div align="center">

![PR Diff Analyzer](https://raw.githubusercontent.com/yourusername/pull-requstooor/main/assets/logo.png)

[![Build Status](https://github.com/yourusername/pull-requstooor/workflows/Build%20and%20Publish%20Docker%20Image/badge.svg)](https://github.com/yourusername/pull-requstooor/actions)
[![Version](https://img.shields.io/github/v/release/yourusername/pull-requstooor?include_prereleases)](https://github.com/yourusername/pull-requstooor/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

AI-powered pull request analysis tool that provides comprehensive code reviews, impact analysis, and documentation updates.

[Features](#features) •
[Quick Start](#quick-start) •
[Documentation](#documentation) •
[Contributing](#contributing)

</div>

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [GitHub Action Usage](#-github-action-usage)
- [Manual Installation](#-manual-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Output Examples](#-output-examples)
- [Error Handling](#-error-handling)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)
- [Requirements](#-requirements)

## ✨ Features

- 🔍 Analyzes file changes in pull requests
- 📊 Provides detailed statistics (files changed, lines added/deleted)
- 🧠 Uses OpenRouter AI models (default: Claude 3.5 Sonnet) to:
  - Analyze code changes and their impact
  - Identify potential risks and concerns
  - Suggest improvements
  - Generate documentation updates
- 💬 Posts formatted summaries as PR comments
- 📚 Maintains documentation requirements
- 🔐 Supports authentication via GitHub token
- 🚀 Available as a GitHub Action

## 🚀 Quick Start

```yaml
name: PR Analysis
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: PR Diff Analysis
        uses: yourusername/pr-diff-analyzer@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
          # Optional: specify a different model
          # model: "anthropic/claude-2"
```

## 🔧 GitHub Action Usage

Add this to your workflow file (e.g., `.github/workflows/pr-analysis.yml`):

```yaml
name: PR Analysis
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - name: PR Diff Analysis
        uses: yourusername/pr-diff-analyzer@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
          repository: ${{ github.repository }}
          pull_request_number: ${{ github.event.pull_request.number }}
          # Optional: specify a different model (default: anthropic/claude-3.5-sonnet)
          # model: "anthropic/claude-2"
```

### Action Inputs

| Input                 | Description                        | Required | Default                     |
| --------------------- | ---------------------------------- | -------- | --------------------------- |
| `github_token`        | GitHub token for API access        | ✅       | -                           |
| `openrouter_key`      | OpenRouter API key for AI analysis | ✅       | -                           |
| `repository`          | Repository name (owner/repo)       | ✅       | -                           |
| `pull_request_number` | PR number to analyze               | ✅       | -                           |
| `model`               | OpenRouter model to use            | ❌       | anthropic/claude-3.5-sonnet |

## 💻 Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/pull-requstooor.git
cd pull-requstooor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Create a `.env` file:

```env
GITHUB_TOKEN=your_github_personal_access_token
OPENAI_API_KEY=your_openai_api_key
```

2. Set up GitHub Token:

   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with:
     - `repo` (Full control of private repositories)
     - `pull_requests` (Access to pull requests)

3. Set up OpenAI API Key:
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new key
   - Add to `.env` file

## 📝 Usage Examples

Analyze a pull request with default model (Claude 3.5 Sonnet):

```bash
python pr_diff_analyzer.py --repo octocat/Hello-World --pr 123
```

Analyze with a different model:

```bash
python pr_diff_analyzer.py --repo octocat/Hello-World --pr 123 --model "anthropic/claude-2"
```

## 📊 Output Examples

The analyzer posts a PR comment with:

<details>
<summary>Click to see example output</summary>

```markdown
## 🤖 Pull Request Analysis

### 📊 Statistics

- Files changed: 3
- Lines added: 150
- Lines deleted: 50

### 🧠 AI Code Review

This PR introduces significant changes to the authentication system:

- Impact: Moderate, affects user login flow
- Risks: Need to ensure backward compatibility
- Suggestions: Consider adding rate limiting
- Quality: Good separation of concerns

### 📚 Documentation Updates Needed

1. Update authentication API docs
2. Add examples for new login flow
3. Update configuration guide

### 🔍 Notable Changes

- Major changes in src/auth.py: +100/-30 lines
- New file: tests/test_auth.py
```

</details>

## ⚠️ Error Handling

The script includes comprehensive error handling for:

- GitHub API errors
- OpenAI API errors
- File access issues
- Authentication problems

Check console output for detailed error messages.

## 🎯 Best Practices

1. 🔒 Keep API keys secure and never commit them
2. 🔄 Run analyzer on significant PRs
3. 👀 Review AI suggestions before implementing
4. 📚 Keep documentation updated
5. 🧪 Add tests for new features
6. 🤖 Consider using different models for different types of analysis

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📋 Requirements

- Python 3.8+
- GitHub Personal Access Token
- OpenAI API Key
- Dependencies from requirements.txt

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
