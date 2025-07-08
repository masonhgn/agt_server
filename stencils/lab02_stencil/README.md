# CS1440/2440 Lab 2: Finite State Machines and Games of Incomplete Information

## Introduction

In Lab 2, you will work with the **Battle of the Sexes (BOS)** game in both complete and incomplete information scenarios. You'll design agent strategies using **finite state machines (FSMs)** and test these strategies against various opponents.

## Game Description

### Battle of the Sexes (Complete Information)
- **Actions**: 0 = Compromise, 1 = Stubborn
- **Payoff Matrix**:
  ```
  C\S  C  S
  C    0  3
  S    7  0
  ```
- **Nash Equilibria**: (Compromise, Stubborn) and (Stubborn, Compromise)

### Battle of the Sexes with Incomplete Information (BOSII)
- **Row Player**: Has complete information
- **Column Player**: Has a mood that affects payoffs
  - **GOOD_MOOD** (2/3 probability): Standard BOS payoffs
  - **BAD_MOOD** (1/3 probability): Modified payoffs
- **Row Player**: Doesn't know column player's mood

## Setup and Installation

**IMPORTANT: Please install/use a version of `Python >= 3.10`**

### Step 1: Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install numpy
```

## Agent Interface

Your agents must inherit from `BaseAgent` and implement:
- `act(obs)`: Return an action given the current observation
- `update(reward)`: Update internal state with the reward received

### Available Methods
- `self.get_action_history()`: Your action history
- `self.get_reward_history()`: Your reward history
- `self.get_last_action()`: Your last action
- `self.get_last_reward()`: Your last reward
- `self.reset()`: Reset agent state

### BOSII-Specific Methods
- `self.is_row_player()`: True if you're the row player
- `self.get_mood()`: Your current mood (column player only)
- `self.get_last_mood()`: Your mood last round (column player only)
- `self.get_mood_history()`: Your mood history (column player only)

## Finite State Machines

FSMs are a powerful way to implement strategies:
- **States**: Represent different phases of your strategy
- **Transitions**: How you move between states based on game history
- **Actions**: What action to take in each state

### Example FSM Strategy
```
State 0: Start with Stubborn
State 1: If opponent was Stubborn, be Compromise for 2 rounds
State 2: Return to Stubborn
State 3: If opponent was Stubborn again, be Compromise for 2 rounds
State 4: Stay Compromise (punishment phase)
```

## Running Your Agent

Use the provided test scripts:
```bash
python test_bos_finite_state.py
python test_bosii_competition.py
```

## Submission

When ready to submit:
1. Complete the TODO sections in the stencil files
2. Test your agents thoroughly
3. Set your agent name in the test files 