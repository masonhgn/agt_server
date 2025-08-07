# System Overview

Welcome to the Algorithmic Game Theory (AGT) system! This page provides a comprehensive overview of how the system works, from the high-level architecture down to the detailed interactions that enable students to learn game theory through hands-on experience.

## High-Level Architecture

The AGT system is a distributed game engine that enables students to create intelligent agents and compete in various game theory scenarios. The system follows a layered architecture where each layer has specific responsibilities and communicates with adjacent layers through well-defined interfaces.

```
┌─────────────────────────────────────────────────────────────┐
│                    STUDENT CLIENTS                          │
├─────────────────────────────────────────────────────────────┤
│  Student 1  │  Student 2  │  Student 3  │  Student N     │
│  Agent      │  Agent      │  Agent      │  Agent         │
└────────────────────┼─────────────────────┼──────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      AGT SERVER                            │
├─────────────────────────────────────────────────────────────┤
│  Connection Manager → Game Manager → Results Manager       │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       GAME ENGINE                          │
├─────────────────────────────────────────────────────────────┤
│  Game Coordinator → Action Collector → Reward Distributor  │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        GAME LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  RPS Game  │  BOS Game  │  Chicken Game  │  Lemonade Game │
└────────────┼────────────┼────────────────┼────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                       STAGE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  Matrix Stage  │  Spatial Stage  │  Auction Stage        │
└────────────────┼─────────────────┼────────────────────────┘
```

The architecture diagram illustrates how the system scales from individual student agents to a centralized server that manages all game execution. Student agents connect to the server over the network, which coordinates game sessions and manages the overall competition. The game engine handles the core game logic, while the game layer provides different game types and the stage layer breaks complex games into manageable phases.

## Core Components

### Student Clients
Student clients run on individual student machines and contain the intelligent agents that students implement. Each agent must implement three core methods: `get_action()` to choose actions based on observations, `update()` to learn from rewards and feedback, and `reset()` to prepare for new games. Agents connect to the server over TCP sockets and communicate in real-time during games, sending their chosen actions and receiving game state updates and rewards.

### AGT Server
The AGT Server acts as the central coordination hub, running on the instructor's machine and managing all game sessions and tournaments. It handles client connections, coordinates game sessions between multiple students, manages tournament brackets and matchmaking, and collects and stores all competition results. The server communicates with student agents through TCP connections and orchestrates the game engine to execute actual game logic.

### Game Engine
The Game Engine is the core execution unit that manages individual game sessions. It collects actions from all participating agents, executes the game logic by calling the appropriate game implementation, distributes rewards and new observations back to agents, and tracks game progress and completion. The engine ensures all agents are synchronized and maintains consistent game state throughout each session.

### Game Layer
The Game Layer contains the actual game implementations that define the rules, mechanics, and payoff structures for different game types. Each game (RPS, BOS, Chicken, Lemonade, Auctions) implements a standard interface with methods for resetting the game state, processing player actions, calculating rewards, and determining when the game is complete. Games can contain multiple stages for complex scenarios like auctions.

### Stage Layer
The Stage Layer breaks complex games into manageable phases or rounds. Simple games like matrix games use a single stage that repeats, while complex games like auctions use multiple stages with different rules and objectives. Each stage processes actions for the current phase, manages state transitions between phases, and handles phase-specific logic and reward calculations.

## Key Interfaces

### Agent Interface
```python
class BaseAgent:
    def get_action(self, observation: Dict[str, Any]) -> Any
    def update(self, reward: float, info: Dict[str, Any]) -> None
    def reset(self) -> None
```

### Game Interface
```python
class BaseGame:
    def reset(self, seed: int | None = None) -> ObsDict
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]
    def players_to_move(self) -> List[PlayerId]
```

