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
    
    def __init__(self, agent: AGTAgent, host: str = "localhost", port: int = 8080, verbose: bool = False):
        self.agent = agent
        self.host = host
        self.port = port
        self.verbose = verbose
        self.reader = None
        self.writer = None
        self.connected = False
        self.should_exit = False  # Add exit flag
    
    def log(self, message: str, level: str = "info"):
        """Log message with appropriate level and formatting."""
        if level == "debug" and not self.verbose:
            return
        
        prefix = ""
        if level == "debug":
            prefix = "[DEBUG] "
        elif level == "info":
            prefix = "[INFO] "
        elif level == "success":
            prefix = "[SUCCESS] "
        elif level == "warning":
            prefix = "[WARNING] "
        elif level == "error":
            prefix = "[ERROR] "
        
        print(f"{prefix}{message}")
    
    async def connect(self):
        """connect to the agt server."""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.connected = True
            self.log(f"Connected to AGT server at {self.host}:{self.port}", "success")
            
            # handle initial handshake
            await self.handle_connection()
            
        except Exception as e:
            self.log(f"Failed to connect to server: {e}", "error")
            self.connected = False
    
    async def handle_connection(self):
        """handle the initial connection handshake."""
        self.log("Starting connection handshake...", "debug")

        # wait for request_device_id
        msg = await self.receive_message()
        self.log(f"Received: {msg}", "debug")
        if not msg or msg.get("message") != "request_device_id":
            self.log("Failed: expected request_device_id", "error")
            self.connected = False
            return

        # send device id
        self.log("Sending device id...", "debug")
        await self.send_message({
            "message": "provide_device_id",
            "device_id": self.agent.device_id
        })

        # wait for request_name
        msg = await self.receive_message()
        self.log(f"Received: {msg}", "debug")
        if not msg or msg.get("message") != "request_name":
            self.log("Failed: expected request_name", "error")
            self.connected = False
            return

        # send name
        self.log("Sending name...", "debug")
        await self.send_message({
            "message": "provide_name",
            "name": self.agent.name
        })

        # wait for connection_established
        message = await self.receive_message()
        self.log(f"Received: {message}", "debug")
        if message and message.get("message") == "connection_established":
            assigned_name = message.get("name")
            if assigned_name:
                self.agent.name = assigned_name
            self.log(f"Connection established as '{self.agent.name}'", "success")
            available_games = message.get('available_games', [])
            if available_games:
                self.log(f"Available games: {', '.join(available_games)}", "info")
            
            # send ready message to let server know we're ready
            self.log("Sending ready message...", "debug")
            await self.send_message({
                "message": "ready"
            })
            self.log("Connection handshake complete", "debug")
        else:
            self.log("Failed to establish connection", "error")
            self.log(f"Expected 'connection_established' but got: {message}", "debug")
            self.connected = False
    
    async def join_game(self, game_type: str):
        """join a specific game."""
        if not self.connected:
            self.log("Not connected to server", "error")
            return False
        
        await self.send_message({
            "message": "join_game",
            "game_type": game_type
        })
        
        message = await self.receive_message()
        if message and message.get("message") == "joined_game":
            self.log(f"Joined {game_type} game", "success")
            self.agent.game_type = game_type
            return True
        else:
            self.log(f"Failed to join {game_type} game", "error")
            return False
    
    async def run(self):
        """main client loop."""
        if not self.connected:
            self.log("Not connected to server", "error")
            return
        try:
            while not self.should_exit:
                message = await self.receive_message()
                if not message:
                    break
                # If game_end, break after handling
                should_exit = await self.handle_message(message)
                if should_exit:
                    self.log("Game ended, exiting...", "info")
                    self.should_exit = True
                    break
        except Exception as e:
            self.log(f"Error in client loop: {e}", "error")
        finally:
            await self.disconnect()
    
    async def handle_message(self, message: Dict[str, Any]):
        """handle messages from the server."""
        msg_type = message.get("message", "")
        self.log(f"Received: {msg_type}", "debug")
        
        if msg_type == "game_end":
            self.log("Game ended", "info")
            return True  # Signal to exit
        elif msg_type == "tournament_end":
            # Print final leaderboard to client terminal
            results = message.get("results", {})
            game_type = results.get("game_type", "unknown")
            final_rankings = results.get("final_rankings", [])
            
            print("\n" + "="*50)
            print(f"FINAL LEADERBOARD - {game_type.upper()}")
            print("="*50)
            
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
                    
                    # Add rank indicator for top 3
                    rank_indicator = f"#{rank}" if rank <= 3 else f"#{rank}"
                    print(f"{rank_indicator} {name:<20} | Total: {total:>8.2f} | Games: {games:>3} | Avg: {avg:>6.2f}")
            except Exception as e:
                self.log(f"Could not render leaderboard: {e}", "warning")

            # Also print this client's own summary
            final_rank = message.get('final_rank', 'N/A')
            final_reward = message.get('final_reward', 0)
            games_played = message.get('games_played', 0)
            avg_reward = message.get('average_reward', 0)
            
            print("-" * 50)
            print(f"YOUR RESULTS:")
            print(f"   Rank: {final_rank}")
            print(f"   Total Reward: {final_reward:.2f}")
            print(f"   Games Played: {games_played}")
            print(f"   Average Reward: {avg_reward:.2f}")
            print("="*50 + "\n")
            
            return True  # Signal to exit
        elif msg_type == "server_shutdown":
            self.log(f"Server is shutting down: {message.get('reason', 'Unknown reason')}", "warning")
            return True  # Signal to exit
        elif msg_type == "tournament_error":
            error_message = message.get("error", "Unknown tournament error")
            self.log(f"Tournament error: {error_message}", "error")
            return True  # Signal to exit
        elif msg_type == "tournament_start":
            players = message.get('players', [])
            num_rounds = message.get('num_rounds', 0)
            self.log("Tournament starting!", "success")
            self.log(f"Players: {', '.join(players)}", "info")
            self.log(f"Rounds: {num_rounds}", "info")
        elif msg_type == "tournament_status":
            players_connected = message.get('players_connected', 0)
            tournament_started = message.get('tournament_started', False)
            self.log(f"Status: {players_connected} players connected, tournament {'started' if tournament_started else 'waiting'}", "info")
        elif msg_type == "heartbeat":
            # nly log heartbeats  in verbose mode
            if self.verbose:
                players_connected = message.get('players_connected', 0)
                tournament_started = message.get('tournament_started', False)
                self.log(f"Heartbeat: {players_connected} players, tournament {'started' if tournament_started else 'waiting'}", "debug")
        elif msg_type == "request_action":
            # Handle action request silently unless verbose
            observation = message.get("observation", {})
            print(f"[CLIENT DEBUG] {self.agent.name}: Received observation: {observation}")
            
            # Special handling for auction games - setup agent and set valuations
            if hasattr(self.agent, 'setup') and 'goods' in observation:
                # First time setup - initialize goods and goods_to_index mapping
                if not hasattr(self.agent, '_goods_to_index') or not self.agent._goods_to_index:
                    self.agent.setup(observation['goods'], observation.get('kth_price', 1))
                    print(f"[CLIENT DEBUG] {self.agent.name}: Setup completed with goods: {observation['goods']}")
                
                # Set valuations for this round
                if hasattr(self.agent, 'set_valuations') and 'valuations' in observation:
                    self.agent.set_valuations(observation['valuations'])
                    print(f"[CLIENT DEBUG] {self.agent.name}: Set valuations to {observation['valuations']}")
            
            # All agents should have get_action method (either native or via adapter)
            action = self.agent.get_action(observation)
            print(f"[CLIENT DEBUG] {self.agent.name}: Sending action: {action}")
            
            # For ADX games, we need to serialize the OneDayBidBundle to a simple format
            if hasattr(action, 'campaign_id') and hasattr(action, 'bid_entries'):
                # This is a OneDayBidBundle - convert to simple dict
                serialized_action = {
                    "campaign_id": action.campaign_id,
                    "day_limit": action.day_limit,
                    "bid_entries": [
                        {
                            "market_segment": entry.market_segment.value,
                            "bid": entry.bid,
                            "spending_limit": entry.spending_limit
                        }
                        for entry in action.bid_entries
                    ]
                }
            else:
                # For other games, use the action as-is
                serialized_action = action
            
            await self.send_message({
                "message": "action",
                "action": serialized_action
            })
        elif msg_type == "round_result":
            # Handle round result
            reward = message.get("reward", 0)
            info = message.get("info", {})
            print(f"[CLIENT DEBUG] {self.agent.name}: Received round result - reward: {reward}, info: {info}")
            # Note: The server already called update() on the agent, so we don't need to call it again here
            round_num = message.get('round', 0)
            self.log(f"Round {round_num}: +{reward:.2f} points", "info")
        elif msg_type == "round_summary":
            # Handle round summary
            rank = message.get("rank", 0)
            total_reward = message.get("total_reward", 0)
            round_num = message.get('round', 0)
            self.log(f"Round {round_num} complete - Rank: {rank}, Total: {total_reward:.2f}", "info")
        else:
            self.log(f"Unknown message type: {msg_type}", "warning")
        
        return False 
    
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
            self.log(f"Sending: {message}", "debug")
            data = json.dumps(message).encode() + b'\n'
            self.writer.write(data)
            await self.writer.drain()
    
    async def receive_message(self):
        self.log("Waiting for message...", "debug")
        try:
            if self.should_exit:
                self.log("Early exit due to should_exit", "debug")
                return None
            if not self.reader:
                self.log("No reader available", "debug")
                return None
            
            # Add timeout to prevent hanging
            try:
                data = await asyncio.wait_for(self.reader.readline(), timeout=30.0)
            except asyncio.TimeoutError:
                self.log("Receive timeout", "debug")
                return None
                
            if not data:
                self.log("No data received (connection closed)", "debug")
                return None
            
            # Decode and strip whitespace
            decoded_data = data.decode().strip()
            if not decoded_data:
                self.log("Empty data received", "debug")
                return None
                
            try:
                message = json.loads(decoded_data)
                self.log(f"Received: {message}", "debug")
                return message
            except json.JSONDecodeError as e:
                self.log(f"JSON decode error: {e}", "error")
                self.log(f"Raw data: {repr(decoded_data)}", "debug")
                return None
        except Exception as e:
            self.log(f"Receive exception: {e}", "error")
            return None
    
    async def disconnect(self):
        """disconnect from the server."""
        self.log("Disconnecting...", "debug")
        if self.writer:
            try:
                self.log("Closing writer...", "debug")
                self.writer.close()
                self.log("Waiting for writer to close...", "debug")
                await self.writer.wait_closed()
                self.log("Writer closed", "debug")
            except Exception as e:
                self.log(f"Error during disconnect: {e}", "error")
        self.connected = False
        self.log("Disconnected from server", "info")


