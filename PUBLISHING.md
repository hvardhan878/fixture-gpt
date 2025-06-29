# Publishing FixtureGPT to PyPI

This guide covers how to build and publish FixtureGPT to PyPI.

## Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Create accounts:
   - [PyPI Account](https://pypi.org/account/register/)
   - [TestPyPI Account](https://test.pypi.org/account/register/) (for testing)

3. Configure API tokens:
   - Generate API tokens on PyPI and TestPyPI
   - Store in `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## Building the Package

1. Clean previous builds:
```bash
rm -rf build/ dist/ *.egg-info/
```

2. Build the package:
```bash
python -m build
```

This creates:
- `dist/fixturegpt-0.1.0.tar.gz` (source distribution)
- `dist/fixturegpt-0.1.0-py3-none-any.whl` (wheel distribution)

## Testing the Build

1. Test on TestPyPI first:
```bash
python -m twine upload --repository testpypi dist/*
```

2. Install from TestPyPI to test:
```bash
pip install --index-url https://test.pypi.org/simple/ fixturegpt
```

3. Test the installation:
```bash
python -c "from fixturegpt import snapshot; print('Import successful!')"
fixturegpt --help
```

## Publishing to PyPI

1. Upload to PyPI:
```bash
python -m twine upload dist/*
```

2. Verify the upload at: https://pypi.org/project/fixturegpt/

3. Test installation from PyPI:
```bash
pip install fixturegpt
```

## Automated Publishing Script

Use the included `publish.py` script:

```bash
# Test release
python publish.py --test

# Production release
python publish.py --prod
```

## Version Management

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a git tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```

## Post-Publication

1. Update documentation
2. Announce on social media/forums
3. Monitor for issues and feedback
4. Plan next version features

## Troubleshooting

### Common Issues

1. **Version already exists**: Increment version number
2. **Authentication failed**: Check API tokens
3. **Package validation errors**: Run `python -m build` and fix issues
4. **Missing files**: Check `MANIFEST.in` and `pyproject.toml`

### Validation

Before publishing, validate your package:
```bash
python -m twine check dist/*
``` 