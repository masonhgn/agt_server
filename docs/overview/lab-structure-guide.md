# Understanding the AGT Lab Structure

Welcome to the Algorithmic Game Theory (AGT) lab system! This guide provides a comprehensive overview of how the system works, from the fundamental building blocks to how everything comes together to create learning experiences.

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

Agents are **intelligent players** that make decisions. Every agent inherits from `BaseAgent`:

```python
class BaseAgent(ABC):
    def get_action(self, observation) -> Any:  # Strategy implementation
    def update(self, reward, info):            # Learn from results
    def reset(self):                           # Start fresh
```

**The Three Key Methods:**

1. **`get_action(observation)`** - This is where intelligence lives!
   - Receives the current game state
   - Returns the chosen action
   - This is where strategies are implemented

2. **`update(reward, info)`** - Learning from experience
   - Called after each action with the result
   - Used to update strategies
   - Stores information for future decisions

3. **`reset()`** - Fresh start
   - Called when starting a new game
   - Clears any game-specific state
   - Prepares for a new competition

### 5. Server (AGTServer)

The **AGTServer** manages the distributed system:
- Handles client connections
- Coordinates game sessions
- Manages tournaments
- Collects and stores results

```python
class AGTServer:
    def handle_client(self, reader, writer):  # Handle new connections
    def start_game(self, game_type):          # Initialize games
    def run_tournament(self):                 # Manage competitions
```

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

**Learning Focus:** Basic game theory, Nash equilibria, best responses

**Game Structure:**
- **One stage** that repeats for many rounds
- **Two players** making simultaneous moves
- **Payoff matrix** defines rewards for each action combination

### Lab 02: Finite State Machines

**Learning Focus:** State machines, coordination, repeated games

**Game Structure:**
- **Multiple states** with different rules
- **State transitions** based on actions
- **Coordination challenges** between players

### Lab 03: Q-Learning

**Learning Focus:** Reinforcement learning, exploration vs exploitation

**Game Structure:**
- **Repeated interactions** with the same opponent
- **State-based observations** (previous actions)
- **Learning opportunities** across many rounds

### Lab 04: Spatial Games (Lemonade Stand)

**Learning Focus:** Spatial competition, location-based strategies

**Game Structure:**
- **Multiple locations** to choose from
- **Spatial competition** with other players
- **Customer distribution** affects profits

### Lab 06: Auctions

**Learning Focus:** Auction theory, bidding strategies, mechanism design

**Game Structure:**
- **Multiple items** to bid on
- **Valuation functions** for each player
- **Auction mechanisms** determine winners and payments

## Key Concepts for Understanding

### 1. Observation Structure

Observations tell agents what's happening in the game:

```python
# Matrix games (Lab 01-03)
observation = {}  # Often empty - agents know the game structure

# Spatial games (Lab 04)  
observation = {
    "locations": [0, 1, 2, 3],  # Available locations
    "opponent_positions": [1, 3],  # Where opponents are
    "customer_distribution": {...}  # Customer flow info
}

# Auctions (Lab 06)
observation = {
    "items": [{"id": 1, "value": 10}, {"id": 2, "value": 15}],
    "my_valuations": [8, 12],  # Agent's values for items
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

## System Architecture

### Component Interactions

```
Students → Agents → Engine → Games → Stages
    ↓
Server ← Results ← Engine ← Games
    ↓
Administrators → Server → Tournaments → Results
```

### Data Flow

```
Client Request → Server Validation → Game Engine → Agent Processing → Game Logic → Result Calculation → Response to Client
```

### Error Handling

The system handles various error conditions:
- **Timeouts**: Use default actions and continue
- **Invalid Actions**: Reject and request new actions
- **Connection Loss**: Disconnect player and notify others
- **Game Errors**: End game early and save partial results

## Next Steps

This overview provides the foundation for understanding the AGT system. From here:

- **Students** should proceed to the "For Students" section to learn how to create and run agents
- **Administrators** should proceed to the "For Administrators" section to learn how to manage the system
- **Developers** can explore the API Reference for technical implementation details

The beauty of this system is that it provides a consistent interface for learning game theory concepts while handling all the complex infrastructure behind the scenes. 