# Using PR Genius GitHub Action

This guide explains how to use the PR Genius GitHub Action in your repositories for automated PR analysis.

## Installation

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

2. Set up required secrets:

   a. Personal Access Token (PAT):

   - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Generate new token with:
     - `repo` scope (for repository access)
     - `pull_requests` scope (for commenting on PRs)
   - Add to repository secrets as `PAT_TOKEN`
   - Note: GITHUB_TOKEN doesn't have sufficient permissions for PR comments

   b. OpenRouter API Key:

   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Create an API key
   - Add to repository secrets as `OPENROUTER_API_KEY`

## Configuration

### Action Inputs

| Input                 | Description                  | Required | Default                     |
| --------------------- | ---------------------------- | -------- | --------------------------- |
| `github_token`        | Personal Access Token (PAT)  | Yes      | -                           |
| `openrouter_key`      | OpenRouter API key           | Yes      | -                           |
| `repository`          | Repository name (owner/repo) | No       | Current repository          |
| `pull_request_number` | PR number to analyze         | No       | Current PR number           |
| `model`               | OpenRouter model to use      | No       | anthropic/claude-3.5-sonnet |

### Workflow Triggers

Control when the action runs:

```yaml
on:
  pull_request:
    types: [opened, synchronize] # Run on PR open and updates
    paths: # Optional: filter by file types
      - "**.py"
      - "**.js"
      - "**.ts"
```

### Permissions

Required workflow permissions:

```yaml
permissions:
  pull-requests: write # For posting comments
  contents: read # For accessing repository contents
```

Required PAT scopes:

- `repo` - For repository access
- `pull_requests` - For commenting on PRs

### AI Models

Available OpenRouter models:

- `anthropic/claude-3.5-sonnet` (default)
- `anthropic/claude-2`
- Other models from [OpenRouter](https://openrouter.ai/docs#models)

Example with custom model:

```yaml
- uses: sudo-whodo/pr-genius@v1
  with:
    github_token: ${{ secrets.PAT_TOKEN }}
    openrouter_key: ${{ secrets.OPENROUTER_API_KEY }}
    model: "anthropic/claude-2"
```

## Features

### PR Analysis

For each pull request, PR Genius:

1. Analyzes changed files
2. Calculates statistics
3. Reviews code changes with AI
4. Suggests documentation updates
5. Posts a detailed comment

### Analysis Output

The PR comment includes:

- File change statistics
- AI-powered code review
- Documentation suggestions
- Notable changes
- Detailed file analysis

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**

   ```
   Error: Resource not accessible by integration
   ```

   Solution:

   - Use PAT_TOKEN instead of GITHUB_TOKEN
   - Verify PAT has required scopes
   - Check token expiration

2. **Missing API Key**

   ```
   Error: OPENROUTER_API_KEY environment variable is not set
   ```

   Solution:

   - Add OPENROUTER_API_KEY to repository secrets
   - Check secret name spelling

3. **Rate Limits**
   - OpenRouter limits based on plan
   - GitHub API rate limits
     Solution:
   - Check usage limits
   - Consider upgrading plan

### Security Best Practices

1. Token Security:

   - Never commit tokens in code
   - Use repository secrets
   - Rotate PAT regularly
   - Limit token scopes

2. Repository Settings:
   - Enable branch protection
   - Require PR reviews
   - Set up required status checks

## Local Testing

For testing locally:

1. Clone the repository:

```bash
git clone https://github.com/sudo-whodo/pr-genius.git
cd pr-genius
```

2. Run the test script:

```bash
./test-local.sh "owner/repo" "pr_number" "model"
```

This builds and runs the container locally for testing.

## Support

- [Open an issue](https://github.com/sudo-whodo/pr-genius/issues)
- [Contributing guidelines](../CONTRIBUTING.md)
- [Release workflow](release-workflow.md)
