#!/bin/sh -l

# Exit on error
set -e

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    exit 1
fi

# Parse named arguments
while [ "$#" -gt 0 ]; do
    case "$1" in
        --repo) REPO="$2"; shift 2;;
        --pr) PR="$2"; shift 2;;
        --provider) PROVIDER="$2"; shift 2;;
        --model)
            if [ "$2" != "null" ] && [ "$2" != "" ]; then
                MODEL="$2"
            fi
            shift 2
            ;;
        "") shift;; # Skip empty arguments
        *)
            if [ "$1" != "null" ] && [ "$1" != "" ]; then
                echo "Unknown parameter: $1"; exit 1
            fi
            shift
            ;;
    esac
done

# Use environment variables as fallbacks
REPO=${REPO:-$REPOSITORY}
PR=${PR:-$PR_NUMBER}
PROVIDER=${PROVIDER:-${LLM_PROVIDER:-"openrouter"}}

# Check provider-specific requirements
case "$PROVIDER" in
    "openrouter")
        if [ -z "$OPENROUTER_API_KEY" ]; then
            echo "Error: OPENROUTER_API_KEY environment variable is required for OpenRouter provider"
            exit 1
        fi
        ;;
    "bedrock")
        if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
            echo "Error: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required for Bedrock provider"
            exit 1
        fi
        ;;
    "ollama")
        echo "Warning: Using Ollama provider. Ensure Ollama is running in the container environment."
        ;;
    *)
        echo "Error: Invalid provider '$PROVIDER'. Must be one of: openrouter, ollama, bedrock"
        exit 1
        ;;
esac

# Run the PR diff analyzer
echo "Running analysis for repository: $REPO, PR: $PR, Provider: $PROVIDER${MODEL:+, Model: $MODEL}"
if [ -n "$MODEL" ]; then
    python /app/pr_diff_analyzer.py --repo "$REPO" --pr "$PR" --provider "$PROVIDER" --model "$MODEL"
else
    python /app/pr_diff_analyzer.py --repo "$REPO" --pr "$PR" --provider "$PROVIDER"
fi
