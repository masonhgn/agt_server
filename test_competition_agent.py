#!/usr/bin/env python3
"""
Test script to test the lab01 competition agent with the server
"""

import asyncio
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from client import AGTClient
from adapters import load_agent_from_stencil


async def main():
    """Test the lab01 competition agent with the server."""
    
    print("Testing Lab01 Competition Agent with AGT Server")
    print("=" * 50)
    
    try:
        # Load agent from stencil
        stencil_path = "stencils/lab01_stencil/competition_agent.py"
        print(f"Loading agent from {stencil_path}...")
        
        agent = load_agent_from_stencil(stencil_path, "rps")
        agent.name = "TestCompetition"
        
        print(f"Successfully loaded agent: {agent.name}")
        print(f"Game type: rps")
        
        # Create client and connect
        print(f"Connecting to server at localhost:8080...")
        client = AGTClient(agent, "localhost", 8080)
        await client.connect()
        
        if client.connected:
            print("Connected to server!")
            print("Joining rps game...")
            
            if await client.join_game("rps"):
                print("Joined game successfully!")
                print("Waiting for game to start...")
                await client.run()
            else:
                print("Failed to join game")
        else:
            print("Failed to connect to server")
            print("Make sure the server is running with: python server/server.py --config server/configs/lab01_rps.json")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
