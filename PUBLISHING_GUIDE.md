# Publishing AGT Server to PyPI

This guide explains how to publish the AGT Server package to PyPI so users can install it with `pip install agt-server`.

## 🎯 **What This Achieves**

After publishing, users will be able to:
```bash
pip install agt-server
agt-server --help
agt-dashboard --help
```

## 📋 **Prerequisites**

### **1. PyPI Accounts**
- **TestPyPI**: https://test.pypi.org/account/register/ (for testing)
- **PyPI**: https://pypi.org/account/register/ (for production)

### **2. Required Tools**
```bash
pip install build twine
```

### **3. Package Preparation**
Make sure your package is ready:
- All tests pass: `python test_package.py`
- Package builds successfully: `python -m build`
- CLI commands work: `agt-server --help`

## 🚀 **Quick Publishing Process**

### **Step 1: Test Build**
```bash
cd agt_server
python publish.py
```

### **Step 2: Test on TestPyPI**
```bash
python publish.py --test
```

### **Step 3: Publish to PyPI**
```bash
python publish.py --publish
```

## 📝 **Manual Publishing Steps**

If you prefer to do it manually:

### **1. Build the Package**
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build
```

### **2. Test the Build**
```bash
# Test installation from wheel
pip install dist/*.whl --force-reinstall

# Verify it works
python -c "import agt_server; print(agt_server.__version__)"
agt-server --help
```

### **3. Upload to TestPyPI**
```bash
# Upload to test repository
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ agt-server
```

### **4. Upload to Production PyPI**
```bash
# Upload to production
twine upload dist/*
```

## 🔧 **Using the Publishing Script**

The `publish.py` script automates the entire process:

### **Basic Usage**
```bash
# Just build and test
python publish.py

# Upload to TestPyPI
python publish.py --test

# Upload to PyPI
python publish.py --publish

# Test then publish
python publish.py --test --publish
```

### **Advanced Options**
```bash
# Skip building (use existing dist/ files)
python publish.py --test --skip-build

# Provide credentials
python publish.py --publish --username yourname --password yourpass
```

## 📦 **What Gets Published**

The package includes:
- ✅ All Python source code
- ✅ Command-line entry points (`agt-server`, `agt-dashboard`)
- ✅ Package metadata and dependencies
- ✅ README and documentation
- ✅ Dashboard templates and server configs

**Excludes:**
- ❌ Test files and directories
- ❌ Development artifacts
- ❌ Git history
- ❌ Build files

## 🔍 **Verifying Your Publication**

### **Check TestPyPI**
```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ agt-server

# Test functionality
agt-server --help
agt-dashboard --help
```

### **Check Production PyPI**
```bash
# Install from PyPI
pip install agt-server

# Test functionality
agt-server --help
agt-dashboard --help
```

## 🚨 **Important Considerations**

### **1. Package Name**
- The package will be published as `agt-server` on PyPI
- Make sure this name is available (check https://pypi.org/project/agt-server/)
- If taken, update `name` in `pyproject.toml` and `setup.py`

### **2. Version Management**
- Each upload must have a unique version
- Update version in both `pyproject.toml` and `setup.py`
- Follow semantic versioning (e.g., 0.1.0, 0.1.1, 1.0.0)

### **3. Dependencies**
- All dependencies in `requirements.txt` will be automatically installed
- Make sure all dependencies are available on PyPI
- Consider version constraints (e.g., `>=1.21.0` vs `==1.21.0`)

### **4. Security**
- Never commit credentials to version control
- Use environment variables or interactive prompts for passwords
- Consider using API tokens instead of passwords

## 🔄 **Updating Published Packages**

### **1. Update Version**
```toml
# In pyproject.toml
[project]
version = "0.1.1"  # Increment version
```

```python
# In setup.py
setup(
    version="0.1.1",  # Increment version
    # ... rest of config
)
```

### **2. Rebuild and Publish**
```bash
python publish.py --publish
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Package Name Already Taken**
```bash
# Check if name is available
pip search agt-server  # (if pip search works)
# Or check manually at https://pypi.org/project/agt-server/
```

**Solution**: Choose a different name or contact the owner

#### **Upload Fails with Authentication Error**
```bash
# Check your credentials
twine check dist/*

# Try interactive login
twine upload --username yourname dist/*
# (will prompt for password)
```

#### **Package Installs but Commands Don't Work**
```bash
# Check if entry points were created
pip show agt-server

# Check PATH
which agt-server

# Reinstall
pip uninstall agt-server
pip install agt-server
```

### **Verification Commands**
```bash
# Check package info
pip show agt-server

# List installed packages
pip list | grep agt

# Test imports
python -c "import agt_server; print(agt_server.__version__)"

# Test CLI
agt-server --help
agt-dashboard --help
```

## 📚 **After Publishing**

### **1. Update Documentation**
- Update your README with installation instructions
- Add PyPI badge: `[![PyPI version](https://badge.fury.io/py/agt-server.svg)](https://badge.fury.io/py/agt-server)`
- Update any installation guides

### **2. Announce Release**
- GitHub releases
- Social media
- Mailing lists
- Documentation updates

### **3. Monitor Usage**
- PyPI download statistics
- GitHub stars and issues
- User feedback

## 🎉 **Success!**

Once published, users can install your package with:
```bash
pip install agt-server
```

And immediately start using:
```bash
# Start server
agt-server --game rps

# Start dashboard
agt-dashboard

# Use in Python
python -c "
from agt_server import AGTServer
print('Package works!')
"
```

## 📖 **Additional Resources**

- **PyPI Help**: https://pypi.org/help/
- **Python Packaging Guide**: https://packaging.python.org/
- **Twine Documentation**: https://twine.readthedocs.io/
- **Build Documentation**: https://pypa-build.readthedocs.io/

## 🚀 **Next Steps**

1. **Test locally**: `python publish.py`
2. **Test on TestPyPI**: `python publish.py --test`
3. **Publish to PyPI**: `python publish.py --publish`
4. **Verify installation**: `pip install agt-server`
5. **Celebrate**: 🎉 Your package is now available worldwide!
