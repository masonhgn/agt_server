#!/usr/bin/env python3
"""
Comprehensive test script for Lab 3 - Q-Learning and Collusion
Runs all tests and provides a summary.
"""

from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_chicken_agent import RandomChickenAgent
from core.agents.lab03.swerve_agent import SwerveAgent
from core.agents.lab03.continue_agent import ContinueAgent
from stencils.lab03_stencil.chicken_q_learning_stencil import ChickenQLearningAgent
from stencils.lab03_stencil.collusion_environment_stencil import CollusionQLearningAgent, CollusionEnvironment


def test_chicken_basic():
    """Test basic Chicken game functionality."""
    print("Testing Basic Chicken Game...")
    
    game = ChickenGame(rounds=10)
    agents = {0: SwerveAgent("Swerve"), 1: ContinueAgent("Continue")}
    
    engine = Engine(game, timeout=1.0)
    final_rewards = engine.run(agents)
    
    print(f"  Swerve vs Continue: {final_rewards}")
    print(f"  Expected: Swerve gets -1, Continue gets 1")
    print("  PASS: Basic Chicken test passed")


def test_q_learning_interface():
    """Test that Q-Learning agents implement the required interface."""
    print("Testing Q-Learning Agent Interface...")
    
    # Test Chicken Q-Learning agent interface
    chicken_agent = ChickenQLearningAgent("TestChickenQL")
    assert hasattr(chicken_agent, 'act'), "Chicken Q-Learning agent missing 'act' method"
    assert hasattr(chicken_agent, 'update'), "Chicken Q-Learning agent missing 'update' method"
    assert hasattr(chicken_agent, 'reset'), "Chicken Q-Learning agent missing 'reset' method"
    assert hasattr(chicken_agent, 'determine_state'), "Chicken Q-Learning agent missing 'determine_state' method"
    print("  PASS: Chicken Q-Learning agent interface correct")
    
    # Test Collusion Q-Learning agent interface
    collusion_agent = CollusionQLearningAgent("TestCollusionQL")
    assert hasattr(collusion_agent, 'act'), "Collusion Q-Learning agent missing 'act' method"
    assert hasattr(collusion_agent, 'update'), "Collusion Q-Learning agent missing 'update' method"
    assert hasattr(collusion_agent, 'reset'), "Collusion Q-Learning agent missing 'reset' method"
    assert hasattr(collusion_agent, 'determine_state'), "Collusion Q-Learning agent missing 'determine_state' method"
    print("  PASS: Collusion Q-Learning agent interface correct")


def test_stencils():
    """Test that stencils can be imported and instantiated."""
    print("Testing Stencil Imports...")
    
    try:
        chicken_agent = ChickenQLearningAgent("TestChickenQL")
        print("  PASS: Chicken Q-Learning stencil imported successfully")
    except Exception as e:
        print(f"  FAIL: Chicken Q-Learning stencil failed: {e}")
    
    try:
        collusion_agent = CollusionQLearningAgent("TestCollusionQL")
        print("  PASS: Collusion Q-Learning stencil imported successfully")
    except Exception as e:
        print(f"  FAIL: Collusion Q-Learning stencil failed: {e}")


def test_collusion_basic():
    """Test basic collusion environment functionality."""
    print("Testing Basic Collusion Environment...")
    
    agent1 = CollusionQLearningAgent("TestCollusionQL1")
    agent2 = CollusionQLearningAgent("TestCollusionQL2")
    
    # Test price conversion
    action = 5
    price = agent1.get_price(action)
    print(f"  Action {action} -> Price {price:.3f}")
    
    # Test demand calculation
    my_price = 1.5
    opponent_price = 1.8
    demand = agent1.calculate_demand(my_price, opponent_price)
    print(f"  Demand calculation: {demand:.3f}")
    
    # Test profit calculation
    profit = agent1.calculate_profit(my_price, opponent_price)
    print(f"  Profit calculation: {profit:.3f}")
    
    print("  PASS: Basic collusion environment test passed")


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("Lab 3 - Q-Learning and Collusion Comprehensive Tests")
    print("=" * 60)
    
    try:
        test_chicken_basic()
        test_q_learning_interface()
        test_stencils()
        test_collusion_basic()
        
        print("\n" + "=" * 60)
        print("PASS: All basic tests passed!")
        print("\nNext steps:")
        print("1. Implement the TODO sections in the stencils")
        print("2. Run individual test scripts:")
        print("   - python test_chicken_q_learning.py")
        print("   - python test_collusion_environment.py")
        print("3. Test your agents against the example solutions")
        print("4. Experiment with different state representations")
        print("5. Analyze collusion behavior in pricing games")
        print("6. Submit your completed implementation")
        
    except Exception as e:
        print(f"\nFAIL: Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_comprehensive_tests() 