# PR Genius 🤖

<div align="center">

[![Build Status](https://github.com/sudo-whodo/pr-genius/actions/workflows/build.yml/badge.svg)](https://github.com/sudo-whodo/pr-genius/actions)
[![Version](https://img.shields.io/github/v/release/sudo-whodo/pr-genius?include_prereleases)](https://github.com/sudo-whodo/pr-genius/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

AI-powered pull request analysis tool that provides comprehensive code reviews, impact analysis, and documentation updates.

[Features](#features) •
[Quick Start](#quick-start) •
[Documentation](#documentation) •
[Contributing](#contributing)

</div>

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

Add this workflow to your repository at `.github/workflows/pr-analysis.yml`:

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
        uses: sudo-whodo/pr-genius@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
```

That's it! The action will now analyze your pull requests and provide AI-powered feedback.

## 📚 Documentation

- [Usage Guide](docs/usage-guide.md) - How to use this action in your repositories
- [Release Workflow](docs/release-workflow.md) - Understanding our release process
- [API Reference](docs/usage-guide.md#configuration-options) - Available configuration options

## 🔧 Required Secrets

1. `GITHUB_TOKEN`: Automatically provided by GitHub Actions
2. `OPENROUTER_API_KEY`: Your OpenRouter API key
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Create an API key
   - Add it to your repository secrets

## 📊 Example Output

The action will add a comment to your PR with:

<details>
<summary>Click to see example output</summary>

```markdown
## 🤖 Pull Request Analysis

### 📊 Statistics

- Files changed: 3
- Lines added: 150
- Lines deleted: 50

### 🧠 AI Code Review

[AI-generated code review comments]

### 📚 Documentation Updates Needed

[Documentation suggestions]

### 🔍 Notable Changes

[List of significant changes]
```

</details>

## ⚠️ Error Handling

The action includes comprehensive error handling for:

- GitHub API errors
- OpenRouter API errors
- Rate limiting
- Authentication issues

Check workflow logs for detailed error messages.

## 🎯 Best Practices

1. 🔒 Keep API keys secure in repository secrets
2. 🔄 Use on significant PRs for best value
3. 👀 Review AI suggestions before implementing
4. 📚 Keep documentation updated
5. 🤖 Consider different models for different needs

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using conventional commits:
   - `feat: add new feature`
   - `fix: resolve issue`
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📋 Requirements

- Python 3.8+
- GitHub Personal Access Token
- OpenRouter API Key

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
