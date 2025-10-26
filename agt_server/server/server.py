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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dashboard'))
from binary_encoding import (
    encode_player_connect, encode_player_disconnect, 
    encode_tournament_start, encode_tournament_end,
    encode_results_saved
)
import signal
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Dashboard is now separate - no longer integrated

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.utils import server_print




@dataclass
class PlayerConnection:
    """Represents a connected player."""
    name: str
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    address: Tuple[str, int]
    device_id: str
    connected_at: float
    pending_action: Optional[Any] = None
    total_reward: float = 0.0
    games_played: int = 0
    


class AGTServer:
    """Modern AGT Server for lab competitions."""
    
    def __init__(self, config: Dict[str, Any], host: str = "0.0.0.0", port: int = 8080):
        self.server_config = config
        self.host = host
        self.port = port
        
        #server metadata
        self.players: Dict[str, PlayerConnection] = {} #dictionary of player names to player objects
        self.game_config = None #the config with params for the game
        self.tournament_started = False
        self.results: List[Dict[str, Any]] = []

        

        #set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            stream=sys.stdout  # Force logging to stdout for dashboard capture
        )
        self.logger = logging.getLogger(__name__)
        
        #create results directory if it doesn't exist
        os.makedirs("results", exist_ok=True)
        
        #load all game configs so that we can select any game we want
        all_game_configs = self._load_game_configs()
        
        # Set up single game configuration
        allowed_game = config.get("game_title", None)
        if allowed_game is None:
            raise ValueError("Server requires exactly a game type to be specified")
        print(type(allowed_game))
        print(allowed_game)
        if allowed_game not in all_game_configs:
            raise ValueError(f"Unknown game type: {allowed_game}")
        
        self.game_config = all_game_configs[allowed_game]
    
    def _load_game_configs(self):
        """Load game configurations from config files."""
        game_configs = {}
        

        from core.game.RPSGame import RPSGame
        from core.game.BOSGame import BOSGame
        from core.game.BOSIIGame import BOSIIGame
        from core.game.ChickenGame import ChickenGame
        from core.game.PDGame import PDGame
        from core.game.LemonadeGame import LemonadeGame
        from core.game.AuctionGame import AuctionGame
        from core.game.AdxTwoDayGame import AdxTwoDayGame
        from core.game.AdxOneDayGame import AdxOneDayGame
        
        # map class names to actual classes
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
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                
                # extract game information from config - fail loudly if missing
                game_class_name = config_data['game_class']
                game_class = class_map[game_class_name]
                
                # Create game config for each allowed game
                for game_type in config_data['allowed_games']:
                    game_configs[game_type] = {
                        "name": config_data['name'],
                        "game_class": game_class,
                        "num_players": config_data['num_players'],
                        "num_rounds": config_data['num_rounds'],
                        "description": config_data['description']
                    }
        
        return game_configs
    
    def server_print(self, message: str, flush: bool = True):
        """Unified print method for all server output."""
        print(f"[SERVER] {message}", flush=flush)
    
    





    async def handle_new_client_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """WHEN A NEW PLAYER JOINS THE SERVER, THIS FUNCTION IS CALLED"""
        address = writer.get_extra_info('peername')
        player_name = None
        
        self.server_print(f"New client connection from {address}")
        
        try:
            # Request device id
            await self.send_message(writer, {"message": "request_client_info"})
            client_info = await self.receive_message(reader)
            
            if not client_info or client_info.get("message") != "provide_client_info":
                print(f"Invalid client info response from {address}")
                return
            
            device_id = client_info.get("device_id", f"device_{address[0]}_{address[1]}")
            player_game_type = client_info.get("game_type",None)
            player_name = client_info.get("player_name",None)
            


            #validate player name
            if not player_name:
                print(f"Invalid name response from {address}")
                await self.send_message(writer, {
                    "message": "error",
                    "error": "no name or invalid name provided",
                })

                return

            #validate game type
            if not player_game_type or player_game_type != self.server_config["game_title"]:
                self.server_print(f"Invalid game type response from {address}")
                await self.send_message(writer, {
                    "message": "error",
                    "error": "wrong game type provided",
                })

                return
            

            
            # handle duplicate names
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
            )
            
            self.players[player_name] = player
            
            # Send confirmation with only the single allowed game
            await self.send_message(writer, {
                "message": "connection_established",
                "assigned_name": player_name,
            })
            




            #print out saying the player connected successfully
            if player_name == original_name:
                print(f"Player '{player_name}' connected from {address[0]}:{address[1]} (no name conflicts)", flush=True)
                print(encode_player_connect(player_name, f"{address[0]}:{address[1]}"), flush=True)
                self.server_print(f"Player '{player_name}' connected successfully")
            else:
                print(f"Player '{player_name}' connected from {address[0]}:{address[1]} (resolved from '{original_name}')", flush=True)
                print(encode_player_connect(player_name, f"{address[0]}:{address[1]}"), flush=True)
                self.server_print(f"Player '{player_name}' connected with name conflict resolution")
            



            # Client is now connected and ready for tournament
            # Keep connection alive by waiting for tournament to start
            self.server_print(f"[DEBUG] Player '{player_name}' is waiting for tournament to start...")
            self.server_print(f"[DEBUG] Current tournament_started flag: {self.tournament_started}")
            
            # Send a waiting message to the client
            self.server_print(f"[DEBUG] Sending waiting message to {player_name}")
            await self._send_waiting_message(player)
            self.server_print(f"[DEBUG] Waiting message sent to {player_name}")
            
            # Wait for tournament to start (this will be set by the signal handler)
            self.server_print(f"[DEBUG] Entering wait loop for {player_name}")
            loop_count = 0
            while not self.tournament_started:
                loop_count += 1
                if loop_count % 100 == 0:  # Print every 10 seconds (100 * 0.1s)
                    self.server_print(f"[DEBUG] Still waiting for tournament... loop {loop_count}, flag: {self.tournament_started}")
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
            
            self.server_print(f"[DEBUG] Tournament started! Player '{player_name}' will participate.")
            
            # Keep the connection alive during the tournament
            # The tournament will communicate with this client through the Engine
            self.server_print(f"[DEBUG] Keeping connection alive for {player_name} during tournament")
            
            # Listen for messages during the tournament
            while self.tournament_started:
                try:
                    # Try to receive a message with a short timeout
                    message = await asyncio.wait_for(
                        self.receive_message(player.reader, player), 
                        timeout=0.1
                    )
                    if message:
                        self.server_print(f"[DEBUG] Received message for {player_name} during tournament: {message.get('message', 'unknown')}")
                        # Handle the message (this will be processed by the Engine)
                        await self.handle_message(player, message)
                except asyncio.TimeoutError:
                    # No message received, continue waiting
                    pass
                except Exception as e:
                    self.server_print(f"[DEBUG] Error receiving message for {player_name}: {e}")
                    break
            
            self.server_print(f"[DEBUG] Tournament completed for {player_name}")
            
        except Exception as e:
            print(f"Error handling client {address}: {e}")

        finally:
            #at this point the player has disconnected from the server, so we need to remove them from the game they were in if they were in one


            player = self.players[player_name] #get current player

            print(f"Player {player_name} disconnected from the server, {len(self.players)} players left", flush=True)
            print(encode_player_disconnect(player_name, len(self.players)), flush=True)

            del self.players[player_name]

            #close the connection to the player
            writer.close()
            await writer.wait_closed()
    








    async def client_loop(self, player: PlayerConnection):
        """THIS IS HOW WE COMMUNICATE WITH PLAYERS CURRENTLY CONNECTED TO THE SERVER"""
        try:
            
            while True:

                #wait for a message from the client

                #we just received a message from the client
                message = await self.receive_message(player.reader, player)
                if not message:
                    break
                
                #handle the message
                await self.handle_message(player, message)
                
        except Exception as e:
            self.server_print(f"error in client loop for {player.name}: {e}")

    






    
    async def handle_message(self, player: PlayerConnection, message: Dict[str, Any]):
        """Handle a message from a client."""
        msg_type = message.get("message")
        self.server_print(f"Received message from {player.name}: {msg_type}")
        
        
        if msg_type == "action":
            # Store the action for the current round
            player.pending_action = message.get("action")

        else:
            self.server_print(f"unknown message type from {player.name}: {msg_type}")
    



    # async def handle_join_game(self, player: PlayerConnection, message: Dict[str, Any]):
    #     """Handle a player joining a game."""
    #     game_type = message.get("game_type")
    #     expected_game_type = self.game_config["name"]
        
    #     if game_type != expected_game_type:
    #         await self.send_message(player.writer, {
    #             "message": "error",
    #             "error": f"This server only supports '{expected_game_type}'. You requested: {game_type}"
    #         })
    #         return
        
    #     # Check if player is already in a game
    #     if player.current_game:
    #         await self.send_message(player.writer, {
    #             "message": "error",
    #             "error": "Already in a game"
    #         })
    #         return
        
    #     # Player is already in self.players, just mark them as in game
    #     player.current_game = expected_game_type
        
    #     await self.send_message(player.writer, {
    #         "message": "joined_game",
    #         "game_type": expected_game_type,
    #         "position": len(self.players)
    #     })
        
    #     # Print player join status for TA
    #     current_players = len(self.players)
    #     print(f"Player {player.name} joined {expected_game_type} game! ({current_players} players total)", flush=True)
    #     self.debug_print(f"Player {player.name} joined {expected_game_type} game (position {current_players})")
        
    #     # Inform player about tournament status
    #     await self.send_message(player.writer, {
    #         "message": "tournament_status",
    #         "game_type": expected_game_type,
    #         "players_connected": len(self.players),
    #         "tournament_started": self.tournament_started,
    #         "waiting_for_start": True
    #     })
    


    
    








    async def run_tournament(self):
        """Run a tournament with all connected players."""
        self.server_print(f"==========================================")
        self.server_print(f"run_tournament called with {len(self.players)} players")
        self.server_print(f"==========================================")
        

        game_title = self.game_config['name']
        self.tournament_started = True  # Set flag to enable timeouts
        self.server_print(f"TOURNAMENT {game_title} started with {len(self.players)} players")
        print(encode_tournament_start(game_title, len(self.players)), flush=True)
        
        # Get game class and configuration
        game_class = self.game_config["game_class"]
        num_rounds = self.game_config["num_rounds"]
        num_agents_per_game = self.game_config["num_players"]
        
        # Create LocalArena with PlayerConnection objects directly
        from core.local_arena import LocalArena
        print('creating local arena')
        arena = LocalArena(
            game_title=self.server_config["game_title"],
            game_class=game_class,
            agents=list(self.players.values()),  # Pass PlayerConnection objects directly
            num_agents_per_game=num_agents_per_game,
            num_rounds=num_rounds,
            timeout=30.0,
            save_results=False,  # Server handles result saving
            verbose=True
        )
        print('local arena created')
        
        # Run tournament asynchronously
        self.server_print(f"Running tournament with async LocalArena...")
        results_json = await arena.run_tournament_async()
        
        # Send results to clients
        await self._send_tournament_results(list(self.players.values()), results_json, arena.agent_stats)
        
        self.server_print(f"TOURNAMENT {game_title} ended.")
        print(encode_tournament_end(game_title), flush=True)
        
        # Reset tournament flag so client connections can complete
        self.tournament_started = False
        self.server_print(f"[DEBUG] Tournament flag reset to False")
        
        # except Exception as e:
        #     self.server_print(f"error running tournament: {e}")
        #     await self._send_tournament_error(list(self.players.values()), str(e))
        # finally:
        #     self.tournament_started = False  # Reset flag to disable timeouts
        #     self.server_print(f"==========================================")
        #     self.server_print(f"run_tournament method completed")
        #     self.server_print(f"==========================================")

        self.tournament_started = False
    












        



















    
    async def _send_tournament_results(self, players: List[PlayerConnection], results_json, agent_stats: Dict):
        """Send tournament results to all players."""
        for player in players:
            try:
                await self.send_message(player.writer, {
                    "message": "tournament_complete",
                    "results": results_json
                })
            except Exception as e:
                self.server_print(f"Failed to send results to {player.name}: {e}")
    








    async def _send_tournament_error(self, players: List[PlayerConnection], error_message: str):
        """Send tournament error to all players."""
        for player in players:
            try:
                await self.send_message(player.writer, {
                    "message": "tournament_error",
                    "error": error_message
                })
            except Exception as e:
                self.server_print(f"Failed to send error to {player.name}: {e}")
    
    
    

    
    async def send_message(self, writer: asyncio.StreamWriter, message: Dict[str, Any]):
        """Send a message to a client."""
        try:

            # # Convert sets to lists for JSON serialization
            # def convert_sets(obj):
            #     if isinstance(obj, set):
            #         return list(obj)
            #     elif isinstance(obj, dict):
            #         return {k: convert_sets(v) for k, v in obj.items()}
            #     elif isinstance(obj, list):
            #         return [convert_sets(item) for item in obj]
            #     else:
            #         return obj
            # message = convert_sets(message)


            data = json.dumps(message).encode() + b'\n'
            # Sending message to client - no logging needed
            writer.write(data)
            await writer.drain()
        except Exception as e:
            print(f"Error sending message: {e}")

    async def _send_waiting_message(self, player: PlayerConnection):
        """Send a waiting message to a connected player."""
        try:
            self.server_print(f"[DEBUG] Creating waiting message for {player.name}")
            message = {
                "message": "waiting_for_tournament",
                "status": "connected",
                "message_text": "Connected to server. Waiting for tournament to start..."
            }
            self.server_print(f"[DEBUG] Sending waiting message to {player.name}: {message}")
            await self.send_message(player.writer, message)
            self.server_print(f"[DEBUG] Waiting message sent successfully to {player.name}")
        except Exception as e:
            self.server_print(f"[DEBUG] Error sending waiting message to {player.name}: {e}")
            print(f"Error sending waiting message to {player.name}: {e}")

    async def receive_message(self, reader: asyncio.StreamReader, player: Optional[PlayerConnection] = None) -> Optional[Dict[str, Any]]:
        """Receive a message from a client."""
        try:
            # Use different timeouts based on tournament state
            # Before tournament: long timeout (grace period for connection)
            # During tournament: short timeout (enforce responsiveness)
            timeout = 300.0 if not self.tournament_started else 10.0
            data = await asyncio.wait_for(reader.readline(), timeout=timeout)
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

            print(f"Attempting to start server on {self.host}:{self.port}")
            
            server = await asyncio.start_server(
                self.handle_new_client_connection,
                self.host,
                self.port
            )
            
            print(f"Server running on {self.host}:{self.port}", flush=True)
            print("Commands:", flush=True)
            print("  Ctrl+Z                - Start tournament", flush=True)
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
            print(encode_results_saved(filename), flush=True)


