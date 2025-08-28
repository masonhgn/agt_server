# AGT Server - Algorithmic Game Theory Lab Platform

A platform for running algorithmic game theory lab competitions with real-time dashboard monitoring.

## Installation and Setup

### 1. Create Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install main requirements
pip install -r requirements.txt

# Install server requirements
pip install -r server/requirements.txt

# Install dashboard requirements
pip install -r dashboard/requirements.txt
```

## Running the Labs

### 1. Start the AGT Server

```bash
# Start the main AGT server
python server/server.py

# The server will start on localhost:8080 by default
```

### 2. Start the Dashboard (Optional)

In a new terminal:

```bash
# Navigate to dashboard directory
cd dashboard

# Start the Flask dashboard
python app.py

# The dashboard will be available at http://localhost:8081
```

### 3. Connect a Stencil Solution

Navigate to any lab stencil directory and run a competition agent:

```bash
# Example: Lab 1 Chicken Game
cd stencils/lab01_stencil/solutions

# Edit competition_agent.py to set server = True
# Then run:
python competition_agent_solution.py


```

