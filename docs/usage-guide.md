# Using PR Genius GitHub Action

This guide explains how to use the PR Genius GitHub Action in your repositories for automated PR analysis.

## Quick Start

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

## Required Secrets

1. `GITHUB_TOKEN`: Automatically provided by GitHub Actions
2. `OPENROUTER_API_KEY`: Your OpenRouter API key
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Create an API key
   - Add it to your repository secrets

## Configuration Options

| Input          | Description                 | Required | Default                     |
| -------------- | --------------------------- | -------- | --------------------------- |
| github_token   | GitHub token for API access | ✅       | -                           |
| openrouter_key | OpenRouter API key          | ✅       | -                           |
| model          | OpenRouter model to use     | ❌       | anthropic/claude-3.5-sonnet |

## Features

The action will:

1. Analyze PR changes
2. Provide AI-powered code review
3. Generate documentation suggestions
4. Post results as PR comments

## Example Output

The action will add a comment to your PR with:

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

## Advanced Configuration

### Using a Different Model

```yaml
- uses: sudo-whodo/pr-genius@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
    model: "anthropic/claude-2"
```

### Running on Specific Branches

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    branches:
      - main
      - develop
```

### Running on Specific File Changes

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - "**.py"
      - "**.js"
      - "**.ts"
```

## Best Practices

1. **API Key Security**

   - Never commit API keys
   - Use repository secrets
   - Regularly rotate keys

2. **Model Selection**

   - Use claude-3.5-sonnet for general use
   - Consider claude-2 for complex analysis
   - Test different models for your needs

3. **PR Size**

   - Keep PRs focused and small
   - Split large changes into multiple PRs
   - Makes analysis more effective

4. **Review Process**
   - Use AI analysis as a supplement
   - Always perform human review
   - Consider AI suggestions carefully

## Troubleshooting

### Common Issues

1. **Missing API Key**

   ```
   Error: OpenRouter API key not found
   ```

   Solution: Add OPENROUTER_API_KEY to repository secrets

2. **Permission Issues**

   ```
   Error: Resource not accessible by integration
   ```

   Solution: Check workflow permissions in repository settings

3. **Rate Limits**
   ```
   Error: API rate limit exceeded
   ```
   Solution: Check OpenRouter usage limits and plan

### Getting Help

1. Open an issue in the [PR Genius repository](https://github.com/sudo-whodo/pr-genius)
2. Include:
   - Workflow file
   - Error message
   - PR details
   - Steps to reproduce

## Version History

Check the [releases page](https://github.com/sudo-whodo/pr-genius/releases) for:

- Latest versions
- New features
- Bug fixes
- Breaking changes

## Contributing

We welcome contributions! See our [Contributing Guide](../CONTRIBUTING.md) for:

- Development setup
- Coding standards
- PR process
- Feature requests
