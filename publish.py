#!/usr/bin/env python3
"""
Publishing script for AGT Server package

This script automates the process of building and publishing
the package to PyPI or TestPyPI.
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error code: {e.returncode}")
        if e.stdout:
            print(f"  stdout: {e.stdout}")
        if e.stderr:
            print(f"  stderr: {e.stderr}")
        return False

def check_requirements():
    """Check if required tools are installed."""
    print("Checking requirements...")
    
    # Check build
    try:
        subprocess.run([sys.executable, "-m", "build", "--version"], 
                      check=True, capture_output=True)
        print("✓ build tool is available")
    except (subprocess.CalledProcessError, ImportError):
        print("✗ build tool not found. Installing...")
        if not run_command([sys.executable, "-m", "pip", "install", "build"], 
                          "Installing build tool"):
            return False
    
    # Check twine
    try:
        subprocess.run([sys.executable, "-m", "twine", "--version"], 
                      check=True, capture_output=True)
        print("✓ twine tool is available")
    except (subprocess.CalledProcessError, ImportError):
        print("✗ twine tool not found. Installing...")
        if not run_command([sys.executable, "-m", "pip", "install", "twine"], 
                          "Installing twine tool"):
            return False
    
    return True

def clean_build():
    """Clean previous build artifacts."""
    print("\nCleaning previous build artifacts...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed directory: {path}")
            elif path.is_file():
                path.unlink()
                print(f"  Removed file: {path}")
    
    print("✓ Build cleanup completed")

def build_package():
    """Build the package distribution."""
    print("\nBuilding package distribution...")
    
    if not run_command([sys.executable, "-m", "build"], "Building package"):
        return False
    
    # Check what was built
    dist_dir = Path("dist")
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        print(f"✓ Built {len(files)} distribution files:")
        for file in files:
            print(f"  {file.name}")
    
    return True

def test_package():
    """Test the built package."""
    print("\nTesting built package...")
    
    # Find the wheel file
    dist_dir = Path("dist")
    wheel_files = list(dist_dir.glob("*.whl"))
    
    if not wheel_files:
        print("✗ No wheel files found to test")
        return False
    
    wheel_file = wheel_files[0]
    print(f"Testing wheel: {wheel_file.name}")
    
    # Test installation
    if not run_command([sys.executable, "-m", "pip", "install", "--force-reinstall", str(wheel_file)], 
                      "Testing package installation"):
        return False
    
    # Test import
    try:
        import agt_server
        print(f"✓ Package imported successfully: {agt_server.__version__}")
        return True
    except ImportError as e:
        print(f"✗ Package import failed: {e}")
        return False

def upload_to_pypi(repository="pypi", username=None, password=None):
    """Upload package to PyPI."""
    print(f"\nUploading to {repository.upper()}...")
    
    cmd = [sys.executable, "-m", "twine", "upload"]
    
    if repository == "testpypi":
        cmd.extend(["--repository", "testpypi"])
    
    if username and password:
        cmd.extend(["--username", username, "--password", password])
    
    cmd.append("dist/*")
    
    if not run_command(cmd, f"Uploading to {repository}"):
        return False
    
    print(f"✓ Package uploaded to {repository.upper()} successfully!")
    return True

def main():
    """Main publishing function."""
    parser = argparse.ArgumentParser(
        description="Publish AGT Server package to PyPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python publish.py                    # Build and test package
  python publish.py --test            # Upload to TestPyPI
  python publish.py --publish         # Upload to PyPI
  python publish.py --test --publish  # Test then publish
        """
    )
    
    parser.add_argument(
        "--test", 
        action="store_true",
        help="Upload to TestPyPI for testing"
    )
    parser.add_argument(
        "--publish", 
        action="store_true",
        help="Upload to production PyPI"
    )
    parser.add_argument(
        "--username", 
        type=str,
        help="PyPI username (will prompt if not provided)"
    )
    parser.add_argument(
        "--password", 
        type=str,
        help="PyPI password (will prompt if not provided)"
    )
    parser.add_argument(
        "--skip-build", 
        action="store_true",
        help="Skip building, use existing dist/ files"
    )
    
    args = parser.parse_args()
    
    print("AGT Server Package Publisher")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n✗ Requirements check failed. Please install missing tools.")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build package (unless skipped)
    if not args.skip_build:
        if not build_package():
            print("\n✗ Package build failed.")
            sys.exit(1)
    
    # Test package
    if not test_package():
        print("\n✗ Package test failed.")
        sys.exit(1)
    
    # Upload to TestPyPI if requested
    if args.test:
        print("\n" + "=" * 40)
        print("TESTING: Uploading to TestPyPI")
        print("=" * 40)
        
        if not upload_to_pypi("testpypi", args.username, args.password):
            print("\n✗ TestPyPI upload failed.")
            sys.exit(1)
        
        print("\n🎉 Package uploaded to TestPyPI successfully!")
        print("You can now test installation with:")
        print("  pip install --index-url https://test.pypi.org/simple/ agt-server")
    
    # Upload to production PyPI if requested
    if args.publish:
        print("\n" + "=" * 40)
        print("PRODUCTION: Uploading to PyPI")
        print("=" * 40)
        
        if not args.test:
            print("⚠ WARNING: Publishing directly to PyPI without testing on TestPyPI!")
            response = input("Are you sure you want to continue? (y/N): ")
            if response.lower() != 'y':
                print("Publishing cancelled.")
                sys.exit(0)
        
        if not upload_to_pypi("pypi", args.username, args.password):
            print("\n✗ PyPI upload failed.")
            sys.exit(1)
        
        print("\n🎉 Package published to PyPI successfully!")
        print("Users can now install with:")
        print("  pip install agt-server")
    
    # Summary
    print("\n" + "=" * 40)
    if args.test or args.publish:
        print("🎉 Publishing completed successfully!")
    else:
        print("✅ Package built and tested successfully!")
        print("\nTo publish, run:")
        print("  python publish.py --test        # Upload to TestPyPI")
        print("  python publish.py --publish     # Upload to PyPI")
        print("  python publish.py --test --publish  # Test then publish")

if __name__ == "__main__":
    main()
