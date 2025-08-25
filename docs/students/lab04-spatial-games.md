# Lab 04: The Lemonade Stand Game

In this lab, you will be implement agent strategies for the Lemonade Stand Game,
a generalization of a famous game of electoral politics studied by Hotelling.

## Game Overview

**Type:** Spatial competition games
**Players:** 2 players
**Rounds:** 1000 rounds per game
**Stages:** Single stage with spatial observations

## Games

### Lemonade Stand Game
- **Actions:** Location choices (0-11 on a circle)
- **State Space:** Current locations and market dynamics
- **Key Concept:** Spatial competition and location strategy

## State Space

### Observations
```python
observation = {
    "my_location": 3,           # My current location
    "opponent_location": 7,      # Opponent's current location
    "market_demand": [0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0],
    "round_count": 45           # Current round number
}
```

### Actions
```python
action = 0   # Location 0
action = 1   # Location 1
# ... up to location 11
action = 11   # Location 11
```

### Rewards
Spatial competition payoffs:
```python
# Distance-based competition
distance = abs(my_location - opponent_location)
if distance == 0:  # Same location
    reward = market_demand[my_location] / 2  # Split market
else:
    reward = market_demand[my_location]  # Full market share
```

## Game Structure

### Stage Type
- **Single stage** that repeats for all rounds
- **Spatial observations** - location and market information
- **Competitive dynamics** - players compete for market share

### Learning Opportunities
- **Location optimization** - find best positions given market
- **Competitive positioning** - respond to opponent's location
- **Market dynamics** - understand demand patterns

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.LemonadeGame import LemonadeGame
from core.agents.lab04.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(LemonadeGame(), [my_agent, opponent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Location Analysis
```python
def analyze_locations(self):
    if hasattr(self, 'location_history'):
        print(f"Most common location: {max(set(self.location_history), key=self.location_history.count)}")
        print(f"Average distance from opponent: {self.calculate_average_distance()}")
```

## Next Steps

1. **Implement a spatial agent** using the common patterns
2. **Analyze market dynamics** to understand optimal positioning
3. **Test competitive strategies** against different opponents
4. **Compete against other students**

Focus on understanding spatial competition and location optimization! 