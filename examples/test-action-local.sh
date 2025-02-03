#!/bin/bash

# Exit on error
set -e

# Function to show usage
show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --provider <provider>  LLM provider to use (openrouter, ollama, or bedrock)"
    echo "  --model <model>        Model name to use"
    echo "  --pr <number>          PR number to analyze (default: 1)"
    echo ""
    echo "Examples:"
    echo "1. Using OpenRouter:"
    echo "   $0 --provider openrouter"
    echo "   Required env: GITHUB_TOKEN, OPENROUTER_API_KEY"
    echo ""
    echo "2. Using AWS Bedrock:"
    echo "   $0 --provider bedrock --model anthropic.claude-3-sonnet"
    echo "   Required env: GITHUB_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
    echo ""
    echo "3. Using Ollama:"
    echo "   $0 --provider ollama --model deepseek-r1:1.5b"
    echo "   Required env: GITHUB_TOKEN"
    echo ""
    exit 1
}

# Parse command line arguments
PROVIDER="openrouter"
MODEL=""
PR_NUMBER="1"

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
        --pr)
            PR_NUMBER="$2"
            shift 2
            ;;
        --help)
            show_usage
            ;;
        *)
            echo "Error: Unknown argument: $1"
            show_usage
            ;;
    esac
done

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "Error: 'act' is not installed"
    echo "Please install it with: brew install act"
    exit 1
fi

# Create temporary workflow file
WORKFLOW_FILE=".github/workflows/test.yml"
mkdir -p .github/workflows

# Backup existing test.yml if it exists
if [ -f "$WORKFLOW_FILE" ]; then
    mv "$WORKFLOW_FILE" "${WORKFLOW_FILE}.bak"
fi

cat > "$WORKFLOW_FILE" << EOL
name: Test PR Analysis
on: workflow_dispatch
jobs:
  analyze:
    runs-on: ubuntu-latest
    name: Analyze PR
    steps:
      - uses: actions/checkout@v4
      - name: PR Analysis
        uses: ./
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
          LLM_PROVIDER: $PROVIDER
          REPOSITORY: "sudo-whodo/pr-genius"
          PR_NUMBER: "$PR_NUMBER"
EOL

# Add provider-specific environment variables
if [ "$PROVIDER" = "openrouter" ]; then
    echo "          OPENROUTER_API_KEY: \${{ secrets.OPENROUTER_API_KEY }}" >> "$WORKFLOW_FILE"
elif [ "$PROVIDER" = "bedrock" ]; then
    echo "          AWS_ACCESS_KEY_ID: \${{ secrets.AWS_ACCESS_KEY_ID }}" >> "$WORKFLOW_FILE"
    echo "          AWS_SECRET_ACCESS_KEY: \${{ secrets.AWS_SECRET_ACCESS_KEY }}" >> "$WORKFLOW_FILE"
elif [ "$PROVIDER" = "ollama" ]; then
    if [ ! -z "$OLLAMA_BASE_URL" ]; then
        echo "          OLLAMA_BASE_URL: $OLLAMA_BASE_URL" >> "$WORKFLOW_FILE"
    fi
fi

# Add model if specified
if [ ! -z "$MODEL" ]; then
    echo "          MODEL: $MODEL" >> "$WORKFLOW_FILE"
fi

# Add custom review prompts if set
if [ ! -z "$PR_REVIEW_SYSTEM_CONTENT" ]; then
    echo "          PR_REVIEW_SYSTEM_CONTENT: $PR_REVIEW_SYSTEM_CONTENT" >> "$WORKFLOW_FILE"
fi
if [ ! -z "$PR_REVIEW_DOCS_SYSTEM_CONTENT" ]; then
    echo "          PR_REVIEW_DOCS_SYSTEM_CONTENT: $PR_REVIEW_DOCS_SYSTEM_CONTENT" >> "$WORKFLOW_FILE"
fi

# Add args for entrypoint.sh
echo "        with:" >> "$WORKFLOW_FILE"
echo "          args: --repo \"sudo-whodo/pr-genius\" --pr \"$PR_NUMBER\" --provider \"$PROVIDER\"" >> "$WORKFLOW_FILE"
if [ ! -z "$MODEL" ]; then
    echo "          args: \${{ inputs.args }} --model \"$MODEL\"" >> "$WORKFLOW_FILE"
fi

echo "Created workflow file: $WORKFLOW_FILE"
cat "$WORKFLOW_FILE"

# Create .secrets file for act
SECRETS_FILE=".secrets"
echo "GITHUB_TOKEN=$GITHUB_TOKEN" > "$SECRETS_FILE"

if [ "$PROVIDER" = "openrouter" ]; then
    echo "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" >> "$SECRETS_FILE"
elif [ "$PROVIDER" = "bedrock" ]; then
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> "$SECRETS_FILE"
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> "$SECRETS_FILE"
fi

# Run the action with secrets
echo -e "\nRunning action with act..."
act workflow_dispatch -W .github/workflows/test.yml \
    --secret-file "$SECRETS_FILE" \
    --container-architecture linux/amd64

# Clean up secrets file
rm "$SECRETS_FILE"

# Clean up test workflow file and restore backup if it existed
rm "$WORKFLOW_FILE"
if [ -f "${WORKFLOW_FILE}.bak" ]; then
    mv "${WORKFLOW_FILE}.bak" "$WORKFLOW_FILE"
fi
