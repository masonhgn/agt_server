#!/usr/bin/env python3
"""
Test script to verify example solution works with server.
"""

import asyncio
import sys
import os



from server.client import AGTAgent, AGTClient


class ExampleSolutionAgent(AGTAgent):
    """Example solution agent for testing."""
    
    def __init__(self, name: str = "ExampleSolution"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.opponent_action_counts = [0, 0, 0]
        self.action_history = []  # Track our actions
    
    def get_action(self, observation):
        """Return the best response to predicted opponent action."""
        # Simple strategy: play rock, paper, scissors in sequence
        if len(self.action_history) % 3 == 0:
            action = self.ROCK
        elif len(self.action_history) % 3 == 1:
            action = self.PAPER
        else:
            action = self.SCISSORS
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """Store the reward."""
        super().update(reward, info or {})
        print(f"Received reward: {reward}")


async def test_example_solution():
    """Test the example solution with the server."""
    print("Testing Example Solution with Server")
    print("=" * 50)
    
    # Create example solution agent
    agent = ExampleSolutionAgent("ExampleSolution")
    
    # Create client
    client = AGTClient(agent, "localhost", 8081)
    
    print("1. Connecting to server...")
    await client.connect()
    
    if not client.connected:
        print("FAIL: Failed to connect to server")
        return False
    
    print("2. Successfully connected to server")
    
    print("3. Joining RPS game...")
    success = await client.join_game("rps")
    
    if not success:
        print("FAIL: Failed to join game")
        await client.disconnect()
        return False
    
    print("4. Successfully joined RPS game")
    print("5. Running game...")
    
    # Run the game for a short time
    try:
        await asyncio.wait_for(client.run(), timeout=30.0)
    except asyncio.TimeoutError:
        print("6. Game timeout reached, disconnecting...")
        await client.disconnect()
        return True
    
    print("6. Game completed, disconnecting...")
    await client.disconnect()
    
    print("PASS: Example solution test completed successfully!")
    print(f"Agent total reward: {agent.total_reward}")
    print(f"Agent rounds played: {len(agent.action_history)}")
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_example_solution())
        if success:
            print("\n✅ SUCCESS: Example solution works correctly with server!")
        else:
            print("\n❌ FAIL: Example solution test failed!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc() 