async def main():
    """Main server function."""
    parser = argparse.ArgumentParser(description='AGT Server for Lab Competitions')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--game', type=str, choices=['rps', 'bos', 'bosii', 'chicken', 'pd', 'lemonade', 'auction', 'adx_twoday', 'adx_oneday'],
                       help='Restrict server to a specific game type (required)')
    # Dashboard is now separate - run with: python dashboard/app.py

    
    args = parser.parse_args()
    
    # Default configuration
    config = {
        "server_name": "AGT Lab Server",
        "max_players": 50,
        "timeout": 300,
        "save_results": True
    }
    
    
    # Require either a config file or game specification
    if not args.game:
        print("ERROR: Server requires game specification --game")
        print("This ensures all players join the same server with the same game type.")
        print("Example: python server.py --game rps")
        return

    config["game_title"] = args.game
    print(f"server restricted to game: {args.game}")

    
    server = AGTServer(config, args.host, args.port)
    
    # Flag to track if tournament has been started
    tournament_started = False
    
    async def start_tournament():
        """Start tournament function for main."""
        nonlocal tournament_started
        print("\nStarting tournament...")
        tournament_started = True
        await server.run_tournament()

    
    def signal_handler(signum, frame):
        nonlocal tournament_started
        if signum == signal.SIGTSTP:
            # SIGTSTP (Ctrl+Z) = Start tournament
            print(f"[DEBUG] Signal handler called - tournament_started: {tournament_started}, server.tournament_started: {server.tournament_started}")
            if not tournament_started:
                print("\nStarting tournament...")
                tournament_started = True
                server.tournament_started = True  # Set instance variable too
                print(f"[DEBUG] Set both flags - tournament_started: {tournament_started}, server.tournament_started: {server.tournament_started}")
        elif signum == signal.SIGINT:
            # SIGINT (Ctrl+C) = Exit server
            print("\nShutting down server...")
            server.save_results()
            sys.exit(0)

    # Set up signal handlers
    signal.signal(signal.SIGTSTP, signal_handler)  # Start tournaments (Ctrl+Z)
    signal.signal(signal.SIGINT, signal_handler)   # Exit server (Ctrl+C)
    
    
    try:
        # Dashboard is now separate - run with: python dashboard/app.py
        
        # Start server
        print(f"[DEBUG] Creating server task...")
        server_task = asyncio.create_task(server.start())
        
        # Wait for manual interrupt to start tournaments
        tournament_task = None
        while True:
            await asyncio.sleep(1)
            # Check if tournament should be started
            if tournament_started and tournament_task is None:
                tournament_task = asyncio.create_task(start_tournament())
            elif tournament_task and tournament_task.done():
                break
            
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        import traceback
        traceback.print_exc()
        server.save_results()
        raise


if __name__ == "__main__":
    asyncio.run(main()) 