# Release Process

This document describes the release process for the MCP Descope SDK.

## Automated Release Process

The SDK uses GitHub Actions workflows to automate releases and PyPI publishing.

### Triggering a Release

There are two ways to trigger a release:

#### 1. Create a GitHub Release (Recommended)

1. Go to the [Releases page](https://github.com/your-org/mcp-descope/releases)
2. Click "Draft a new release"
3. Create a new tag (e.g., `v1.0.0`)
4. Fill in the release title and description
5. Click "Publish release"

The workflow will automatically:
- Extract the version from the tag
- Update version in `pyproject.toml` and `__init__.py`
- Build the package
- Publish to PyPI

#### 2. Push a Version Tag

```bash
# Update version in pyproject.toml and __init__.py first
git tag v1.0.0
git push origin v1.0.0
```

The workflow will automatically:
- Extract the version from the tag
- Build the package
- Publish to PyPI

#### 3. Manual Workflow Dispatch

1. Go to Actions → Release workflow
2. Click "Run workflow"
3. Enter the version number (e.g., `1.0.0`)
4. Click "Run workflow"

This will:
- Update version in files
- Build the package
- Publish to PyPI
- Create a git tag
- Create a GitHub release

## Manual Release Process

If you need to release manually:

### Prerequisites

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Set up PyPI credentials:
   ```bash
   # Create ~/.pypirc or use environment variables
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=your-pypi-token
   ```

### Steps

1. **Update version** in `pyproject.toml` and `src/descope_mcp/__init__.py`

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Check the package**:
   ```bash
   twine check dist/*
   ```

4. **Test the package** (optional):
   ```bash
   pip install dist/descope_mcp-*.whl
   ```

5. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

6. **Create git tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

7. **Create GitHub release** (optional but recommended)

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backward compatible manner
- **PATCH**: Backward compatible bug fixes

## PyPI Trusted Publishing

The workflows use PyPI's trusted publishing feature. To set it up:

1. Go to your PyPI project settings
2. Navigate to "Manage" → "Publishing"
3. Add a new trusted publisher
4. Use the GitHub Actions workflow:
   - Owner: `your-org`
   - Repository: `mcp-descope`
   - Workflow filename: `.github/workflows/publish.yml`
   - Environment: (leave empty or use `release`)

## Troubleshooting

### Build fails
- Check that `pyproject.toml` is valid
- Ensure all dependencies are listed correctly
- Check Python version compatibility

### Upload fails
- Verify PyPI credentials
- Check if version already exists (PyPI doesn't allow overwriting)
- Ensure you have maintainer/owner permissions

### Version not updating
- Check that version format matches exactly (e.g., `"1.0.0"` not `1.0.0`)
- Verify sed command worked correctly
- Check git tag format (should be `v1.0.0`)
