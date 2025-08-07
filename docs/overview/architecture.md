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