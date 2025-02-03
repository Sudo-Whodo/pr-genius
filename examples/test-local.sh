#!/bin/bash

# Exit on error
set -e

# Function to show usage
show_usage() {
    echo "Usage: $0 [options] <pr_number>"
    echo ""
    echo "Options:"
    echo "  --provider <provider>  LLM provider to use (openrouter, ollama, or bedrock)"
    echo "  --model <model>        Model name to use"
    echo "  --dry-run             Don't post comment to PR, just print locally"
    echo ""
    echo "Examples:"
    echo "1. Using OpenRouter (default):"
    echo "   $0 123"
    echo "   Required env: GITHUB_TOKEN, OPENROUTER_API_KEY"
    echo ""
    echo "2. Using AWS Bedrock:"
    echo "   $0 --provider bedrock --model anthropic.claude-3-sonnet 123"
    echo "   Required env: GITHUB_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
    echo ""
    echo "3. Using Ollama:"
    echo "   $0 --provider ollama --model deepseek-r1:1.5b 123"
    echo "   Required env: GITHUB_TOKEN"
    echo ""
    exit 1
}

# Parse command line arguments
PROVIDER="openrouter"
MODEL=""  # No default, use provider defaults
PR_NUMBER=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --provider)
            PROVIDER="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            show_usage
            ;;
        *)
            if [ -z "$PR_NUMBER" ]; then
                PR_NUMBER="$1"
            else
                echo "Error: Unexpected argument: $1"
                show_usage
            fi
            shift
            ;;
    esac
done

# Set default values if not provided
REPO="sudo-whodo/pr-genius"  # Using this repo for testing
PR_NUMBER=${PR_NUMBER:-"1"}

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    echo "Please set it with: export GITHUB_TOKEN=your_token"
    echo "You can create a Personal Access Token at: https://github.com/settings/tokens"
    echo "Required scopes: repo, pull_requests"
    exit 1
fi

# Check provider-specific requirements
case "$PROVIDER" in
    "openrouter")
        if [ -z "$OPENROUTER_API_KEY" ]; then
            echo "Error: OPENROUTER_API_KEY environment variable is required for OpenRouter"
            echo "Please set it with: export OPENROUTER_API_KEY=your_key"
            echo "You can get an API key at: https://openrouter.ai/"
            exit 1
        fi
        ;;
    "bedrock")
        if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
            echo "Error: AWS credentials are required for Bedrock"
            echo "Please set:"
            echo "  export AWS_ACCESS_KEY_ID=your_key"
            echo "  export AWS_SECRET_ACCESS_KEY=your_secret"
            exit 1
        fi
        ;;
    "ollama")
        if [ -z "$OLLAMA_BASE_URL" ]; then
            echo "Note: OLLAMA_BASE_URL not set, will try localhost:11434"
            echo "To use external Ollama API, set OLLAMA_BASE_URL:"
            echo "  export OLLAMA_BASE_URL=http://your-ollama-server:11434"
        else
            echo "Using Ollama API at: $OLLAMA_BASE_URL"
        fi
        ;;
    *)
        echo "Error: Invalid provider '$PROVIDER'. Must be one of: openrouter, ollama, bedrock"
        exit 1
        ;;
esac

# Print configuration
echo "Configuration:"
echo "- Repository: $REPO (this repo)"
echo "- PR Number: $PR_NUMBER"
echo "- Provider: $PROVIDER"
echo "- Model: $MODEL"
echo "- GitHub Token: ${GITHUB_TOKEN:0:4}...${GITHUB_TOKEN: -4}"

# Print provider-specific configuration
case "$PROVIDER" in
    "openrouter")
        echo "- OpenRouter Key: ${OPENROUTER_API_KEY:0:4}...${OPENROUTER_API_KEY: -4}"
        ;;
    "bedrock")
        echo "- AWS Access Key ID: ${AWS_ACCESS_KEY_ID:0:4}...${AWS_ACCESS_KEY_ID: -4}"
        echo "- AWS Secret Key: ${AWS_SECRET_ACCESS_KEY:0:4}...${AWS_SECRET_ACCESS_KEY: -4}"
        ;;
esac

# Create Docker network if it doesn't exist
NETWORK_NAME="pr-genius-test"
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME"
fi

