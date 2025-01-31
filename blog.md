# Implementing Semantic Versioning with Docker Tags and Pre-releases

In this blog post, we'll explore how our Pull Requstooor project implements Docker image versioning using semantic release, with a focus on managing both stable and pre-release versions through Docker tags.

## Our Versioning Strategy

We use a sophisticated versioning approach that supports:

- Semantic version tags (e.g., `v1.2.3`)
- Pre-release versions for testing (e.g., `v1.2.3-beta.1`)
- Latest tag for stable releases
- Automated version management through GitHub Actions

## Implementation Details

### 1. Build and Publish Workflow

Our `.github/workflows/build-and-publish.yml` handles Docker image building and tagging:

```yaml
name: Build and Publish
on:
  release:
    types: [published]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            # Use the release version
            type=semver,pattern=v{{version}}
            # Set latest tag only for stable releases
            type=raw,value=latest,enable=${{ !github.event.release.prerelease }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

### 2. Automated Release Process

Our `.github/workflows/auto-release.yml` manages version creation:

```yaml
name: Auto Release
on:
  push:
    branches:
      - main
      - beta

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Python Semantic Release
        uses: python-semantic-release/python-semantic-release@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### 3. Release Configuration

In `pyproject.toml`, we configure semantic-release to handle both stable and pre-releases:

```toml
[tool.semantic_release]
version_variable = [
    "pr-diff-bot/__init__.py:__version__",
    "pyproject.toml:version"
]
branch = "main"
prerelease_branches = ["beta"]
prerelease = true
```

## How Version Tagging Works

### Stable Releases

When merging to main:

```bash
# Commit with conventional commit message
git commit -m "feat: add new analysis feature"
```

This triggers:

1. Semantic Release creates new version (e.g., `v1.2.0`)
2. GitHub Release is published
3. Build and Publish workflow:
   ```bash
   # Docker tags created
   ghcr.io/org/pull-requstooor:v1.2.0
   ghcr.io/org/pull-requstooor:latest
   ```

### Pre-releases

When merging to beta:

```bash
# Commit with conventional commit message
git commit -m "feat: experimental analysis feature"
```

This creates:

1. Pre-release version (e.g., `v1.3.0-beta.1`)
2. GitHub Pre-release
3. Docker image with beta tag:
   ```bash
   ghcr.io/org/pull-requstooor:v1.3.0-beta.1
   # Note: latest tag is not updated for pre-releases
   ```

## Using Different Versions

### Production Usage

```yaml
# Kubernetes deployment using latest stable
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: pull-requstooor
          image: ghcr.io/org/pull-requstooor:latest
```

### Testing Pre-releases

```yaml
# Kubernetes deployment using beta version
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: pull-requstooor
          image: ghcr.io/org/pull-requstooor:v1.3.0-beta.1
```

## Benefits of This Approach

1. **Version Control**

   - Clear separation between stable and pre-release versions
   - Automated version bumping based on commit messages
   - Semantic versioning for easy version comparison

2. **Docker Tag Management**

   - Latest tag always points to newest stable release
   - Pre-release versions clearly marked
   - Version-specific tags for reproducibility

3. **Release Process**
   - Automated releases from commits
   - Pre-releases for testing
   - No manual version management needed

## Conclusion

This versioning strategy provides several advantages:

- Automated version management
- Clear distinction between stable and pre-release versions
- Reliable Docker image tagging
- Easy rollback capabilities
- Simplified testing of new features

By leveraging semantic release with Docker tags, we maintain a clear and automated versioning system that supports both production stability and feature testing.

---

_Note: All configuration files mentioned are available in our repository._
