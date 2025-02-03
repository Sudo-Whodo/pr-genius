# Release Workflow

This document outlines the process for releasing new versions of PR Genius.

## Automated Release Process

PR Genius uses python-semantic-release and GitHub Actions to automate the release process. The workflow is configured to:

1. Monitor commits for version-worthy changes using conventional commit messages
2. Create release PRs automatically when changes warrant a new version
3. Generate changelogs and update version numbers
4. Create GitHub releases and Docker images

### Release Types

The system supports three types of releases:

1. **Regular Releases** (from main branch)

   - Created when changes are pushed to main
   - Version format: v1.2.3
   - Full production releases

2. **Alpha Releases** (from feature branches)

   - Created when changes are pushed to feature/\* branches
   - Version format: v1.2.3-alpha.1
   - Used for testing new features
   - Created automatically from feature branches

3. **Beta Releases** (from fix branches)
   - Created when changes are pushed to fix/\* branches
   - Version format: v1.2.3-beta.1
   - Used for testing bug fixes
   - Created automatically from fix branches

### Commit Message Format

The release process relies on conventional commit messages to determine version bumps:

- `feat:` - New feature (minor version bump)
- `fix:` or `perf:` - Bug fix or performance improvement (patch version bump)
- `BREAKING CHANGE:` - Breaking API change (major version bump)

Example commit messages:

```
feat: add new analysis feature
fix: resolve memory leak in processor
feat!: redesign API (includes BREAKING CHANGE)
```

## Manual Testing

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

### Automated Release Flow

1. **Triggering a Release**

   - Push changes to main, feature/_, or fix/_ branches
   - Or manually trigger the Release workflow in GitHub Actions

2. **Version Check**

   - The system analyzes commit messages since the last release
   - Determines if a version bump is needed and what type
   - Creates a release PR if changes warrant a new version

3. **Release PR**

   - Contains version updates and changelog
   - For main branch: targets main
   - For feature branches: targets the feature branch with alpha version
   - For fix branches: targets the fix branch with beta version

4. **After PR Merge**
   - Creates GitHub release
   - Pushes Docker images
   - Regular releases go to main
   - Prereleases stay on their respective branches

### Manual Release (if needed)

You can still create releases manually if needed:

1. Create a release branch:

```bash
git checkout -b release/v1.2.3
```

2. Update version and changelog:

```bash
semantic-release version --no-commit
git add .
git commit -m "chore(release): prepare v1.2.3"
```

3. Create and merge a PR to main

4. The workflow will handle the rest automatically

## Post-release

1. Verify the release:

   - Check GitHub releases page
   - Verify Docker images are published
   - Test the new version in a clean environment

2. Update documentation if needed:

   - README.md
   - docs/usage-guide.md
   - Example workflows

3. Verify the GitHub Action works with the new release:

```yaml
- uses: sudo-whodo/pr-genius@v1.2.3
```

## Hotfix Process

For urgent fixes to a released version:

1. Create a fix branch:

```bash
git checkout -b fix/urgent-issue main
```

2. Make your changes and commit with appropriate message:

```bash
git commit -m "fix: resolve critical issue"
```

3. Push the branch:

```bash
git push origin fix/urgent-issue
```

4. The workflow will automatically:
   - Create a beta release for testing
   - Create a release PR when ready

## Version Numbering

We follow semantic versioning with prerelease support:

### Regular Releases (main branch)

- Format: MAJOR.MINOR.PATCH
- Example: 1.2.3
  - MAJOR: Incompatible API changes
  - MINOR: New features (backwards compatible)
  - PATCH: Bug fixes (backwards compatible)

### Prerelease Versions

- Alpha (feature branches)

  - Format: MAJOR.MINOR.PATCH-alpha.N
  - Example: 1.2.3-alpha.1
  - Used for new feature testing

- Beta (fix branches)
  - Format: MAJOR.MINOR.PATCH-beta.N
  - Example: 1.2.3-beta.1
  - Used for bug fix testing

Version bumps are determined automatically from commit messages using conventional commit format.