# example usage and command line interface
async def main():
    """example usage of the agt client."""
    parser = argparse.ArgumentParser(description='AGT Client - Connect your agent to the AGT server')
    parser.add_argument('--name', type=str, required=True, help='Agent name')
    parser.add_argument('--game', type=str, required=True, 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='Game type to join')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--agent-file', type=str, help='Path to agent implementation file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    
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
                        raw_agent = agent_module.agent_submission
                        
                        # Wrap with appropriate adapter based on game type
                        try:
                            from adapters import create_adapter
                            agent = create_adapter(raw_agent, args.game)
                            print(f"[SUCCESS] Loaded and wrapped agent from {args.agent_file} for game {args.game}")
                        except Exception as adapter_error:
                            print(f"[WARNING] Could not create adapter for {args.game}: {adapter_error}")
                            print("Using raw agent (may not work for all game types)")
                            agent = raw_agent
        except Exception as e:
            print(f"[WARNING] Could not load agent from {args.agent_file}: {e}")
            print("Using default random agent instead.")
    
    # create client and connect
    client = AGTClient(agent, args.host, args.port, verbose=args.verbose)
    await client.connect()
    
    if client.connected:
        # join game and run
        if await client.join_game(args.game):
            await client.run()
        else:
            print(f"[ERROR] Failed to join {args.game} game")
    else:
        print("[ERROR] Failed to connect to server")


if __name__ == "__main__":
    asyncio.run(main()) 