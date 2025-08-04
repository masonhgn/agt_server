Quick Start Guide
================

This guide will get you up and running with AGT Server in minutes.

Prerequisites
------------

* AGT Server installed (see :doc:`installation`)
* Python 3.8 or higher
* Basic understanding of Python

Starting the Server
------------------

1. **Navigate to the project directory**:

   .. code-block:: bash

      cd agt_server_new

2. **Start the server**:

   .. code-block:: bash

      python server/server.py

   You should see output like:

   .. code-block:: text

      INFO - AGT Server starting on 0.0.0.0:8080
      INFO - Server ready for connections

3. **Keep the server running** in a terminal window

Running Your First Lab
---------------------

1. **Open a new terminal** and navigate to a lab directory:

   .. code-block:: bash

      cd stencils/lab01_stencil

2. **Run the example solution**:

   .. code-block:: bash

      python example_solution.py

   This will connect to the server and play Rock Paper Scissors.

3. **Check the results** in the `results/` directory

Creating Your First Agent
------------------------

1. **Navigate to a lab stencil**:

   .. code-block:: bash

      cd stencils/lab01_stencil

2. **Edit the competition agent**:

   .. code-block:: python

      # In competition_agent.py
      class MyAgent(BaseAgent):
          def get_action(self, observation):
              # Your strategy here
              return "rock"  # Simple example
          
          def update(self, reward, info):
              # Learn from results
              pass

3. **Run your agent**:

   .. code-block:: bash

      python competition_agent.py

Connecting Multiple Clients
--------------------------

1. **Start the server** (if not already running):

   .. code-block:: bash

      python server/server.py

2. **Open multiple terminals** and run different agents:

   Terminal 1:
   .. code-block:: bash

      cd stencils/lab01_stencil
      python example_solution.py

   Terminal 2:
   .. code-block:: bash

      cd stencils/lab01_stencil
      python competition_agent.py

3. **Watch the tournament** unfold in the server logs

Running Tournaments
-------------------

1. **Use the local arena** for automated tournaments:

   .. code-block:: bash

      python core/local_arena.py --game rps --agents random stubborn

2. **Check tournament results**:

   .. code-block:: bash

      ls results/
      cat results/tournament_results_*.csv

Common Commands
---------------

.. code-block:: bash

   # Start server
   python server/server.py

   # Run a specific lab
   python stencils/lab01_stencil/example_solution.py

   # Run tests
   pytest tests/

   # Run local tournament
   python core/local_arena.py --help

   # Check server status
   curl http://localhost:8080/status

Configuration
------------

The server can be configured through:

1. **Command line arguments**:

   .. code-block:: bash

      python server/server.py --host 127.0.0.1 --port 9000

2. **Environment variables**:

   .. code-block:: bash

      export AGT_SERVER_HOST=127.0.0.1
      export AGT_SERVER_PORT=9000
      python server/server.py

3. **Configuration files**:

   .. code-block:: bash

      cp server/configs/lab01_rps.json my_config.json
      python server/server.py --config my_config.json

Troubleshooting
--------------

**Server won't start**:
   * Check if port 8080 is available
   * Try a different port: `python server/server.py --port 9000`

**Client can't connect**:
   * Ensure server is running
   * Check firewall settings
   * Verify host/port configuration

**Import errors**:
   * Ensure you're in the correct directory
   * Activate virtual environment if using one
   * Check Python path: `python -c "import sys; print(sys.path)"`

**No results generated**:
   * Check permissions for results directory
   * Ensure agents are completing games
   * Look for error messages in server logs

Next Steps
----------

Now that you're up and running:

1. **Explore different labs**:
   * :doc:`../labs/lab01-rps` - Basic game theory
   * :doc:`../labs/lab02-bos` - Finite state machines
   * :doc:`../labs/lab03-chicken` - Q-learning
   * :doc:`../labs/lab04-lemonade` - Spatial games
   * :doc:`../labs/lab06-auction` - Auction theory

2. **Learn about the architecture**:
   * :doc:`../developer-guide/architecture`
   * :doc:`../diagrams/architecture`

3. **Extend the system**:
   * :doc:`../developer-guide/adding-games`
   * :doc:`../developer-guide/adding-agents`

4. **Join the community**:
   * Report issues on GitHub
   * Contribute improvements
   * Share your agent strategies

For more detailed information, see the :doc:`../user-guide/running-labs` guide. 