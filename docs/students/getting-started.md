# Getting Started for Students

Welcome to the AGT lab system! This guide will help you get up and running with creating and running your own game theory agents.

## What You'll Be Doing

As a student, your main tasks are:
1. **Create intelligent agents** that can play different games
2. **Test your agents** locally before submitting
3. **Connect to the server** to compete against other students
4. **Analyze results** to improve your strategies

## Prerequisites

Before you start, make sure you have:
- Python 3.8+ installed
- Basic Python programming knowledge
- Understanding of the [lab structure overview](../overview/lab-structure-guide.md)

## Quick Setup

### 1. Get the Code

```bash
# Clone the repository
git clone <repository-url>
cd agt_server_new

# Install dependencies
pip install -r requirements.txt
```

### 2. Explore the Stencils

Each lab has a stencil directory with starter code:

```
stencils/
├── lab01_stencil/
│   ├── example_solution.py
│   └── competition_agent.py
├── lab02_stencil/
│   ├── bos_finite_state_stencil.py
│   └── bosii_competition_stencil.py
├── lab03_stencil/
│   ├── chicken_q_learning_stencil.py
│   └── collusion_environment_stencil.py
└── ...
```

### 3. Start with Lab 01

Lab 01 (Rock Paper Scissors) is the best place to start:

```bash
cd stencils/lab01_stencil
python example_solution.py
```

This will run a simple example agent against a random opponent.

## Your First Agent

Let's create a simple agent for Lab 01:

```python
from core.agents.common.base_agent import BaseAgent
import random

class MyFirstAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_history = []
    
    def get_action(self, observation):
        # Simple strategy: play Rock most of the time
        if random.random() < 0.7:
            return 0  # Rock
        else:
            return random.choice([1, 2])  # Paper or Scissors
    
    def update(self, reward, info):
        super().update(reward, info)
        # Store opponent's action if available
        if 'opponent_action' in info:
            self.opponent_history.append(info['opponent_action'])
    
    def reset(self):
        super().reset()
        self.opponent_history = []
```

### Testing Your Agent

Test your agent locally before submitting:

```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent

# Create your agent
my_agent = MyFirstAgent("MyAgent")
opponent = RandomAgent("Random")

# Run a test game
engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My agent score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

## Connecting to the Server

### 1. Start the Server

In one terminal:

```bash
python server/server.py
```

### 2. Connect Your Agent

In another terminal:

```bash
cd stencils/lab01_stencil
python example_solution.py
```

Your agent will connect to the server and start competing!

## Understanding the Interface

### The Three Key Methods

Every agent you create must implement these three methods:

#### 1. `get_action(observation)`

This is where your strategy lives:

```python
def get_action(self, observation):
    # observation contains game state information
    # Return your chosen action
    return my_action
```

**What you get:**
- `observation`: Current game state (varies by lab)
- **Return:** Your chosen action

**Examples:**
```python
# Lab 01: Matrix games
return 0  # Rock
return 1  # Paper  
return 2  # Scissors

# Lab 04: Spatial games
return 2  # Choose location 2

# Lab 06: Auctions
return [5, 8]  # Bid 5 on item 1, 8 on item 2
```

#### 2. `update(reward, info)`

Learn from your experience:

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Store this experience
    self.my_history.append(self.get_last_action())
    
    # Learn from opponent's action (if available)
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
    
    # Update your strategy
    self.update_strategy()
```

