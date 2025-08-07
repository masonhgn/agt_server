# System Architecture

This page provides a comprehensive overview of how the AGT system works, from the high-level components down to the detailed interactions.

## System Overview

The AGT system is a distributed game engine that enables students to create intelligent agents and compete in various game theory scenarios. The system follows a layered architecture where each layer has specific responsibilities and communicates with adjacent layers through well-defined interfaces.

The diagram below shows the complete system architecture, from student clients at the top down to the stage layer at the bottom. Each layer builds upon the layers below it, creating a modular and extensible system.

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

### 1. Student Clients
**Purpose:** Where students implement their agents
- **Location:** Student machines
- **Responsibility:** Implement intelligent decision-making
- **Interface:** Three required methods (`get_action`, `update`, `reset`)

### 2. AGT Server
**Purpose:** Central coordination and management
- **Location:** Instructor/TA machine
- **Responsibilities:**
  - Handle client connections
  - Coordinate game sessions
  - Manage tournaments
  - Collect and store results

### 3. Game Engine
**Purpose:** Execute game logic and manage state
- **Location:** Server
- **Responsibilities:**
  - Collect actions from all agents
  - Execute game logic
  - Distribute rewards and observations
  - Track game progress

### 4. Game Layer
**Purpose:** Define game rules and mechanics
- **Types:** Matrix games, spatial games, auctions
- **Responsibilities:**
  - Define game rules
  - Calculate payoffs
  - Manage game state
  - Determine game completion

### 5. Stage Layer
**Purpose:** Break complex games into manageable phases
- **Types:** Single stage (matrix games), multi-stage (auctions)
- **Responsibilities:**
  - Process actions for current phase
  - Manage state transitions
  - Handle phase-specific logic

## Data Flow

The system processes data through several key flows, each serving a specific purpose in the overall game execution. Understanding these flows helps clarify how information moves through the system and how different components interact.

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

## Component Interactions

### Student Agent ↔ Server
- **Connection:** TCP socket connection
- **Messages:** Join game, get action, send action, receive results
- **Frequency:** Real-time during games

### Server ↔ Game Engine
- **Interface:** Direct method calls
- **Data:** Game state, actions, results
- **Timing:** Synchronous during game execution

### Game Engine ↔ Games
- **Interface:** Standard game interface
- **Methods:** `reset()`, `step()`, `players_to_move()`
- **Data:** Game state, actions, rewards

### Games ↔ Stages
- **Relationship:** Games contain stages
- **Interface:** Stage interface
- **Methods:** `step()`, `legal_actions()`, `is_done()`

## System Characteristics

### Scalability
- **Multiple clients** can connect simultaneously
- **Concurrent games** run independently
- **Tournament mode** supports many players

### Reliability
- **Error handling** for client disconnections
- **Timeout mechanisms** for unresponsive agents
- **State persistence** for interrupted games

### Extensibility
- **Modular design** allows easy addition of new games
- **Standard interfaces** enable new agent types
- **Configuration-driven** game parameters

## Key Interfaces

### Agent Interface
```python
class BaseAgent:
    def get_action(self, observation) -> Any
    def update(self, reward, info) -> None
    def reset(self) -> None
```

### Game Interface
```python
class BaseGame:
    def reset(self) -> ObsDict
    def step(self, actions) -> Tuple[ObsDict, RewardDict, bool, InfoDict]
    def players_to_move(self) -> List[PlayerId]
```

### Stage Interface
```python
class BaseStage:
    def step(self, actions) -> Tuple[ObsDict, RewardDict, bool, InfoDict]
    def legal_actions(self, player) -> Any
    def is_done(self) -> bool
```

## Next Steps

This architecture enables:
- **Students** to focus on implementing intelligent agents
- **Instructors** to manage competitions effectively
- **Researchers** to conduct experiments at scale

The modular design ensures that each component can be developed, tested, and improved independently while maintaining a cohesive system. 