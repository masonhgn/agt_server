# Getting Started for Students

This guide covers the essential setup and functions you'll use across all AGT labs.

## Quick Setup

### 1. Install Dependencies
```bash
git clone <repository-url>
cd agt_server_new
pip install -r requirements.txt
```

### 2. Explore Stencils
Each lab has starter code in the `stencils/` directory:
```
stencils/
├── lab01_stencil/
├── lab02_stencil/
├── lab03_stencil/
├── lab04_stencil/
└── lab06_stencil/
```

## Common Functions Across All Labs

### The Three Required Methods

Every agent must implement these methods:

#### `get_action(observation)`
```python
def get_action(self, observation):
    # observation: current game state (varies by lab)
    # Return: your chosen action (format varies by lab)
    return my_action
```

#### `update(reward, info)`
```python
def update(self, reward, info):
    super().update(reward, info)
    # reward: points earned from last action
    # info: additional information (opponent action, etc.)
```

#### `reset()`
```python
def reset(self):
    super().reset()
    # Clear any game-specific state
    self.opponent_history = []
    self.my_history = []
```

### Common State Management

```python
class MyAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_history = []
        self.my_history = []
        self.round_count = 0
    
    def reset(self):
        super().reset()
        self.opponent_history = []
        self.my_history = []
        self.round_count = 0
```

## Running Labs Locally

### Test Your Agent
```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent

# Create your agent
my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

# Run test game
engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Debug Your Agent
```python
def get_action(self, observation):
    print(f"Observation: {observation}")
    print(f"Opponent history: {self.opponent_history}")
    
    action = self.choose_action(observation)
    print(f"Chosen action: {action}")
    
    return action
```

## Connecting to Server

### 1. Start Server
```bash
python server/server.py
```

### 2. Connect Your Agent
```bash
cd stencils/lab01_stencil
python example_solution.py
```

Your agent will connect and start competing automatically.

## Next Steps

1. **Read the lab overview** to understand common patterns
2. **Choose a lab** and read its specific documentation
3. **Implement your agent** using the patterns above
4. **Test locally** before submitting
5. **Connect to server** and compete

Each lab has its own game mechanics and state space. The patterns above work across all labs, but the specific details vary. 