**What you get:**
- `reward`: Points earned from your last action
- `info`: Additional information (opponent's action, etc.)

#### 3. `reset()`

Start fresh for a new game:

```python
def reset(self):
    super().reset()
    # Clear any game-specific state
    self.opponent_history = []
    self.my_history = []
    self.round_count = 0
```

## Lab-Specific Strategies

### Lab 01: Matrix Games

**Goal:** Learn basic game theory concepts

**Strategy Ideas:**
- **Random**: `return random.choice([0, 1, 2])`
- **Fictitious Play**: Track opponent's frequencies, play best response
- **Nash Equilibrium**: Play mixed strategy that's optimal

### Lab 02: Finite State Machines

**Goal:** Learn state-based strategies

**Strategy Ideas:**
- **Tit-for-Tat**: Copy opponent's last action
- **State Machine**: Different behavior in different states
- **Coordination**: Try to coordinate with opponent

### Lab 03: Q-Learning

**Goal:** Learn reinforcement learning

**Strategy Ideas:**
- **Epsilon-Greedy**: Explore sometimes, exploit best action
- **Q-Table**: Store value of each state-action pair
- **Learning Rate**: Balance new vs old information

### Lab 04: Spatial Games

**Goal:** Learn spatial competition

**Strategy Ideas:**
- **Location Analysis**: Choose locations with most customers
- **Opponent Avoidance**: Stay away from crowded areas
- **Dynamic Positioning**: Move based on opponent locations

### Lab 06: Auctions

**Goal:** Learn auction theory

**Strategy Ideas:**
- **Truthful Bidding**: Bid your true valuation
- **Strategic Bidding**: Bid below your valuation
- **Marginal Value**: Consider opportunity cost

## Debugging Tips

### 1. Print Debugging

```python
def get_action(self, observation):
    print(f"Observation: {observation}")
    print(f"Opponent history: {self.opponent_history}")
    
    action = self.choose_action(observation)
    print(f"Chosen action: {action}")
    
    return action
```

### 2. Track Performance

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Track performance every 10 rounds
    if len(self.reward_history) % 10 == 0:
        recent_rewards = self.reward_history[-10:]
        avg_reward = sum(recent_rewards) / len(recent_rewards)
        print(f"Average reward over last 10 rounds: {avg_reward}")
```

### 3. Test Against Different Opponents

```python
# Test against random agent
random_opponent = RandomAgent("Random")
engine = Engine(RPSGame(), [my_agent, random_opponent], rounds=100)
results = engine.run()

# Test against stubborn agent
stubborn_opponent = StubbornAgent("Stubborn")
engine = Engine(RPSGame(), [my_agent, stubborn_opponent], rounds=100)
results = engine.run()
```

## Common Patterns

### Tracking Opponent Behavior

```python
class OpponentTracker(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_counts = {0: 0, 1: 0, 2: 0}  # Count each action
    
    def update(self, reward, info):
        super().update(reward, info)
        if 'opponent_action' in info:
            self.opponent_counts[info['opponent_action']] += 1
    
    def get_opponent_most_likely_action(self):
        return max(self.opponent_counts, key=self.opponent_counts.get)
```

### Learning from Experience

```python
class LearningAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.action_values = {0: 0.0, 1: 0.0, 2: 0.0}
        self.learning_rate = 0.1
    
    def update(self, reward, info):
        super().update(reward, info)
        
        # Update value of last action
        last_action = self.get_last_action()
        if last_action is not None:
            self.action_values[last_action] += self.learning_rate * reward
    
    def get_best_action(self):
        return max(self.action_values, key=self.action_values.get)
```

### Exploration vs Exploitation

```python
class EpsilonGreedyAgent(BaseAgent):
    def __init__(self, name, epsilon=0.1):
        super().__init__(name)
        self.epsilon = epsilon
    
    def get_action(self, observation):
        if random.random() < self.epsilon:  # Explore
            return random.choice([0, 1, 2])
        else:  # Exploit
            return self.get_best_action()
```

## Next Steps

1. **Start with Lab 01** - Implement a simple agent
2. **Test locally** - Make sure your agent works before submitting
3. **Connect to server** - Compete against other students
4. **Analyze results** - Learn from your performance
5. **Iterate and improve** - Make your agent better

Remember: The goal is to learn game theory concepts through hands-on experience. Don't worry about being perfect - focus on understanding the concepts and having fun!

For more detailed information about specific labs, see the [Labs section](../labs/). 