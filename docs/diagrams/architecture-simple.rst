# System Architecture (Simple)

## High-Level Architecture

The AGT Server follows a layered architecture pattern with clear separation of concerns.

### System Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  Student Client 1  │  Student Client 2  │  Student Client N │
└────────────────────┼─────────────────────┼──────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVER LAYER                            │
├─────────────────────────────────────────────────────────────┤
│                    AGTServer                               │
│                         │                                  │
│                         ▼                                  │
│                      Engine                                │
└─────────────────────────┼──────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     GAME LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  RPS Game  │  BOS Game  │  Chicken Game  │  Lemonade Game  │
└────────────┼────────────┼────────────────┼────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LAYER                             │
├─────────────────────────────────────────────────────────────┤
│ Q-Learning │ Fictitious Play │ Random Agent │ Custom Agent │
└────────────┼─────────────────┼──────────────┼──────────────┘
```

### Data Flow

```
Client Request → Server Validation → Game Engine → Agent Processing → Game Logic → Result Calculation → Response to Client
```

### Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| AGTServer | Client connection management, game session coordination |
| Engine | Game execution, action collection, reward distribution |
| BaseGame | Game state management, rule enforcement |
| BaseAgent | Action selection, learning, state tracking |
| Stage | Multi-phase game management |

## Server Components

### AGTServer Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        AGTServer                           │
├─────────────────────────────────────────────────────────────┤
│  Connection Manager → Game Manager → Player Manager → Results Manager │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                         Engine                             │
├─────────────────────────────────────────────────────────────┤
│  Game Coordinator → Action Collector → Reward Distributor  │
└─────────────────────────────────────────────────────────────┘
```

### Game Hierarchy

```
BaseGame (Abstract)
├── RPSGame
├── BOSGame
├── BOSIIGame
├── ChickenGame
├── LemonadeGame
├── AuctionGame
├── AdxOneDayGame
└── AdxTwoDayGame

Interface Methods:
├── reset()
├── step()
└── players_to_move()
```

### Agent Hierarchy

```
BaseAgent (Abstract)
├── QLearningAgent
├── FictitiousPlayAgent
├── RandomAgent
├── StubbornAgent
└── CompromiseAgent

Interface Methods:
├── get_action()
├── update()
└── reset()
``` 