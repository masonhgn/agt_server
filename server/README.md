# agt server

a modern, scalable server for running algorithmic game theory lab competitions.

## overview

the agt server provides a centralized platform for students to compete their algorithmic agents in various game theory scenarios. it supports all lab games including rock paper scissors, battle of the sexes, chicken games, lemonade stand, and auctions.

## features

- **multi-game support**: run all lab games on a single server
- **real-time competition**: students can connect and compete in real-time
- **flexible configuration**: restrict games by lab or allow all games
- **comprehensive logging**: detailed logs for debugging and analysis
- **easy integration**: simple client library for connecting agents
- **stencil compatibility**: adapters for all lab stencils

## quick start

### running the server

```bash
# run with all games available
python server.py

# restrict to specific lab
python server.py --game rps
python server.py --config configs/lab01_rps.json

# restrict to multiple games
python server.py --games rps bos chicken
```

### connecting an agent

```python
from server.client import AGTAgent, AGTClient

class MyAgent(AGTAgent):
    def get_action(self, observation):
        # implement your agent logic here
        return 0

# connect to server
client = AGTClient(MyAgent("MyAgent"), "localhost", 8080)
await client.connect()
await client.join_game("rps")
await client.run()
```

### using stencils

```python
from server.adapters import create_adapter
from lab01_stencil.fictitious_play import agent_submission

# create adapter for your stencil
agent = create_adapter(agent_submission, "rps")

# connect to server
client = AGTClient(agent, "localhost", 8080)
await client.connect()
await client.join_game("rps")
await client.run()
```

## server architecture

### message protocol

the server uses a simple json-based message protocol:

**client to server:**
- `provide_device_id` - send device identifier
- `provide_name` - send agent name
- `join_game` - request to join a game
- `provide_action` - send game action
- `ready_next_round` - ready for next round

**server to client:**
- `request_device_id` - request device id
- `request_name` - request agent name
- `connection_established` - confirm connection
- `game_start` - game is starting
- `request_action` - request action for current round
- `round_result` - results from last round
- `game_end` - game has ended

### adapter system

the adapter system converts between stencil interfaces and server format:

- **rpsadapter**: converts rps agent interface to server format
- **bosadapter**: converts bos agent interface to server format
- **bosiiadapter**: converts bosii agent interface to server format
- **chickenadapter**: converts chicken agent interface to server format
- **lemonadeadapter**: converts lemonade agent interface to server format
- **auctionadapter**: converts auction agent interface to server format

## troubleshooting

### common issues

1. **connection refused**
   - make sure the server is running
   - check host and port settings
   - ensure firewall allows connections

2. **stencil not found**
   - verify the stencil file path is correct
   - make sure the stencil has `agent_submission` defined
   - check that the stencil is compatible with the game type

3. **game not starting**
   - ensure enough players have joined
   - check that all players are connected
   - verify game type is supported

4. **agent errors**
   - check that the agent implements the correct interface
   - verify the agent returns valid actions
   - look for exceptions in the agent code

### debug mode

enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.debug)
```

## security considerations

- the server accepts connections from any ip by default
- consider using a firewall for production deployments
- validate all incoming messages
- implement rate limiting if needed

## performance

- the server can handle multiple concurrent games
- each game runs in its own asyncio task
- results are saved asynchronously
- memory usage scales with number of connected players

## future enhancements

potential improvements for the server system:

1. **web interface**: add a web dashboard for monitoring games
2. **tournament mode**: support for tournament brackets
3. **replay system**: save and replay game histories
4. **leaderboards**: track player performance over time
5. **authentication**: add user authentication system
6. **spectator mode**: allow watching games without participating 