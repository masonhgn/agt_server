#!/usr/bin/env python3
"""
test script for rock paper scissors game.

this script tests the rps game implementation and basic agent functionality.
"""

from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.rock_agent import RockAgent
from core.agents.lab01.paper_agent import PaperAgent
from core.agents.lab01.scissors_agent import ScissorsAgent
from core.agents.lab01.random_agent import RandomAgent


def test_rps_game():
    """test the rps game implementation."""
    print("testing rock paper scissors game...")
    
    # create game
    game = RPSGame()
    
    # test basic game mechanics
    print("testing basic game mechanics...")
    
    # rock vs paper
    obs, rewards, done, info = game.step({0: 0, 1: 1})
    assert rewards[0] == -1, "rock should lose to paper"
    assert rewards[1] == 1, "paper should beat rock"
    
    # rock vs scissors
    obs, rewards, done, info = game.step({0: 0, 1: 2})
    assert rewards[0] == 1, "rock should beat scissors"
    assert rewards[1] == -1, "scissors should lose to rock"
    
    # paper vs scissors
    obs, rewards, done, info = game.step({0: 1, 1: 2})
    assert rewards[0] == -1, "paper should lose to scissors"
    assert rewards[1] == 1, "scissors should beat paper"
    
    # ties
    obs, rewards, done, info = game.step({0: 0, 1: 0})
    assert rewards[0] == 0, "rock vs rock should be a tie"
    assert rewards[1] == 0, "rock vs rock should be a tie"
    
    print("PASS: basic game mechanics test passed")


def test_rps_agents():
    """test rps agents."""
    print("testing rps agents...")
    
    # create agents
    rock_agent = RockAgent("rock")
    paper_agent = PaperAgent("paper")
    scissors_agent = ScissorsAgent("scissors")
    random_agent = RandomAgent("random")
    
    # test rock agent
    for _ in range(10):
        action = rock_agent.get_action({})
        assert action == 0, "rock agent should always play rock"
    
    # test paper agent
    for _ in range(10):
        action = paper_agent.get_action({})
        assert action == 1, "paper agent should always play paper"
    
    # test scissors agent
    for _ in range(10):
        action = scissors_agent.get_action({})
        assert action == 2, "scissors agent should always play scissors"
    
    # test random agent
    actions = []
    for _ in range(100):
        action = random_agent.get_action({})
        assert action in [0, 1, 2], "random agent should return valid action"
        actions.append(action)
    
    # check distribution
    unique_actions = set(actions)
    assert len(unique_actions) == 3, "random agent should use all actions"
    
    print("PASS: agent tests passed")


def test_rps_matches():
    """test rps matches between agents."""
    print("testing rps matches...")
    
    # create game and agents
    game = RPSGame()
    rock_agent = RockAgent("rock")
    paper_agent = PaperAgent("paper")
    scissors_agent = ScissorsAgent("scissors")
    
    # rock vs paper
    engine = Engine(game, [rock_agent, paper_agent])
    results = engine.run(100)
    print(f"rock vs paper: {results}")
    assert results[0] < results[1], "paper should beat rock over many rounds"
    
    # rock vs scissors
    engine = Engine(game, [rock_agent, scissors_agent])
    results = engine.run(100)
    print(f"rock vs scissors: {results}")
    assert results[0] > results[1], "rock should beat scissors over many rounds"
    
    # paper vs scissors
    engine = Engine(game, [paper_agent, scissors_agent])
    results = engine.run(100)
    print(f"paper vs scissors: {results}")
    assert results[0] < results[1], "scissors should beat paper over many rounds"
    
    print("PASS: match tests passed")


def main():
    """run all rps tests."""
    print("rps game test suite")
    print("=" * 40)
    
    try:
        test_rps_game()
        test_rps_agents()
        test_rps_matches()
        
        print("\n" + "=" * 40)
        print("PASS: all rps tests passed!")
        
    except Exception as e:
        print(f"\nFAIL: test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 