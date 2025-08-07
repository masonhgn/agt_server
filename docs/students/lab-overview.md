# Lab Overview for Students

This guide provides a general overview of how all AGT labs are structured, helping you understand the common patterns you'll encounter across different labs.

## What You'll Be Doing in Each Lab

Every lab follows the same basic pattern:

1. **Study the game** - Understand the rules and mechanics
2. **Analyze the state space** - Figure out what information you have
3. **Design your strategy** - Implement your agent's decision-making
4. **Test locally** - Make sure your agent works before submitting
5. **Compete** - Connect to the server and compete against others

## The Three Key Methods

Every agent you create must implement these three methods:

### 1. `get_action(observation)`

This is where your strategy lives. You receive the current game state and return your chosen action.

```python
def get_action(self, observation):
    # observation contains the current game state
    # Your job is to analyze this and choose the best action
    return my_chosen_action
```

**What you get:**
- `observation`: A dictionary containing the current game state
- **Return:** Your chosen action (format varies by lab)

**Your job:** Analyze the observation and implement your strategy to choose the best action.

### 2. `update(reward, info)`

Learn from your experience. Called after each action with the results.

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Store this experience for learning
    self.my_history.append(self.get_last_action())
    
    # Learn from opponent's action if available
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
    
    # Update your strategy based on new information
    self.update_strategy()
```

**What you get:**
- `reward`: Points earned from your last action
- `info`: Additional information (opponent's action, game state, etc.)

**Your job:** Use this information to improve your strategy over time.

### 3. `reset()`

Start fresh for a new game. Clear any game-specific state.

```python
def reset(self):
    super().reset()
    # Clear any game-specific state
    self.opponent_history = []
    self.my_history = []
    self.round_count = 0
    # Reset any learning parameters
    self.learning_rate = self.initial_learning_rate
```

**Your job:** Prepare your agent for a new game by clearing old information.

## Common Patterns Across Labs

### 1. State Management

Most agents need to track information across rounds:

```python
class MyAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        # Track what you need to know
        self.opponent_history = []
        self.my_history = []
        self.round_count = 0
        self.game_state = {}
    
    def reset(self):
        super().reset()
        # Clear everything for new game
        self.opponent_history = []
        self.my_history = []
        self.round_count = 0
        self.game_state = {}
```

### 2. Learning from Experience

Use the `update` method to learn:

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Store this experience
    self.my_history.append(self.get_last_action())
    
    # Learn from opponent's action if available
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
    
    # Update your strategy
    self.update_strategy()
```

### 3. Strategy Implementation

Your strategy goes in `get_action`:

```python
def get_action(self, observation):
    # Analyze the current situation
    situation = self.analyze_situation(observation)
    
    # Choose action based on your strategy
    if situation == "explore":
        return self.explore_action()
    elif situation == "exploit":
        return self.exploit_action()
    else:
        return self.default_action()
```

## Understanding Observations

Observations tell you what's happening in the game. The structure varies by lab:

### Common Observation Patterns

```python
# Simple games (Lab 01-03)
observation = {}  # Often empty - you know the game structure

# Complex games (Lab 04, 06)
observation = {
    "game_state": {...},      # Current game state
    "available_actions": [...], # What you can do
    "opponent_info": {...},    # Information about opponents
    "history": [...]          # Previous actions/events
}
```

### What to Look For

1. **Available actions** - What can you do right now?
2. **Opponent information** - What do you know about other players?
3. **Game state** - What's the current situation?
4. **History** - What has happened so far?

## Understanding Actions

Different labs expect different action formats:

### Common Action Types

```python
# Discrete actions (Lab 01-04)
action = 0  # Integer representing your choice

# Continuous actions (Lab 06)
action = 5.2  # Real number (like a bid amount)

# Multiple actions (Lab 06)
action = [5, 8]  # List of actions (like multiple bids)
```

## Learning Strategies

### 1. Exploration vs Exploitation

Balance trying new things with using what works:

```python
def get_action(self, observation):
    if self.should_explore():
        return self.explore_action()  # Try something new
    else:
        return self.exploit_action()  # Use what works best
```

### 2. Opponent Modeling

Track and predict opponent behavior:

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Track opponent's actions
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
    
    # Update your model of the opponent
    self.update_opponent_model()

def predict_opponent_action(self):
    # Use your model to predict what opponent will do
    return self.opponent_model.predict()
```

### 3. Adaptive Strategies

Change your strategy based on the situation:

```python
def get_action(self, observation):
    # Analyze the current situation
    if self.is_winning():
        return self.conservative_action()
    elif self.is_losing():
        return self.aggressive_action()
    else:
        return self.balanced_action()
```

## Testing Your Agent

### Local Testing

Always test your agent locally before submitting:

```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent

# Create your agent
my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

# Run a test game
engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My agent score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Debugging Tips

1. **Print observations** to understand the game state:
```python
def get_action(self, observation):
    print(f"Observation: {observation}")
    # Your strategy here
    pass
```

2. **Track performance** to see how you're doing:
```python
def update(self, reward, info):
    super().update(reward, info)
    
    if len(self.reward_history) % 10 == 0:
        recent_rewards = self.reward_history[-10:]
        avg_reward = sum(recent_rewards) / len(recent_rewards)
        print(f"Average reward over last 10 rounds: {avg_reward}")
```

3. **Test against different opponents**:
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

## Connecting to the Server

### 1. Start the Server

In one terminal:
```bash
python server/server.py
```

### 2. Connect Your Agent

In another terminal:
```bash
cd stencils/lab01_stencil
python example_solution.py
```

Your agent will connect to the server and start competing!

## Common Mistakes to Avoid

### 1. Not Implementing Required Methods

Make sure you implement all three methods:
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
- Verify that actions are in the correct format

### 3. Not Learning from Experience

Use the `update` method to improve your strategy:
```python
def update(self, reward, info):
    super().update(reward, info)
    # Don't forget to learn from this experience!
    self.learn_from_experience(reward, info)
```

### 4. Not Handling Edge Cases

Consider what happens when:
- You have no history yet
- The observation is empty
- You're in an unexpected state

## Next Steps

Now that you understand the general structure:

1. **Read the specific lab documentation** for the lab you're working on
2. **Study the game mechanics** and state space
3. **Implement your agent** using the patterns above
4. **Test thoroughly** before submitting
5. **Compete and learn** from the results

Each lab will have its own specific details about the game mechanics, state space, and optimal strategies. The general patterns above will help you implement effective agents across all labs! 