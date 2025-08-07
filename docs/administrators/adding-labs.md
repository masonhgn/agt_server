# Adding Labs

This guide covers how to add new labs to the AGT system for administrators and instructors.

## Lab Structure Overview

Each lab in the AGT system consists of several components that work together to create a complete learning experience:

### Core Components
- **Game Implementation**: Defines the game mechanics and rules
- **Agent Interface**: Standard interface for student implementations
- **Server Configuration**: Enables the lab on the server
- **Documentation**: Student and instructor guides
- **Testing**: Validation and testing procedures

## Adding a New Lab

### 1. Create Game Implementation

#### Game Class Structure
```python
# core/game/NewGame.py
from core.game.base_game import BaseGame
import numpy as np

class NewGame(BaseGame):
    """New game implementation."""
    
    def __init__(self, rounds: int = 1000):
        # Define payoff matrix or game mechanics
        self.payoff_matrix = np.array([
            [[1.0, -1.0], [-1.0, 1.0]],  # Player 1 actions
            [[-1.0, 1.0], [1.0, -1.0]]   # Player 2 actions
        ])
        
        super().__init__(rounds)
    
    def reset(self, seed: int | None = None) -> ObsDict:
        """Reset game state."""
        if seed is not None:
            np.random.seed(seed)
        
        # Initialize game state
        self.current_round = 0
        self.game_history = []
        
        # Return initial observations
        return {
            0: {"game_state": "initial", "round": 0},
            1: {"game_state": "initial", "round": 0}
        }
    
    def players_to_move(self) -> List[PlayerId]:
        """Return players who need to act."""
        return [0, 1]  # Both players act simultaneously
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Process actions and return results."""
        action1, action2 = actions[0], actions[1]
        
        # Calculate rewards based on payoff matrix
        reward1 = self.payoff_matrix[action1][action2][0]
        reward2 = self.payoff_matrix[action1][action2][1]
        
        # Update game state
        self.current_round += 1
        self.game_history.append((action1, action2, reward1, reward2))
        
        # Check if game is done
        done = self.current_round >= self.rounds
        
        # Return observations, rewards, done flag, and info
        return (
            {
                0: {"game_state": "playing", "round": self.current_round},
                1: {"game_state": "playing", "round": self.current_round}
            },
            {0: reward1, 1: reward2},
            done,
            {
                0: {"opponent_action": action2, "history": self.game_history},
                1: {"opponent_action": action1, "history": self.game_history}
            }
        )
```

#### Stage Implementation (if needed)
```python
# core/stage/NewStage.py
from core.stage.BaseStage import BaseStage

class NewStage(BaseStage):
    """Stage implementation for complex games."""
    
    def __init__(self, num_players: int):
        super().__init__(num_players)
        self.current_phase = 0
        self.phase_data = {}
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Process actions for current stage."""
        # Stage-specific logic here
        pass
    
    def legal_actions(self, player: PlayerId) -> Any:
        """Return legal actions for player."""
        # Return available actions based on current state
        pass
    
    def is_done(self) -> bool:
        """Check if stage is complete."""
        return self.current_phase >= self.max_phases
```

### 2. Create Agent Examples

#### Random Agent
```python
# core/agents/labXX/random_agent.py
from core.agents.common.base_agent import BaseAgent
import random

class RandomAgent(BaseAgent):
    """Random agent for new lab."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.actions = [0, 1]  # Available actions
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Choose random action."""
        return random.choice(self.actions)
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Update agent with reward and info."""
        super().update(reward, info)
        # Add any learning logic here
    
    def reset(self):
        """Reset agent for new game."""
        super().reset()
        # Clear any game-specific state
```

#### Example Solution
```python
# core/agents/labXX/example_solution.py
from core.agents.common.base_agent import BaseAgent

class ExampleSolution(BaseAgent):
    """Example solution for new lab."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.opponent_history = []
        self.my_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Implement your strategy here."""
        # Analyze opponent's history
        if len(self.opponent_history) > 0:
            # Implement strategy based on opponent's behavior
            opponent_freq = self.analyze_opponent()
            return self.best_response(opponent_freq)
        else:
            # First move strategy
            return 0
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Learn from experience."""
        super().update(reward, info)
        
        # Store opponent's action if available
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
        
        # Store my action
        if hasattr(self, 'last_action'):
            self.my_history.append(self.last_action)
    
    def reset(self):
        """Reset for new game."""
        super().reset()
        self.opponent_history = []
        self.my_history = []
    
    def analyze_opponent(self):
        """Analyze opponent's action frequencies."""
        if not self.opponent_history:
            return {}
        
        freq = {}
        for action in set(self.opponent_history):
            freq[action] = self.opponent_history.count(action) / len(self.opponent_history)
        return freq
    
    def best_response(self, opponent_freq):
        """Choose best response to opponent's strategy."""
        # Implement best response logic
        return 0  # Placeholder
```

### 3. Update Server Configuration

