# Competition Guide

This guide covers participating in AGT lab competitions and maximizing your performance.

## Competition Overview

AGT competitions allow you to test your agent against other students' implementations in real-time tournaments. The system automatically matches players and tracks results across multiple games.

## Preparing for Competition

### Code Quality
```python
# Ensure your agent is robust
class MyAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_history = []
        self.my_history = []
    
    def get_action(self, observation):
        try:
            # Your strategy here
            return action
        except Exception as e:
            # Fallback to random if strategy fails
            return random.choice([0, 1])
    
    def update(self, reward, info):
        super().update(reward, info)
        # Store opponent action if available
        if "opponent_action" in info:
            self.opponent_history.append(info["opponent_action"])
    
    def reset(self):
        super().reset()
        self.opponent_history = []
        self.my_history = []
```

### Testing Strategy
```python
# Test against multiple opponent types
def test_competition_readiness():
    opponents = [
        RandomAgent("Random"),
        StubbornAgent("Stubborn"),
        TitForTatAgent("TitForTat")
    ]
    
    for opponent in opponents:
        engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)
        results = engine.run()
        print(f"vs {opponent.name}: {results[0]} vs {results[1]}")
```

## Competition Process

### 1. Connect to Server
```bash
# Navigate to your stencil directory
cd stencils/lab01_stencil

# Run your agent
python example_solution.py
```

### 2. Tournament Structure
- **Registration**: Your agent connects and registers for the tournament
- **Matchmaking**: System pairs you with other players
- **Games**: Multiple rounds against each opponent
- **Results**: Cumulative scores determine rankings

### 3. Competition Timeline
```
Tournament Start → Registration Period → Matchmaking → 
Game Execution → Results Collection → Final Rankings
```

## Competition Strategies

### Adaptive Play
```python
def get_action(self, observation):
    # Analyze opponent's recent behavior
    if len(self.opponent_history) > 20:
        recent_actions = self.opponent_history[-20:]
        opponent_pattern = self.analyze_pattern(recent_actions)
        return self.adapt_to_pattern(opponent_pattern)
    
    # Default strategy for early rounds
    return self.default_strategy()
```

### Exploitation vs Exploration
```python
def get_action(self, observation):
    # Balance exploitation and exploration
    if random.random() < 0.1:  # 10% exploration
        return random.choice([0, 1])
    else:
        return self.exploit_opponent()
```

### Memory Management
```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Store opponent action
    if "opponent_action" in info:
        self.opponent_history.append(info["opponent_action"])
    
    # Limit memory to recent history
    if len(self.opponent_history) > 100:
        self.opponent_history = self.opponent_history[-50:]
```

## Performance Optimization

### Speed Optimization
```python
# Cache frequently used calculations
class OptimizedAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.action_cache = {}
        self.pattern_cache = {}
    
    def get_action(self, observation):
        # Use cached results when possible
        state_key = self.get_state_key(observation)
        if state_key in self.action_cache:
            return self.action_cache[state_key]
        
        # Calculate and cache
        action = self.calculate_action(observation)
        self.action_cache[state_key] = action
        return action
```

### Memory Optimization
```python
def reset(self):
    super().reset()
    # Clear caches to prevent memory leaks
    self.action_cache.clear()
    self.pattern_cache.clear()
    self.opponent_history.clear()
```

## Competition Analysis

### Performance Tracking
```python
def analyze_competition_performance(self):
    if len(self.reward_history) > 0:
        # Overall performance
        total_score = sum(self.reward_history)
        avg_score = total_score / len(self.reward_history)
        
        # Recent performance (last 50 rounds)
        recent_score = sum(self.reward_history[-50:]) / 50
        
        print(f"Total Score: {total_score}")
        print(f"Average Score: {avg_score:.3f}")
        print(f"Recent Average: {recent_score:.3f}")
        
        # Performance trend
        if recent_score > avg_score:
            print("Improving over time!")
        elif recent_score < avg_score:
            print("Performance declining.")
        else:
            print("Performance stable.")
```

### Opponent Analysis
```python
def analyze_opponents(self):
    if self.opponent_history:
        # Action frequencies
        action_counts = {}
        for action in self.opponent_history:
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print("Opponent Action Frequencies:")
        for action, count in action_counts.items():
            freq = count / len(self.opponent_history)
            print(f"  Action {action}: {freq:.2%}")
        
        # Pattern detection
        patterns = self.detect_patterns(self.opponent_history)
        print(f"Detected patterns: {patterns}")
```

## Competition Tips

### Before Competition
1. **Test thoroughly** - Run extensive local testing
2. **Optimize performance** - Ensure your agent is fast and reliable
3. **Handle edge cases** - Make sure your agent doesn't crash
4. **Document strategy** - Understand what your agent does and why

### During Competition
1. **Monitor performance** - Watch how your agent performs
2. **Stay connected** - Ensure stable network connection
3. **Don't panic** - Trust your testing and strategy
4. **Learn from results** - Analyze what worked and what didn't

### After Competition
1. **Review results** - Analyze your performance
2. **Identify weaknesses** - What strategies beat your agent?
3. **Improve strategy** - Make adjustments for next competition
4. **Share insights** - Discuss strategies with classmates

## Common Competition Mistakes

### Technical Issues
```python
# Avoid these common problems:

# 1. Not handling exceptions
def get_action(self, observation):
    # BAD: No error handling
    return self.complex_calculation(observation)
    
    # GOOD: Handle errors gracefully
    try:
        return self.complex_calculation(observation)
    except Exception:
        return random.choice([0, 1])

# 2. Not resetting state
def reset(self):
    # BAD: Forgetting to reset
    pass
    
    # GOOD: Proper reset
    super().reset()
    self.opponent_history = []
    self.my_history = []

# 3. Memory leaks
def update(self, reward, info):
    # BAD: Unlimited memory growth
    self.all_history.append(info)
    
    # GOOD: Limited memory
    self.recent_history.append(info)
    if len(self.recent_history) > 100:
        self.recent_history = self.recent_history[-50:]
```

### Strategic Issues
```python
# Avoid these strategic mistakes:

# 1. Overfitting to specific opponents
def get_action(self, observation):
    # BAD: Hard-coded responses
    if opponent_action == 0:
        return 1
    elif opponent_action == 1:
        return 0
    
    # GOOD: Adaptive strategy
    return self.adaptive_response(opponent_history)

# 2. Not learning from experience
def update(self, reward, info):
    # BAD: Ignoring feedback
    pass
    
    # GOOD: Learning from results
    super().update(reward, info)
    self.update_strategy(reward, info)

# 3. Predictable behavior
def get_action(self, observation):
    # BAD: Always same response
    return 0
    
    # GOOD: Some randomness
    if random.random() < 0.1:
        return random.choice([0, 1])
    else:
        return self.strategic_choice()
```

## Competition Etiquette

### Good Practices
1. **Test locally first** - Don't submit untested code
2. **Be respectful** - Don't try to crash the server
3. **Learn from others** - Study successful strategies
4. **Share knowledge** - Help classmates improve

### What to Avoid
1. **Submitting broken code** - Test thoroughly first
2. **Spamming the server** - Don't make excessive connections
3. **Cheating** - Don't try to exploit system vulnerabilities
4. **Being disruptive** - Follow competition rules

## Next Steps

1. **Implement robust agent** - Handle errors and edge cases
2. **Test extensively** - Against various opponent types
3. **Optimize performance** - Speed and memory efficiency
4. **Participate actively** - Join competitions regularly
5. **Learn continuously** - Analyze results and improve

Competitions are opportunities to test and improve your strategies! 