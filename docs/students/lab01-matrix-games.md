# Lab 01: Matrix Games

This lab introduces basic game theory through simultaneous-move matrix games.

## Game Overview

**Type:** Simultaneous-move games with payoff matrices
**Players:** 2 players
**Rounds:** 1000 rounds per game
**Stages:** Single stage that repeats

## Games

### Rock Paper Scissors (RPS)
- **Actions:** Rock (0), Paper (1), Scissors (2)
- **Payoff Matrix:** Zero-sum game
- **Key Concept:** No pure Nash equilibrium

### Chicken Game
- **Actions:** Swerve (0), Straight (1)
- **Payoff Matrix:** Conflict game
- **Key Concept:** Asymmetric equilibria

### Prisoner's Dilemma (PD)
- **Actions:** Cooperate (0), Defect (1)
- **Payoff Matrix:** Classic dilemma game
- **Key Concept:** Dominant strategy equilibrium

## State Space

### Observations
```python
observation = {}  # Empty - you know the game structure
```

### Actions
```python
# RPS
action = 0  # Rock
action = 1  # Paper
action = 2  # Scissors

# Chicken/PD
action = 0  # Swerve / Cooperate
action = 1  # Straight / Defect
```

### Rewards
Immediate payoffs from the payoff matrix:
```python
# RPS example
if my_action == 0 and opponent_action == 1:  # Rock vs Paper
    reward = -1  # I lose
elif my_action == 1 and opponent_action == 0:  # Paper vs Rock
    reward = 1   # I win
```

## Game Structure

### Stage Type
- **Single stage** that repeats for all rounds
- **Simultaneous moves** - both players act at same time
- **Immediate feedback** - rewards given after each round

### Learning Opportunities
- **Opponent modeling** - track opponent's action frequencies
- **Best response** - play optimally against opponent's strategy
- **Nash equilibrium** - find unexploitable strategies

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.game.ChickenGame import ChickenGame
from core.game.PDGame import PDGame
from core.agents.lab01.random_agent import RandomAgent
from core.agents.lab01.random_chicken_agent import RandomChickenAgent
from core.agents.lab01.random_pd_agent import RandomPDAgent

# Test RPS
my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(RPSGame(), [my_agent, opponent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")

# Test Chicken
chicken_opponent = RandomChickenAgent("RandomChicken")
engine = Engine(ChickenGame(), [my_agent, chicken_opponent], rounds=1000)
results = engine.run()

# Test Prisoner's Dilemma
pd_opponent = RandomPDAgent("RandomPD")
engine = Engine(PDGame(), [my_agent, pd_opponent], rounds=1000)
results = engine.run()
```

### Performance Analysis
```python
def analyze_performance(self):
    if len(self.reward_history) > 0:
        avg_reward = sum(self.reward_history) / len(self.reward_history)
        print(f"Average reward: {avg_reward}")
        
        if avg_reward > 0:
            print("Performing above random!")
        elif avg_reward < 0:
            print("Performing below random.")
        else:
            print("Performing at random level.")
```

## Next Steps

1. **Implement a basic agent** using the common patterns
2. **Test against different opponents** to understand performance
3. **Analyze results** to see what works
4. **Compete against other students**

Focus on understanding the game mechanics and learning from experience! 