# Understanding the AGT Lab Structure

Welcome to the Algorithmic Game Theory (AGT) lab system! This guide will walk you through how everything works, starting with the fundamental building blocks and showing how they come together to create the learning experiences you'll encounter in each lab.

## The Big Picture

Think of the AGT system as a **game engine** where students write **agents** that compete in different **games**. The system manages everything from connecting players to running tournaments, all while providing a consistent interface for learning game theory concepts.

## Core Building Blocks

### 1. The Game Engine (Engine)

The **Engine** is the heart of the system. It's like a referee that:
- Manages the flow of a game between multiple agents
- Collects actions from each agent
- Updates the game state
- Distributes rewards and observations
- Keeps track of scores and statistics

```python
# The Engine orchestrates everything
engine = Engine(game=RPSGame(), agents=[my_agent, opponent_agent], rounds=100)
final_scores = engine.run()
```

**What it does for you:** You don't need to worry about the Engine - it's already built! Your job is to create agents that can play the games.

### 2. Games (BaseGame)

Games define the **rules and mechanics** of the competition. Every game inherits from `BaseGame`, which provides a consistent interface:

```python
class BaseGame(ABC):
    def reset(self) -> ObsDict:          # Start a fresh game
    def step(self, actions) -> Tuple:    # Take actions, return results  
    def players_to_move(self) -> List:   # Who needs to act now?
```

**Key Methods:**
- **`reset()`**: Starts a new game, returns initial observations
- **`step(actions)`**: Processes player actions, returns new state and rewards
- **`players_to_move()`**: Tells the engine which players need to act

**What it means for you:** Each lab focuses on a different type of game, teaching you different game theory concepts.

### 3. Stages (BaseStage)

Stages represent **phases or rounds** within a game. Think of them as the individual steps that make up a complete game:

```python
class BaseStage(ABC):
    def step(self, actions) -> Tuple:    # Process actions for this stage
    def legal_actions(self, player) -> Any:  # What can this player do?
    def is_done(self) -> bool:           # Is this stage finished?
```

**Why Stages Matter:**
- **Simple games** (like RPS) have one stage that repeats
- **Complex games** (like auctions) have multiple stages with different rules
- Stages help break down complex games into manageable pieces

**Example:** In an auction, you might have:
1. **Bidding Stage**: Players submit bids
2. **Allocation Stage**: System determines winners
3. **Payment Stage**: Winners pay their bids

### 4. Agents (BaseAgent)

Agents are **your code** - the intelligent players that make decisions. Every agent inherits from `BaseAgent`:

```python
class BaseAgent(ABC):
    def get_action(self, observation) -> Any:  # Your strategy here!
    def update(self, reward, info):            # Learn from results
    def reset(self):                           # Start fresh
```

**The Three Key Methods:**

1. **`get_action(observation)`** - This is where your intelligence lives!
   - Receives the current game state
   - Returns your chosen action
   - This is where you implement your strategy

2. **`update(reward, info)`** - Learning from experience
   - Called after each action with the result
   - Use this to update your strategy
   - Store information for future decisions

3. **`reset()`** - Fresh start
   - Called when starting a new game
   - Clear any game-specific state
   - Prepare for a new competition

**What you'll implement:** In each lab, you'll create a class that inherits from `BaseAgent` and implements these methods with your own strategy.

## How Everything Works Together

### The Game Loop

Here's how a typical game session flows:

```
1. Engine creates a game and agents
2. Game.reset() → Initial observations
3. For each round:
   a. Engine asks agents: "What's your action?"
   b. Agents call get_action(observation)
   c. Engine collects all actions
   d. Game.step(actions) → New state and rewards
   e. Engine calls agent.update(reward, info)
4. Repeat until game is done
5. Engine returns final scores
```

### Example: Rock Paper Scissors

Let's trace through a simple RPS game:

```python
# 1. Setup
game = RPSGame(rounds=10)
my_agent = MyRPSAgent("Alice")
opponent = RandomAgent("Bob")
engine = Engine(game, [my_agent, opponent])

# 2. Game starts
observations = game.reset()  # Both agents see: {}

# 3. First round
my_action = my_agent.get_action({})      # Alice chooses "Rock"
opponent_action = opponent.get_action({}) # Bob chooses "Paper"

# 4. Process round
new_obs, rewards, done, info = game.step({
    0: my_action,      # Alice's action
    1: opponent_action # Bob's action
})

# 5. Update agents
my_agent.update(rewards[0], info[0])      # Alice learns she lost
opponent.update(rewards[1], info[1])      # Bob learns he won

# 6. Continue for 10 rounds...
```

## Lab-Specific Patterns

### Lab 01: Matrix Games (RPS, BOS, Chicken)

**What you learn:** Basic game theory, Nash equilibria, best responses

**Game Structure:**
- **One stage** that repeats for many rounds
- **Two players** making simultaneous moves
- **Payoff matrix** defines rewards for each action combination

**Your Agent:**
```python
class MyMatrixAgent(BaseAgent):
    def get_action(self, observation):
        # Implement your strategy here!
        # You might use:
        # - Random play
        # - Fictitious play (learn from opponent)
        # - Nash equilibrium strategies
        pass
```

### Lab 02: Finite State Machines

**What you learn:** State machines, coordination, repeated games

**Game Structure:**
- **Multiple states** with different rules
- **State transitions** based on actions
- **Coordination challenges** between players

**Your Agent:**
```python
class MyFSMAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.current_state = "initial"
        self.state_memory = {}
    
    def get_action(self, observation):
        # Use current state to choose action
        # Update state based on results
        pass
```

