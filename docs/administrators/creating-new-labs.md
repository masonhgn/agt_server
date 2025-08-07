# Creating New Labs

This guide provides a complete process for creating new labs in the AGT system. We'll use a simple "Coin Flip" game as an example.

## Lab Creation Overview

A new lab requires these components:
1. **Game Implementation** - Defines game mechanics and rules
2. **Agent Examples** - Reference implementations for students
3. **Server Integration** - Enables the lab on the server
4. **Student Stencil** - Starting point for students
5. **Documentation** - Student and administrator guides
6. **Testing** - Validates everything works correctly

## Step 1: Design Your Game

### Game Concept
Define your game clearly:
- **Objective**: What are players trying to achieve?
- **Actions**: What can players do on their turn?
- **State**: What information do players have?
- **Rewards**: How do players score points?

### Example: Coin Flip Game
A simple 2-player coordination game:
- Players simultaneously choose "Heads" or "Tails"
- If both choose the same, they both get 1 point
- If they choose differently, they both get 0 points
- Game runs for 100 rounds

## Step 2: Implement the Game

### 2.1 Create Game Class

Create `core/game/CoinFlipGame.py`:

```python
import numpy as np
from core.game.MatrixGame import MatrixGame

class CoinFlipGame(MatrixGame):
    """Coin Flip coordination game."""
    
    def __init__(self, rounds: int = 100):
        # Payoff matrix: both players get same reward
        payoff_tensor = np.array([
            [[1.0, 1.0], [0.0, 0.0]],  # Heads vs Heads, Tails
            [[0.0, 0.0], [1.0, 1.0]]   # Tails vs Heads, Tails
        ]).reshape(1, 2, 2, 2)
        
        action_labels = ["Heads", "Tails"]
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels
```

### 2.2 Understanding MatrixGame Pattern

The `MatrixGame` class provides:
- **Automatic stage management** - Creates new stages for each round
- **Reward accumulation** - Tracks cumulative scores
- **Standard interface** - Implements BaseGame methods

**Key Methods to Override:**
- `__init__()` - Set up payoff matrix and game parameters
- `action_labels` - Human-readable action names (optional)

### 2.3 Alternative: Custom Game Implementation

For complex games, implement `BaseGame` directly:

```python
from core.game.base_game import BaseGame, ObsDict, ActionDict, RewardDict, InfoDict

class CustomGame(BaseGame):
    def __init__(self, rounds: int = 100):
        self.rounds = rounds
        self.current_round = 0
        self.metadata = {"num_players": 2}
    
    def reset(self, seed: int | None = None) -> ObsDict:
        if seed is not None:
            np.random.seed(seed)
        self.current_round = 0
        return {0: {}, 1: {}}
    
    def players_to_move(self) -> List[int]:
        return [0, 1]
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        action1, action2 = actions[0], actions[1]
        
        # Calculate rewards based on game logic
        if action1 == action2:
            reward1 = reward2 = 1.0  # Both get 1 if they coordinate
        else:
            reward1 = reward2 = 0.0  # Both get 0 if they don't coordinate
        
        self.current_round += 1
        done = self.current_round >= self.rounds
        
        return (
            {0: {}, 1: {}},
            {0: reward1, 1: reward2},
            done,
            {0: {"opponent_action": action2}, 1: {"opponent_action": action1}}
        )
```

## Step 3: Create Agent Examples

### 3.1 Random Agent

Create `core/agents/labXX/random_coinflip_agent.py`:

```python
from core.agents.common.base_agent import BaseAgent
import random

class RandomCoinFlipAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = [0, 1]  # Heads, Tails
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        return random.choice(self.actions)
    
    def update(self, reward: float, info: Dict[str, Any]):
        super().update(reward, info)
    
    def reset(self):
        super().reset()
```

### 3.2 Example Solution

Create `core/agents/labXX/example_coinflip_solution.py`:

