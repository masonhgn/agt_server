#!/usr/bin/env python3
"""
Connect Stencil to AGT Server

This script allows students to easily connect their completed stencils to the AGT server
for competitions and testing.
"""

import asyncio
import argparse
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from client import AGTClient
from adapters import load_agent_from_stencil


async def connect_agent_to_server(agent, game_type: str, name: str = None, 
                                 host: str = 'localhost', port: int = 8080, 
                                 verbose: bool = False):
    """
    Connect an agent to the AGT server.
    
    Args:
        agent: The agent to connect
        game_type: Type of game to join
        name: Agent name (optional)
        host: Server host
        port: Server port
        verbose: Enable verbose output
    
    Returns:
        bool: True if connection and game join successful, False otherwise
    """
    try:
        # Set name if provided
        if name:
            agent.name = name
        
        print(f"Connecting agent: {agent.name}")
        print(f"Game type: {game_type}")
        
        # Create client and connect
        print(f"Connecting to server at {host}:{port}...")
        client = AGTClient(agent, host, port, verbose=verbose)
        await client.connect()
        
        if client.connected:
            await client.run()
            return True
        else:
            print("Failed to connect to server")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False


async def main():
    """Main function for connecting a stencil to the server."""
    parser = argparse.ArgumentParser(description='Connect Stencil to AGT Server')
    parser.add_argument('--stencil', type=str, required=True, 
                       help='Path to completed stencil file (e.g., lab01_stencil/fictitious_play.py)')
    parser.add_argument('--game', type=str, required=True,
                       choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='Game type to play')
    parser.add_argument('--name', type=str, help='Agent name (optional, defaults to stencil name)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    
    args = parser.parse_args()
    
    # Validate stencil file exists
    if not os.path.exists(args.stencil):
        print(f"Error: Stencil file not found: {args.stencil}")
        sys.exit(1)
    
    try:
        # Load agent from stencil
        print(f"Loading agent from {args.stencil}...")
        agent = load_agent_from_stencil(args.stencil, args.game)
        
        print(f"Successfully loaded agent: {agent.name}")
        
        # Connect agent to server
        success = await connect_agent_to_server(
            agent, args.game, args.name, args.host, args.port, args.verbose
        )
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 