# CS1440/2440 Lab 1: Learning Agents for Repeated Games (Updated Codebase)

## Introduction
In this lab, part of the CS1440/2440 course, you will develop autonomous agents to play repeated games like Rock-Paper-Scissors. 
You'll implement strategies like Fictitious Play and Exponential Weights, and participate in a class competition.

This version uses the updated AGT codebase with a cleaner, more modular architecture.

## Setup and Installation

**IMPORTANT: Please install/use a version of `Python >= 3.10`**
To check which version of Python you're using please run
```bash
python --version
```

### Step 1: Create a Virtual Environment
Please navigate to your project directory. Run the following commands to create a Python virtual environment named `.venv`.

If you own a Mac 
```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you own a Windows 
```bash 
python3 -m venv .venv
.venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install numpy
```

## Agent Interface
The new codebase uses a simplified agent interface. Your agent must inherit from `BaseAgent` and implement:

- `act(obs)`: Return an action given an observation
- `update(reward)`: Update internal state with the reward received

### Available Methods
Your agent has access to these helpful methods:
- `self.get_action_history()`: Returns a list of your actions from previous rounds
- `self.get_reward_history()`: Returns a list of your rewards from previous rounds  
- `self.get_last_action()`: Returns your last action from the previous round
- `self.get_last_reward()`: Returns your last reward from the previous round
- `self.reset()`: Resets the agent's internal state for a new game

### Rock Paper Scissors Actions
- `0` = Rock
- `1` = Paper  
- `2` = Scissors

### Payoff Matrix (Row vs Column)
```
      Rock  Paper Scissors
Rock     0     -1       1
Paper    1      0      -1
Scissors -1      1       0
```

## Running Your Agent
Use the provided test scripts to run your agent against other agents locally:

```bash
python test_fictitious_play.py
python test_exponential.py
```

## Submission
When you're ready to submit, make sure your agent name is set correctly in the test files and that your implementation is complete. 