#!/usr/bin/env python3
"""
comprehensive test suite for the agt system.

this script tests all components of the agt system including games, agents, and arenas.
"""

import numpy as np

from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.rock_agent import RockAgent
from core.agents.lab01.random_agent import RandomAgent


def test_basic_game():
    """test basic game functionality."""
    print("1. testing basic game functionality")
    print("-" * 40)
    
    # create game and agents
    game = RPSGame()
    rock_agent = RockAgent("rock")
    random_agent = RandomAgent("random")
    
    # create engine
    engine = Engine(game, [rock_agent, random_agent])
    
    # run a few rounds
    final_rewards = engine.run(10)
    
    # verify rock agent always plays rock (action 0)
    rock_actions = [action for action in rock_agent.action_history if action == 0]
    assert len(rock_actions) == len(rock_agent.action_history), "rock agent should always play rock"
    print("PASS: rock agent always plays rock")
    
    # verify game ran correctly
    assert len(final_rewards) == 2, "should have rewards for 2 players"
    print("PASS: basic game test passed!\n")


def test_agent_interface():
    """test agent interface compliance."""
    print("2. testing agent interface")
    print("-" * 40)
    
    # test rock agent
    rock_agent = RockAgent("rock")
    assert hasattr(rock_agent, 'get_action'), "agent should have get_action method"
    assert hasattr(rock_agent, 'update'), "agent should have update method"
    assert hasattr(rock_agent, 'reset'), "agent should have reset method"
    
    # test random agent
    random_agent = RandomAgent("random")
    assert hasattr(random_agent, 'get_action'), "agent should have get_action method"
    assert hasattr(random_agent, 'update'), "agent should have update method"
    assert hasattr(random_agent, 'reset'), "agent should have reset method"
    
    # test action generation
    for _ in range(10):
        rock_action = rock_agent.get_action({})
        random_action = random_agent.get_action({})
        
        assert rock_action == 0, "rock agent should always return 0"
        assert random_action in [0, 1, 2], "random agent should return valid action"
    
    print("PASS: all agent interface tests passed!\n")


def test_payoff_matrix():
    """test payoff matrix calculations."""
    print("3. testing payoff matrix")
    print("-" * 40)
    
    game = RPSGame()
    
    # test rock vs paper
    rewards = game.step({0: 0, 1: 1})[1]  # rock vs paper
    assert rewards[0] == -1, "rock should lose to paper"
    assert rewards[1] == 1, "paper should beat rock"
    
    # test rock vs scissors
    rewards = game.step({0: 0, 1: 2})[1]  # rock vs scissors
    assert rewards[0] == 1, "rock should beat scissors"
    assert rewards[1] == -1, "scissors should lose to rock"
    
    # test paper vs scissors
    rewards = game.step({0: 1, 1: 2})[1]  # paper vs scissors
    assert rewards[0] == -1, "paper should lose to scissors"
    assert rewards[1] == 1, "scissors should beat paper"
    
    # test ties
    rewards = game.step({0: 0, 1: 0})[1]  # rock vs rock
    assert rewards[0] == 0, "rock vs rock should be a tie"
    assert rewards[1] == 0, "rock vs rock should be a tie"
    
    print("PASS: all payoff matrix tests passed!\n")


def test_agent_strategies():
    """test agent strategies."""
    print("4. testing agent strategies")
    print("-" * 40)
    
    # test rock agent strategy
    rock_agent = RockAgent("rock")
    for _ in range(10):
        action = rock_agent.get_action({})
        assert action == 0, "rock agent should always play rock"
    print("PASS: rock agent always plays rock")
    
    # test random agent distribution
    random_agent = RandomAgent("random")
    actions = []
    for _ in range(100):
        action = random_agent.get_action({})
        actions.append(action)
    
    # check that all actions appear
    unique_actions = set(actions)
    assert len(unique_actions) == 3, "random agent should use all actions"
    
    # check reasonable distribution (not too skewed)
    action_counts = [actions.count(i) for i in range(3)]
    min_count = min(action_counts)
    max_count = max(action_counts)
    assert max_count - min_count < 50, "random agent should have reasonable distribution"
    
    print("PASS: random agent has reasonable distribution")
    print("PASS: all agent strategy tests passed!\n")


def main():
    """run all tests."""
    print("agt comprehensive test suite")
    print("=" * 50)
    
    try:
        test_basic_game()
        test_agent_interface()
        test_payoff_matrix()
        test_agent_strategies()
        
        print("=" * 50)
        print("PASS: all tests passed!")
        print("\nagt system is working correctly.")
        
    except Exception as e:
        print(f"\nFAIL: test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 