#### Add Game to Server
```python
# server/server.py (add to game_configs)
"newgame": {
    "name": "New Game",
    "game_class": NewGame,
    "num_players": 2,
    "num_rounds": 100,
    "description": "New game for learning"
}
```

#### Update Configuration Files
```json
// server/configs/labXX_newgame.json
{
    "game_type": "newgame",
    "num_players": 2,
    "rounds_per_game": 100,
    "timeout": 300,
    "description": "New Game Lab"
}
```

### 4. Create Student Stencil

#### Stencil Structure
```
stencils/labXX_stencil/
├── README.md
├── requirements.txt
├── example_solution.py
├── my_agent.py
└── test_agent.py
```

#### Stencil Files
```python
# stencils/labXX_stencil/my_agent.py
from core.agents.common.base_agent import BaseAgent

class MyAgent(BaseAgent):
    """Your agent implementation."""
    
    def __init__(self, name: str):
        super().__init__(name)
        # Initialize your agent's state
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Implement your strategy here."""
        # Your strategy implementation
        pass
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Learn from experience."""
        super().update(reward, info)
        # Your learning logic
    
    def reset(self):
        """Reset for new game."""
        super().reset()
        # Clear game-specific state
```

```python
# stencils/labXX_stencil/example_solution.py
import asyncio
import json
from my_agent import MyAgent

async def main():
    """Connect agent to server."""
    # Connection logic here
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Create Documentation

#### Student Documentation
```markdown
# docs/students/labXX-new-game.md
# Lab XX: New Game

This lab introduces [game concept] through [game mechanics].

## Game Overview

**Type:** [Game type description]
**Players:** [Number] players
**Rounds:** [Number] rounds per game
**Stages:** [Stage description]

## Games

### New Game
- **Actions:** [Action description]
- **State Space:** [State description]
- **Key Concept:** [Learning objective]

## State Space

### Observations
```python
observation = {
    # Observation structure
}
```

### Actions
```python
action = 0  # Action description
action = 1  # Action description
```

### Rewards
[Reward structure description]

## Game Structure

### Stage Type
[Stage description]

### Learning Opportunities
[Learning objectives]

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.NewGame import NewGame
from core.agents.labXX.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(NewGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

## Next Steps

1. **Implement your agent** using the common patterns
2. **Test your strategy** against different opponents
3. **Compete against other students**

Focus on [learning objective]!
```

### 6. Create Tests

#### Test Implementation
```python
# tests/labs/labXX/test_new_game.py
import unittest
from core.game.NewGame import NewGame
from core.agents.labXX.random_agent import RandomAgent
from core.engine import Engine

class TestNewGame(unittest.TestCase):
    """Test new game implementation."""
    
    def test_game_creation(self):
        """Test game can be created."""
        game = NewGame()
        self.assertIsNotNone(game)
    
    def test_game_execution(self):
        """Test game can be executed."""
        game = NewGame(rounds=10)
        agent1 = RandomAgent("Agent1")
        agent2 = RandomAgent("Agent2")
        
        engine = Engine(game, [agent1, agent2], rounds=10)
        results = engine.run()
        
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], (int, float))
        self.assertIsInstance(results[1], (int, float))
    
    def test_agent_interface(self):
        """Test agent interface compliance."""
        agent = RandomAgent("TestAgent")
        
        # Test required methods exist
        self.assertTrue(hasattr(agent, 'get_action'))
        self.assertTrue(hasattr(agent, 'update'))
        self.assertTrue(hasattr(agent, 'reset'))
        
        # Test method signatures
        action = agent.get_action({})
        self.assertIsNotNone(action)
        
        agent.update(1.0, {})
        agent.reset()

if __name__ == '__main__':
    unittest.main()
```

### 7. Update Index and Navigation

#### Update Documentation Index
```rst
# docs/index.rst (add to toctree)
   students/labXX-new-game
```

#### Update Server Documentation
```python
# Update server help text
GAME_TYPES = {
    "rps": "Rock Paper Scissors",
    "bos": "Battle of the Sexes", 
    "newgame": "New Game"  # Add new game
}
```

## Validation Checklist

### Before Deployment
- [ ] **Game implementation** works correctly
- [ ] **Agent interface** is properly implemented
- [ ] **Server configuration** includes new game
- [ ] **Student stencil** is complete and functional
- [ ] **Documentation** is clear and accurate
- [ ] **Tests** pass and cover key functionality
- [ ] **Integration** with existing system works

### Testing Procedures
```bash
# Test game implementation
python -c "from core.game.NewGame import NewGame; print('Game OK')"

# Test agent loading
python -c "from core.agents.labXX.random_agent import RandomAgent; print('Agent OK')"

# Test engine integration
python tests/labs/labXX/test_new_game.py

# Test server integration
python server/server.py --test-game newgame

# Test student stencil
cd stencils/labXX_stencil
python test_agent.py
```

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

## Next Steps

1. **Implement the game** following the structure above
2. **Create agent examples** and student stencil
3. **Write documentation** for students and instructors
4. **Test thoroughly** with sample implementations
5. **Deploy gradually** starting with a small group

New labs are now ready to be added to the system! 