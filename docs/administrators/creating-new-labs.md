# Creating New Labs

This guide provides a step-by-step process for creating new labs in the AGT system. We'll use a simple "Coin Flip" game as an example to demonstrate the complete lab creation process.

## Lab Creation Overview

Creating a new lab involves several components that work together:

1. **Game Implementation** - Defines the game mechanics and rules
2. **Agent Examples** - Provides reference implementations for students
3. **Server Integration** - Enables the lab on the server
4. **Student Stencil** - Gives students a starting point
5. **Documentation** - Explains the lab to students
6. **Testing** - Validates everything works correctly

## Step 1: Design Your Game

### Game Concept
Start by clearly defining your game:
- **Objective**: What are players trying to achieve?
- **Actions**: What can players do on their turn?
- **State**: What information do players have?
- **Rewards**: How do players score points?

### Example: Coin Flip Game
Let's create a simple 2-player game where:
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
    """
    Coin Flip coordination game.
    
    Actions:
    0 = Heads
    1 = Tails
    
    Payoff matrix (both players get same reward):
    H\T  H  T
    H    1  0
    T    0  1
    
    Players coordinate to choose the same action.
    """
    
    def __init__(self, rounds: int = 100):
        # Create the payoff tensor for Coin Flip
        # Shape: (hidden_states=1, actions=2, actions=2, players=2)
        payoff_tensor = np.array([
            # Heads vs Heads, Tails
            [[1.0, 1.0], [0.0, 0.0]],
            # Tails vs Heads, Tails
            [[0.0, 0.0], [1.0, 1.0]]
        ])
        
        # Reshape to (1, 2, 2, 2) for the tensor format
        payoff_tensor = payoff_tensor.reshape(1, 2, 2, 2)
        
        action_labels = ["Heads", "Tails"]
        
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels
```

### 2.2 Understanding the MatrixGame Pattern

The `MatrixGame` class provides:
- **Automatic stage management** - Creates new stages for each round
- **Reward accumulation** - Tracks cumulative scores
- **Standard interface** - Implements BaseGame methods

**Key Methods to Override:**
- `__init__()` - Set up payoff matrix and game parameters
- `action_labels` - Human-readable action names (optional)

**Methods Inherited from MatrixGame:**
- `reset()` - Initializes new game
- `players_to_move()` - Returns [0, 1] for 2-player games
- `step()` - Processes actions and returns results

### 2.3 Alternative: Custom Game Implementation

For more complex games, implement `BaseGame` directly:

```python
from core.game.base_game import BaseGame, ObsDict, ActionDict, RewardDict, InfoDict
from typing import List, Tuple

class CustomGame(BaseGame):
    def __init__(self, rounds: int = 100):
        self.rounds = rounds
        self.current_round = 0
        self.metadata = {"num_players": 2}
    
    def reset(self, seed: int | None = None) -> ObsDict:
        """Initialize a fresh game."""
        if seed is not None:
            np.random.seed(seed)
        
        self.current_round = 0
        return {0: {}, 1: {}}  # Initial observations
    
    def players_to_move(self) -> List[int]:
        """Return players who need to act."""
        return [0, 1]  # Both players act simultaneously
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Process actions and return results."""
        action1, action2 = actions[0], actions[1]
        
        # Calculate rewards based on game logic
        if action1 == action2:
            reward1 = reward2 = 1.0  # Both get 1 if they coordinate
        else:
            reward1 = reward2 = 0.0  # Both get 0 if they don't coordinate
        
        self.current_round += 1
        done = self.current_round >= self.rounds
        
        return (
            {0: {}, 1: {}},  # Observations (empty for simple games)
            {0: reward1, 1: reward2},  # Rewards
            done,  # Game finished?
            {0: {"opponent_action": action2}, 1: {"opponent_action": action1}}  # Info
        )
```

## Step 3: Create Agent Examples

### 3.1 Random Agent

Create `core/agents/labXX/random_coinflip_agent.py`:

```python
from core.agents.common.base_agent import BaseAgent
import random

class RandomCoinFlipAgent(BaseAgent):
    """Random agent for Coin Flip game."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = [0, 1]  # Heads, Tails
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Choose random action."""
        return random.choice(self.actions)
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Update agent with reward and info."""
        super().update(reward, info)
        # Random agent doesn't learn, but you could add learning here
    
    def reset(self):
        """Reset agent for new game."""
        super().reset()
        # Clear any game-specific state
