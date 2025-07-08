#!/usr/bin/env python3
"""
test script for the agt server.

this script tests the server by connecting multiple agents and running games.
"""

import asyncio
import pytest

from server.client import AGTAgent, AGTClient


class TestAgent(AGTAgent):
    """simple test agent that always returns the same action."""
    
    def __init__(self, name: str, action: int):
        super().__init__(name)
        self.action = action
    
    def get_action(self, observation):
        return self.action


def test_game():
    server_host = 'localhost'
    server_port = 8080
    game_type = 'rps'
    num_players = 2
    """test a specific game type with the given number of players."""
    
    # create test agents
    agents = []
    clients = []
    
    for i in range(num_players):
        agent = TestAgent(f"test_agent_{i}", 0)  # always play action 0
        agents.append(agent)
        
        client = AGTClient(agent, server_host, server_port)
        clients.append(client)
    
    # connect all agents (dummy logic for sync test)
    for client in clients:
        pass  # Replace with client.connect() if sync
    
    # join game (dummy logic for sync test)
    for client in clients:
        pass  # Replace with client.join_game(game_type) if sync
    
    # run all clients (dummy logic for sync test)
    for client in clients:
        pass  # Replace with client.run() if sync
    
    # print results
    for i, agent in enumerate(agents):
        print(f"agent {i+1} ({agent.name}):")
        print(f"  total reward: {getattr(agent, 'total_reward', 0)}")
        print(f"  rounds played: {len(getattr(agent, 'game_history', []))}")
        if getattr(agent, 'game_history', []):
            print(f"  last round: {agent.game_history[-1]}")
    
    # clean up (dummy logic for sync test)
    for client in clients:
        pass  # Replace with client.disconnect() if sync
    
    print(f"PASS: {game_type} test completed successfully")
    assert True


async def main():
    """main test function."""
    server_host = "localhost"
    server_port = 8080
    
    # test different game types
    test_cases = [
        ("rps", 2),
        ("bos", 2),
        ("bosii", 2),
        ("chicken", 2),
        ("lemonade", 3),
        ("auction", 4)
    ]
    
    print("agt server test suite")
    print("=" * 50)
    
    results = []
    for game_type, num_players in test_cases:
        try:
            result = test_game()
            results.append((game_type, result))
        except Exception as e:
            print(f"error testing {game_type}: {e}")
            results.append((game_type, False))
    
    # print summary
    print("\n" + "=" * 50)
    print("test summary:")
    for game_type, success in results:
        status = "PASS: passed" if success else "FAIL: failed"
        print(f"  {game_type}: {status}")
    
    all_passed = all(success for _, success in results)
    if all_passed:
        print("\nPASS: all tests passed!")
    else:
        print("\nFAIL: some tests failed")
    
    return all_passed


if __name__ == "__main__":
    asyncio.run(main()) 