```python
from core.agents.common.base_agent import BaseAgent

class ExampleCoinFlipSolution(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.opponent_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        if len(self.opponent_history) == 0:
            return 0  # Start with Heads
        else:
            # Try to coordinate on most common opponent action
            opponent_freq = self.analyze_opponent()
            return 0 if opponent_freq[0] > opponent_freq[1] else 1
    
    def update(self, reward: float, info: Dict[str, Any]):
        super().update(reward, info)
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
    
    def reset(self):
        super().reset()
        self.opponent_history = []
    
    def analyze_opponent(self):
        if not self.opponent_history:
            return {0: 0.5, 1: 0.5}
        freq = {}
        for action in [0, 1]:
            freq[action] = self.opponent_history.count(action) / len(self.opponent_history)
        return freq
```

## Step 4: Update Server Configuration

### 4.1 Add Game to Server

Add to `server/server.py` in the `game_configs` dictionary:

```python
"coinflip": {
    "name": "Coin Flip",
    "game_class": CoinFlipGame,
    "num_players": 2,
    "num_rounds": 100,
    "description": "Simple coordination game"
},
```

### 4.2 Import the Game

Add the import at the top of `server/server.py`:

```python
from core.game.CoinFlipGame import CoinFlipGame
```

### 4.3 Create Configuration File

Create `server/configs/labXX_coinflip.json`:

```json
{
    "game_type": "coinflip",
    "num_players": 2,
    "rounds_per_game": 100,
    "timeout": 300,
    "description": "Coin Flip Coordination Lab"
}
```

## Step 5: Create Student Stencil

### 5.1 Stencil Structure

Create directory `stencils/labXX_stencil/`:

```
stencils/labXX_stencil/
├── README.md
├── requirements.txt
├── my_agent.py
├── example_solution.py
└── test_agent.py
```

### 5.2 Student Agent Template

Create `stencils/labXX_stencil/my_agent.py`:

```python
from core.agents.common.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name)
        self.opponent_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        # TODO: Implement your coordination strategy
        # You can access self.opponent_history to see opponent's actions
        return 0  # Example: always choose Heads
    
    def update(self, reward: float, info: Dict[str, Any]):
        super().update(reward, info)
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
    
    def reset(self):
        super().reset()
        self.opponent_history = []
```

### 5.3 Example Solution

Create `stencils/labXX_stencil/example_solution.py`:

```python
#!/usr/bin/env python3
"""
Example solution for Lab XX - Coin Flip
This shows what a completed implementation looks like.
"""

import sys
import os
import numpy as np

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.CoinFlipGame import CoinFlipGame
from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent


class ExampleCoordinationAgent(BaseAgent):
    """Example implementation of coordination strategy for Coin Flip."""
    
    def __init__(self, name: str = "ExampleCoord"):
        super().__init__(name)
        self.HEADS, self.TAILS = 0, 1
        self.actions = [self.HEADS, self.TAILS]
        self.opponent_history = []
        self.coordination_count = 0
    
    def get_action(self, obs):
        """Return action based on opponent analysis."""
        if len(self.opponent_history) == 0:
            return self.HEADS  # Start with Heads
        else:
            # Analyze opponent's behavior
            opponent_freq = self.analyze_opponent()
            return self.best_coordination_action(opponent_freq)
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Store the reward and update opponent action counts."""
        super().update(reward, info)
        
        # Store opponent's action if available
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
        
        # Track coordination success
        if reward > 0:
            self.coordination_count += 1
    
    def analyze_opponent(self):
        """Analyze opponent's action frequencies."""
        if not self.opponent_history:
            return {0: 0.5, 1: 0.5}  # Default to 50/50
        
        freq = {}
        for action in self.actions:
            freq[action] = self.opponent_history.count(action) / len(self.opponent_history)
        return freq
    
    def best_coordination_action(self, opponent_freq):
        """Choose action that maximizes coordination probability."""
        if opponent_freq[self.HEADS] > opponent_freq[self.TAILS]:
            return self.HEADS  # Opponent prefers Heads
        else:
            return self.TAILS  # Opponent prefers Tails
    
    def reset(self):
        """Reset for new game."""
        super().reset()
        self.opponent_history = []
        self.coordination_count = 0


if __name__ == "__main__":
    print("Example Solution for Lab XX")
    print("=" * 40)
    
    # Test coordination strategy vs Random
    print("\nTesting Coordination vs Random:")
    game = CoinFlipGame(rounds=100)
    agents = [
        ExampleCoordinationAgent("ExampleCoord"),
        RandomCoinFlipAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print detailed statistics
    coord_agent = agents[0]
    action_counts = [0, 0]  # Heads, Tails
    for action in coord_agent.action_history:
        action_counts[action] += 1
    
    print(f"\n{coord_agent.name} statistics:")
    print(f"Heads: {action_counts[0]}, Tails: {action_counts[1]}")
    print(f"Total reward: {sum(coord_agent.reward_history)}")
    print(f"Average reward: {sum(coord_agent.reward_history) / len(coord_agent.reward_history):.3f}")
    print(f"Coordination rate: {coord_agent.coordination_count / len(coord_agent.reward_history):.1%}")
    
    print("\nExample solution completed!")
    print("Use this as reference for implementing your own agents.")
```