```

### 3.2 Example Solution

Create `core/agents/labXX/example_coinflip_solution.py`:

```python
from core.agents.common.base_agent import BaseAgent

class ExampleCoinFlipSolution(BaseAgent):
    """Example solution for Coin Flip game."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.opponent_history = []
        self.my_history = []
        self.coordination_count = 0
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Implement coordination strategy."""
        if len(self.opponent_history) == 0:
            # First move: start with Heads
            return 0
        elif len(self.opponent_history) < 10:
            # Early game: try to coordinate on most common opponent action
            opponent_freq = self.analyze_opponent()
            return self.best_coordination_action(opponent_freq)
        else:
            # Late game: stick with what works
            return self.find_best_coordination()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Learn from experience."""
        super().update(reward, info)
        
        # Store opponent's action
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
        
        # Track coordination success
        if reward > 0:
            self.coordination_count += 1
    
    def reset(self):
        """Reset for new game."""
        super().reset()
        self.opponent_history = []
        self.my_history = []
        self.coordination_count = 0
    
    def analyze_opponent(self):
        """Analyze opponent's action frequencies."""
        if not self.opponent_history:
            return {0: 0.5, 1: 0.5}  # Default to 50/50
        
        freq = {}
        for action in [0, 1]:
            freq[action] = self.opponent_history.count(action) / len(self.opponent_history)
        return freq
    
    def best_coordination_action(self, opponent_freq):
        """Choose action that maximizes coordination probability."""
        if opponent_freq[0] > opponent_freq[1]:
            return 0  # Opponent prefers Heads
        else:
            return 1  # Opponent prefers Tails
    
    def find_best_coordination(self):
        """Find the action that led to most coordination."""
        if len(self.my_history) == 0:
            return 0
        
        # Count coordination success for each action
        coordination_by_action = {0: 0, 1: 0}
        for i, my_action in enumerate(self.my_history):
            if i < len(self.opponent_history):
                if my_action == self.opponent_history[i]:
                    coordination_by_action[my_action] += 1
        
        # Return action with most coordination
        if coordination_by_action[0] >= coordination_by_action[1]:
            return 0
        else:
            return 1
```

## Step 4: Update Server Configuration

### 4.1 Add Game to Server

Add to `server/server.py` in the `game_configs` dictionary:

```python
# Add this to the game_configs dictionary in AGTServer.__init__
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
    """Your agent implementation for the Coin Flip game."""
    
    def __init__(self, name: str):
        super().__init__(name)
        # Initialize your agent's state here
        self.opponent_history = []
        self.my_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """
        Implement your strategy here.
        
        Args:
            observation: Current game state (empty for this game)
            
        Returns:
            Your chosen action: 0 for Heads, 1 for Tails
        """
        # TODO: Implement your coordination strategy
        # You can access self.opponent_history to see what your opponent has done
        # You can access self.my_history to see what you've done
        
        # Example: always choose Heads
        return 0
    
    def update(self, reward: float, info: Dict[str, Any]):
        """
        Learn from the result of your action.
        
        Args:
            reward: Points earned (1 if coordinated, 0 if not)
            info: Additional information (opponent's action, etc.)
        """
        super().update(reward, info)
        
        # Store opponent's action if available
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
        
        # Store your action
        if hasattr(self, 'last_action'):
            self.my_history.append(self.last_action)
    
    def reset(self):
        """Reset for a new game."""
        super().reset()
        self.opponent_history = []
        self.my_history = []
```

### 5.3 Example Solution

Create `stencils/labXX_stencil/example_solution.py`:

```python
import asyncio
import json
import socket
from my_agent import MyAgent

