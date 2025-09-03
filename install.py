#!/usr/bin/env python3
"""
Installation script for AGT Server

This script provides an easy way to install the AGT Server package
with various installation options.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
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

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        print(f"  Current version: {sys.version}")
        return False
    
    print(f"✓ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("✗ pip is not available. Please install pip first.")
        return False
    
    # Install dependencies
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        if not run_command([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         "Installing requirements from requirements.txt"):
            return False
    else:
        print("⚠ requirements.txt not found, skipping dependency installation")
    
    return True

def install_package(editable=False, user=False):
    """Install the AGT Server package."""
    print("\nInstalling AGT Server package...")
    
    cmd = [sys.executable, "-m", "pip", "install"]
    
    if editable:
        cmd.append("-e")
        print("Installing in editable mode (development)")
    
    if user:
        cmd.append("--user")
        print("Installing for current user only")
    
    cmd.append(".")
    
    if not run_command(cmd, "Installing AGT Server package"):
        return False
    
    return True

def verify_installation():
    """Verify that the package was installed correctly."""
    print("\nVerifying installation...")
    
    try:
        # Try to import the package
        import agt_server
        print(f"✓ Package imported successfully: {agt_server.__version__}")
        
        # Check if CLI commands are available
        try:
            result = subprocess.run(["agt-server", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ CLI command 'agt-server' is available")
            else:
                print("⚠ CLI command 'agt-server' may not be in PATH")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠ CLI command 'agt-server' not found in PATH")
        
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import package: {e}")
        return False

def main():
    """Main installation function."""
    parser = argparse.ArgumentParser(
        description="Install AGT Server package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py                    # Install in development mode
  python install.py --production      # Install in production mode
  python install.py --user            # Install for current user only
  python install.py --no-deps         # Skip dependency installation
        """
    )
    
    parser.add_argument(
        "--production", 
        action="store_true",
        help="Install in production mode (not editable)"
    )
    parser.add_argument(
        "--user", 
        action="store_true",
        help="Install for current user only"
    )
    parser.add_argument(
        "--no-deps", 
        action="store_true",
        help="Skip dependency installation"
    )
    
    args = parser.parse_args()
    
    print("AGT Server Installation Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Change to package directory
    package_dir = Path(__file__).parent
    os.chdir(package_dir)
    print(f"Working directory: {os.getcwd()}")
    
    # Install dependencies
    if not args.no_deps:
        if not install_dependencies():
            print("\n✗ Dependency installation failed. Please check the errors above.")
            sys.exit(1)
    
    # Install package
    editable = not args.production
    if not install_package(editable=editable, user=args.user):
        print("\n✗ Package installation failed. Please check the errors above.")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\n✗ Installation verification failed.")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("🎉 AGT Server installation completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: agt-server --game rps")
    print("2. Start the dashboard: agt-dashboard")
    print("3. Or run both: python -m agt_server.cli both")
    print("4. View examples: python examples/basic_usage.py")
    print("\nFor help: agt-server --help")

if __name__ == "__main__":
    main()