### Lab 03: Q-Learning

**What you learn:** Reinforcement learning, exploration vs exploitation

**Game Structure:**
- **Repeated interactions** with the same opponent
- **State-based observations** (previous actions)
- **Learning opportunities** across many rounds

**Your Agent:**
```python
class MyQLearningAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.q_table = {}  # State -> Action -> Value
    
    def get_action(self, observation):
        # Use Q-table to choose best action
        # Maybe explore sometimes (epsilon-greedy)
        pass
    
    def update(self, reward, info):
        # Update Q-table based on experience
        # Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        pass
```

### Lab 04: Spatial Games (Lemonade Stand)

**What you learn:** Spatial competition, location-based strategies

**Game Structure:**
- **Multiple locations** to choose from
- **Spatial competition** with other players
- **Customer distribution** affects profits

**Your Agent:**
```python
class MyLemonadeAgent(BaseAgent):
    def get_action(self, observation):
        # Choose which location to set up shop
        # Consider where opponents are
        # Think about customer flow
        pass
```

### Lab 06: Auctions

**What you learn:** Auction theory, bidding strategies, mechanism design

**Game Structure:**
- **Multiple items** to bid on
- **Valuation functions** for each player
- **Auction mechanisms** determine winners and payments

**Your Agent:**
```python
class MyAuctionAgent(BaseAgent):
    def get_action(self, observation):
        # Calculate your valuation for items
        # Decide how much to bid
        # Consider other bidders' likely strategies
        pass
```

## Key Concepts for Success

### 1. Observation Structure

Observations tell you what's happening in the game:

```python
# Matrix games (Lab 01-03)
observation = {}  # Often empty - you know the game structure

# Spatial games (Lab 04)  
observation = {
    "locations": [0, 1, 2, 3],  # Available locations
    "opponent_positions": [1, 3],  # Where opponents are
    "customer_distribution": {...}  # Customer flow info
}

# Auctions (Lab 06)
observation = {
    "items": [{"id": 1, "value": 10}, {"id": 2, "value": 15}],
    "my_valuations": [8, 12],  # Your values for items
    "bidding_history": [...]  # Previous bids
}
```

### 2. Action Formats

Different games expect different action types:

```python
# Matrix games
action = 0  # Integer representing action (0=Rock, 1=Paper, 2=Scissors)

# Spatial games  
action = 2  # Integer representing location (0-3 for 4 locations)

# Auctions
action = [5, 8]  # List of bids for each item
```

### 3. Learning Patterns

**Fictitious Play (Lab 01):**
```python
def get_action(self, observation):
    # Track opponent's action frequencies
    # Choose best response to their most likely action
    pass
```

**Q-Learning (Lab 03):**
```python
def get_action(self, observation):
    state = self.get_state_key(observation)
    if random.random() < self.epsilon:  # Explore
        return random.choice(self.legal_actions)
    else:  # Exploit
        return self.get_best_action(state)

def update(self, reward, info):
    # Update Q-table based on experience
    # Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
    pass
```

**Reinforcement Learning (Lab 04):**
```python
def get_action(self, observation):
    # Use policy network or value function
    # Consider spatial dynamics
    # Balance exploration and exploitation
    pass
```

## Common Patterns and Best Practices

### 1. State Management

Always track what you need to know:

```python
class MyAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.opponent_history = []  # Track opponent actions
        self.my_history = []        # Track my actions
        self.round_count = 0        # Track game progress
    
    def reset(self):
        super().reset()
        self.opponent_history = []
        self.my_history = []
        self.round_count = 0
```

### 2. Learning from Experience

Use the `update` method to learn:

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Store this experience
    self.my_history.append(self.get_last_action())
    
    # Learn from opponent's action (if available)
    if 'opponent_action' in info:
        self.opponent_history.append(info['opponent_action'])
    
    # Update your strategy based on new information
    self.update_strategy()
```

### 3. Exploration vs Exploitation

Balance trying new things with using what works:

```python
def get_action(self, observation):
    if self.round_count < 10:  # Early game: explore
        return self.explore_action()
    else:  # Later game: exploit
        return self.exploit_action()
```

## Debugging and Testing

### 1. Local Testing

Test your agent locally before submitting:

```python
# Test against a simple opponent
from core.agents.lab01.random_agent import RandomAgent

my_agent = MyAgent("TestAgent")
opponent = RandomAgent("Random")
engine = Engine(RPSGame(), [my_agent, opponent], rounds=100)

results = engine.run()
print(f"My agent score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### 2. Understanding Observations

Print observations to understand the game state:

```python
def get_action(self, observation):
    print(f"Observation: {observation}")
    # Your strategy here
    pass
```

### 3. Tracking Performance

Monitor how your agent is doing:

```python
def update(self, reward, info):
    super().update(reward, info)
    
    # Track performance
    if len(self.reward_history) % 10 == 0:
        recent_rewards = self.reward_history[-10:]
        avg_reward = sum(recent_rewards) / len(recent_rewards)
        print(f"Average reward over last 10 rounds: {avg_reward}")
```

## Next Steps

Now that you understand the structure:

1. **Start with Lab 01** - Implement a simple agent for matrix games
2. **Read the specific lab documentation** - Each lab has detailed requirements
3. **Experiment locally** - Test your agents before submitting
4. **Learn from competition** - See how other students approach the same problems
5. **Iterate and improve** - Use what you learn to build better agents

The beauty of this system is that you can focus on the **strategy and learning algorithms** while the infrastructure handles all the game management, networking, and tournament organization. Happy coding! 