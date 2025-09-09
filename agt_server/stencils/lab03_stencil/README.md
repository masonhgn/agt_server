# CS1440/2440 Lab 3: Q-Learning and Collusion

## Introduction

In Lab 3, you will implement **Q-Learning** in two simulated environments. The lab emphasizes the importance of state representation in reinforcement learning and demonstrates that Q-learners can learn collusive strategies in competitive games.

## Key Concepts

### Q-Learning
Q-Learning is a reinforcement learning algorithm that learns the quality of actions, telling an agent what action to take under what circumstances.

**Q-Learning Update Rule:**
```
Q(s, a) = Q(s, a) + alpha[r + gamma max_{a'} Q(s', a') - Q(s, a)]
```

Where:
- `Q(s, a)`: Current Q-value for state s and action a
- `alpha`: Learning rate
- `r`: Reward received
- `gamma`: Discount factor
- `max_{a'} Q(s', a')`: Maximum Q-value for next state

### Chicken Game
A 2x2 matrix game where players choose to "Swerve" or "Continue":
- **Actions**: 0 = Swerve, 1 = Continue
- **Payoff Matrix**:
  ```
  S\C  S  C
  S    0  -1
  C    1  -5
  ```
- **Nash Equilibria**: (Swerve, Continue) and (Continue, Swerve)

### Collusion Environment
A pricing game where Q-learners can learn to collude by setting high prices together, even in competitive settings.

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
pip install numpy matplotlib
```

## Agent Interface

Your Q-Learning agents must inherit from `QLearningAgent` and implement:
- `determine_state()`: Define how to represent the current game state
- `act(obs)`: Return an action (handled by base class)
- `update(reward)`: Update Q-table (handled by base class)

### Available Methods
- `self.get_action_history()`: Your action history
- `self.get_reward_history()`: Your reward history
- `self.get_last_action()`: Your last action
- `self.get_last_reward()`: Your last reward
- `self.get_opponent_last_action()`: Opponent's last action (inferred)
- `self.reset()`: Reset agent state

## State Representation

The key challenge in Q-Learning is choosing a good state representation:

### Simple State Representations
1. **Last Move**: State = opponent's last action (2 states)
2. **Lookback**: State = last 2 opponent actions (4 states)
3. **History**: State = last N opponent actions (2^N states)

### Advanced State Representations
- Combine action and reward history
- Use opponent's action patterns
- Consider game phase or round number

## Running Your Agent

Use the provided test scripts:
```bash
python test_chicken_q_learning.py
python test_collusion_environment.py
```

## Submission

When ready to submit:
1. Complete the TODO sections in the stencil files
2. Test your agents thoroughly
3. Experiment with different state representations
4. Analyze the learned strategies for collusion 