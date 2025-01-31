# PR Genius Examples

This directory contains example configurations for using PR Genius in your repositories.

## Quick Start

1. Create a `.github/workflows` directory in your repository if it doesn't exist.

2. Copy `pr-analysis.yml` to `.github/workflows/pr-analysis.yml` in your repository.

3. Add your OpenRouter API key to your repository secrets:
   - Go to your repository Settings
   - Navigate to Secrets and Variables > Actions
   - Click "New repository secret"
   - Name: `OPENROUTER_API_KEY`
   - Value: Your OpenRouter API key from https://openrouter.ai/

That's it! PR Genius will now analyze your pull requests automatically.

## Configuration Options

### Trigger Events

By default, the workflow runs on pull request open and synchronize events:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

You can also limit analysis to specific paths:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - "**.py"
      - "**.js"
      - "**.ts"
```

### Action Inputs

| Input                 | Description                  | Required | Default                       |
| --------------------- | ---------------------------- | -------- | ----------------------------- |
| `github_token`        | GitHub token for API access  | Yes      | `${{ secrets.GITHUB_TOKEN }}` |
| `openrouter_key`      | OpenRouter API key           | Yes      | -                             |
| `repository`          | Repository name (owner/repo) | No       | Current repository            |
| `pull_request_number` | PR number to analyze         | No       | Current PR number             |
| `model`               | OpenRouter model to use      | No       | anthropic/claude-3.5-sonnet   |

### Custom Model

To use a different AI model:

```yaml
- uses: sudo-whodo/pr-genius@v1
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
    model: "anthropic/claude-2"
```

### Required Permissions

The workflow needs these permissions:

```yaml
permissions:
  pull-requests: write # For posting comments
  contents: read # For accessing repository contents
```

## Example Output

PR Genius will add a comment to your pull request with:

- File change statistics
- AI-powered code review
- Documentation suggestions
- Notable changes
- Detailed file analysis

## Troubleshooting

1. **Missing OpenRouter API Key**

   - Ensure you've added the `OPENROUTER_API_KEY` to your repository secrets
   - Check that the secret name matches exactly

2. **Permission Issues**

   - Verify the workflow has the required permissions
   - Check that the GitHub token has sufficient access

3. **Rate Limits**
   - OpenRouter has rate limits based on your plan
   - GitHub API also has rate limits

For more help, visit our [documentation](../docs/usage-guide.md) or open an issue.
