# Getting Started for Students

This guide covers the common setup and functions you'll use across all AGT labs.

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

### 1. Test Your Agent
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

### 2. Debug Your Agent
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

## Common Patterns

### Tracking Opponent Actions
```python
def update(self, reward, info):
    super().update(reward, info)
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
```

### Performance Monitoring
```python
def update(self, reward, info):
    super().update(reward, info)
    
    if len(self.reward_history) % 10 == 0:
        recent_rewards = self.reward_history[-10:]
        avg_reward = sum(recent_rewards) / len(recent_rewards)
        print(f"Average reward: {avg_reward}")
```

### Testing Against Different Opponents
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

## Common Mistakes

### 1. Missing Required Methods
```python
class MyAgent(BaseAgent):
    def get_action(self, observation):  # Required
        pass
    
    def update(self, reward, info):     # Required
        super().update(reward, info)
    
    def reset(self):                    # Required
        super().reset()
```

### 2. Not Testing Locally
Always test your agent before submitting:
- Test against different opponents
- Check that your agent doesn't crash
- Verify action format is correct

### 3. Not Learning from Experience
```python
def update(self, reward, info):
    super().update(reward, info)
    # Use this information to improve your strategy!
```

## Next Steps

1. **Read the lab overview** to understand common patterns
2. **Choose a lab** and read its specific documentation
3. **Implement your agent** using the patterns above
4. **Test locally** before submitting
5. **Connect to server** and compete

Each lab has its own game mechanics and state space. The patterns above work across all labs, but the specific details vary. 