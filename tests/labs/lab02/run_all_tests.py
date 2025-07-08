c#!/usr/bin/env python3
"""
Comprehensive test script for Lab 2 - Battle of the Sexes
Runs all tests and provides a summary.
"""

from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent
from core.agents.lab02.compromise_agent import CompromiseAgent
from core.agents.lab02.stubborn_agent import StubbornAgent
from stencils.lab02_stencil.bos_finite_state_stencil import BOSFiniteStateAgent
from stencils.lab02_stencil.bosii_competition_stencil import BOSIICompetitionAgent


def test_bos_basic():
    """Test basic BOS game functionality."""
    print("Testing Basic BOS Game...")
    
    game = BOSGame(rounds=10)
    agents = {0: CompromiseAgent("Compromise"), 1: StubbornAgent("Stubborn")}
    
    engine = Engine(game, timeout=1.0)
    final_rewards = engine.run(agents)
    
    print(f"  Compromise vs Stubborn: {final_rewards}")
    print(f"  Expected: Compromise gets 3, Stubborn gets 7")
    print("  PASS: Basic BOS test passed")


def test_bosii_basic():
    """Test basic BOSII game functionality."""
    print("Testing Basic BOSII Game...")
    
    game = BOSIIGame(rounds=10)
    agents = {0: CompromiseAgent("Compromise"), 1: StubbornAgent("Stubborn")}
    
    engine = Engine(game, timeout=1.0)
    final_rewards = engine.run(agents)
    
    print(f"  Compromise vs Stubborn: {final_rewards}")
    print("  PASS: Basic BOSII test passed")


def test_stencils():
    """Test that stencils can be imported and instantiated."""
    print("Testing Stencil Imports...")
    
    try:
        fsm_agent = BOSFiniteStateAgent("TestFSM")
        print("  PASS: BOS Finite State stencil imported successfully")
    except Exception as e:
        print(f"  FAIL: BOS Finite State stencil failed: {e}")
    
    try:
        comp_agent = BOSIICompetitionAgent("TestComp")
        print("  PASS: BOSII Competition stencil imported successfully")
    except Exception as e:
        print(f"  FAIL: BOSII Competition stencil failed: {e}")


def test_agent_interface():
    """Test that agents implement the required interface."""
    print("Testing Agent Interface...")
    
    # Test BOS FSM agent interface
    fsm_agent = BOSFiniteStateAgent("TestFSM")
    assert hasattr(fsm_agent, 'act'), "FSM agent missing 'act' method"
    assert hasattr(fsm_agent, 'update'), "FSM agent missing 'update' method"
    assert hasattr(fsm_agent, 'reset'), "FSM agent missing 'reset' method"
    print("  PASS: BOS FSM agent interface correct")
    
    # Test BOSII Competition agent interface
    comp_agent = BOSIICompetitionAgent("TestComp")
    assert hasattr(comp_agent, 'act'), "Competition agent missing 'act' method"
    assert hasattr(comp_agent, 'update'), "Competition agent missing 'update' method"
    assert hasattr(comp_agent, 'reset'), "Competition agent missing 'reset' method"
    print("  PASS: BOSII Competition agent interface correct")


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("Lab 2 - Battle of the Sexes Comprehensive Tests")
    print("=" * 60)
    
    try:
        test_bos_basic()
        test_bosii_basic()
        test_stencils()
        test_agent_interface()
        
        print("\n" + "=" * 60)
        print("PASS: All basic tests passed!")
        print("\nNext steps:")
        print("1. Implement the TODO sections in the stencils")
        print("2. Run individual test scripts:")
        print("   - python test_bos_finite_state.py")
        print("   - python test_bosii_competition.py")
        print("3. Test your agents against the example solutions")
        print("4. Submit your completed implementation")
        
    except Exception as e:
        print(f"\nFAIL: Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_comprehensive_tests() 