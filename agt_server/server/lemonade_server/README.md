# Lemonade Competition Server

## Why Separate Infrastructure?

The lemonade lab requires fundamentally different architecture than short-form labs:

### Current System (Short-form Labs)
- **Real-time client connections** - Students run agents locally and connect via network
- **Immediate results** - Tournaments run in single sessions (<1 hour)
- **Session-based** - Server starts/stops with each lab session
- **Dashboard integration** - Tightly coupled with real-time dashboard

### Lemonade Lab Requirements
- **File submissions** - Students submit agent code files, not network connections
- **Multi-day competitions** - Tournaments run continuously over several days
- **Batch execution** - Server loads and runs all agents together
- **External leaderboard** - Results pushed to separate leaderboard system
- **Persistent operation** - Server runs continuously, processing new submissions

## How It Works

### Directory Structure
```
server/lemonade_server/
├── lemonade_competition.py  # Main competition logic
├── lemonade_web.py          # Web interface
├── leaderboard_pusher.py    # Push results to external leaderboard
├── run_server.py           # Start the server
├── agents/                 # Directory for agent submissions
└── results/                # Tournament results
```

### Agent Submission Format
Students submit Python files to the `agents/` directory with format:
```
student_id_agent_name.py
```

Example: `alice_smart_agent.py`, `bob_random_agent.py`

Each file must contain:
```python
from core.agents.common.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def get_action(self, observation):
        # Your agent logic here
        return position  # 0-11
    
    def update(self, reward, info):
        # Update agent state
        pass

# Required export
agent_submission = MyAgent("MyAgentName")
```

## Usage

### 1. Start the server
```bash
cd server/lemonade_server
python run_server.py
```

### 2. Submit agents
Students place their agent files in the `agents/` directory. The server automatically detects new files.

### 3. Run tournaments
- Web interface: http://localhost:8083
- Click "Scan for New Agents" to detect new submissions
- Click "Run Tournament" to execute competitions
- Click "Push to Leaderboard" to send results to external system

### 4. Automatic operation
The server can be configured to:
- Automatically scan for new agents every few minutes
- Run tournaments on a schedule (e.g., every 6 hours)
- Push results to leaderboard automatically

## Benefits of Separate Infrastructure

1. **No risk to existing labs** - Current system remains unchanged
2. **Clean separation** - Each system optimized for its use case
3. **Independent deployment** - Can run on different servers/schedules
4. **Simpler maintenance** - Each system does one thing well
5. **Future flexibility** - Can evolve independently

## Integration with Existing Code

The lemonade server reuses existing components:
- `core/game/LemonadeGame.py` - Game logic
- `core/engine.py` - Game execution engine
- `server/adapters.py` - Agent adapters
- `core/agents/common/base_agent.py` - Base agent class

This minimizes code duplication while maintaining clean separation of concerns.
