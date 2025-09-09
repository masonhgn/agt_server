#!/usr/bin/env python3
"""
Test script for Collusion Environment stencil.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stencils.lab03_stencil.collusion_environment_stencil import CollusionQLearningAgent, CollusionEnvironment
from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_chicken_agent import RandomChickenAgent


def test_collusion_environment():
    """Test the Collusion Environment stencil."""
    print("Testing Collusion Environment Stencil")
    print("=" * 50)
    
    # Create agents
    agent1 = CollusionQLearningAgent("CollusionQL1")
    agent2 = CollusionQLearningAgent("CollusionQL2")
    
    # Test basic functionality
    print("Testing basic agent functionality...")
    
    # Test price conversion
    action = 5
    price = agent1.get_price(action)
    print(f"  Action {action} -> Price {price:.3f}")
    
    # Test demand calculation
    my_price = 1.5
    opponent_price = 1.8
    demand = agent1.calculate_demand(my_price, opponent_price)
    print(f"  Demand at price {my_price} vs {opponent_price}: {demand:.3f}")
    
    # Test profit calculation
    profit = agent1.calculate_profit(my_price, opponent_price)
    print(f"  Profit at price {my_price} vs {opponent_price}: {profit:.3f}")
    
    # Test environment creation
    print("\nTesting environment creation...")
    env = CollusionEnvironment(agent1, agent2)
    print(f"  Environment created successfully")
    print(f"  Agent 1 Q-table shape: {agent1.get_q_table().shape}")
    print(f"  Agent 2 Q-table shape: {agent2.get_q_table().shape}")
    
    # Test short simulation
    print("\nTesting short simulation...")
    try:
        price_history, profit_history = env.run_simulation(num_rounds=10, save_plots=False)
        print(f"  Simulation completed successfully")
        print(f"  Price history length: {len(price_history)}")
        print(f"  Profit history length: {len(profit_history)}")
        
        # Show final prices
        if price_history:
            final_prices = price_history[-1]
            print(f"  Final prices: Agent 1 = {final_prices[0]:.3f}, Agent 2 = {final_prices[1]:.3f}")
            
    except NotImplementedError as e:
        print(f"  FAIL: Simulation failed: {e}")
        print("  This is expected - implement determine_state() to fix")

    # Test new simulation
    print("\nTesting new simulation...")
    try:
        game = ChickenGame()
        agents = [RandomChickenAgent("Random"), RandomChickenAgent("Random2")]
        engine = Engine(game, agents)
        final_rewards = engine.run(10)
        print(f"  Simulation completed successfully")
        print(f"  Final rewards: {final_rewards}")
    except NotImplementedError as e:
        print(f"  FAIL: Simulation failed: {e}")
        print("  This is expected - implement determine_state() to fix")


if __name__ == "__main__":
    try:
        test_collusion_environment()
        print("\nPASS: All tests completed successfully!")
    except NotImplementedError as e:
        print(f"\nFAIL: Test failed: {e}")
        print("Please implement the TODO sections in the stencil before running tests.")
    except Exception as e:
        print(f"\nFAIL: Test failed with error: {e}")
        import traceback
        traceback.print_exc() 