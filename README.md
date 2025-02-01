# PR Genius 🤖

<div align="center">

[![Build Status](https://github.com/sudo-whodo/pr-genius/actions/workflows/release.yml/badge.svg)](https://github.com/sudo-whodo/pr-genius/actions)
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

1. Create `.github/workflows/pr-analysis.yml` in your repository:

```yaml
name: PR Analysis
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: PR Diff Analysis
        uses: sudo-whodo/pr-genius@v1
        with:
          github_token: ${{ secrets.PAT_TOKEN }}
          openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
```

2. Add required secrets to your repository:

   a. Personal Access Token (PAT):

   - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Generate new token with:
     - `repo` scope (for repository access)
     - `pull_requests` scope (for commenting on PRs)
   - Add to repository secrets as `PAT_TOKEN`

   b. OpenRouter API Key:

   - Get your API key from https://openrouter.ai/
   - Add to repository secrets as `OPENROUTER_API_KEY`

That's it! PR Genius will now analyze your pull requests automatically.

## 📚 Documentation

- [Usage Guide](docs/usage-guide.md) - Detailed setup and configuration
- [Example Configurations](examples/README.md) - Ready-to-use workflow examples
- [Release Process](docs/release-workflow.md) - Understanding our versioning

## 🔧 Configuration

### Action Inputs

| Input                 | Description                  | Required | Default                     |
| --------------------- | ---------------------------- | -------- | --------------------------- |
| `github_token`        | Personal Access Token (PAT)  | Yes      | -                           |
| `openrouter_key`      | OpenRouter API key           | Yes      | -                           |
| `repository`          | Repository name (owner/repo) | No       | Current repository          |
| `pull_request_number` | PR number to analyze         | No       | Current PR number           |
| `model`               | OpenRouter model to use      | No       | anthropic/claude-3.5-sonnet |

### Required Permissions

The workflow needs these permissions:

```yaml
permissions:
  pull-requests: write # For posting comments
  contents: read # For accessing repository contents
```

Additionally, your PAT_TOKEN must have:

- `repo` scope for repository access
- `pull_requests` scope for commenting on PRs

## 📊 Example Output

PR Genius adds a comment to your pull request with:

<details>
<summary>Click to see example output</summary>

```markdown
## 🤖 Pull Request Analysis

### 📊 Statistics

- Files changed: 3
- Lines added: 150
- Lines deleted: 50

### 🧠 AI Code Review

Analysis by anthropic/claude-3.5-sonnet:
[Detailed code review with impact assessment, risks, and suggestions]

### 📚 Documentation Updates Needed

[Documentation suggestions based on changes]

### 🔍 Notable Changes

- Major changes in src/main.py: +100/-30 lines
- New file: tests/test_feature.py
```

</details>

## ⚠️ Troubleshooting

1. **Permission Issues (403 Forbidden)**

   - Ensure you're using PAT_TOKEN, not GITHUB_TOKEN
   - Verify PAT has required scopes (repo, pull_requests)
   - Check that the token hasn't expired

2. **Missing OpenRouter API Key**

   - Ensure you've added the `OPENROUTER_API_KEY` to your repository secrets
   - Check that the secret name matches exactly

3. **Rate Limits**

   - OpenRouter has rate limits based on your plan
   - GitHub API also has rate limits

4. **Token Security**
   - Never commit tokens directly in workflow files
   - Always use repository secrets
   - Regularly rotate your PAT for security

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using conventional commits:
   - `feat: add new feature`
   - `fix: resolve issue`
   - `docs: update documentation`
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📋 Requirements

- Python 3.8+
- GitHub Personal Access Token
- OpenRouter API Key

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
