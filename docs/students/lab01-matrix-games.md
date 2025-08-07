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

### Battle of the Sexes (BOS)
- **Actions:** Action A (0), Action B (1)
- **Payoff Matrix:** Coordination game
- **Key Concept:** Multiple Nash equilibria

### Chicken Game
- **Actions:** Swerve (0), Straight (1)
- **Payoff Matrix:** Conflict game
- **Key Concept:** Asymmetric equilibria

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

# BOS/Chicken
action = 0  # Action A / Swerve
action = 1  # Action B / Straight
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
from core.agents.lab01.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(RPSGame(), [my_agent, opponent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
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