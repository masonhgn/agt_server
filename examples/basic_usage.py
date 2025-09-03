#!/usr/bin/env python3
"""
Basic Usage Example for AGT Server

This example demonstrates how to use the AGT Server package
to run a simple tournament.
"""

import asyncio
import time
from agt_server import AGTServer

async def run_basic_tournament():
    """Run a basic RPS tournament."""
    
    # Configuration for the tournament
    config = {
        "game_type": "rps",
        "num_rounds": 50,
        "num_players": 2,
        "verbose": True
    }
    
    print("Starting AGT Server Basic Tournament Example")
    print("=" * 50)
    print(f"Game: {config['game_type']}")
    print(f"Rounds: {config['num_rounds']}")
    print(f"Players: {config['num_players']}")
    print("=" * 50)
    
    # Create server instance
    server = AGTServer(
        config=config,
        host="localhost",
        port=8080,
        verbose=True
    )
    
    try:
        # Start the server
        print("Starting server...")
        await server.run()
        
    except KeyboardInterrupt:
        print("\nTournament interrupted by user")
    except Exception as e:
        print(f"Error running tournament: {e}")
    finally:
        print("Tournament finished")

def run_with_python_api():
    """Example of using the Python API directly."""
    
    print("\nPython API Example")
    print("=" * 30)
    
    # Import specific game classes
    from agt_server import RPSGame, BOSGame
    
    # Create a game instance
    rps_game = RPSGame(num_rounds=10)
    print(f"Created {rps_game.__class__.__name__} with {rps_game.num_rounds} rounds")
    
    # You can also create other game types
    bos_game = BOSGame(num_rounds=20)
    print(f"Created {bos_game.__class__.__name__} with {bos_game.num_rounds} rounds")

if __name__ == "__main__":
    print("AGT Server Basic Usage Examples")
    print("=" * 40)
    
    # Example 1: Python API usage
    run_with_python_api()
    
    # Example 2: Run a tournament (uncomment to run)
    # asyncio.run(run_basic_tournament())
    
    print("\nExamples completed!")
    print("\nTo run a full tournament, uncomment the last line in the script.")
    print("Or use the command line tools:")
    print("  agt-server --game rps --verbose")
    print("  agt-dashboard --port 8081")