### Stage Interface
```python
class BaseStage:
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]
    def legal_actions(self, player: PlayerId) -> Any
    def is_done(self) -> bool
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

## Data Flow

The system processes data through several key flows, each serving a specific purpose in the overall game execution.

### 1. Game Session Flow
```
Client Connect → Server Validation → Game Initialization → 
Round Loop: [Collect Actions → Process Game → Distribute Results] → 
Game Complete → Results Collection
```

The game session flow shows the complete lifecycle of a single game, from initial connection through multiple rounds of play to final results collection. This flow ensures that all players are properly synchronized and that game state is maintained consistently throughout the session.

### 2. Agent Interaction Flow
```
Agent receives observation → Agent chooses action → 
Engine collects all actions → Game processes actions → 
Engine distributes rewards → Agent learns from experience
```

The agent interaction flow represents the core learning loop that enables agents to improve over time. Each iteration of this flow allows agents to observe the game state, make decisions, and learn from the outcomes of their actions.

### 3. Tournament Flow
```
Tournament Start → Match Players → Run Games → 
Collect Results → Calculate Rankings → Save Results
```

The tournament flow manages the higher-level competition structure, coordinating multiple games between different players and aggregating results to determine overall rankings and performance metrics.

## Lab-Specific Patterns

### Lab 01: Matrix Games (RPS, BOS, Chicken)

**Learning Focus:** Basic game theory, Nash equilibria, best responses

**Game Structure:**
- **One stage** that repeats for many rounds
- **Two players** making simultaneous moves
- **Payoff matrix** defines rewards for each action combination

**Observation Structure:**
```python
observation = {}  # Often empty - agents know the game structure
```

**Action Format:**
```python
action = 0  # Integer representing action (0=Rock, 1=Paper, 2=Scissors)
```

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

**Learning Pattern:**
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

### Lab 04: Spatial Games (Lemonade Stand)

**Learning Focus:** Spatial competition, location-based strategies

**Game Structure:**
- **Multiple locations** to choose from
- **Spatial competition** with other players
- **Customer distribution** affects profits

**Observation Structure:**
```python
observation = {
    "locations": [0, 1, 2, 3],  # Available locations
    "opponent_positions": [1, 3],  # Where opponents are
    "customer_distribution": {...}  # Customer flow info
}
```

**Action Format:**
```python
action = 2  # Integer representing location (0-3 for 4 locations)
```

### Lab 06: Auctions

**Learning Focus:** Auction theory, bidding strategies, mechanism design

**Game Structure:**
- **Multiple items** to bid on
- **Valuation functions** for each player
- **Auction mechanisms** determine winners and payments

**Observation Structure:**
```python
observation = {
    "items": [{"id": 1, "value": 10}, {"id": 2, "value": 15}],
    "my_valuations": [8, 12],  # Agent's values for items
    "bidding_history": [...]  # Previous bids
}
```

**Action Format:**
```python
action = [5, 8]  # List of bids for each item
```

## Key Concepts for Understanding

### 1. Observation Structure

Observations tell agents what's happening in the game. The structure varies by lab:

- **Matrix games (Lab 01-03)**: Often empty observations since agents know the game structure
- **Spatial games (Lab 04)**: Include location information and opponent positions
- **Auctions (Lab 06)**: Include item valuations and bidding history

### 2. Action Formats

Different games expect different action types:

- **Matrix games**: Integer representing action choice
- **Spatial games**: Integer representing location choice
- **Auctions**: List of bids for each item

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

## Component Interactions

```
Students → Agents → Engine → Games → Stages
    ↓
Server ← Results ← Engine ← Games
    ↓
Administrators → Server → Tournaments → Results
```

## Error Handling

The system handles various error conditions:
- **Timeouts**: Use default actions and continue
- **Invalid Actions**: Reject and request new actions
- **Connection Loss**: Disconnect player and notify others
- **Game Errors**: End game early and save partial results

## Next Steps

This overview provides the foundation for understanding the AGT system. From here:

- **Students** should proceed to the "For Students" section to learn how to create and run agents
- **Administrators** should proceed to the "For Administrators" section to learn how to manage the system

The beauty of this system is that it provides a consistent interface for learning game theory concepts while handling all the complex infrastructure behind the scenes. 