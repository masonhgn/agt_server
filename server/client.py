#!/usr/bin/env python3
"""
agt client library

this library allows students to connect their completed stencils to the agt server
for competitions and testing.
"""

import asyncio
import json
import socket
import time
import argparse
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class AGTAgent(ABC):
    """base class for agt agents that can connect to the server."""
    
    def __init__(self, name: str):
        self.name = name
        # Use more unique device ID with microseconds and random component
        import random
        self.device_id = f"{name}_{int(time.time() * 1000000)}_{random.randint(1000, 9999)}"
        self.game_type: Optional[str] = None
        self.current_round = 0
        self.total_reward = 0
        self.game_history = []
    
    @abstractmethod
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """
        get the agent's action based on the current observation.
        
        args:
            observation: game state information
            
        returns:
            the action to take
        """
        pass
    
    def reset(self):
        """reset the agent for a new game."""
        self.current_round = 0
        self.total_reward = 0
        self.game_history = []
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the agent with reward and info from the last action."""
        self.total_reward += reward
        self.current_round += 1
        self.game_history.append({
            "round": self.current_round,
            "reward": reward,
            "info": info
        })


class AGTClient:
    """client for connecting to the agt server."""
    
    def __init__(self, agent: AGTAgent, host: str = "localhost", port: int = 8080):
        self.agent = agent
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.connected = False
        self.should_exit = False  # Add exit flag
    
    async def connect(self):
        """connect to the agt server."""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.connected = True
            print(f"connected to agt server at {self.host}:{self.port}")
            
            # handle initial handshake
            await self.handle_connection()
            
        except Exception as e:
            print(f"failed to connect to server: {e}")
            self.connected = False
    
    async def handle_connection(self):
        """handle the initial connection handshake."""
        print("debug: starting connection handshake...")

        # wait for request_device_id
        msg = await self.receive_message()
        print(f"debug: received (expect request_device_id): {msg}")
        if not msg or msg.get("message") != "request_device_id":
            print("failed: expected request_device_id")
            self.connected = False
            return

        # send device id
        print("debug: sending device id...")
        await self.send_message({
            "message": "provide_device_id",
            "device_id": self.agent.device_id
        })

        # wait for request_name
        msg = await self.receive_message()
        print(f"debug: received (expect request_name): {msg}")
        if not msg or msg.get("message") != "request_name":
            print("failed: expected request_name")
            self.connected = False
            return

        # send name
        print("debug: sending name...")
        await self.send_message({
            "message": "provide_name",
            "name": self.agent.name
        })

        # wait for connection_established
        message = await self.receive_message()
        print(f"debug: received (expect connection_established): {message}")
        if message and message.get("message") == "connection_established":
            print(f"connection established as {message.get('name')}")
            assigned_name = message.get("name")
            if assigned_name:
                self.agent.name = assigned_name
            print(f"available games: {message.get('available_games', [])}")
            # send ready message to let server know we're ready
            print("debug: sending ready message...")
            await self.send_message({
                "message": "ready"
            })
            print("debug: connection handshake complete")
        else:
            print("failed to establish connection")
            print(f"debug: expected 'connection_established' but got: {message}")
            self.connected = False
    
    async def join_game(self, game_type: str):
        """join a specific game."""
        if not self.connected:
            print("not connected to server")
            return False
        
        await self.send_message({
            "message": "join_game",
            "game_type": game_type
        })
        
        message = await self.receive_message()
        if message and message.get("message") == "joined_game":
            print(f"joined {game_type} game")
            self.agent.game_type = game_type
            return True
        else:
            print(f"failed to join {game_type} game")
            return False
    
    async def run(self):
        """main client loop."""
        if not self.connected:
            print("not connected to server")
            return
        try:
            while not self.should_exit:
                message = await self.receive_message()
                if not message:
                    break
                # If game_end, break after handling
                should_exit = await self.handle_message(message)
                if should_exit:
                    print(f"CLIENT {self.agent.name} exiting run loop after game_end")
                    self.should_exit = True
                    break
        except Exception as e:
            print(f"error in client loop: {e}")
        finally:
            await self.disconnect()
        print(f"CLIENT {self.agent.name} run() coroutine has returned")
    
    async def handle_message(self, message: Dict[str, Any]):
        """handle messages from the server."""
        msg_type = message.get("message", "")
        print(f"CLIENT {self.agent.name}: Received message type: {msg_type}")
        
        if msg_type == "game_end":
            print(f"CLIENT {self.agent.name}: Received game_end, will exit")
            return True  # Signal to exit
        # elif msg_type == "tournament_end":
        #     print(f"CLIENT {self.agent.name}: Received tournament_end, will exit")
        #     return True  # Signal to exit
        elif msg_type == "tournament_end":
            # Print final leaderboard to client terminal
            results = message.get("results", {})
            game_type = results.get("game_type", "unknown")
            final_rankings = results.get("final_rankings", [])
            print("")
            print(f"FINAL LEADERBOARD for {game_type}:")
            try:
                # final_rankings is list of [name, stats] pairs
                for rank, entry in enumerate(final_rankings, 1):
                    if isinstance(entry, (list, tuple)) and len(entry) == 2:
                        name, stats = entry
                    else:
                        name = entry.get("name") if isinstance(entry, dict) else str(entry)
                        stats = entry.get("stats", {}) if isinstance(entry, dict) else {}
                    total = float(stats.get("total_reward", 0))
                    games = int(stats.get("games_played", 0))
                    avg = total / max(games, 1)
                    print(f"  #{rank}: {name} - Total: {total:.2f}, Games: {games}, Avg: {avg:.2f}")
            except Exception as e:
                print(f"(Could not render leaderboard: {e})")

            # Also print this client's own summary
            print(f"Your final rank: {message.get('final_rank')}, "
                    f"Total: {message.get('final_reward'):.2f}, "
                    f"Games: {message.get('games_played')}, "
                    f"Avg: {message.get('average_reward'):.2f}")
            print("")
            print(f"CLIENT {self.agent.name}: Received tournament_end, will exit")
            return True  # Signal to exit
        elif msg_type == "server_shutdown":
            print(f"CLIENT {self.agent.name}: Server is shutting down: {message.get('reason', 'Unknown reason')}")
            return True  # Signal to exit
        elif msg_type == "tournament_start":
            print(f"CLIENT {self.agent.name}: Tournament starting!")
            print(f"  Players: {message.get('players', [])}")
            print(f"  Rounds: {message.get('num_rounds', 0)}")
        elif msg_type == "tournament_status":
            print(f"CLIENT {self.agent.name}: Tournament status update")
            print(f"  Players connected: {message.get('players_connected', 0)}")
            print(f"  Tournament started: {message.get('tournament_started', False)}")
        elif msg_type == "heartbeat":
            print(f"CLIENT {self.agent.name}: Heartbeat received")
            print(f"  Players connected: {message.get('players_connected', 0)}")
            print(f"  Tournament started: {message.get('tournament_started', False)}")
        elif msg_type == "request_action":
            # Handle action request
            observation = message.get("observation", {})
            action = self.agent.get_action(observation)
            await self.send_message({
                "message": "action",
                "action": action
            })
        elif msg_type == "round_result":
            # Handle round result
            reward = message.get("reward", 0)
            info = message.get("info", {})
            self.agent.update(reward, info)
            print(f"CLIENT {self.agent.name}: Round {message.get('round', 0)} - Reward: {reward}")
        elif msg_type == "round_summary":
            # Handle round summary
            rank = message.get("rank", 0)
            total_reward = message.get("total_reward", 0)
            print(f"CLIENT {self.agent.name}: Round {message.get('round', 0)} summary - Rank: {rank}, Total Reward: {total_reward}")
        else:
            print(f"CLIENT {self.agent.name}: Unknown message type: {msg_type}")
        
        return False  # Continue running
    
    async def send_message(self, message: Dict[str, Any]):
        """send a message to the server."""
        if self.writer:
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy(obj):
                import numpy as np
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {k: convert_numpy(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy(item) for item in obj]
                else:
                    return obj
            
            message = convert_numpy(message)
            print(f"CLIENT SENDING: {message}")
            data = json.dumps(message).encode() + b'\n'
            self.writer.write(data)
            await self.writer.drain()
    
    async def receive_message(self):
        print(f"CLIENT {self.agent.name}: receive_message() called")
        try:
            if self.should_exit:
                print(f"CLIENT {self.agent.name}: receive_message() early exit due to should_exit")
                return None
            if not self.reader:
                print(f"CLIENT {self.agent.name}: receive_message() no reader available")
                return None
            
            # Add timeout to prevent hanging
            try:
                data = await asyncio.wait_for(self.reader.readline(), timeout=30.0)
            except asyncio.TimeoutError:
                print(f"CLIENT {self.agent.name}: receive_message() timeout")
                return None
                
            if not data:
                print(f"CLIENT {self.agent.name}: receive_message() got no data (connection closed)")
                return None
            
            # Decode and strip whitespace
            decoded_data = data.decode().strip()
            if not decoded_data:
                print(f"CLIENT {self.agent.name}: receive_message() got empty data")
                return None
                
            try:
                message = json.loads(decoded_data)
                print(f"CLIENT {self.agent.name}: receive_message() got message: {message}")
                return message
            except json.JSONDecodeError as e:
                print(f"CLIENT {self.agent.name}: receive_message() JSON decode error: {e}")
                print(f"CLIENT {self.agent.name}: Raw data: {repr(decoded_data)}")
                return None
        except Exception as e:
            print(f"CLIENT {self.agent.name}: receive_message() exception: {e}")
            return None
    
    async def disconnect(self):
        """disconnect from the server."""
        print(f"CLIENT {self.agent.name}: disconnect() called")
        if self.writer:
            try:
                print(f"CLIENT {self.agent.name}: closing writer...")
                self.writer.close()
                print(f"CLIENT {self.agent.name}: writer.close() called, awaiting wait_closed()...")
                await self.writer.wait_closed()
                print(f"CLIENT {self.agent.name}: writer.wait_closed() finished")
            except Exception as e:
                print(f"CLIENT {self.agent.name}: error during disconnect: {e}")
        self.connected = False
        print("disconnected from server")


# example usage and command line interface
async def main():
    """example usage of the agt client."""
    parser = argparse.ArgumentParser(description='agt client')
    parser.add_argument('--name', type=str, required=True, help='agent name')
    parser.add_argument('--game', type=str, required=True, 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='game type to join')
    parser.add_argument('--host', type=str, default='localhost', help='server host')
    parser.add_argument('--port', type=int, default=8080, help='server port')
    parser.add_argument('--agent-file', type=str, help='path to agent implementation file')
    
    args = parser.parse_args()
    
    # create a simple random agent as default
    class RandomAgent(AGTAgent):
        def get_action(self, observation):
            import random
            if self.game_type == "auction":
                return {"A": random.randint(0, 10), "B": random.randint(0, 10),
                       "C": random.randint(0, 10), "D": random.randint(0, 10)}
            else:
                return random.randint(0, 2)
    
    agent = RandomAgent(args.name)
    
    # import agent from file if provided
    if args.agent_file:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_module", args.agent_file)
            if spec is not None:
                agent_module = importlib.util.module_from_spec(spec)
                if spec.loader is not None:
                    spec.loader.exec_module(agent_module)
                    
                    # look for agent_submission
                    if hasattr(agent_module, 'agent_submission'):
                        agent = agent_module.agent_submission
        except Exception as e:
            print(f"warning: could not load agent from {args.agent_file}: {e}")
            print("using default random agent instead.")
    
    # create client and connect
    client = AGTClient(agent, args.host, args.port)
    await client.connect()
    
    if client.connected:
        # join game and run
        if await client.join_game(args.game):
            await client.run()
        else:
            print(f"failed to join {args.game} game")
    else:
        print("failed to connect to server")


if __name__ == "__main__":
    asyncio.run(main()) 