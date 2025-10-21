#!/usr/bin/env python3
"""
Modern AGT Server for Lab Competitions

This server allows students to connect their completed stencils and compete against each other
in all the labs we've implemented: RPS, BOS, Chicken, Lemonade, and Auctions.
"""

import asyncio
import json
import time
import argparse
import os
import sys
import logging
import signal
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Dashboard is now separate - no longer integrated

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.utils import debug_print

# Game classes are now imported dynamically in _load_game_configs()


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
    total_reward: float = 0.0
    games_played: int = 0
    
    def __post_init__(self):
        if self.read_lock is None:
            self.read_lock = asyncio.Lock()


class AGTServer:
    """Modern AGT Server for lab competitions."""
    
    def __init__(self, config: Dict[str, Any], host: str = "0.0.0.0", port: int = 8080, verbose: bool = False):
        self.config = config
        self.host = host
        self.port = port
        self.verbose = verbose
        
        # Server state
        self.players: Dict[str, PlayerConnection] = {}
        self.games: Dict[str, Any] = {} #this is a dictionary that maps game types to game data. The game data is a dictionary that contains the players in the game, the game object, the game configuration, and the tournament started flag.
        self.results: List[Dict[str, Any]] = []
        
        # Game restrictions
        self.allowed_games = config.get("allowed_games", None)  # none means all games allowed
        
        # Setup logging - minimal output
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Create results directory
        os.makedirs("results", exist_ok=True)
        
        # Load game configurations from config files
        self.game_configs = self._load_game_configs()
        
        # Filter game configs based on allowed games
        if self.allowed_games is not None:
            filtered_configs = {}
            for game_id in self.allowed_games:
                if game_id in self.game_configs:
                    filtered_configs[game_id] = self.game_configs[game_id]
                else:
                    print(f"Unknown game type in allowed_games: {game_id}")
            self.game_configs = filtered_configs
    
    def _load_game_configs(self):
        """Load game configurations from config files."""
        game_configs = {}
        
        # Import all game classes
        from core.game.RPSGame import RPSGame
        from core.game.BOSGame import BOSGame
        from core.game.BOSIIGame import BOSIIGame
        from core.game.ChickenGame import ChickenGame
        from core.game.PDGame import PDGame
        from core.game.LemonadeGame import LemonadeGame
        from core.game.AuctionGame import AuctionGame
        from core.game.AdxTwoDayGame import AdxTwoDayGame
        from core.game.AdxOneDayGame import AdxOneDayGame
        
        # Map class names to actual classes
        class_map = {
            "RPSGame": RPSGame,
            "BOSGame": BOSGame,
            "BOSIIGame": BOSIIGame,
            "ChickenGame": ChickenGame,
            "PDGame": PDGame,
            "LemonadeGame": LemonadeGame,
            "AuctionGame": AuctionGame,
            "AdxTwoDayGame": AdxTwoDayGame,
            "AdxOneDayGame": AdxOneDayGame
        }
        
        # Load configs from all JSON files in configs directory
        config_dir = os.path.join(os.path.dirname(__file__), 'configs')
        for filename in os.listdir(config_dir):
            if filename.endswith('.json'):
                config_path = os.path.join(config_dir, filename)
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                    
                    # Extract game information from config
                    if 'allowed_games' in config_data and 'game_class' in config_data:
                        game_class_name = config_data['game_class']
                        if game_class_name in class_map:
                            game_class = class_map[game_class_name]
                            
                            # Create game config for each allowed game
                            for game_type in config_data['allowed_games']:
                                game_configs[game_type] = {
                                    "name": config_data.get('name', game_type),
                                    "game_class": game_class,
                                    "num_players": config_data.get('num_players', 2),
                                    "num_rounds": config_data.get('num_rounds', 100),
                                    "description": config_data.get('description', f"{game_type} game")
                                }
                        else:
                            print(f"Warning: Unknown game class '{game_class_name}' in {filename}")
                    else:
                        print(f"Warning: Config file {filename} missing required fields")
                        
                except Exception as e:
                    print(f"Error loading config file {filename}: {e}")
        
        return game_configs
    
    def debug_print(self, message: str, flush: bool = True):
        """Print debug message only if verbose mode is enabled."""
        if self.verbose:
            print(f"[SERVER DEBUG] {message}", flush=flush)
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a new client connection."""
        address = writer.get_extra_info('peername')
        player_name = None
        
        self.debug_print(f"New client connection from {address}")
        
        try:
            # Request device ID
            await self.send_message(writer, {"message": "request_device_id"})
            device_id = await self.receive_message(reader)
            
            if not device_id or device_id.get("message") != "provide_device_id":
                print(f"Invalid device ID response from {address}")
                return
            
            device_id = device_id.get("device_id", f"device_{address[0]}_{address[1]}")
            
            # Request player name
            await self.send_message(writer, {"message": "request_name"})
            name_response = await self.receive_message(reader)
            
            if not name_response or name_response.get("message") != "provide_name":
                print(f"Invalid name response from {address}")
                return
            
            player_name = name_response.get("name", f"Player_{address[0]}_{address[1]}")
            
            # Check for duplicate names
            original_name = player_name
            counter = 1
            while player_name in self.players:
                player_name = f"{original_name}_{counter}"
                counter += 1
            
            # Log if name was modified due to conflict
            if player_name != original_name:
                print(f"Name conflict resolved: '{original_name}' -> '{player_name}'", flush=True)
            
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
            
            # Player connected successfully
            if player_name == original_name:
                print(f"Player '{player_name}' connected from {address[0]}:{address[1]} (no name conflicts)", flush=True)
                self.debug_print(f"Player '{player_name}' connected successfully")
            else:
                print(f"Player '{player_name}' connected from {address[0]}:{address[1]} (resolved from '{original_name}')", flush=True)
                self.debug_print(f"Player '{player_name}' connected with name conflict resolution")
            
            # Main client loop
            await self.client_loop(player)
            
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            if player_name and player_name in self.players:
                # Remove player from any games they're in
                if player_name in self.players:
                    player = self.players[player_name]
                    if player.current_game and player.current_game in self.games:
                        game_players = self.games[player.current_game]["players"]
                        # Remove player from game list
                        game_players[:] = [p for p in game_players if p.name != player_name]
                        print(f"Player {player_name} disconnected from {player.current_game} game! ({len(game_players)} players remaining)", flush=True)
                
                del self.players[player_name]
            writer.close()
            await writer.wait_closed()
            if player_name:
                if player.current_game and player.current_game in self.games:
                    remaining_count = len(self.games[player.current_game]['players'])
                    print(f"Player {player_name} disconnected from {player.current_game} game! ({remaining_count} players remaining)", flush=True)
                else:
                    print(f"Player {player_name} disconnected (game no longer active)", flush=True)
            else:
                print(f"Unknown player from {address} disconnected", flush=True)
    
    async def client_loop(self, player: PlayerConnection):
        """Main loop for handling client messages."""
        try:
            # Start heartbeat task for this client
            heartbeat_task = asyncio.create_task(self.send_heartbeat(player))
            
            while True:
                message = await self.receive_message(player.reader, player)
                if not message:
                    break
                
                await self.handle_message(player, message)
                
        except Exception as e:
            self.logger.error(f"error in client loop for {player.name}: {e}")
        finally:
            # Cancel heartbeat task when client disconnects
            if 'heartbeat_task' in locals():
                heartbeat_task.cancel()
    
    async def send_heartbeat(self, player: PlayerConnection):
        """Send periodic heartbeat messages to keep client alive."""
        try:
            while True:
                await asyncio.sleep(15)  # Send heartbeat every 15 seconds
                
                # Only send heartbeat if client is still connected and waiting
                if (player.current_game and 
                    player.current_game in self.games and 
                    not self.games[player.current_game]["tournament_started"]):
                    
                    await self.send_message(player.writer, {
                        "message": "heartbeat",
                        "game_type": player.current_game,
                        "players_connected": len(self.games[player.current_game]["players"]),
                        "tournament_started": False,
                        "waiting_for_start": True
                    })
                    
        except asyncio.CancelledError:
            # Task was cancelled, exit gracefully
            pass
        except Exception as e:
            # Log error but don't crash the heartbeat
            pass
    
    async def handle_message(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a message from a client."""
        msg_type = message.get("message")
        self.debug_print(f"Received message from {player.name}: {msg_type}")
        
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
                "config": self.game_configs[game_type],
                "tournament_started": False
            }
        
        self.games[game_type]["players"].append(player)
        player.current_game = game_type
        
        await self.send_message(player.writer, {
            "message": "joined_game",
            "game_type": game_type,
            "position": len(self.games[game_type]["players"])
        })
        
        # Print player join status for TA
        current_players = len(self.games[game_type]["players"])
        print(f"Player {player.name} joined {game_type} game! ({current_players} players total)", flush=True)
        self.debug_print(f"Player {player.name} joined {game_type} game (position {current_players})")
        
        # Inform player about tournament status
        await self.send_message(player.writer, {
            "message": "tournament_status",
            "game_type": game_type,
            "players_connected": len(self.games[game_type]["players"]),
            "tournament_started": self.games[game_type]["tournament_started"],
            "waiting_for_start": True
        })
    
    async def handle_get_action(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a get_action request (legacy support)."""
        # This is handled in the game loop, but we keep it for compatibility
        pass
    
    async def handle_ready_next_round(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a ready_next_round message."""
        # This is handled in the game loop, but we keep it for compatibility
        pass
    

    
    async def start_tournament(self, game_type: str):
        """Start a tournament with all connected players."""
        self.debug_print(f"start_tournament called for {game_type}")
        game_data = self.games[game_type]
        print(f"Game data: {game_data}")
        players = game_data["players"]
        
        self.debug_print(f"Game data: {game_data}")
        self.debug_print(f"Players: {[p.name for p in players]}")
        
        if len(players) < 2:
            self.logger.warning(f"Not enough players to start tournament: {len(players)}")
            self.debug_print(f"Not enough players ({len(players)}), cannot start tournament")
            return
        
        if game_data["tournament_started"]:
            self.logger.warning(f"Tournament already started for {game_type}")
            self.debug_print(f"Tournament already started, cannot start again")
            return
        
        print(f"Starting tournament for {game_type} with {len(players)} players!", flush=True)
        self.debug_print(f"Setting tournament_started to True")
        game_data["tournament_started"] = True
        
        # Announce tournament start to all players
        self.debug_print(f"Announcing tournament start to players")
        for player in players:
            await self.send_message(player.writer, {
                "message": "tournament_start",
                "game_type": game_type,
                "num_players": len(players),
                "num_rounds": game_data["config"]["num_rounds"],
                "players": [p.name for p in players]
            })
        
        # Start lab tournament loop
        self.debug_print(f"Creating tournament task")
        self.debug_print(f"Current event loop: {asyncio.get_running_loop()}")
        task = asyncio.create_task(self.run_lab(game_type, players))
        self.debug_print(f"Tournament task created: {task}")
        self.debug_print(f"Task done: {task.done()}")
        self.debug_print(f"Task pending: {not task.done()}")
    








    async def run_lab(self, game_type: str, players: List[PlayerConnection]):
        """Run a lab tournament using LocalArena in a separate thread."""
        self.debug_print(f"==========================================")
        self.debug_print(f"run_lab called for {game_type} with {len(players)} players")
        self.debug_print(f"==========================================")
        
        try:
            print(f"TOURNAMENT {game_type} started with {len(players)} players", flush=True)
            
            # Convert PlayerConnections to NetworkAgents
            from server.network_agent import NetworkAgent
            agents = [NetworkAgent(player.name, player) for player in players]
            
            # Get game class and configuration
            game_data = self.game_configs[game_type]
            game_class = game_data["game_class"]
            num_rounds = game_data["num_rounds"]
            num_agents_per_game = game_data["num_players"]
            
            # Create LocalArena
            from core.local_arena import LocalArena
            arena = LocalArena(
                game_class=game_class,
                agents=agents,
                num_agents_per_game=num_agents_per_game,
                num_rounds=num_rounds,
                timeout=30.0,
                save_results=False,  # Server handles result saving
                verbose=True
            )
            
            # Run tournament synchronously in the main thread
            print(f"Running tournament with LocalArena...", flush=True)
            results_df = arena.run_tournament()
            
            # Send results to clients
            await self._send_tournament_results(players, results_df, arena.agent_stats)
            
            print(f"TOURNAMENT {game_type} ended.", flush=True)
            
        except Exception as e:
            self.logger.error(f"error running {game_type} tournament: {e}")
            self.debug_print(f"Exception in tournament: {e}")
            print(f"error running {game_type} tournament: {e}")
            await self._send_tournament_error(players, str(e))
        finally:
            self.debug_print(f"==========================================")
            self.debug_print(f"run_lab method completed for {game_type}")
            self.debug_print(f"==========================================")
    
















    
    async def _send_tournament_results(self, players: List[PlayerConnection], results_df, agent_stats: Dict):
        """Send tournament results to all players."""
        for player in players:
            try:
                # Get player's stats from results
                player_stats = agent_stats.get(player.name, {})
                
                await self.send_message(player.writer, {
                    "message": "tournament_complete",
                    "results": {
                        "total_score": player_stats.get("total_score", 0),
                        "average_score": player_stats.get("average_score", 0),
                        "wins": player_stats.get("wins", 0),
                        "losses": player_stats.get("losses", 0),
                        "ties": player_stats.get("ties", 0),
                        "win_rate": player_stats.get("win_rate", 0)
                    }
                })
            except Exception as e:
                self.debug_print(f"Failed to send results to {player.name}: {e}")
    
    async def _send_tournament_error(self, players: List[PlayerConnection], error_message: str):
        """Send tournament error to all players."""
        for player in players:
            try:
                await self.send_message(player.writer, {
                    "message": "tournament_error",
                    "error": error_message
                })
            except Exception as e:
                self.debug_print(f"Failed to send error to {player.name}: {e}")
    
    
    

    
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
            # Sending message to client - no logging needed
            writer.write(data)
            await writer.drain()
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def receive_message(self, reader: asyncio.StreamReader, player: Optional[PlayerConnection] = None) -> Optional[Dict[str, Any]]:
        """Receive a message from a client."""
        try:
            if player and player.read_lock:
                async with player.read_lock:
                    data = await reader.readline()
                    if not data:
                        return None
                    decoded_data = data.decode().strip()
                    if not decoded_data:
                        return None
                    try:
                        msg = json.loads(decoded_data)
                        return msg
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error from {player.name if player else 'unknown'}: {e}")
                        print(f"Raw data: {repr(decoded_data)}")
                        return None
            else:
                data = await reader.readline()
                if not data:
                    return None
                decoded_data = data.decode().strip()
                if not decoded_data:
                    return None
                try:
                    msg = json.loads(decoded_data)
                    return msg
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Raw data: {repr(decoded_data)}")
                    return None
        except Exception as e:
            print(f"Error receiving message: {e}")
        return None
    
    
    async def start(self):
        """Start the server."""
        try:

            debug_print(f"Attempting to start server on {self.host}:{self.port}")
            debug_print(f"Allowed games: {self.allowed_games}")
            debug_print(f"Game configs: {list(self.game_configs.keys())}")
            
            server = await asyncio.start_server(
                self.handle_client,
                self.host,
                self.port
            )
            
            print(f"AGT Tournament Server")
            print("=====================", flush=True)
            print(f"Server running on {self.host}:{self.port}", flush=True)
            if self.allowed_games is not None:
                print(f"Game restrictions: {', '.join(self.allowed_games)}", flush=True)
            else:
                print("No game restrictions: all games available", flush=True)
            print("Commands:", flush=True)
            print("  Ctrl+Z                - Start tournaments", flush=True)
            print("  Ctrl+C                - Exit server", flush=True)
            print("", flush=True)
            print("Waiting for players to connect...", flush=True)
            
            async with server:
                await server.serve_forever()
                
        except Exception as e:
            print(f"[ERROR] Failed to start AGT server: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            raise
    
    def save_results(self):
        """Save game results to file."""
        if self.results:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"results/agt_server_results_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
            
            print(f"Results saved to {filename}")


async def main():
    """Main server function."""
    parser = argparse.ArgumentParser(description='AGT Server for Lab Competitions')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--config', type=str, help='Configuration file (required if no game specified)')
    parser.add_argument('--game', type=str, choices=['rps', 'bos', 'bosii', 'chicken', 'pd', 'lemonade', 'auction', 'adx_twoday', 'adx_oneday'],
                       help='Restrict server to a specific game type (required if no config specified)')
    parser.add_argument('--games', type=str, nargs='+', 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'pd', 'lemonade', 'auction', 'adx_twoday', 'adx_oneday'],
                       help='Restrict server to specific game types (multiple allowed, required if no config specified)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose debug output (shows all debug messages)')
    # Dashboard is now separate - run with: python dashboard/app.py

    
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
    
    # Require either a config file or game specification
    if not args.config and not args.game and not args.games:
        print("ERROR: Server requires either a config file (--config) or game specification (--game or --games)")
        print("This ensures all players join the same server with the same game type.")
        print("Example: python server.py --game rps")
        print("Example: python server.py --config lab01_rps.json")
        return
    
    # Set allowed games based on command line arguments
    if args.game:
        config["allowed_games"] = [args.game]
        print(f"server restricted to game: {args.game}")
    elif args.games:
        config["allowed_games"] = args.games
        print(f"server restricted to games: {', '.join(args.games)}")
    elif args.config:
        # If config file is provided but no games specified, require games in config
        if "allowed_games" not in config:
            print("ERROR: Config file must specify 'allowed_games'")
            print("Example config: {\"allowed_games\": [\"rps\"]}")
            return
    
    server = AGTServer(config, args.host, args.port, args.verbose)
    
    # Flag to track if tournaments have been started
    tournaments_started = False
    
    async def start_tournaments():
        """Start tournaments for all active games."""
        # Start tournaments for all games that have players
        for game_type, game_data in server.games.items():
            if len(game_data["players"]) >= 2 and not game_data["tournament_started"]:
                print(f"Starting tournament for {game_type} with {len(game_data['players'])} players")
                await server.start_tournament(game_type)
        
        # Wait for all tournaments to complete
        while any(game_data["tournament_started"] for game_data in server.games.values()):
            await asyncio.sleep(1)
        
        print("All tournaments completed!")
        server.save_results()
    
    def signal_handler(signum, frame):
        nonlocal tournaments_started
        if signum == signal.SIGTSTP:
            # SIGTSTP (Ctrl+Z) = Start tournaments
            if not tournaments_started:
                print("\nStarting tournaments for all active games...")
                tournaments_started = True
                # Schedule tournament start in the event loop
                asyncio.create_task(start_tournaments())
        elif signum == signal.SIGINT:
            # SIGINT (Ctrl+C) = Exit server
            print("\nShutting down server...")
            server.save_results()
            sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGTSTP, signal_handler)  # Start tournaments (Ctrl+Z)
    signal.signal(signal.SIGINT, signal_handler)   # Exit server (Ctrl+C)
    
    print("AGT Tournament Server")
    print("=====================")
    print("Commands:")
    print("  Ctrl+Z                - Start tournaments")
    print("  Ctrl+C                - Exit server")
    print("")
    print("Dashboard: Run 'python dashboard/app.py' in a separate terminal")
    print("")
    
    try:
        # Dashboard is now separate - run with: python dashboard/app.py
        
        # Start server
        print(f"[DEBUG] Creating server task...")
        server_task = asyncio.create_task(server.start())
        
        # Wait for manual interrupt to start tournaments
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        server.save_results()
        raise


if __name__ == "__main__":
    asyncio.run(main()) 