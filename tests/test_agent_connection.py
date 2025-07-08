#!/usr/bin/env python3
"""
test script for running two agents against each other.

this script demonstrates how to connect two agents to the server and run a game.
"""

import asyncio
import pytest

from server.client import AGTAgent, AGTClient


class SimpleAgent(AGTAgent):
    """simple agent that always plays the same action."""
    
    def __init__(self, name: str, action: int):
        super().__init__(name)
        self.action = action
    
    def get_action(self, observation):
        return self.action


@pytest.mark.asyncio
async def test_two_agents():
    """test running two agents against each other."""
    
    # create two simple agents
    agent1 = SimpleAgent("agent1", 0)  # always play rock
    agent2 = SimpleAgent("agent2", 1)  # always play paper
    
    # create clients
    client1 = AGTClient(agent1, "localhost", 8080)
    client2 = AGTClient(agent2, "localhost", 8080)
    
    print("connecting agents...")
    
    # connect both agents
    await client1.connect()
    await client2.connect()
    
    if not client1.connected or not client2.connected:
        print("failed to connect agents")
        return
    
    print("joining rps game...")
    
    # join the same game
    success1 = await client1.join_game("rps")
    success2 = await client2.join_game("rps")
    
    if not success1 or not success2:
        print("failed to join game")
        return
    
    print("running game...")
    
    # run both clients concurrently
    try:
        await asyncio.gather(client1.run(), client2.run())
    except Exception as e:
        print(f"error during game: {e}")
    
    # print results
    print(f"\nresults:")
    print(f"agent1 ({agent1.name}): total reward = {agent1.total_reward}")
    print(f"agent2 ({agent2.name}): total reward = {agent2.total_reward}")
    
    # clean up
    await client1.disconnect()
    await client2.disconnect()
    
    print("test completed")


if __name__ == "__main__":
    asyncio.run(test_two_agents()) 