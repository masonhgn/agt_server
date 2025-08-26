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
        
        # Set name if provided
        if args.name:
            agent.name = args.name
        
        print(f"Successfully loaded agent: {agent.name}")
        print(f"Game type: {args.game}")
        
        # Create client and connect
        print(f"Connecting to server at {args.host}:{args.port}...")
        client = AGTClient(agent, args.host, args.port, verbose=args.verbose)
        await client.connect()
        
        if client.connected:
            print("Connected to server!")
            print(f"Joining {args.game} game...")
            
            if await client.join_game(args.game):
                print("Joined game successfully!")
                print("Waiting for game to start...")
                await client.run()
            else:
                print("Failed to join game")
        else:
            print("Failed to connect to server")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 