### 5.4 Test Script

Create `stencils/labXX_stencil/test_agent.py`:

```python
from core.engine import Engine
from core.game.CoinFlipGame import CoinFlipGame
from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent
from my_agent import MyAgent

def test_agent():
    my_agent = MyAgent("MyAgent")
    random_agent = RandomCoinFlipAgent("Random")
    
    game = CoinFlipGame(rounds=100)
    engine = Engine(game, [my_agent, random_agent], rounds=100)
    results = engine.run()
    
    print(f"My score: {results[0]}")
    print(f"Random opponent score: {results[1]}")
    
    coordination_rate = results[0] / 100.0
    print(f"Coordination rate: {coordination_rate:.1%}")

if __name__ == "__main__":
    test_agent()
```

## Step 6: Create Documentation

### 6.1 Student Documentation

Create `docs/students/labXX-coin-flip.md`:

```markdown
# Lab XX: Coin Flip

This lab introduces coordination games through a simple coin flip scenario.

## Game Overview

**Type:** Coordination game
**Players:** 2 players
**Rounds:** 100 rounds per game
**Stages:** Single stage that repeats

## Games

### Coin Flip Game
- **Actions:** Heads (0), Tails (1)
- **State Space:** Empty observations (players know the game structure)
- **Key Concept:** Coordination and strategic thinking

## State Space

### Observations
```python
observation = {}  # Empty - you know the game structure
```

### Actions
```python
action = 0  # Heads
action = 1  # Tails
```

### Rewards
Coordination payoffs:
```python
if my_action == opponent_action:  # Both choose same
    reward = 1  # Both get 1 point
else:  # Different choices
    reward = 0  # Both get 0 points
```

## Game Structure

### Stage Type
- **Single stage** that repeats for all rounds
- **Simultaneous moves** - both players act at same time
- **Coordination challenge** - players must choose the same action

### Learning Opportunities
- **Opponent modeling** - understand what your opponent will do
- **Coordination strategies** - find ways to coordinate effectively
- **Strategic thinking** - balance between leading and following

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.CoinFlipGame import CoinFlipGame
from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent

my_agent = MyAgent("MyAgent")
opponent = RandomCoinFlipAgent("Random")

engine = Engine(CoinFlipGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

## Next Steps

1. **Implement a coordination agent** using the common patterns
2. **Test against different opponents** to understand performance
3. **Analyze results** to see what works
4. **Compete against other students**

Focus on understanding coordination and strategic thinking!
```

## Step 7: Create Tests

### 7.1 Unit Tests

Create `tests/labs/labXX/test_coinflip.py`:

```python
import unittest
from core.game.CoinFlipGame import CoinFlipGame
from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent
from core.engine import Engine

class TestCoinFlipGame(unittest.TestCase):
    def test_game_creation(self):
        game = CoinFlipGame()
        self.assertIsNotNone(game)
    
    def test_game_execution(self):
        game = CoinFlipGame(rounds=10)
        agent1 = RandomCoinFlipAgent("Agent1")
        agent2 = RandomCoinFlipAgent("Agent2")
        
        engine = Engine(game, [agent1, agent2], rounds=10)
        results = engine.run()
        
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], (int, float))
        self.assertIsInstance(results[1], (int, float))
    
    def test_coordination_rewards(self):
        game = CoinFlipGame(rounds=100)
        agent1 = RandomCoinFlipAgent("Agent1")
        agent2 = RandomCoinFlipAgent("Agent2")
        
        engine = Engine(game, [agent1, agent2], rounds=100)
        results = engine.run()
        
        # Both agents should have similar scores (coordination game)
        self.assertAlmostEqual(results[0], results[1], delta=20)
    
    def test_agent_interface(self):
        agent = RandomCoinFlipAgent("TestAgent")
        
        # Test required methods exist
        self.assertTrue(hasattr(agent, 'get_action'))
        self.assertTrue(hasattr(agent, 'update'))
        self.assertTrue(hasattr(agent, 'reset'))
        
        # Test method signatures
        action = agent.get_action({})
        self.assertIn(action, [0, 1])  # Valid actions
        
        agent.update(1.0, {})
        agent.reset()

if __name__ == '__main__':
    unittest.main()
```

## Step 8: Integration Checklist

### 8.1 Pre-Deployment Checklist

- [ ] **Game implementation** works correctly
- [ ] **Agent interface** is properly implemented
- [ ] **Server configuration** includes new game
- [ ] **Student stencil** is complete and functional
- [ ] **Documentation** is clear and accurate
- [ ] **Tests** pass and cover key functionality
- [ ] **Integration** with existing system works

### 8.2 Testing Procedures

```bash
# Test game implementation
python -c "from core.game.CoinFlipGame import CoinFlipGame; print('Game OK')"

# Test agent loading
python -c "from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent; print('Agent OK')"

# Test engine integration
python tests/labs/labXX/test_coinflip.py

# Test server integration
python server/server.py --test-game coinflip

# Test student stencil
cd stencils/labXX_stencil
python test_agent.py
```

### 8.3 Validation Steps

1. **Test locally** - Run the game with sample agents
2. **Test server** - Verify server can handle the new game
3. **Test stencil** - Ensure students can use the provided template
4. **Test documentation** - Verify all instructions are clear
5. **Test integration** - Make sure it works with existing labs

## Best Practices

### Game Design
1. **Start simple** - Begin with basic mechanics
2. **Test thoroughly** - Ensure game works correctly
3. **Document clearly** - Explain rules and objectives
4. **Consider learning** - Design for educational value

### Implementation
1. **Follow patterns** - Use existing code as templates
2. **Test incrementally** - Test each component separately
3. **Validate thoroughly** - Ensure all edge cases work
4. **Document everything** - Include clear comments and docs

### Deployment
1. **Test with small group** - Validate with limited users
2. **Monitor performance** - Watch for issues during rollout
3. **Gather feedback** - Collect student and instructor input
4. **Iterate quickly** - Fix issues promptly

## Common Pitfalls

### Game Implementation
- **Forgetting metadata** - Always set `self.metadata["num_players"]`
- **Incorrect payoff matrix** - Double-check reward calculations
- **Missing imports** - Ensure all dependencies are imported

### Agent Implementation
- **Not calling super()** - Always call parent class methods
- **Forgetting reset()** - Clear state between games
- **Incorrect action types** - Match expected action format

### Server Integration
- **Missing game config** - Add to `game_configs` dictionary
- **Wrong import path** - Use correct import statements
- **Incorrect game ID** - Use consistent naming

## Next Steps

1. **Follow this guide** step by step for your new lab
2. **Adapt the example** to your specific game mechanics
3. **Test thoroughly** before deploying to students
4. **Gather feedback** and improve the lab
5. **Document lessons learned** for future labs

Creating new labs is now straightforward and systematic! 