async def main():
    """Connect agent to server."""
    # Create your agent
    agent = MyAgent("MyCoinFlipAgent")
    
    # Server connection details
    host = "localhost"
    port = 8080
    
    try:
        # Connect to server
        reader, writer = await asyncio.open_connection(host, port)
        
        # Send device ID
        device_id = "coinflip_student_001"
        await send_message(writer, {"device_id": device_id})
        
        # Join game
        await send_message(writer, {
            "message": "join_game",
            "game_type": "coinflip",
            "player_name": agent.name
        })
        
        # Game loop
        while True:
            message = await receive_message(reader)
            if message is None:
                break
            
            if message.get("message") == "get_action":
                # Get action from agent
                observation = message.get("observation", {})
                action = agent.get_action(observation)
                
                # Send action
                await send_message(writer, {
                    "message": "action",
                    "action": action
                })
            
            elif message.get("message") == "update":
                # Update agent with result
                reward = message.get("reward", 0.0)
                info = message.get("info", {})
                agent.update(reward, info)
                
                # Ready for next round
                await send_message(writer, {"message": "ready_next_round"})
            
            elif message.get("message") == "game_complete":
                print(f"Game complete! Final score: {message.get('final_score', 0)}")
                break
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def send_message(writer, message):
    """Send message to server."""
    data = json.dumps(message).encode()
    writer.write(data + b'\n')
    await writer.drain()

async def receive_message(reader):
    """Receive message from server."""
    try:
        data = await reader.readuntil(b'\n')
        return json.loads(data.decode().strip())
    except Exception:
        return None

if __name__ == "__main__":
    asyncio.run(main())
```

### 5.4 Test Script

Create `stencils/labXX_stencil/test_agent.py`:

```python
from core.engine import Engine
from core.game.CoinFlipGame import CoinFlipGame
from core.agents.labXX.random_coinflip_agent import RandomCoinFlipAgent
from my_agent import MyAgent

def test_agent():
    """Test your agent against a random opponent."""
    # Create agents
    my_agent = MyAgent("MyAgent")
    random_agent = RandomCoinFlipAgent("Random")
    
    # Create game
    game = CoinFlipGame(rounds=100)
    
    # Run test
    engine = Engine(game, [my_agent, random_agent], rounds=100)
    results = engine.run()
    
    print(f"Test Results:")
    print(f"My score: {results[0]}")
    print(f"Random opponent score: {results[1]}")
    
    # Analyze performance
    if results[0] > results[1]:
        print("✅ Your agent is performing well!")
    elif results[0] == results[1]:
        print("🤔 Your agent is performing at random level.")
    else:
        print("❌ Your agent needs improvement.")
    
    # Show coordination rate
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

### Coordination Analysis
```python
def analyze_coordination(self):
    if len(self.reward_history) > 0:
        coordination_rate = sum(self.reward_history) / len(self.reward_history)
        print(f"Coordination rate: {coordination_rate:.1%}")
        
        if coordination_rate > 0.5:
            print("Good coordination!")
        else:
            print("Need to improve coordination.")
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
    """Test Coin Flip game implementation."""
    
    def test_game_creation(self):
        """Test game can be created."""
        game = CoinFlipGame()
        self.assertIsNotNone(game)
    
    def test_game_execution(self):
        """Test game can be executed."""
        game = CoinFlipGame(rounds=10)
        agent1 = RandomCoinFlipAgent("Agent1")
        agent2 = RandomCoinFlipAgent("Agent2")
        
        engine = Engine(game, [agent1, agent2], rounds=10)
        results = engine.run()
        
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], (int, float))
        self.assertIsInstance(results[1], (int, float))
    
    def test_coordination_rewards(self):
        """Test that coordination gives positive rewards."""
        game = CoinFlipGame(rounds=100)
        agent1 = RandomCoinFlipAgent("Agent1")
        agent2 = RandomCoinFlipAgent("Agent2")
        
        engine = Engine(game, [agent1, agent2], rounds=100)
        results = engine.run()
        
        # Both agents should have similar scores (coordination game)
        self.assertAlmostEqual(results[0], results[1], delta=20)
    
    def test_agent_interface(self):
        """Test agent interface compliance."""
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