#!/usr/bin/env python3
"""
Modern AGT Server for Lab Competitions

This server allows students to connect their completed stencils and compete against each other
in all the labs we've implemented: RPS, BOS, Chicken, Lemonade, and Auctions.
"""

import asyncio
import json
import socket
import time
import argparse
import os
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import pandas as pd
import numpy as np

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.game.RPSGame import RPSGame
from core.game.BOSGame import BOSGame
from core.game.BOSIIGame import BOSIIGame
from core.game.ChickenGame import ChickenGame
from core.game.LemonadeGame import LemonadeGame
from core.game.AuctionGame import AuctionGame


@dataclass
class PlayerConnection:
    """Represents a connected player."""
    name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    address: Tuple[str, int]
    device_id: str
    connected_at: float
    game_history: List[Dict[str, Any]]
    current_game: Optional[str] = None
    read_lock: Optional[asyncio.Lock] = None
    pending_action: Optional[Any] = None
    
    def __post_init__(self):
        if self.read_lock is None:
            self.read_lock = asyncio.Lock()


class AGTServer:
    """Modern AGT Server for lab competitions."""
    
    def __init__(self, config: Dict[str, Any], host: str = "0.0.0.0", port: int = 8080):
        self.config = config
        self.host = host
        self.port = port
        
        # Server state
        self.players: Dict[str, PlayerConnection] = {}
        self.games: Dict[str, Any] = {}
        self.results: List[Dict[str, Any]] = []
        
        # Game restrictions
        self.allowed_games = config.get("allowed_games", None)  # none means all games allowed
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Game configurations
        self.game_configs = {
            "rps": {
                "name": "Rock Paper Scissors",
                "game_class": RPSGame,
                "num_players": 2,
                "num_rounds": 100,
                "description": "Classic Rock Paper Scissors game"
            },
            "bos": {
                "name": "Battle of the Sexes",
                "game_class": BOSGame,
                "num_players": 2,
                "num_rounds": 100,
                "description": "Battle of the Sexes coordination game"
            },
            "bosii": {
                "name": "Battle of the Sexes II",
                "game_class": BOSIIGame,
                "num_players": 2,
                "num_rounds": 100,
                "description": "Battle of the Sexes with incomplete information"
            },
            "chicken": {
                "name": "Chicken Game",
                "game_class": ChickenGame,
                "num_players": 2,
                "num_rounds": 100,
                "description": "Chicken game with Q-Learning and collusion"
            },
            "lemonade": {
                "name": "Lemonade Stand",
                "game_class": LemonadeGame,
                "num_players": 3,
                "num_rounds": 100,
                "description": "3-player Lemonade Stand positioning game"
            },
            "auction": {
                "name": "Simultaneous Auction",
                "game_class": AuctionGame,
                "num_players": 4,
                "num_rounds": 10,
                "description": "Simultaneous sealed bid auction"
            }
        }
        
        # Filter game configs based on allowed games
        if self.allowed_games is not None:
            filtered_configs = {}
            for game_id in self.allowed_games:
                if game_id in self.game_configs:
                    filtered_configs[game_id] = self.game_configs[game_id]
                else:
                    self.logger.warning(f"unknown game type in allowed_games: {game_id}")
            self.game_configs = filtered_configs
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a new client connection."""
        address = writer.get_extra_info('peername')
        self.logger.info(f"new connection from {address}")
        
        try:
            # Request device ID
            await self.send_message(writer, {"message": "request_device_id"})
            device_id = await self.receive_message(reader)
            
            if not device_id or device_id.get("message") != "provide_device_id":
                self.logger.warning(f"invalid device id response from {address}")
                return
            
            device_id = device_id.get("device_id", f"device_{address[0]}_{address[1]}")
            
            # Request player name
            await self.send_message(writer, {"message": "request_name"})
            name_response = await self.receive_message(reader)
            
            if not name_response or name_response.get("message") != "provide_name":
                self.logger.warning(f"invalid name response from {address}")
                return
            
            player_name = name_response.get("name", f"Player_{address[0]}_{address[1]}")
            
            # Check for duplicate names
            original_name = player_name
            counter = 1
            while player_name in self.players:
                player_name = f"{original_name}_{counter}"
                counter += 1
            
            # Create player connection
            player = PlayerConnection(
                name=player_name,
                reader=reader,
                writer=writer,
                address=address,
                device_id=device_id,
                connected_at=time.time(),
                game_history=[]
            )
            
            self.players[player_name] = player
            
            # Send confirmation
            await self.send_message(writer, {
                "message": "connection_established",
                "name": player_name,
                "available_games": list(self.game_configs.keys())
            })
            
            self.logger.info(f"player {player_name} connected successfully")
            
            # Main client loop
            await self.client_loop(player)
            
        except Exception as e:
            self.logger.error(f"error handling client {address}: {e}")
        finally:
            if player_name in self.players:
                del self.players[player_name]
            writer.close()
            await writer.wait_closed()
            self.logger.info(f"player {player_name} disconnected")
    
    async def client_loop(self, player: PlayerConnection):
        """Main loop for handling client messages."""
        try:
            while True:
                message = await self.receive_message(player.reader, player)
                if not message:
                    break
                
                await self.handle_message(player, message)
                
        except Exception as e:
            self.logger.error(f"error in client loop for {player.name}: {e}")
    
    async def handle_message(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a message from a client."""
        msg_type = message.get("message")
        
        if msg_type == "ready":
            # Client is ready, no action needed
            pass
        elif msg_type == "join_game":
            await self.handle_join_game(player, message)
        elif msg_type == "provide_action":
            # Store the action for the current round
            player.pending_action = message.get("action")
        elif msg_type == "action":
            # Store the action for the current round
            player.pending_action = message.get("action")
        elif msg_type == "get_action":
            await self.handle_get_action(player, message)
        elif msg_type == "ready_next_round":
            await self.handle_ready_next_round(player, message)
        elif msg_type == "ping":
            await self.send_message(player.writer, {"message": "pong"})
        else:
            self.logger.warning(f"unknown message type from {player.name}: {msg_type}")
    
    async def handle_join_game(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a player joining a game."""
        game_type = message.get("game_type")
        
        if game_type not in self.game_configs:
            await self.send_message(player.writer, {
                "message": "error",
                "error": f"Unknown game type: {game_type}"
            })
            return
        
        # Check if player is already in a game
        if player.current_game:
            await self.send_message(player.writer, {
                "message": "error",
                "error": "Already in a game"
            })
            return
        
        # Add player to game queue
        if game_type not in self.games:
            self.games[game_type] = {
                "players": [],
                "game": None,
                "config": self.game_configs[game_type]
            }
        
        self.games[game_type]["players"].append(player)
        player.current_game = game_type
        
        await self.send_message(player.writer, {
            "message": "joined_game",
            "game_type": game_type,
            "position": len(self.games[game_type]["players"])
        })
        
        # Check if we have enough players to start
        game_config = self.game_configs[game_type]
        if len(self.games[game_type]["players"]) >= game_config["num_players"]:
            await self.start_game(game_type)
    
    async def handle_get_action(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a get_action request (legacy support)."""
        # This is handled in the game loop, but we keep it for compatibility
        pass
    
    async def handle_ready_next_round(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a ready_next_round message."""
        # This is handled in the game loop, but we keep it for compatibility
        pass
    
    async def start_game(self, game_type: str):
        """Start a game with the available players."""
        game_data = self.games[game_type]
        players = game_data["players"][:game_data["config"]["num_players"]]
        
        self.logger.info(f"starting {game_type} game with players: {[p.name for p in players]}")
        
        # Create game instance
        game_config = game_data["config"]
        
        # Create valuation functions for auction games
        if game_type == "auction":
            valuation_functions = {}
            for i, player in enumerate(players):
                def make_valuation(player_name):
                    def valuation(bundle):
                        return sum(10 for item in bundle)  # simple additive valuation
                    return valuation
                valuation_functions[player.name] = make_valuation(player.name)
            
            game = game_config["game_class"](
                goods={"A", "B", "C", "D"},
                valuation_functions=valuation_functions,
                num_rounds=game_config["num_rounds"]
            )
        else:
            # For other games, create simple game instances
            game = game_config["game_class"](rounds=game_config["num_rounds"])
        
        game_data["game"] = game
        
        # Send game start message to all players
        for player in players:
            await self.send_message(player.writer, {
                "message": "game_start",
                "game_type": game_type,
                "num_rounds": game_config["num_rounds"],
                "players": [p.name for p in players]
            })
        
        # Start game loop
        asyncio.create_task(self.run_game(game_type, players))
    
    async def run_game(self, game_type: str, players: List[PlayerConnection]):
        """Run a game with the given players."""
        game_data = self.games[game_type]
        game = game_data["game"]
        try:
            # Initialize game
            obs = game.reset()
            self.logger.info(f"GAME {game_type} started with players: {[p.name for p in players]}")
            for round_num in range(game_data["config"]["num_rounds"]):
                self.logger.info(f"ROUND {round_num + 1} for {game_type}")
                # Get actions from all players
                actions = {}
                for i, player in enumerate(players):
                    # Clear any pending action
                    player.pending_action = None
                    self.logger.info(f"Requesting action from {player.name}")
                    await self.send_message(player.writer, {
                        "message": "request_action",
                        "round": round_num + 1,
                        "observation": obs.get(i, {})
                    })
                    # Wait for action response with timeout
                    timeout = 5.0  # 5 second timeout
                    start_time = time.time()
                    while player.pending_action is None and (time.time() - start_time) < timeout:
                        await asyncio.sleep(0.1)
                    if player.pending_action is not None:
                        actions[i] = player.pending_action  # Use integer index
                        self.logger.info(f"Collected action from {player.name}: {player.pending_action}")
                    else:
                        # Use default action if timeout
                        actions[i] = 0  # Default action
                        self.logger.warning(f"Timeout waiting for action from {player.name}, using default")
                
                # Step the game
                obs, rewards, done, info = game.step(actions)
                self.logger.info(f"Actions: {actions}, Rewards: {rewards}")
                # Send results to players
                for i, player in enumerate(players):
                    await self.send_message(player.writer, {
                        "message": "round_result",
                        "round": round_num + 1,
                        "reward": rewards.get(i, 0),  # Use integer index
                        "info": info.get(i, {})  # Use integer index
                    })
                # Check if game is over
                if done:
                    print(f"SERVER: Game is terminal after round {round_num + 1}")
                    break
                
                # Check if we've reached max rounds
                if round_num + 1 >= game_data["config"]["num_rounds"]:
                    print(f"SERVER: Reached max rounds ({game_data['config']['num_rounds']}) after round {round_num + 1}")
                    break
                
                round_num += 1
                print(f"SERVER: Starting round {round_num + 1}")
            
            print(f"SERVER: Game loop finished, calling finish_game")
            await self.finish_game(game_type, players)
            print(f"SERVER: finish_game completed")
            self.logger.info(f"GAME {game_type} ended.")
        except Exception as e:
            self.logger.error(f"error running {game_type} game: {e}")
            await self.finish_game(game_type, players, error=True)
    
    def get_default_action(self, game_type: str):
        """Get a default action for a game type."""
        if game_type == "rps":
            return 0  # rock
        elif game_type in ["bos", "bosii"]:
            return 0  # first action
        elif game_type == "chicken":
            return 0  # swerve
        elif game_type == "lemonade":
            return 0  # position 0
        elif game_type == "auction":
            return {"A": 0, "B": 0, "C": 0, "D": 0}  # zero bids
        else:
            return 0
    
    async def finish_game(self, game_type: str, players: List[PlayerConnection], error: bool = False):
        """Finish a game and send results to players."""
        print(f"SERVER: finish_game called for {game_type} with {len(players)} players")
        game_data = self.games[game_type]
        # Calculate final results
        results = {
            "game_type": game_type,
            "players": [p.name for p in players],
            "total_rounds": game_data["config"]["num_rounds"],
            "error": error
        }
        if not error and game_data["game"]:
            # Get game state for results
            game_state = game_data["game"].get_game_state()
            results.update(game_state)
        # Send final results to players
        print(f"SERVER: Sending game_end to all players for {game_type}")
        for player in players:
            game_end_msg = {
                "message": "game_end",
                "results": results
            }
            print(f"SERVER: Sending game_end to {player.name}: {game_end_msg}")
            await self.send_message(player.writer, game_end_msg)
        
        # Add a small delay to ensure messages are sent
        await asyncio.sleep(0.1)
        print(f"SERVER: Sent game_end to all players for {game_type}")
        # Store results
        self.results.append(results)
        
        # Clean up game
        if game_type in self.games:
            del self.games[game_type]
        
        self.logger.info(f"finished {game_type} game")
    
    async def send_message(self, writer: asyncio.StreamWriter, message: Dict[str, Any]):
        """Send a message to a client."""
        try:
            # Convert sets to lists for JSON serialization
            def convert_sets(obj):
                if isinstance(obj, set):
                    return list(obj)
                elif isinstance(obj, dict):
                    return {k: convert_sets(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_sets(item) for item in obj]
                else:
                    return obj
            message = convert_sets(message)
            data = json.dumps(message).encode() + b'\n'
            self.logger.info(f"SENDING to client: {message}")
            writer.write(data)
            await writer.drain()
        except Exception as e:
            self.logger.error(f"error sending message: {e}")
    
    async def receive_message(self, reader: asyncio.StreamReader, player: Optional[PlayerConnection] = None) -> Optional[Dict[str, Any]]:
        """Receive a message from a client."""
        try:
            if player and player.read_lock:
                async with player.read_lock:
                    data = await reader.readline()
                    if data:
                        msg = json.loads(data.decode().strip())
                        self.logger.info(f"RECEIVED from client {getattr(player, 'name', '?')}: {msg}")
                        return msg
            else:
                data = await reader.readline()
                if data:
                    msg = json.loads(data.decode().strip())
                    self.logger.info(f"RECEIVED from client: {msg}")
                    return msg
        except Exception as e:
            self.logger.error(f"error receiving message: {e}")
        return None
    
    async def start(self):
        """Start the server."""
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        
        self.logger.info(f"agt server started on {self.host}:{self.port}")
        if self.allowed_games is not None:
            self.logger.info(f"game restrictions: only {', '.join(self.allowed_games)} allowed")
        else:
            self.logger.info("no game restrictions: all games available")
        self.logger.info("available games:")
        for game_id, config in self.game_configs.items():
            self.logger.info(f"  {game_id}: {config['name']} ({config['num_players']} players)")
        
        async with server:
            await server.serve_forever()
    
    def save_results(self):
        """Save game results to file."""
        if self.results:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"results/agt_server_results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            self.logger.info(f"results saved to {filename}")


async def main():
    """Main server function."""
    parser = argparse.ArgumentParser(description='AGT Server for Lab Competitions')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--config', type=str, help='Configuration file (optional)')
    parser.add_argument('--game', type=str, choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='Restrict server to a specific game type')
    parser.add_argument('--games', type=str, nargs='+', 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='Restrict server to specific game types (multiple allowed)')
    
    args = parser.parse_args()
    
    # Default configuration
    config = {
        "server_name": "AGT Lab Server",
        "max_players": 100,
        "timeout": 30,
        "save_results": True
    }
    
    # Load custom config if provided
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config.update(json.load(f))
    
    # Set allowed games based on command line arguments
    if args.game:
        config["allowed_games"] = [args.game]
        print(f"server restricted to game: {args.game}")
    elif args.games:
        config["allowed_games"] = args.games
        print(f"server restricted to games: {', '.join(args.games)}")
    
    server = AGTServer(config, args.host, args.port)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        print("\nshutting down server...")
        server.save_results()
    except Exception as e:
        print(f"server error: {e}")
        server.save_results()


if __name__ == "__main__":
    asyncio.run(main()) 