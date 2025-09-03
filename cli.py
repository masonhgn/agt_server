#!/usr/bin/env python3
"""
AGT Server Command Line Interface

Provides easy command-line access to start the AGT server and dashboard.
"""

import argparse
import sys
import os
import asyncio
import threading
import time
from pathlib import Path

# Add the current directory to the path to import local modules
sys.path.insert(0, os.path.dirname(__file__))

def run_server():
    """Entry point for the agt-server command."""
    parser = argparse.ArgumentParser(
        description="Start the AGT tournament server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agt-server                    # Start with default settings
  agt-server --port 8080       # Start on specific port
  agt-server --game rps        # Start with specific game type
  agt-server --verbose         # Enable verbose logging
  agt-server --config config.json  # Use custom config file
        """
    )
    
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8080,
        help="Port to bind to (default: 8080)"
    )
    parser.add_argument(
        "--game", 
        choices=["rps", "bos", "bosii", "chicken", "pd", "lemonade", "auction", "adx2d", "adx1d"],
        default="rps",
        help="Game type to run (default: rps)"
    )
    parser.add_argument(
        "--num-rounds", 
        type=int, 
        default=100,
        help="Number of rounds per game (default: 100)"
    )
    parser.add_argument(
        "--num-players", 
        type=int, 
        default=2,
        help="Number of players per game (default: 2)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--config", 
        type=str,
        help="Path to custom configuration file"
    )
    
    args = parser.parse_args()
    
    # Import here to avoid circular imports
    from .server.server import AGTServer
    
    # Create configuration
    config = {
        "game_type": args.game,
        "num_rounds": args.num_rounds,
        "num_players": args.num_players,
        "allowed_games": [args.game] if args.game else None,
        "verbose": args.verbose
    }
    
    # Load custom config if provided
    if args.config:
        import json
        try:
            with open(args.config, 'r') as f:
                custom_config = json.load(f)
                config.update(custom_config)
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)
    
    print(f"Starting AGT Server...")
    print(f"  Host: {args.host}")
    print(f"  Port: {args.port}")
    print(f"  Game: {args.game}")
    print(f"  Rounds: {args.num_rounds}")
    print(f"  Players: {args.num_players}")
    print(f"  Verbose: {args.verbose}")
    print("-" * 50)
    
    try:
        # Create and start server
        server = AGTServer(config, host=args.host, port=args.port, verbose=args.verbose)
        
        # Run the server
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

def run_dashboard():
    """Entry point for the agt-dashboard command."""
    parser = argparse.ArgumentParser(
        description="Start the AGT dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agt-dashboard                    # Start with default settings
  agt-dashboard --port 8081       # Start on specific port
  agt-dashboard --server-port 8080  # Connect to server on specific port
        """
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8081,
        help="Dashboard port (default: 8081)"
    )
    parser.add_argument(
        "--server-port", 
        type=int, 
        default=8080,
        help="AGT server port to connect to (default: 8080)"
    )
    parser.add_argument(
        "--host", 
        default="localhost",
        help="Dashboard host (default: localhost)"
    )
    parser.add_argument(
        "--server-host", 
        default="localhost",
        help="AGT server host (default: localhost)"
    )
    
    args = parser.parse_args()
    
    # Set environment variables for the dashboard
    os.environ['AGT_SERVER_HOST'] = args.server_host
    os.environ['AGT_SERVER_PORT'] = str(args.server_port)
    os.environ['DASHBOARD_PORT'] = str(args.port)
    
    print(f"Starting AGT Dashboard...")
    print(f"  Dashboard: http://{args.host}:{args.port}")
    print(f"  Server: {args.server_host}:{args.server_port}")
    print("-" * 50)
    
    try:
        # Import and run the dashboard
        from .dashboard.app import app
        
        app.run(
            host=args.host,
            port=args.port,
            debug=False,
            use_reloader=False
        )
        
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        sys.exit(1)

def run_both():
    """Entry point for running both server and dashboard together."""
    parser = argparse.ArgumentParser(
        description="Start both AGT server and dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agt-both                    # Start both with default settings
  agt-both --server-port 8080 --dashboard-port 8081
        """
    )
    
    parser.add_argument(
        "--server-port", 
        type=int, 
        default=8080,
        help="Server port (default: 8080)"
    )
    parser.add_argument(
        "--dashboard-port", 
        type=int, 
        default=8081,
        help="Dashboard port (default: 8081)"
    )
    parser.add_argument(
        "--game", 
        choices=["rps", "bos", "bosii", "chicken", "pd", "lemonade", "auction", "adx2d", "adx1d"],
        default="rps",
        help="Game type to run (default: rps)"
    )
    
    args = parser.parse_args()
    
    print(f"Starting AGT Server and Dashboard...")
    print(f"  Server Port: {args.server_port}")
    print(f"  Dashboard Port: {args.dashboard_port}")
    print(f"  Game: {args.game}")
    print("-" * 50)
    
    # Start server in background thread
    def start_server():
        os.environ['AGT_SERVER_HOST'] = 'localhost'
        os.environ['AGT_SERVER_PORT'] = str(args.server_port)
        
        from .server.server import AGTServer
        config = {"game_type": args.game, "num_rounds": 100, "num_players": 2}
        server = AGTServer(config, port=args.server_port)
        asyncio.run(server.run())
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Start dashboard
    try:
        os.environ['AGT_SERVER_HOST'] = 'localhost'
        os.environ['AGT_SERVER_PORT'] = str(args.server_port)
        os.environ['DASHBOARD_PORT'] = str(args.dashboard_port)
        
        from .dashboard.app import app
        app.run(host='localhost', port=args.dashboard_port, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "both":
        sys.argv.pop(1)
        run_both()
    elif len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        sys.argv.pop(1)
        run_dashboard()
    else:
        run_server()
