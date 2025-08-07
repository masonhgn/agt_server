# Lab 01: Matrix Games

This lab introduces you to basic game theory concepts through matrix games like Rock Paper Scissors, Battle of the Sexes, and Chicken.

## Game Overview

Matrix games are **simultaneous-move games** where:
- Two players choose actions at the same time
- Payoffs are determined by the combination of actions
- The game repeats for many rounds
- Players can learn from experience

## Games in This Lab

### 1. Rock Paper Scissors (RPS)

**Actions:** Rock (0), Paper (1), Scissors (2)

**Payoff Matrix:**
```
        Opponent
        R  P  S
You  R  0 -1  1
     P  1  0 -1  
     S -1  1  0
```

**Key Concept:** Zero-sum game with no pure Nash equilibrium

### 2. Battle of the Sexes (BOS)

**Actions:** Action A (0), Action B (1)

**Payoff Matrix:**
```
        Opponent
        A    B
You  A  3,3  0,0
     B  0,0  2,2
```

**Key Concept:** Coordination game with multiple Nash equilibria

### 3. Chicken Game

**Actions:** Swerve (0), Straight (1)

**Payoff Matrix:**
```
        Opponent
        Swerve  Straight
You  Swerve    0,0      -1,1
     Straight  1,-1     -10,-10
```

**Key Concept:** Conflict game with asymmetric equilibria

## State Space Structure

### Observations

For matrix games, observations are typically **empty**:

```python
observation = {}  # No additional information needed
```

**Why empty?** You know the game structure and payoff matrix. The only information you need is what you've learned from previous rounds.

### Actions

Actions are **integers** representing your choice:

```python
# RPS
action = 0  # Rock
action = 1  # Paper  
action = 2  # Scissors

# BOS/Chicken
action = 0  # Action A / Swerve
action = 1  # Action B / Straight
```

### Rewards

Rewards are **immediate payoffs** from the payoff matrix:

```python
# RPS example
if my_action == 0 and opponent_action == 1:  # Rock vs Paper
    reward = -1  # I lose
elif my_action == 1 and opponent_action == 0:  # Paper vs Rock
    reward = 1   # I win
```

## Key Learning Concepts

### 1. Nash Equilibrium

A strategy profile where no player can improve their payoff by changing their strategy.

**RPS:** Mixed strategy (1/3, 1/3, 1/3) is a Nash equilibrium
**BOS:** Pure strategies (A,A) and (B,B) are Nash equilibria
**Chicken:** Mixed strategies can be Nash equilibria

### 2. Best Response

The optimal action given your belief about the opponent's strategy.

```python
def best_response(self, opponent_strategy):
    # Calculate expected payoff for each action
    expected_payoffs = []
    for my_action in [0, 1, 2]:
        expected_payoff = 0
        for opponent_action, prob in opponent_strategy.items():
            payoff = self.payoff_matrix[my_action][opponent_action]
            expected_payoff += prob * payoff
        expected_payoffs.append(expected_payoff)
    
    # Return action with highest expected payoff
    return expected_payoffs.index(max(expected_payoffs))
```

### 3. Fictitious Play

Learn by observing opponent's action frequencies and playing best response:

```python
def fictitious_play(self, observation):
    # Calculate opponent's empirical distribution
    if len(self.opponent_history) > 0:
        opponent_counts = {0: 0, 1: 0, 2: 0}
        for action in self.opponent_history:
            opponent_counts[action] += 1
        
        # Convert to probabilities
        total = sum(opponent_counts.values())
        opponent_strategy = {action: count/total for action, count in opponent_counts.items()}
        
        # Play best response
        return self.best_response(opponent_strategy)
    else:
        # No history yet, play randomly
        return random.choice([0, 1, 2])
```

## Strategy Implementation

### Basic Random Strategy

```python
class RandomAgent(BaseAgent):
    def get_action(self, observation):
        return random.choice([0, 1, 2])  # Random action
```

### Fictitious Play Strategy

