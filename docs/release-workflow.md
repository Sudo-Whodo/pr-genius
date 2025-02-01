# Release Workflow

This document explains our release process and versioning system.

## Overview

We use semantic versioning through conventional commits to automate our release process. When changes are pushed to main, our release workflow:

1. Detects version-worthy changes
2. Creates a release PR
3. Updates version numbers
4. Creates git tags
5. Builds and publishes Docker images

## Version Types

### 1. Patch Version (0.1.0 -> 0.1.1)

Triggered by:

```
fix: bug fix description
```

or

```
perf: performance improvement description
```

### 2. Minor Version (0.1.0 -> 0.2.0)

Triggered by:

```
feat: new feature description
```

### 3. Major Version (0.1.0 -> 1.0.0)

Triggered by:

```
feat!: breaking change description
```

or

```
feat: new feature

BREAKING CHANGE: description of breaking changes
```

## Release Process

1. **Change Detection**

   - Workflow runs on push to main
   - Analyzes commit messages since last release
   - Determines version bump type

2. **Release PR Creation**

   - Creates branch `release-x.y.z`
   - Updates version in `__init__.py`
   - Creates PR with changelog

3. **After PR Merge**
   - Creates git tag
   - Creates GitHub release
   - Builds Docker image
   - Pushes to GitHub Container Registry

## Docker Images

Images are published to GitHub Container Registry:

- `ghcr.io/sudo-whodo/pr-genius:latest`
- `ghcr.io/sudo-whodo/pr-genius:x.y.z`

## Workflow Files

### 1. Release Workflow

`.github/workflows/release.yml` handles:

- Version detection
- PR creation
- Tag creation
- Docker builds

### 2. PR Analysis

`.github/workflows/pr-analysis.yml` handles:

- PR analysis
- AI code review
- Comment posting

## Dependencies

### 1. Required Secrets

- `PAT_TOKEN`: GitHub Personal Access Token
- `OPENROUTER_API_KEY`: OpenRouter API key

### 2. Permissions

The PAT_TOKEN needs:

- `contents: write` for releases
- `packages: write` for Docker images
- `pull-requests: write` for PR creation

## Best Practices

1. **Commit Messages**

   - Use conventional commit format
   - Include scope when relevant
   - Provide clear descriptions

2. **Pull Requests**

   - Use provided PR template
   - Include comprehensive description
   - Link related issues

3. **Version Bumps**
   - Consider impact of changes
   - Use appropriate commit prefix
   - Document breaking changes

## Troubleshooting

### Common Issues

1. **Version Not Incrementing**

   - Check commit message format
   - Ensure changes are in tracked files
   - Verify workflow permissions

2. **Docker Build Fails**

   - Check Dockerfile syntax
   - Verify dependencies
   - Check registry permissions

3. **Release PR Issues**
   - Verify PAT_TOKEN permissions
   - Check branch protection rules
   - Review workflow logs

## Manual Release

If needed, you can trigger a release manually:

1. Via GitHub UI:

   - Go to Actions
   - Select Release workflow
   - Click "Run workflow"

2. Via git tag:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

## Maintenance

1. **Regular Tasks**

   - Review and update dependencies
   - Check workflow performance
   - Monitor Docker image size

2. **Security**

   - Rotate PAT_TOKEN regularly
   - Review workflow permissions
   - Update base images

3. **Documentation**
   - Keep changelog updated
   - Document breaking changes
   - Update version requirements
