# Lab 03: Q-Learning

This lab introduces reinforcement learning through Q-learning in repeated games.

## Game Overview

**Type:** Reinforcement learning in repeated games
**Players:** 2 players
**Rounds:** 1000 rounds per game
**Stages:** Single stage with state-based observations

## Games

### Chicken Game with Q-Learning
- **Actions:** Swerve (0), Straight (1)
- **State Space:** Previous action combinations
- **Key Concept:** Learning optimal strategies through experience

## State Space

### Observations
```python
observation = {
    "last_actions": [0, 1],  # Previous actions from both players
    "round_count": 45         # Current round number
}
```

### Actions
```python
action = 0  # Swerve
action = 1  # Straight
```

### Rewards
Immediate payoffs from the Chicken game payoff matrix:
```python
# Chicken game payoffs
if my_action == 0 and opponent_action == 0:  # Both swerve
    reward = 0
elif my_action == 0 and opponent_action == 1:  # I swerve, they straight
    reward = -1
elif my_action == 1 and opponent_action == 0:  # I straight, they swerve
    reward = 1
else:  # Both straight
    reward = -10
```

## Game Structure

### Stage Type
- **Single stage** that repeats for all rounds
- **State-based observations** - previous actions influence current decisions
- **Learning opportunities** - agents can improve over time

### Learning Opportunities
- **Q-table updates** - learn value of state-action pairs
- **Exploration vs exploitation** - balance trying new actions with using what works
- **Convergence** - strategies may converge to optimal policies

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(ChickenGame(), [my_agent, opponent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Q-Table Analysis
```python
def analyze_q_table(self):
    if hasattr(self, 'q_table'):
        print(f"Q-table size: {len(self.q_table)}")
        for state, actions in self.q_table.items():
            print(f"State {state}: {actions}")
```

## Next Steps

1. **Implement a Q-learning agent** using the common patterns
2. **Track state transitions** to understand the learning process
3. **Test exploration strategies** against different opponents
4. **Compete against other students**

Focus on understanding Q-learning and state-based strategies! 