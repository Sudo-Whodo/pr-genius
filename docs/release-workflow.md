# Release Workflow

This document outlines the process for releasing new versions of PR Genius.

## Pre-release Testing

1. Run the test suite:

```bash
python -m pytest
```

2. Test with different LLM providers using Docker:

```bash
# Test with OpenRouter
./examples/test-local.sh --provider openrouter --pr 3

# Test with Ollama
./examples/test-local.sh --provider ollama --model deepseek-r1:1.5b --pr 3

# Test with AWS Bedrock
./examples/test-local.sh --provider bedrock --model anthropic.claude-3-sonnet --pr 3
```

3. Test the GitHub Action locally using act:

```bash
# Test with OpenRouter
./examples/test-action-local.sh --provider openrouter --pr 3

# Test with custom prompts
export PR_REVIEW_SYSTEM_CONTENT="Focus on security"
./examples/test-action-local.sh --provider openrouter --pr 3

# Test with Ollama
./examples/test-action-local.sh --provider ollama --model deepseek-r1:1.5b --pr 3
```

## Release Process

1. Update version in pyproject.toml:

```toml
[tool.poetry]
name = "pr-genius"
version = "1.2.3"  # New version here
```

2. Update CHANGELOG.md with the new version and changes:

```markdown
## [1.2.3] - YYYY-MM-DD

### Added

- New feature X
- New feature Y

### Changed

- Improvement to Z
- Update to A

### Fixed

- Bug fix for B
- Issue with C
```

3. Create a new release branch:

```bash
git checkout -b release/v1.2.3
```

4. Commit changes:

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): prepare v1.2.3"
```

5. Create a pull request and wait for CI checks

6. After merging, tag the release:

```bash
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

7. Create a GitHub release:

- Go to Releases > Draft a new release
- Choose the tag
- Copy changelog entries
- Publish release

## Post-release

1. Verify the GitHub Action works with the new release:

```yaml
- uses: sudo-whodo/pr-genius@v1.2.3
```

2. Update documentation if needed:

- README.md
- docs/usage-guide.md
- Example workflows

## Hotfix Process

For urgent fixes to a released version:

1. Create a hotfix branch from the tag:

```bash
git checkout -b hotfix/v1.2.4 v1.2.3
```

2. Make the fix and update version/changelog

3. Follow steps 4-7 from the release process

## Version Numbering

We follow semantic versioning:

- MAJOR version for incompatible API changes
- MINOR version for new features in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

Example: 1.2.3

- 1 = Major version
- 2 = Minor version
- 3 = Patch version
