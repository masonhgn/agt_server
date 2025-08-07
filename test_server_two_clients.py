#!/usr/bin/env python3
"""
Test script to run two lab01 clients simultaneously to test the server
"""

import asyncio
import sys
import os
import time

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from client import AGTClient
from adapters import load_agent_from_stencil


async def run_client(client_id: int, agent_name: str):
    """Run a single client."""
    try:
        # Load agent from stencil
        stencil_path = "stencils/lab01_stencil/example_solution.py"
        print(f"[Client {client_id}] Loading agent from {stencil_path}...")
        
        agent = load_agent_from_stencil(stencil_path, "rps")
        agent.name = f"{agent_name}_{client_id}"
        
        print(f"[Client {client_id}] Successfully loaded agent: {agent.name}")
        
        # Create client and connect
        print(f"[Client {client_id}] Connecting to server at localhost:8080...")
        client = AGTClient(agent, "localhost", 8080)
        await client.connect()
        
        if client.connected:
            print(f"[Client {client_id}] Connected to server!")
            print(f"[Client {client_id}] Joining rps game...")
            
            if await client.join_game("rps"):
                print(f"[Client {client_id}] Joined game successfully!")
                print(f"[Client {client_id}] Waiting for game to start...")
                await client.run()
            else:
                print(f"[Client {client_id}] Failed to join game")
        else:
            print(f"[Client {client_id}] Failed to connect to server")
            
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run two clients simultaneously."""
    
    print("Testing Lab01 Example Solution with Two Clients")
    print("=" * 55)
    
    # Start two clients simultaneously
    client1_task = asyncio.create_task(run_client(1, "TestExampleFP"))
    client2_task = asyncio.create_task(run_client(2, "TestExampleFP"))
    
    # Wait for both clients to complete
    await asyncio.gather(client1_task, client2_task)
    
    print("\nTest completed!")


if __name__ == "__main__":
    asyncio.run(main())
