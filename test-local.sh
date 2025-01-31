#!/bin/bash

# Exit on error
set -e

# Check if required environment variables are set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    exit 1
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable is not set"
    exit 1
fi

# Default values
REPO=${1:-"sudo-whodo/pr-genius"}
PR_NUMBER=${2:-"1"}
MODEL=${3:-"anthropic/claude-3.5-sonnet"}

# Build the container
echo "Building container..."
docker build -t pr-diff-analyzer:local .

# Run the container
echo "Running analysis for PR #$PR_NUMBER in $REPO using model $MODEL"
docker run \
    -e GITHUB_TOKEN=$GITHUB_TOKEN \
    -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY \
    pr-diff-analyzer:local \
    "$REPO" "$PR_NUMBER" "$MODEL"