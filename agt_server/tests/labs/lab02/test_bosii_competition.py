#!/usr/bin/env python3
"""
Test script for BOSII Competition stencil.
"""

from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent
from core.agents.lab02.compromise_agent import CompromiseAgent
from core.agents.lab02.stubborn_agent import StubbornAgent
from stencils.lab02_stencil.bosii_competition_stencil import BOSIICompetitionAgent


def test_bosii_competition():
    """Test the BOSII competition stencil."""
    print("Testing BOSII Competition Stencil")
    print("=" * 50)
    
    # Create agents
    competition_agent = BOSIICompetitionAgent("Competition_Agent")
    random_agent = RandomBOSAgent("Random")
    compromise_agent = CompromiseAgent("Compromise")
    stubborn_agent = StubbornAgent("Stubborn")
    
    # Test against different opponents
    opponents = [
        ("Random", random_agent),
        ("Compromise", compromise_agent),
        ("Stubborn", stubborn_agent)
    ]
    
    for opponent_name, opponent in opponents:
        print(f"\nTesting Competition Agent vs {opponent_name}:")
        
        # Create game
        game = BOSIIGame()
        agents = [competition_agent, opponent]
        
        # Reset agents
        competition_agent.reset()
        opponent.reset()
        
        # Run game
        engine = Engine(game, agents)
        final_rewards = engine.run(10)
        
        print(f"  Final rewards: {final_rewards}")
        print(f"  Cumulative rewards: {engine.cumulative_reward}")
        
        # Print competition agent statistics
        action_counts = [0, 0]  # Compromise, Stubborn
        for action in competition_agent.action_history:
            action_counts[action] += 1
        
        print(f"  Competition Agent - Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
        print(f"  Competition Agent - Total reward: {sum(competition_agent.reward_history)}")
        print(f"  Competition Agent - Average reward: {sum(competition_agent.reward_history) / len(competition_agent.reward_history) if competition_agent.reward_history else 0:.3f}")
        print(f"  Competition Agent - Final state: {competition_agent.curr_state}")
        print(f"  Competition Agent - Is row player: {competition_agent.is_row_player()}")
        if competition_agent.mood_history:
            print(f"  Competition Agent - Mood history: {competition_agent.mood_history}")


if __name__ == "__main__":
    try:
        test_bosii_competition()
        print("\nPASS: All tests completed successfully!")
    except NotImplementedError as e:
        print(f"\nFAIL: Test failed: {e}")
        print("Please implement the TODO sections in the stencil before running tests.")
    except Exception as e:
        print(f"\nFAIL: Test failed with error: {e}")
        import traceback
        traceback.print_exc() 