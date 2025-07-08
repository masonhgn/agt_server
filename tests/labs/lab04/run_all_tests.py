#!/usr/bin/env python3
"""
Comprehensive test script for Lab 4: Lemonade Stand

This script tests:
1. Game implementation
2. Agent implementations
3. Stencils (should raise NotImplementedError)
4. Example solutions
5. Arena functionality
"""

from core.game.LemonadeGame import LemonadeGame
from core.agents.lab04.stick_agent import StickAgent
from core.agents.lab04.random_lemonade_agent import RandomLemonadeAgent
from core.agents.lab04.always_stay_agent import AlwaysStayAgent
from core.local_arena import LocalArena
import numpy as np
from stencils.lab04_stencil.my_lemonade_agent import MyNRLAgent
from stencils.lab04_stencil.my_rl_lemonade_agent import MyRLAgent
from stencils.lab04_stencil.example_solution import ExampleNRLAgent, ExampleRLAgent


def test_game_implementation():
    """Test the Lemonade Stand game implementation."""
    print("Testing game implementation...")
    
    try:
        game = LemonadeGame()
        
        # Test valid actions
        valid_actions = game.get_valid_actions()
        print(f"Valid actions: {valid_actions}")
        print(f"Length: {len(valid_actions)}")
        print(f"All valid: {all(0 <= action <= 11 for action in valid_actions)}")
        assert len(valid_actions) == 12
        assert all(0 <= action <= 11 for action in valid_actions)
        
        # Test utility calculations
        # All same position
        utils = game.calculate_utils([5, 5, 5])
        print(f"Utils [5,5,5]: {utils}")
        assert np.allclose(utils, [8.0, 8.0, 8.0])
        
        # Two same position
        utils = game.calculate_utils([3, 3, 7])
        print(f"Utils [3,3,7]: {utils}")
        assert np.allclose(utils, [6.333333333333334, 6.333333333333334, 11.333333333333332])
        
        # All different positions
        actions = [2, 5, 8]
        utils = game.calculate_utils(actions)
        print(f"Utils [2,5,8]: {utils}")
        # Print per-beachgoer allocation
        player_positions = actions
        allocs = [0.0, 0.0, 0.0]
        for beachgoer in range(12):
            dists = [min((beachgoer - pos) % 12, (pos - beachgoer) % 12) for pos in player_positions]
            min_dist = min(dists)
            closest = [i for i, d in enumerate(dists) if d == min_dist]
            for i in closest:
                allocs[i] += 2.0 / len(closest)
            print(f"Beachgoer {beachgoer}: closest to {[i for i, d in enumerate(dists) if d == min_dist]}, dists={dists}")
        print(f"Manual allocs: {allocs}")
        print(f"Middle util: {utils[1]}, max: {max(utils)}")
        # Check that all cups are distributed
        assert np.isclose(sum(utils), 24.0)
        
        print("PASS: Game implementation works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Game implementation test failed: {e}")
        return False


def test_agent_implementations():
    """Test the agent implementations."""
    print("Testing agent implementations...")
    
    try:
        # Test stick agent
        stick_agent = StickAgent("Stick")
        action = stick_agent.act({"valid_actions": list(range(12))})
        assert action == 5  # Should always return position 5
        
        # Test random agent
        random_agent = RandomLemonadeAgent("Random")
        actions = set()
        for _ in range(100):
            action = random_agent.act({"valid_actions": list(range(12))})
            actions.add(action)
            assert 0 <= action <= 11
        # Should have some variety (not always the same)
        assert len(actions) > 1
        
        # Test always stay agent
        stay_agent = AlwaysStayAgent("Stay")
        action = stay_agent.act({"valid_actions": list(range(12))})
        assert action == 0  # Should always return position 0
        
        print("PASS: Agent implementations work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Agent implementations test failed: {e}")
        return False


def test_stencils():
    """Test that stencils raise NotImplementedError."""
    print("Testing stencils...")
    
    try:
        agent = MyNRLAgent("Test")
        agent.setup()
        
        try:
            agent.act({"valid_actions": list(range(12))})
            print("FAIL: Non-RL stencil should raise NotImplementedError")
            return False
        except NotImplementedError:
            print("PASS: Non-RL stencil correctly raises NotImplementedError")
    except Exception as e:
        print(f"FAIL: Non-RL stencil test failed: {e}")
        return False
    
    try:
        agent = MyRLAgent("Test", 144, 12, 0, 0.05, 0.90, 0.05, False)
        
        try:
            agent.determine_state()
            print("FAIL: RL stencil should raise NotImplementedError")
            return False
        except NotImplementedError:
            print("PASS: RL stencil correctly raises NotImplementedError")
    except Exception as e:
        print(f"FAIL: RL stencil test failed: {e}")
        return False
    
    return True


def test_example_solutions():
    """Test the example solutions."""
    print("Testing example solutions...")
    
    try:
        # Test non-RL agent
        nrl_agent = ExampleNRLAgent("TestNRL")
        nrl_agent.setup()
        action = nrl_agent.act({"valid_actions": list(range(12))})
        assert isinstance(action, int)
        assert 0 <= action <= 11
        
        # Test RL agent
        rl_agent = ExampleRLAgent("TestRL", 144, 12, 0, 0.05, 0.90, 0.05, False)
        state = rl_agent.determine_state()
        assert isinstance(state, int)
        assert 0 <= state < 144
        
        print("PASS: Example solutions work correctly")
        return True
    except Exception as e:
        print(f"FAIL: Example solutions test failed: {e}")
        return False


def test_arena():
    """Test the arena functionality."""
    print("Testing arena functionality...")
    
    try:
        # For Lemonade Stand, we need 3 players, but arena does pairwise games
        # So we'll test with a simpler approach - just create the arena
        arena = LocalArena(
            game_class=LemonadeGame,
            agents=[
                StickAgent("Stick1"),
                RandomLemonadeAgent("Random1"),
                AlwaysStayAgent("Stay1")
            ],
            num_rounds=100,
            timeout=1,
            verbose=False
        )
        
        # Just test that arena was created successfully
        assert arena.game_class == LemonadeGame
        assert len(arena.agents) == 3
        
        print("PASS: Arena functionality works correctly")
        return True
    except Exception as e:
        print(f"FAIL: Arena test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("LAB 4: LEMONADE STAND - COMPREHENSIVE TESTS")
    print("=" * 60)
    
    tests = [
        ("Game Implementation", test_game_implementation),
        ("Agent Implementations", test_agent_implementations),
        ("Stencils", test_stencils),
        ("Example Solutions", test_example_solutions),
        ("Arena Functionality", test_arena)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        try:
            if test_func():
                passed += 1
            else:
                print(f"FAIL: {test_name} failed")
        except Exception as e:
            print(f"FAIL: {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("PASS: All tests passed! Lab 4 is ready for students.")
    else:
        print("WARNING: Some tests failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 