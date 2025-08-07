# Debugging Tips

This guide provides practical debugging strategies for AGT lab implementations.

## Common Debugging Techniques

### Print Debugging

Add print statements to understand your agent's behavior:
```python
def get_action(self, observation):
    print(f"Observation: {observation}")
    print(f"My history: {self.my_history}")
    print(f"Opponent history: {self.opponent_history}")
    
    action = self.choose_action(observation)
    print(f"Chosen action: {action}")
    
    return action
```

### State Tracking

Track important variables throughout the game:
```python
def update(self, reward, info):
    super().update(reward, info)
    
    print(f"Round {len(self.reward_history)}:")
    print(f"  My action: {self.get_last_action()}")
    print(f"  Opponent action: {info.get('opponent_action', 'unknown')}")
    print(f"  Reward: {reward}")
    print(f"  Total score: {sum(self.reward_history)}")
```

### Performance Analysis

Monitor your agent's performance:
```python
def analyze_performance(self):
    if len(self.reward_history) > 0:
        avg_reward = sum(self.reward_history) / len(self.reward_history)
        print(f"Average reward: {avg_reward:.3f}")
        
        if avg_reward > 0:
            print("Performing above random!")
        elif avg_reward < 0:
            print("Performing below random.")
        else:
            print("Performing at random level.")
```

## Common Issues and Solutions

### Agent Not Learning

**Problem**: Agent performance doesn't improve over time.

**Solutions**:
```python
# 1. Check if you're storing opponent actions
def update(self, reward, info):
    super().update(reward, info)
    if "opponent_action" in info:
        self.opponent_history.append(info["opponent_action"])

# 2. Verify your learning logic
def get_action(self, observation):
    if len(self.opponent_history) > 10:
        # Analyze recent opponent behavior
        recent_actions = self.opponent_history[-10:]
        opponent_freq = self.calculate_frequency(recent_actions)
        return self.best_response(opponent_freq)
    return random.choice([0, 1])
```

### Agent Always Loses

**Problem**: Agent consistently performs poorly.

**Solutions**:
```python
# 1. Check action format
def get_action(self, observation):
    # Make sure you're returning the correct action type
    return 0  # or 1, or whatever your game expects

# 2. Verify reward interpretation
def update(self, reward, info):
    super().update(reward, info)
    print(f"Reward: {reward}")  # Check if rewards make sense

# 3. Test against random opponent
def test_against_random(self):
    # Your agent should beat random consistently
    pass
```

### Agent Crashes

**Problem**: Agent throws errors during execution.

**Solutions**:
```python
# 1. Add error handling
def get_action(self, observation):
    try:
        # Your logic here
        return action
    except Exception as e:
        print(f"Error in get_action: {e}")
        return 0  # Default action

# 2. Check data types
def update(self, reward, info):
    super().update(reward, info)
    if not isinstance(reward, (int, float)):
        print(f"Warning: reward is {type(reward)}, expected number")
```

## Testing Strategies

### Local Testing

Test your agent thoroughly before submitting:
```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent

# Test against random opponent
my_agent = MyAgent("MyAgent")
random_agent = RandomAgent("Random")

engine = Engine(RPSGame(), [my_agent, random_agent], rounds=1000)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Random score: {results[1]}")

# Should be positive for a good agent
if results[0] > results[1]:
    print("Good! You're beating random.")
else:
    print("Need improvement.")
```

### Performance Testing

Test against different opponent types:
```python
# Test against different strategies
opponents = [
    RandomAgent("Random"),
    StubbornAgent("Stubborn"),  # Always plays same action
    TitForTatAgent("TitForTat")  # Copies your last action
]

for opponent in opponents:
    engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)
    results = engine.run()
    print(f"vs {opponent.name}: {results[0]} vs {results[1]}")
```

### Edge Case Testing

Test your agent in edge cases:
```python
# Test with empty observations
action = my_agent.get_action({})
print(f"Action with empty obs: {action}")

# Test with unexpected data
action = my_agent.get_action({"unexpected": "data"})
print(f"Action with unexpected data: {action}")

# Test reset functionality
my_agent.reset()
action = my_agent.get_action({})
print(f"Action after reset: {action}")
```

## Debugging Tools

### Logging

Use Python's logging module for better debugging:
```python
import logging

class MyAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(self.name)
    
    def get_action(self, observation):
        self.logger.debug(f"Observation: {observation}")
        action = self.choose_action(observation)
        self.logger.debug(f"Chosen action: {action}")
        return action
```

### Visualization

Create visualizations to understand your agent's behavior:
```python
import matplotlib.pyplot as plt

def plot_performance(self):
    if len(self.reward_history) > 0:
        plt.figure(figsize=(10, 6))
        
        # Plot cumulative reward
        cumulative = [sum(self.reward_history[:i+1]) for i in range(len(self.reward_history))]
        plt.plot(cumulative, label='Cumulative Reward')
        
        # Plot moving average
        window = 50
        if len(self.reward_history) >= window:
            moving_avg = [sum(self.reward_history[i:i+window])/window 
                         for i in range(len(self.reward_history)-window+1)]
            plt.plot(range(window-1, len(self.reward_history)), moving_avg, 
                    label=f'{window}-round Moving Average')
        
        plt.xlabel('Round')
        plt.ylabel('Reward')
        plt.title('Agent Performance Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
```

### Statistics

Track detailed statistics about your agent:
```python
def get_statistics(self):
    stats = super().get_statistics()
    
    # Add custom statistics
    if hasattr(self, 'opponent_history') and self.opponent_history:
        opponent_actions = self.opponent_history
        stats['opponent_action_frequencies'] = {
            action: opponent_actions.count(action) / len(opponent_actions)
            for action in set(opponent_actions)
        }
    
    if hasattr(self, 'my_history') and self.my_history:
        my_actions = self.my_history
        stats['my_action_frequencies'] = {
            action: my_actions.count(action) / len(my_actions)
            for action in set(my_actions)
        }
    
    return stats
```

## Best Practices

### Code Organization
1. **Separate concerns** - Keep strategy logic separate from debugging
2. **Use helper methods** - Break complex logic into smaller functions
3. **Add comments** - Explain your strategy and debugging code
4. **Version control** - Use git to track changes and revert if needed

### Testing Strategy
1. **Test incrementally** - Test each component separately
2. **Test against known opponents** - Start with simple strategies
3. **Test edge cases** - Handle unexpected inputs gracefully
4. **Test performance** - Ensure your agent improves over time

### Debugging Workflow
1. **Identify the problem** - What's not working as expected?
2. **Add debugging code** - Print statements, logging, etc.
3. **Run tests** - Execute with debugging enabled
4. **Analyze results** - What do the debug outputs tell you?
5. **Fix the issue** - Implement the solution
6. **Verify the fix** - Test that the problem is resolved
7. **Clean up** - Remove or comment out debugging code

## Next Steps

1. **Start with simple debugging** - Add print statements to understand behavior
2. **Test locally** - Verify your agent works before submitting
3. **Monitor performance** - Track how your agent improves over time
4. **Learn from failures** - Analyze what went wrong and why
5. **Iterate quickly** - Make small changes and test frequently

Effective debugging leads to better agent performance! 