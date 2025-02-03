# Changelog

The changelog tracks user-facing changes to PR Genius, helping users understand what's new, what's changed, and what's been fixed in each version. This is particularly important for:

- Users deciding whether to upgrade
- Understanding breaking changes
- Planning integration updates
- Troubleshooting version-specific issues

## [Unreleased]

### Added

- Customizable review prompts through environment variables:
  ```bash
  # Example: Focus on security
  export PR_REVIEW_SYSTEM_CONTENT="Focus on security vulnerabilities..."
  ```
- Local GitHub Action testing with act:
  ```bash
  # Test locally before pushing
  ./examples/test-action-local.sh --provider openrouter
  ```
- M-series Mac support for all containers

### Changed

- Moved test scripts to examples/ for better organization
- System prompts now configurable (BREAKING CHANGE)
- Improved Docker container management

### Fixed

- Docker container issues on M-series Macs
- Environment variable handling in GitHub Action
- Ollama container networking and health checks
