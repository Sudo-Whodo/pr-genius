#!/bin/bash

# Exit on error
set -e

# Check if required environment variables are set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    echo "Please set it with: export GITHUB_TOKEN=your_token"
    echo "You can create a Personal Access Token at: https://github.com/settings/tokens"
    echo "Required scopes: repo, pull_requests"
    exit 1
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable is not set"
    echo "Please set it with: export OPENROUTER_API_KEY=your_key"
    echo "You can get an API key at: https://openrouter.ai/"
    exit 1
fi

# Default values
REPO=${1:-"sudo-whodo/pr-genius"}
PR_NUMBER=${2:-"1"}
MODEL=${3:-"anthropic/claude-3.5-sonnet"}

# Print configuration
echo "Configuration:"
echo "- Repository: $REPO"
echo "- PR Number: $PR_NUMBER"
echo "- Model: $MODEL"
echo "- GitHub Token: ${GITHUB_TOKEN:0:4}...${GITHUB_TOKEN: -4}"
echo "- OpenRouter Key: ${OPENROUTER_API_KEY:0:4}...${OPENROUTER_API_KEY: -4}"

# Build the container
echo -e "\nBuilding container..."
docker build -t pr_diff_bot:local .

# Run the container
echo -e "\nRunning analysis..."
docker run \
    -e GITHUB_TOKEN=$GITHUB_TOKEN \
    -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
    pr_diff_bot:local \
    "$REPO" "$PR_NUMBER" "--model" "$MODEL"