# Start Ollama container if using Ollama provider
OLLAMA_CONTAINER_NAME="pr-genius-ollama"
if [ "$PROVIDER" = "ollama" ]; then
    echo "Starting Ollama container..."
    # Check if container exists but is stopped
    if docker ps -a -q -f name="$OLLAMA_CONTAINER_NAME" >/dev/null 2>&1; then
        echo "Removing old Ollama container..."
        docker rm -f "$OLLAMA_CONTAINER_NAME" >/dev/null 2>&1
    fi

    echo "Starting Ollama container..."
    docker run -d --name "$OLLAMA_CONTAINER_NAME" \
        --network "$NETWORK_NAME" \
        --network-alias ollama \
        --platform linux/arm64 \
        ollama/ollama

    echo "Waiting for Ollama to start..."
    # Wait for Ollama to be ready (from within Docker network)
    echo "Checking Ollama health..."
    for i in {1..60}; do
        if docker run --rm --network "$NETWORK_NAME" curlimages/curl:8.1.2 -s "http://ollama:11434/api/tags" >/dev/null 2>&1; then
            echo "Ollama is ready!"
            break
        fi
        if [ $i -eq 60 ]; then
            echo "Error: Ollama failed to start"
            exit 1
        fi
        echo -n "."
        sleep 1
    done

    # Set Ollama URL to the network alias
    export OLLAMA_BASE_URL="http://ollama:11434"
    echo "Using Ollama at: $OLLAMA_BASE_URL"

    # Pull the default model
    echo "Pulling default model (this may take a while)..."
    docker exec "$OLLAMA_CONTAINER_NAME" ollama pull deepseek-r1:1.5b
fi

# Build the analyzer container
echo -e "\nBuilding analyzer container..."
# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Go up one level if in examples directory
if [[ "$SCRIPT_DIR" == */examples ]]; then
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
else
    PROJECT_ROOT="$SCRIPT_DIR"
fi
docker build -t pr-diff-analyzer:latest "$PROJECT_ROOT"

# Create a temporary file for environment variables
ENV_FILE=$(mktemp)
echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> "$ENV_FILE"
echo "LLM_PROVIDER=$PROVIDER" >> "$ENV_FILE"

# Add provider-specific environment variables
case "$PROVIDER" in
    "openrouter")
        echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" >> "$ENV_FILE"
        ;;
    "bedrock")
        echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> "$ENV_FILE"
        echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> "$ENV_FILE"
        ;;
    "ollama")
        if [ ! -z "$OLLAMA_BASE_URL" ]; then
            echo "OLLAMA_BASE_URL=$OLLAMA_BASE_URL" >> "$ENV_FILE"
        fi
        ;;
esac

# Add system content environment variables if set
if [ ! -z "$PR_REVIEW_SYSTEM_CONTENT" ]; then
    echo "PR_REVIEW_SYSTEM_CONTENT=$PR_REVIEW_SYSTEM_CONTENT" >> "$ENV_FILE"
fi
if [ ! -z "$PR_REVIEW_DOCS_SYSTEM_CONTENT" ]; then
    echo "PR_REVIEW_DOCS_SYSTEM_CONTENT=$PR_REVIEW_DOCS_SYSTEM_CONTENT" >> "$ENV_FILE"
fi

# Run the analyzer container
echo -e "\nRunning analysis..."
DOCKER_RUN_ARGS="--network $NETWORK_NAME"
if [ "$DRY_RUN" = true ]; then
    echo "Running in dry-run mode (will not post comment to PR)"
    docker run $DOCKER_RUN_ARGS --env-file "$ENV_FILE" \
        -e DRY_RUN=true \
        pr-diff-analyzer:latest \
        --repo "$REPO" --pr "$PR_NUMBER" --provider "$PROVIDER" ${MODEL:+"--model" "$MODEL"}
else
    docker run $DOCKER_RUN_ARGS --env-file "$ENV_FILE" \
        pr-diff-analyzer:latest \
        --repo "$REPO" --pr "$PR_NUMBER" --provider "$PROVIDER" ${MODEL:+"--model" "$MODEL"}
fi

# Clean up temporary file
rm "$ENV_FILE"

# Show how to customize system content
if [ "$DRY_RUN" = true ]; then
    echo -e "\nTo customize the review prompts, set these environment variables:"
    echo "export PR_REVIEW_SYSTEM_CONTENT='Your custom review instructions'"
    echo "export PR_REVIEW_DOCS_SYSTEM_CONTENT='Your custom docs review instructions'"
fi

# Cleanup
if [ "$PROVIDER" = "ollama" ]; then
    echo -e "\nLeaving Ollama container running for future tests."
    echo "To stop it: docker stop $OLLAMA_CONTAINER_NAME && docker rm $OLLAMA_CONTAINER_NAME"
fi
