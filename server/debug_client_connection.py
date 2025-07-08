#!/usr/bin/env python3
"""
debug connection script

this script helps debug the connection issues between client and server.
"""

import asyncio
import json
import sys
import os

# add the server directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from client import AGTAgent, AGTClient


class DebugAgent(AGTAgent):
    """debug agent that prints all messages."""
    
    def get_action(self, observation):
        print(f"debug: get_action called with observation: {observation}")
        return 0


async def debug_connection():
    """debug the connection process step by step."""
    print("=== debug connection ===")
    
    # create debug agent
    agent = DebugAgent("debugagent")
    
    # create client
    client = AGTClient(agent, "localhost", 8080)
    
    print("1. attempting to connect...")
    await client.connect()
    
    if not client.connected:
        print("FAIL: connection failed")
        return
    
    print("2. connection successful, attempting to join rps game...")
    
    success = await client.join_game("rps")
    if not success:
        print("FAIL: failed to join game")
        return
    
    print("3. successfully joined game, waiting for messages...")
    
    # wait for a few messages
    try:
        await asyncio.wait_for(client.run(), timeout=10.0)
    except asyncio.TimeoutError:
        print("4. timeout reached, disconnecting...")
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(debug_connection()) 