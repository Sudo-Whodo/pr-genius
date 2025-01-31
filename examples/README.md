# PR Genius Examples

This directory contains example configurations for using PR Genius in your repositories.

## Quick Start

1. Create a `.github/workflows` directory in your repository if it doesn't exist.

2. Copy `pr-analysis.yml` to `.github/workflows/pr-analysis.yml` in your repository.

3. Add required secrets to your repository:

   a. Personal Access Token (PAT):

   - Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - Generate new token with:
     - `repo` scope (for repository access)
     - `pull_requests` scope (for commenting on PRs)
   - Add to repository secrets as `PAT_TOKEN`
   - Note: GITHUB_TOKEN doesn't have sufficient permissions for PR comments

   b. OpenRouter API Key:

   - Get your API key from https://openrouter.ai/
   - Add to repository secrets as `OPENROUTER_API_KEY`

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

| Input                 | Description                  | Required | Default                     |
| --------------------- | ---------------------------- | -------- | --------------------------- |
| `github_token`        | Personal Access Token (PAT)  | Yes      | -                           |
| `openrouter_key`      | OpenRouter API key           | Yes      | -                           |
| `repository`          | Repository name (owner/repo) | No       | Current repository          |
| `pull_request_number` | PR number to analyze         | No       | Current PR number           |
| `model`               | OpenRouter model to use      | No       | anthropic/claude-3.5-sonnet |

### Custom Model

To use a different AI model:

```yaml
- uses: sudo-whodo/pr-genius@v1
  with:
    github_token: ${{ secrets.PAT_TOKEN }}
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

Additionally, your PAT_TOKEN must have:

- `repo` scope for repository access
- `pull_requests` scope for commenting on PRs

## Example Output

PR Genius will add a comment to your pull request with:

- File change statistics
- AI-powered code review
- Documentation suggestions
- Notable changes
- Detailed file analysis

## Troubleshooting

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

For more help, visit our [documentation](../docs/usage-guide.md) or open an issue.
