Installation Guide
=================

This guide will help you install and set up the AGT Server for development and educational use.

Prerequisites
------------

Before installing AGT Server, ensure you have the following:

* Python 3.8 or higher
* pip (Python package installer)
* Git (for cloning the repository)

System Requirements
------------------

* **Operating System**: Linux, macOS, or Windows
* **Python**: 3.8, 3.9, 3.10, or 3.11
* **Memory**: At least 2GB RAM (4GB recommended)
* **Storage**: 100MB free space
* **Network**: Internet connection for package downloads

Installation Methods
-------------------

Method 1: Clone and Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Clone the repository**:

   .. code-block:: bash

      git clone https://github.com/your-repo/agt_server_new.git
      cd agt_server_new

2. **Create a virtual environment** (recommended):

   .. code-block:: bash

      python -m venv agt_env
      source agt_env/bin/activate  # On Windows: agt_env\Scripts\activate

3. **Install dependencies**:

   .. code-block:: bash

      pip install -r requirements.txt

4. **Verify installation**:

   .. code-block:: bash

      python -c "import core; print('AGT Server installed successfully!')"

Method 2: Using pip (if published to PyPI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install agt-server

Configuration
------------

After installation, you may need to configure the server:

1. **Create configuration directory**:

   .. code-block:: bash

      mkdir -p ~/.agt_server
      cp server/configs/lab01_rps.json ~/.agt_server/

2. **Set environment variables** (optional):

   .. code-block:: bash

      export AGT_SERVER_HOST=0.0.0.0
      export AGT_SERVER_PORT=8080
      export AGT_LOG_LEVEL=INFO

Development Installation
-----------------------

For developers who want to contribute to the project:

1. **Clone with development dependencies**:

   .. code-block:: bash

      git clone https://github.com/your-repo/agt_server_new.git
      cd agt_server_new

2. **Install in development mode**:

   .. code-block:: bash

      pip install -e .
      pip install -r requirements-dev.txt

3. **Install pre-commit hooks**:

   .. code-block:: bash

      pre-commit install

4. **Run tests**:

   .. code-block:: bash

      pytest tests/

Docker Installation
------------------

For containerized deployment:

1. **Build the Docker image**:

   .. code-block:: dockerfile

      FROM python:3.9-slim
      WORKDIR /app
      COPY requirements.txt .
      RUN pip install -r requirements.txt
      COPY . .
      EXPOSE 8080
      CMD ["python", "server/server.py"]

2. **Run with Docker**:

   .. code-block:: bash

      docker build -t agt-server .
      docker run -p 8080:8080 agt-server

Troubleshooting
--------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: ImportError for core modules
   **Solution**: Ensure you're in the project root directory and Python path is set correctly.

**Issue**: Port already in use
   **Solution**: Change the port in server configuration or kill the process using the port.

**Issue**: Permission denied
   **Solution**: Use virtual environment or install with user permissions.

**Issue**: Missing dependencies
   **Solution**: Update pip and reinstall requirements: ``pip install --upgrade pip && pip install -r requirements.txt``

Verification
-----------

To verify your installation is working correctly:

1. **Start the server**:

   .. code-block:: bash

      python server/server.py

2. **Test client connection**:

   .. code-block:: bash

      python server/client.py --test

3. **Run basic tests**:

   .. code-block:: bash

      python -m pytest tests/test_server.py -v

Next Steps
----------

After successful installation:

1. Read the :doc:`../getting-started/quick-start` guide
2. Explore the :doc:`../user-guide/running-labs` documentation
3. Check out the :doc:`../labs/lab01-rps` for your first lab

For more detailed information, see the :doc:`../developer-guide/architecture` guide. 