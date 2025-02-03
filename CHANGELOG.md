# CHANGELOG


## v0.3.4 (2025-02-03)

### Bug Fixes

- Fixing release logic
  ([`615f0bc`](https://github.com/sudo-whodo/pr-genius/commit/615f0bca07f9aae08aa5c9f3927db5d45a2a9c90))


## v0.3.3 (2025-02-03)

### Bug Fixes

- Trigger release
  ([`66423ba`](https://github.com/sudo-whodo/pr-genius/commit/66423ba044604773a93c3cd0c4620d5c4264aa2a))


## v0.3.2 (2025-02-03)

### Bug Fixes

- Update entrypoint logic added more tests
  ([`e9ab4ff`](https://github.com/sudo-whodo/pr-genius/commit/e9ab4ff77850bdf573e951037a35a3eccbb2d8a4))


## v0.3.1 (2025-02-03)

### Bug Fixes

- Correct varaible name and docs
  ([`e77638d`](https://github.com/sudo-whodo/pr-genius/commit/e77638df656a3b0ad52fa44eb9f9e248b17c462e))

- Correcting entrypoint for model
  ([`6e03caa`](https://github.com/sudo-whodo/pr-genius/commit/6e03caabeb2de68d2d49095e35a00f42404e5103))


## v0.3.0 (2025-02-03)

### Features

- Trigger release
  ([`68be615`](https://github.com/sudo-whodo/pr-genius/commit/68be615c56dc7229cd7497360557453c7172fa64))

- **llm**: Add Ollama and Bedrock support with local testing
  ([`b402b4a`](https://github.com/sudo-whodo/pr-genius/commit/b402b4a022c09e12e4919a3d7e4192605cc26c6a))

- Add support for Ollama and AWS Bedrock providers - Add test-action-local.sh script for GitHub
  Action testing - Add Docker container support for Ollama with health checks - Document local
  action testing with act in usage guide - Add testing steps to release workflow - Update changelog
  format and content - Add M-series Mac support for containers

BREAKING CHANGES: - System prompts now configurable via environment variables - test-local.sh moved
  to examples directory"


## v0.2.0 (2025-02-01)

### Features

- Added arm64 image
  ([`8f9c77c`](https://github.com/sudo-whodo/pr-genius/commit/8f9c77c017a1aacbaf05a876ae46329c8ac76c9b))


## v0.1.16 (2025-02-01)

### Bug Fixes

- Update action
  ([`1bd0567`](https://github.com/sudo-whodo/pr-genius/commit/1bd05677215ac96f1698c582fb14f76d3318dee3))


## v0.1.15 (2025-02-01)

### Bug Fixes

- Remove env and wiith
  ([`6cf16ef`](https://github.com/sudo-whodo/pr-genius/commit/6cf16ef607f834ae969f8019a3992f3a53a3f397))

- Test
  ([`0300b5d`](https://github.com/sudo-whodo/pr-genius/commit/0300b5d764b3387d4525dfb9a5d55620beb9fd9a))


## v0.1.14 (2025-02-01)

### Bug Fixes

- Removed redundent inputs to just use env
  ([`069faff`](https://github.com/sudo-whodo/pr-genius/commit/069faff1be3cf2def59941d105ea52d6e92e63ba))


## v0.1.13 (2025-02-01)

### Bug Fixes

- Updating variables
  ([`490adb5`](https://github.com/sudo-whodo/pr-genius/commit/490adb5d040023f6a9b5664194093dd028a2a5cf))


## v0.1.12 (2025-01-31)

### Bug Fixes

- Adding example docs
  ([`958974d`](https://github.com/sudo-whodo/pr-genius/commit/958974d95b311639272fddb0de5d3f050ef0495e))

- Update to use pr token
  ([`de93951`](https://github.com/sudo-whodo/pr-genius/commit/de93951d9b887a52d92d111ec8bd2d4021eac1af))


## v0.1.11 (2025-01-31)

### Bug Fixes

- Update
  ([`bfc31ce`](https://github.com/sudo-whodo/pr-genius/commit/bfc31ce1701f6d8c831c7b9b4d67be132835226b))


## v0.1.10 (2025-01-31)

### Bug Fixes

- Added bash to build and test container locally and updates to the container build and reqirements.
  ([`7945a0c`](https://github.com/sudo-whodo/pr-genius/commit/7945a0cea31164b12714ab65feed216183c7253f))


## v0.1.9 (2025-01-31)

### Bug Fixes

- Removed all extra parameters and kept only the essential ones:
  ([`ed8fffd`](https://github.com/sudo-whodo/pr-genius/commit/ed8fffdc9ef4752b7e35080c97bbae149910cd42))


## v0.1.8 (2025-01-31)

### Bug Fixes

- Adding the bot to pr
  ([`b4b4679`](https://github.com/sudo-whodo/pr-genius/commit/b4b4679f9a16e56e4236ab5a120293fef57d9d82))

- Fixing container issues
  ([`e833ed0`](https://github.com/sudo-whodo/pr-genius/commit/e833ed099fc5de44d432e31d8a841d64b1bc9a57))

- Fixing pr-analysis
  ([`bfec36c`](https://github.com/sudo-whodo/pr-genius/commit/bfec36c072b33c6b5aa563b9dbc4ce1a1df92839))

- Removed proxies configuration and added http_client parameter
  ([`7f884b4`](https://github.com/sudo-whodo/pr-genius/commit/7f884b483d755990ac45ce18ab508ebcfcb026ee))

- Update version
  ([`ac11347`](https://github.com/sudo-whodo/pr-genius/commit/ac113473a72a903bcd1093a909f8e16cdc0f8545))

- Updating openai call
  ([`289ad01`](https://github.com/sudo-whodo/pr-genius/commit/289ad014537c6ad67906226ddc7748713975c3a8))


## v0.1.7 (2025-01-31)

### Bug Fixes

- Update release workflow
  ([`76a573e`](https://github.com/sudo-whodo/pr-genius/commit/76a573ec465762a70210970187124e1a433e608b))


## v0.1.6 (2025-01-31)

### Bug Fixes

- Add label
  ([`fc39fcb`](https://github.com/sudo-whodo/pr-genius/commit/fc39fcb3f5025c18e78c2d293fb500b89a547219))

- Added debugging
  ([`cbf91e0`](https://github.com/sudo-whodo/pr-genius/commit/cbf91e0e6226cbd9b5cc749a3e7640d3f5dbf78b))

- Added labels
  ([`c80178b`](https://github.com/sudo-whodo/pr-genius/commit/c80178b27a516f71e95c540719e5837a9d6340a0))

- Added updates and unit tests
  ([`ae6f8f4`](https://github.com/sudo-whodo/pr-genius/commit/ae6f8f42ba1754d351f3c4d66c56446c1cf26a19))

- Adding build for dependabot and updating merge
  ([`850ebf4`](https://github.com/sudo-whodo/pr-genius/commit/850ebf47e7bcb59eaa9349dedcbd2f89d2b3849d))

- Check if patch works
  ([`0d832f0`](https://github.com/sudo-whodo/pr-genius/commit/0d832f043f43756b3f8ea2408364c02d62d6da9f))

- Init
  ([`a0c382d`](https://github.com/sudo-whodo/pr-genius/commit/a0c382d1c788da5b023f838b475521d4179c9a0d))

- Removed auto-release workflow
  ([`52c38f4`](https://github.com/sudo-whodo/pr-genius/commit/52c38f4f726a7de2165a7be4bb87d54d6837ffe4))

- Removing timestamp from release
  ([`d5d93b5`](https://github.com/sudo-whodo/pr-genius/commit/d5d93b51e994f72515739c24f83d5f65310d833f))

- Up
  ([`d5d2557`](https://github.com/sudo-whodo/pr-genius/commit/d5d25570b8fe8f3bf087b6f4aa88fe8e8c570239))

- Update
  ([`9bbb7de`](https://github.com/sudo-whodo/pr-genius/commit/9bbb7dee2d4eaceada5ed5cb362aca1e6aebb268))

- Update
  ([`80bd207`](https://github.com/sudo-whodo/pr-genius/commit/80bd20725f84a3d81a65bb9fd0e51abe61490648))

- Update
  ([`a9d28ca`](https://github.com/sudo-whodo/pr-genius/commit/a9d28ca185e2139195d2dd6a0fb631591e8b0f11))

- Update
  ([`de4e4f6`](https://github.com/sudo-whodo/pr-genius/commit/de4e4f60476c6bdb1ad90bb826587e079fe9f676))

- Update
  ([`8e090d5`](https://github.com/sudo-whodo/pr-genius/commit/8e090d53af5ed615f4cc8a969d923e06aca33496))

- Update
  ([`dc63038`](https://github.com/sudo-whodo/pr-genius/commit/dc630383c0ce8781b99717720d697d409484a6bf))

- Update
  ([`d4447ae`](https://github.com/sudo-whodo/pr-genius/commit/d4447ae21c0f7b98593a760e11e8abf10faebcf3))

- Update
  ([`8ad567a`](https://github.com/sudo-whodo/pr-genius/commit/8ad567a17f0a6e6266ea4c083c9cf62038733a45))

- Update
  ([`ebe797f`](https://github.com/sudo-whodo/pr-genius/commit/ebe797f0645b6294f7df55d2e5db062473d62d7b))

- Update auto merge
  ([`c262230`](https://github.com/sudo-whodo/pr-genius/commit/c2622304434941efd6406dc73fc739f77426895f))

- Update build
  ([`8981f2f`](https://github.com/sudo-whodo/pr-genius/commit/8981f2f1a457cb5193bf5a7d20a84be0a4a9b7c7))

- Update dependabot
  ([`9b11340`](https://github.com/sudo-whodo/pr-genius/commit/9b113407302b22bff1a5d796f554774e81cf7bf1))

- Update dependabot
  ([`a752bb0`](https://github.com/sudo-whodo/pr-genius/commit/a752bb07ca1bc05357eee37b0be03c8d855ea0b7))

- Update realse for branch protection
  ([`da7e5e9`](https://github.com/sudo-whodo/pr-genius/commit/da7e5e9e8935a86173bbf5df208b0ad9d2b2ba81))

- Update release
  ([`07ecc92`](https://github.com/sudo-whodo/pr-genius/commit/07ecc92e392ae9fa2a4682228365ed2c411ed186))

- Update release
  ([`e4a48de`](https://github.com/sudo-whodo/pr-genius/commit/e4a48de5f0a0df471c85e6f6f658eda49f82dcc6))

- Update release
  ([`b70adba`](https://github.com/sudo-whodo/pr-genius/commit/b70adbaa283d1f1140e0e7b340b1d315bb49b0a0))

- Update release
  ([`2082f25`](https://github.com/sudo-whodo/pr-genius/commit/2082f2518623e886dd5fee11a65119d41def3f0c))

- Update release
  ([`7f49bab`](https://github.com/sudo-whodo/pr-genius/commit/7f49babd719b617eef211f721da593f9becc2037))

- Update release
  ([`65d619d`](https://github.com/sudo-whodo/pr-genius/commit/65d619d4219c190058791b0343f1e0fa95363ac7))

- Update release
  ([`d592f03`](https://github.com/sudo-whodo/pr-genius/commit/d592f03512ea4d88ff9835b42e1940c5dbac2606))

- Update release
  ([`42d23a8`](https://github.com/sudo-whodo/pr-genius/commit/42d23a8f25379002880dc72227545d5bcf106280))

- Update release
  ([`d1b8feb`](https://github.com/sudo-whodo/pr-genius/commit/d1b8feb525ff46e2d27f2aa8ace9b0c2fe769960))

- Update release workflow
  ([`5c40018`](https://github.com/sudo-whodo/pr-genius/commit/5c400183491dedce711127d04c358ad02520002a))

- Update to pat_token
  ([`f95cecf`](https://github.com/sudo-whodo/pr-genius/commit/f95cecfee71abcb3cb77e81c8663798c2346911d))

- Update toml and release
  ([`ae1d58d`](https://github.com/sudo-whodo/pr-genius/commit/ae1d58dbff2ad681635e66c8b63866c0b22881d9))

- Updates
  ([`972c05a`](https://github.com/sudo-whodo/pr-genius/commit/972c05a3475d4a1d023b4c2bdb2416cb661f5f42))

- Updating dependabot
  ([`c93dc0c`](https://github.com/sudo-whodo/pr-genius/commit/c93dc0c96e24371ac2ff4527c4f4442c5fe25d05))

- **deps**: Bump commitizen from 3.13.0 to 4.1.1 in /pr-diff-bot
  ([`fdbb247`](https://github.com/sudo-whodo/pr-genius/commit/fdbb247257aadeb984304493bfdc04ec893beae2))

Bumps [commitizen](https://github.com/commitizen-tools/commitizen) from 3.13.0 to 4.1.1. - [Release
  notes](https://github.com/commitizen-tools/commitizen/releases) -
  [Changelog](https://github.com/commitizen-tools/commitizen/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/commitizen-tools/commitizen/compare/v3.13.0...v4.1.1)

--- updated-dependencies: - dependency-name: commitizen dependency-type: direct:production

update-type: version-update:semver-major

...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump docker/build-push-action from 5 to 6
  ([`7695090`](https://github.com/sudo-whodo/pr-genius/commit/7695090a94617cde4949a045bf6e27a390ae1093))

Bumps [docker/build-push-action](https://github.com/docker/build-push-action) from 5 to 6. -
  [Release notes](https://github.com/docker/build-push-action/releases) -
  [Commits](https://github.com/docker/build-push-action/compare/v5...v6)

--- updated-dependencies: - dependency-name: docker/build-push-action dependency-type:
  direct:production

update-type: version-update:semver-major

...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump gitpython from 3.1.41 to 3.1.44 in /pr-diff-bot
  ([`2f60312`](https://github.com/sudo-whodo/pr-genius/commit/2f6031246de753f8fcd0973a170506df0230d3e3))

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.41 to 3.1.44. -
  [Release notes](https://github.com/gitpython-developers/GitPython/releases) -
  [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES) -
  [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.41...3.1.44)

--- updated-dependencies: - dependency-name: gitpython dependency-type: direct:production

update-type: version-update:semver-patch

...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump python-semantic-release in /pr-diff-bot
  ([`fd7b210`](https://github.com/sudo-whodo/pr-genius/commit/fd7b210c73982265f2c7b3e6a4ed044a1d8afdbd))

Bumps [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 8.7.0 to 9.17.0. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v8.7.0...v9.17)

--- updated-dependencies: - dependency-name: python-semantic-release dependency-type:
  direct:production

update-type: version-update:semver-major

...

Signed-off-by: dependabot[bot] <support@github.com>

### Features

- Init
  ([`38126dd`](https://github.com/sudo-whodo/pr-genius/commit/38126ddbe0d96401992a83343d0c247f2bbbe7c8))

- Testing
  ([`24e7d37`](https://github.com/sudo-whodo/pr-genius/commit/24e7d3716cb5af6b20ba97ec56257942a6bacba1))
