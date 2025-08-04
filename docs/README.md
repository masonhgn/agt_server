# AGT Server Documentation

Welcome to the Algorithmic Game Theory (AGT) Server documentation. This system provides a modern implementation of game theory lab competitions for educational purposes.

## Documentation Versions

- **Online**: [ReadTheDocs](https://agt-server.readthedocs.io/) - Full documentation with search and navigation
- **Local**: This directory contains the source files for building documentation locally

## Quick Navigation

- [System Overview](#system-overview) - High-level architecture
- [Core Components](#core-components) - Detailed component breakdown
- [Game Types](#game-types) - Available games and their mechanics
- [Agent System](#agent-system) - Agent implementations and learning strategies
- [Execution Flow](#execution-flow) - How the system runs
- [Development Guide](#development-guide) - How to extend the system

---

## System Overview

The AGT Server is a distributed system that enables students to implement game theory agents and compete in various game scenarios.

For detailed architecture diagrams, see [System Architecture](diagrams/architecture.md).

The system follows a layered architecture:
- **Client Layer**: Student clients connecting to the server
- **Server Layer**: AGTServer and Engine components
- **Game Layer**: Various game implementations (RPS, BOS, Chicken, etc.)
- **Agent Layer**: Different learning strategies and agent types

---

## Core Components

### Server Architecture

The main server components and their responsibilities:

- **AGTServer**: Client connection management, game session coordination
- **Engine**: Game execution, action collection, reward distribution
- **BaseGame**: Game state management, rule enforcement
- **BaseAgent**: Action selection, learning, state tracking
- **Stage**: Multi-phase game management

For detailed component diagrams, see [System Architecture](diagrams/architecture.md).

---

## Game Types

### Matrix Games (Lab01)

Simple two-player matrix games with payoff matrices:
- **Rock Paper Scissors**: Classic zero-sum game
- **Battle of the Sexes**: Coordination game
- **Chicken Game**: Conflict resolution game

### Spatial Games (Lab04)

Location-based games with spatial competition:
- **Lemonade Stand**: Location choice with customer flow
- **Spatial Competition**: Strategic positioning games

### Auction Games (Lab06)

Bidding and auction mechanisms:
- **Combinatorial Auctions**: Multi-item bidding
- **Marginal Value Bidding**: Value-based strategies

For detailed game diagrams, see [Game System](diagrams/game-system.md).

---

## Agent System

### Learning Strategies

Different agent types implement various learning approaches:

- **Q-Learning (Lab03)**: Reinforcement learning for repeated games
- **Fictitious Play (Lab01)**: Belief-based learning for matrix games
- **Random**: Baseline strategy for comparison
- **Stubborn**: Fixed strategy for testing

### Lab-Specific Agents

- **Lab01**: Basic game theory agents (Rock, Paper, Scissors, Random, Stubborn)
- **Lab02**: Finite state machine agents for BOS
- **Lab03**: Q-learning agents for Chicken game
- **Lab04**: Reinforcement learning for Lemonade stand
- **Lab06**: Auction bidding strategies

For detailed agent diagrams, see [Agent System](diagrams/agent-system.md).

---

## Execution Flow

### Game Session Flow

The typical flow of a game session involves:
1. Client connection and game joining
2. Game initialization and setup
3. Multiple rounds of action collection and execution
4. Result calculation and agent updates
5. Game completion and result reporting

### Tournament Management

Tournaments are managed through:
1. Player matching and game creation
2. Multiple game execution
3. Result collection and aggregation
4. Ranking calculation and result storage

For detailed flow diagrams, see [Execution Flow](diagrams/execution-flow.md).

---

## Development Guide

### Adding New Games

To add a new game type:

1. Create Game Class: Inherit from `BaseGame`
2. Implement Interface: `reset()`, `step()`, `players_to_move()`
3. Add Configuration: Update server configs
4. Create Tests: Add test cases
5. Update Documentation: Document game mechanics

### Adding New Agents

To add a new agent type:

1. Create Agent Class: Inherit from `BaseAgent`
2. Implement Methods: `get_action()`, `update()`, `reset()`
3. Add to Registry: Register in agent factory
4. Create Tests: Add test cases
5. Document Strategy: Explain learning approach

### System Extension Points

The system is designed to be extensible at several points:
- **New Game Types**: Implement BaseGame interface
- **New Agent Types**: Implement BaseAgent interface
- **New Learning Algorithms**: Extend existing agent classes
- **New Tournament Formats**: Modify tournament logic
- **New Communication Protocols**: Extend server communication

---

## File Structure

```
agt_server_new/
├── core/                    # Core game engine
│   ├── agents/             # Agent implementations
│   ├── game/               # Game implementations
│   ├── stage/              # Game stage management
│   └── engine.py           # Main game engine
├── server/                 # Server implementation
│   ├── configs/            # Game configurations
│   └── server.py           # Main server
├── stencils/               # Student assignments
├── tests/                  # Test suite
└── docs/                   # Documentation
    ├── README.md           # This file
    ├── conf.py             # Sphinx configuration
    ├── index.rst           # Main documentation index
    ├── Makefile            # Build automation
    ├── requirements-docs.txt # Documentation dependencies
    └── diagrams/           # Detailed diagrams
        ├── architecture.md  # System architecture
        ├── game-system.md   # Game system details
        ├── agent-system.md  # Agent system details
        └── execution-flow.md # Execution flow details
```

---

## Building Documentation Locally

### Prerequisites

```bash
pip install -r docs/requirements-docs.txt
```

### Build Commands

```bash
# Build HTML documentation
cd docs
make html

# Serve documentation locally
make serve

# Build PDF documentation
make pdf

# Check links
make linkcheck

# Check spelling
make spelling
```

### Development

```bash
# Start development server with auto-reload
make dev

# Watch for changes and rebuild
make watch
```

---

## ReadTheDocs Setup

### Automatic Deployment

1. **Connect to ReadTheDocs**:
   - Go to [readthedocs.org](https://readthedocs.org/)
   - Import your GitHub repository
   - Configure build settings

2. **Build Configuration**:
   - **Documentation Type**: Sphinx
   - **Python Interpreter**: 3.9
   - **Requirements File**: `docs/requirements-docs.txt`
   - **Conf File**: `docs/conf.py`

3. **Custom Build Commands**:
   ```bash
   pip install -r docs/requirements-docs.txt
   cd docs
   make html
   ```

### Manual Deployment

```bash
# Install documentation dependencies
pip install -r docs/requirements-docs.txt

# Build documentation
cd docs
make html

# Deploy to GitHub Pages (if configured)
make github
```

---

## Quick Start

1. Install Dependencies: `pip install -r requirements.txt`
2. Start Server: `python server/server.py`
3. Connect Client: Use provided client stencils
4. Run Tests: `python -m pytest tests/`

For detailed setup instructions, see the individual lab documentation in the `stencils/` directory.

## Contributing to Documentation

1. **Edit source files** in the `docs/` directory
2. **Build locally** to test changes: `make html`
3. **Submit pull request** with documentation improvements
4. **ReadTheDocs** will automatically build and deploy

For more information, see the [Contributing Guide](contributing.md). 