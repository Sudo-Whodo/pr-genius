#!/bin/sh -l

# Exit on error
set -e

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is required"
    exit 1
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable is required"
    exit 1
fi

# Default model if not provided
MODEL=${3:-"anthropic/claude-3.5-sonnet"}

# Run the PR diff analyzer with provided arguments
echo "Running PR analysis for repository: $1, PR: $2, Model: $MODEL"
python /app/pr_diff_analyzer.py --repo "$1" --pr "$2" --model "$MODEL"