```python
class FictitiousPlayAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_counts = {0: 0, 1: 0, 2: 0}
    
    def get_action(self, observation):
        if sum(self.opponent_counts.values()) == 0:
            return random.choice([0, 1, 2])  # No history yet
        
        # Calculate opponent's empirical distribution
        total = sum(self.opponent_counts.values())
        opponent_probs = {action: count/total for action, count in self.opponent_counts.items()}
        
        # Play best response
        return self.best_response(opponent_probs)
    
    def update(self, reward, info):
        super().update(reward, info)
        if 'opponent_action' in info:
            self.opponent_counts[info['opponent_action']] += 1
    
    def reset(self):
        super().reset()
        self.opponent_counts = {0: 0, 1: 0, 2: 0}
    
    def best_response(self, opponent_probs):
        # Calculate expected payoff for each action
        expected_payoffs = []
        for my_action in [0, 1, 2]:
            expected_payoff = 0
            for opponent_action, prob in opponent_probs.items():
                payoff = self.get_payoff(my_action, opponent_action)
                expected_payoff += prob * payoff
            expected_payoffs.append(expected_payoff)
        
        return expected_payoffs.index(max(expected_payoffs))
    
    def get_payoff(self, my_action, opponent_action):
        # RPS payoff matrix
        payoffs = [
            [0, -1, 1],   # Rock vs Rock, Paper, Scissors
            [1, 0, -1],   # Paper vs Rock, Paper, Scissors
            [-1, 1, 0]    # Scissors vs Rock, Paper, Scissors
        ]
        return payoffs[my_action][opponent_action]
```

### Nash Equilibrium Strategy

```python
class NashEquilibriumAgent(BaseAgent):
    def get_action(self, observation):
        # For RPS, play mixed strategy (1/3, 1/3, 1/3)
        rand = random.random()
        if rand < 1/3:
            return 0  # Rock
        elif rand < 2/3:
            return 1  # Paper
        else:
            return 2  # Scissors
```

## Testing Your Agent

### Local Testing

```python
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent

# Test against random opponent
my_agent = MyMatrixAgent("MyAgent")
random_opponent = RandomAgent("Random")

engine = Engine(RPSGame(), [my_agent, random_opponent], rounds=1000)
results = engine.run()

print(f"My agent score: {results[0]}")
print(f"Random opponent score: {results[1]}")
```

### Performance Analysis

```python
def analyze_performance(self):
    if len(self.reward_history) > 0:
        avg_reward = sum(self.reward_history) / len(self.reward_history)
        print(f"Average reward: {avg_reward}")
        
        # Check if we're doing better than random (0 expected value)
        if avg_reward > 0:
            print("Agent is performing above random!")
        elif avg_reward < 0:
            print("Agent is performing below random.")
        else:
            print("Agent is performing at random level.")
```

## Common Strategies

### 1. Tit-for-Tat

Copy your opponent's last action:

```python
def get_action(self, observation):
    if len(self.opponent_history) > 0:
        return self.opponent_history[-1]  # Copy last action
    else:
        return random.choice([0, 1, 2])  # Random if no history
```

### 2. Win-Stay, Lose-Shift

Keep your action if you won, change if you lost:

```python
def get_action(self, observation):
    if len(self.reward_history) > 0:
        last_reward = self.reward_history[-1]
        if last_reward > 0:  # Won
            return self.get_last_action()  # Keep same action
        else:  # Lost or tied
            return random.choice([0, 1, 2])  # Try something new
    else:
        return random.choice([0, 1, 2])
```

### 3. Adaptive Strategy

Change strategy based on opponent behavior:

```python
def get_action(self, observation):
    if len(self.opponent_history) < 10:
        return random.choice([0, 1, 2])  # Explore early
    
    # Analyze opponent's pattern
    recent_actions = self.opponent_history[-10:]
    if len(set(recent_actions)) == 1:  # Opponent is stubborn
        return self.best_response_to_stubborn(recent_actions[0])
    else:  # Opponent is changing
        return self.fictitious_play_strategy()
```

## Expected Outcomes

### Against Random Opponent
- **Random agent**: ~0 average reward
- **Fictitious play**: >0 average reward (should win)
- **Nash equilibrium**: ~0 average reward (unexploitable)

### Against Stubborn Opponent
- **Random agent**: ~0 average reward
- **Fictitious play**: >0 average reward (should exploit)
- **Nash equilibrium**: ~0 average reward (safe)

### Against Fictitious Play Opponent
- **Random agent**: <0 average reward (gets exploited)
- **Fictitious play**: ~0 average reward (may converge)
- **Nash equilibrium**: ~0 average reward (safe)

## Key Takeaways

1. **Learning works**: Fictitious play can outperform random opponents
2. **Nash equilibrium is safe**: Can't be exploited by any strategy
3. **Opponent modeling matters**: Understanding your opponent helps
4. **Mixed strategies are important**: Pure strategies can be exploited

## Next Steps

1. **Implement a basic strategy** (random or fictitious play)
2. **Test against different opponents** to understand performance
3. **Analyze your results** to see what works
4. **Try more sophisticated strategies** like adaptive learning
5. **Compete against other students** to see how you rank

Remember: The goal is to understand game theory concepts through hands-on experience. Don't worry about being perfect - focus on learning the principles! 