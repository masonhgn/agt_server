# AGT Server Package Setup Guide

This document explains how the AGT Server has been set up as a Python package and how users can install and use it.

## Package Structure

The `agt_server` has been transformed into a proper Python package with the following structure:

```
agt_server/
├── __init__.py          # Package initialization with convenient imports
├── cli.py              # Command-line interface for server and dashboard
├── server/             # Tournament server implementation
├── dashboard/          # Web dashboard
├── core/               # Game engine and core logic
├── examples/           # Usage examples
├── pyproject.toml      # Modern Python packaging configuration
├── setup.py            # Traditional setup configuration
├── MANIFEST.in         # Package file inclusion rules
├── requirements.txt    # Dependencies
├── install.py          # Easy installation script
├── test_package.py     # Package verification script
└── README.md           # Comprehensive documentation
```

## Key Features

### 1. **Command Line Tools**
After installation, users get these commands:
- `agt-server` - Start the tournament server
- `agt-dashboard` - Start the web dashboard
- `agt-dashboard-gui` - Start dashboard as GUI application

### 2. **Python API**
Users can import and use the package in their Python code:
```python
from agt_server import AGTServer, RPSGame, BOSGame

# Create server
server = AGTServer({"game_type": "rps", "num_rounds": 100})
```

### 3. **Easy Installation**
Multiple installation methods:
- `pip install -e .` (development)
- `python install.py` (automated installation)
- `pip install .` (production)

## Installation Methods

### Method 1: Automated Installation (Recommended)
```bash
cd agt_server
python install.py
```

### Method 2: Manual Installation
```bash
cd agt_server
pip install -e .
```

### Method 3: Production Installation
```bash
cd agt_server
pip install .
```

## Usage Examples

### Command Line Usage

**Start Server:**
```bash
agt-server --game rps --port 8080 --verbose
```

**Start Dashboard:**
```bash
agt-dashboard --port 8081 --server-port 8080
```

**Start Both Together:**
```bash
python -m agt_server.cli both --game rps
```

### Python API Usage

**Basic Server:**
```python
import asyncio
from agt_server import AGTServer

config = {"game_type": "rps", "num_rounds": 100}
server = AGTServer(config, host="localhost", port=8080)
asyncio.run(server.run())
```

**Direct Game Usage:**
```python
from agt_server import RPSGame, BOSGame

rps = RPSGame(num_rounds=50)
bos = BOSGame(num_rounds=100)
```

## Package Configuration Files

### 1. **pyproject.toml**
- Modern Python packaging standard
- Defines package metadata, dependencies, and entry points
- Entry points create the `agt-server` and `agt-dashboard` commands

### 2. **setup.py**
- Traditional setup configuration for compatibility
- Alternative to pyproject.toml
- Useful for older Python packaging tools

### 3. **MANIFEST.in**
- Controls which files are included in the package
- Excludes test files, documentation, and development artifacts
- Ensures only necessary files are distributed

## Entry Points

The package defines these command-line entry points:

```toml
[project.scripts]
agt-server = "agt_server.cli:run_server"
agt-dashboard = "agt_server.cli:run_dashboard"

[project.gui-scripts]
agt-dashboard-gui = "agt_server.cli:run_dashboard"
```

This means after installation:
- `agt-server` command runs `agt_server.cli.run_server()`
- `agt-dashboard` command runs `agt_server.cli.run_dashboard()`
- `agt-dashboard-gui` command runs the dashboard as a GUI app

## CLI Module Features

The `cli.py` module provides:

1. **`run_server()`** - Starts the tournament server with command-line arguments
2. **`run_dashboard()`** - Starts the web dashboard
3. **`run_both()`** - Starts both server and dashboard together
4. **Argument parsing** - Comprehensive CLI options for all features
5. **Error handling** - Graceful error handling and user feedback

## Package Imports

The `__init__.py` file provides convenient imports:

```python
# Main classes
from agt_server import AGTServer, GameEngine

# Game classes
from agt_server import RPSGame, BOSGame, ChickenGame, PDGame, LemonadeGame, AuctionGame
```

## Testing the Package

After installation, verify everything works:

```bash
python test_package.py
```

This script tests:
- Package imports
- Class availability
- Module functionality
- CLI command availability

## Building and Distributing

### Build the Package
```bash
# Install build tools
pip install build

# Build package
python -m build
```

### Install from Built Package
```bash
pip install dist/agt_server-0.1.0.tar.gz
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory when installing
2. **CLI Commands Not Found**: Check if the package installed correctly with `pip list`
3. **Permission Errors**: Use `--user` flag or virtual environment
4. **Dependency Issues**: Run `python install.py` to install all dependencies

### Verification Steps

1. **Check Installation**: `pip list | grep agt-server`
2. **Test Imports**: `python -c "import agt_server; print(agt_server.__version__)"`
3. **Test CLI**: `agt-server --help`
4. **Run Tests**: `python test_package.py`

## Next Steps

After successful installation:

1. **Start Learning**: Run `agt-server --help` to see all options
2. **Try Examples**: Run `python examples/basic_usage.py`
3. **Run Server**: Start with `agt-server --game rps`
4. **Use Dashboard**: Start with `agt-dashboard`
5. **Integrate**: Import the package in your own Python projects

## Publishing to PyPI

When ready to publish:

1. **Update Version**: Modify version in `pyproject.toml` and `setup.py`
2. **Build Package**: `python -m build`
3. **Upload**: `twine upload dist/*`
4. **Install**: Users can then `pip install agt-server`

## Summary

The AGT Server is now a fully-featured Python package that provides:

- ✅ Easy installation and setup
- ✅ Command-line tools for server and dashboard
- ✅ Python API for programmatic use
- ✅ Comprehensive documentation and examples
- ✅ Professional packaging standards
- ✅ Multiple installation methods
- ✅ Easy testing and verification

Users can now install the package and immediately start using it with simple commands like `agt-server --game rps` or by importing it in their Python code.
