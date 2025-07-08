#!/usr/bin/env python3
"""
test script for the local arena system.

this script tests the arena functionality for running tournaments between agents.
"""

from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.rock_agent import RockAgent
from core.agents.lab01.paper_agent import PaperAgent
from core.agents.lab01.random_agent import RandomAgent


def test_arena():
    """test the arena system."""
    print("testing local arena system...")
    
    # create agents
    agents = [
        RockAgent("rock"),
        PaperAgent("paper")
    ]
    
    # create game
    game = RPSGame()
    
    # create engine
    engine = Engine(game, agents)
    
    # run tournament
    results = engine.run(100)
    
    print(f"tournament results:")
    for i, agent in enumerate(agents):
        print(f"  {agent.name}: {results[i]}")
    
    print("arena test completed!")


if __name__ == "__main__":
    test_arena() 