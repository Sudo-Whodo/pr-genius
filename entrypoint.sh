#!/bin/sh -l

# Exit on error
set -e

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    exit 1
fi

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "Error: OPENROUTER_API_KEY environment variable is not set"
    exit 1
fi

# Use environment variables if available, otherwise use arguments
REPO=${REPOSITORY:-"$1"}
PR=${PR_NUMBER:-"$2"}
MODEL=${MODEL:-"$4"}

# Run the PR diff analyzer
echo "Running analysis for repository: $REPO, PR: $PR, Model: $MODEL"
python /app/pr_diff_analyzer.py --repo "$REPO" --pr "$PR" --model "$MODEL"