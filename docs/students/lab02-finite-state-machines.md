# Lab 02: Finite State Machines

This lab introduces state-based strategies through finite state machine games.

## Game Overview

**Type:** State-based coordination games
**Players:** 2 players
**Rounds:** 1000 rounds per game
**Stages:** Multiple states with different rules

## Games

### Battle of the Sexes (BOS) Finite State
- **States:** Multiple states with different coordination challenges
- **Actions:** Action A (0), Action B (1)
- **Key Concept:** State-dependent coordination

### Battle of the Sexes II (BOSII)
- **States:** Extended state space with more complex transitions
- **Actions:** Action A (0), Action B (1)
- **Key Concept:** Multi-state coordination

## State Space

### Observations
```python
observation = {
    "current_state": 0,  # Current state of the game
    "state_history": [0, 1, 0, 2],  # Recent state transitions
    "round_count": 45  # Current round number
}
```

### Actions
```python
action = 0  # Action A
action = 1  # Action B
```

### Rewards
State-dependent payoffs:
```python
# Example: different payoffs in different states
if current_state == 0:
    # Coordination game in state 0
    if my_action == opponent_action:
        reward = 3  # Both choose same action
    else:
        reward = 0  # Different actions
elif current_state == 1:
    # Different game in state 1
    reward = calculate_state_1_payoff(my_action, opponent_action)
```

## Game Structure

### Stage Type
- **Multiple states** with different rules
- **State transitions** based on actions
- **State-dependent payoffs** - rewards vary by state

### Learning Opportunities
- **State recognition** - understand current game state
- **State transitions** - predict how actions change states
- **State-specific strategies** - adapt to different game rules

## Key Concepts

### State Machines
Games with multiple states and transition rules.

### State-Dependent Strategies
Different optimal actions in different states.

### Coordination
Players must coordinate their actions for optimal payoffs.

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(BOSGame(), [my_agent, opponent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### State Analysis
```python
def analyze_states(self):
    if 'current_state' in self.last_observation:
        current_state = self.last_observation['current_state']
        print(f"Current state: {current_state}")
        
        # Track performance by state
        if current_state not in self.state_performance:
            self.state_performance[current_state] = []
        self.state_performance[current_state].append(self.get_last_reward())
```

## Expected Outcomes

### Against Random Opponent
- **Random agent:** ~0 average reward
- **State-aware agent:** >0 average reward (should win)
- **Coordinating agent:** >0 average reward (should coordinate)

### Against Coordinating Opponent
- **Random agent:** ~0 average reward
- **State-aware agent:** >0 average reward (should coordinate)
- **Coordinating agent:** >0 average reward (should coordinate)

## Next Steps

1. **Implement a state-aware agent** using the common patterns
2. **Track state transitions** to understand the game structure
3. **Test coordination strategies** against different opponents
4. **Compete against other students**

Focus on understanding state transitions and coordination mechanisms! 