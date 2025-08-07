# System Architecture

This page provides a comprehensive overview of how the AGT system works, from the high-level components down to the detailed interactions.

## System Overview

The AGT system is a distributed game engine that enables students to create intelligent agents and compete in various game theory scenarios.

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

### 1. Game Session Flow
```
Client Connect → Server Validation → Game Initialization → 
Round Loop: [Collect Actions → Process Game → Distribute Results] → 
Game Complete → Results Collection
```

### 2. Agent Interaction Flow
```
Agent receives observation → Agent chooses action → 
Engine collects all actions → Game processes actions → 
Engine distributes rewards → Agent learns from experience
```

### 3. Tournament Flow
```
Tournament Start → Match Players → Run Games → 
Collect Results → Calculate Rankings → Save Results
```

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

## System Benefits

### For Students
- **Focus on strategy** - Infrastructure handled by system
- **Real-time competition** - Compete against other students
- **Immediate feedback** - See results instantly
- **Iterative improvement** - Learn from experience

### For Instructors
- **Centralized management** - Control all competitions
- **Automated evaluation** - System tracks performance
- **Scalable deployment** - Handle many students
- **Rich analytics** - Detailed performance data

### For Researchers
- **Standardized environment** - Consistent experimental setup
- **Reproducible results** - Deterministic game execution
- **Extensible platform** - Easy to add new games/agents
- **Rich data collection** - Comprehensive logging

## Next Steps

This architecture enables:
- **Students** to focus on implementing intelligent agents
- **Instructors** to manage competitions effectively
- **Researchers** to conduct experiments at scale

The modular design ensures that each component can be developed, tested, and improved independently while maintaining a cohesive system. 