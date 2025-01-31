#!/bin/sh -l

# Exit on error
set -e

# Run the PR diff analyzer with provided arguments
python /app/pr_diff_analyzer.py --repo "$1" --pr "$2" --model "$4"