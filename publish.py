#!/usr/bin/env python3
"""
Automated publishing script for FixtureGPT.
"""

import argparse
import subprocess
import sys
import shutil
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    
    return result


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed {path}")


def build_package():
    """Build the package."""
    print("🔨 Building package...")
    run_command("python -m build")
    
    # List built files
    dist_dir = Path("dist")
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        print("📦 Built files:")
        for file in files:
            print(f"  - {file}")


def validate_package():
    """Validate the built package."""
    print("✅ Validating package...")
    run_command("python -m twine check dist/*")


def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("🧪 Uploading to TestPyPI...")
    run_command("python -m twine upload --repository testpypi dist/*")
    print("✅ Uploaded to TestPyPI: https://test.pypi.org/project/fixturegpt/")


def upload_to_pypi():
    """Upload to PyPI."""
    print("🚀 Uploading to PyPI...")
    
    # Confirm upload
    response = input("Are you sure you want to upload to PyPI? (y/N): ")
    if response.lower() != 'y':
        print("❌ Upload cancelled")
        return
    
    run_command("python -m twine upload dist/*")
    print("✅ Uploaded to PyPI: https://pypi.org/project/fixturegpt/")


def test_installation(test_pypi=False):
    """Test installation of the package."""
    print("🧪 Testing installation...")
    
    if test_pypi:
        cmd = "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fixturegpt"
    else:
        cmd = "pip install fixturegpt"
    
    print(f"To test installation, run: {cmd}")
    print("Then test with:")
    print('  python -c "from fixturegpt import snapshot; print(\'Import successful!\')"')
    print("  fixturegpt --help")


def main():
    parser = argparse.ArgumentParser(description="Publish FixtureGPT package")
    parser.add_argument("--test", action="store_true", help="Upload to TestPyPI")
    parser.add_argument("--prod", action="store_true", help="Upload to PyPI")
    parser.add_argument("--build-only", action="store_true", help="Only build, don't upload")
    
    args = parser.parse_args()
    
    if not any([args.test, args.prod, args.build_only]):
        parser.print_help()
        return
    
    try:
        # Check if required tools are installed
        run_command("python -m build --version")
        run_command("python -m twine --version")
    except:
        print("❌ Missing required tools. Install with:")
        print("pip install build twine")
        sys.exit(1)
    
    # Always clean and build
    clean_build()
    build_package()
    validate_package()
    
    if args.build_only:
        print("✅ Build complete!")
        return
    
    if args.test:
        upload_to_testpypi()
        test_installation(test_pypi=True)
    
    if args.prod:
        upload_to_pypi()
        test_installation(test_pypi=False)
    
    print("🎉 Publishing complete!")


if __name__ == "__main__":
    main() 