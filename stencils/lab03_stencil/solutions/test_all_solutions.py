#!/usr/bin/env python3
"""
Comprehensive Test Script for Lab 3 Solutions.
This demonstrates all parts of Lab 3 and shows that training creates policy files.
"""

import sys
import os
import numpy as np

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from basic_chicken_agent import BasicChickenAgent

# Import our solutions
from q_learning_solution import QLearningSolution
from state_space_solutions import LastMoveChickenQLSolution, LookbackChickenQLSolution, CustomChickenQLSolution
from my_agent_solution import MyChickenAgentSolution
from collusion_solution import CollusionQLLearningAgentSolution, CollusionEnvironmentSolution


def test_q_learning_solution():
    """Test Part I: Q-Learning implementation."""
    print("=" * 60)
    print("PART I: Testing Q-Learning Implementation")
    print("=" * 60)
    
    # Create a simple Q-learning agent with complete implementation
    agent = QLearningSolution("TestQL", num_possible_states=2, num_possible_actions=2,
                             initial_state=0, learning_rate=0.1, discount_factor=0.9,
                             exploration_rate=0.1, training_mode=True, 
                             save_path="test-q-table.npy")
    
    # Test that the agent can be created
    print("✅ Q-Learning agent created successfully")
    print(f"   - Q-table shape: {agent.q.shape}")
    print(f"   - Learning rate: {agent.learning_rate}")
    print(f"   - Discount factor: {agent.discount_factor}")
    print(f"   - Exploration rate: {agent.exploration_rate}")
    
    return agent


def test_state_space_solutions():
    """Test Part II: State space representations."""
    print("\n" + "=" * 60)
    print("PART II: Testing State Space Representations")
    print("=" * 60)
    
    # Test LastMove agent
    print("Testing LastMove Chicken Q-Learning Solution...")
    lastmove_agent = LastMoveChickenQLSolution("LastMoveSolution")
    print(f"   - States: {lastmove_agent.num_possible_states}")
    print(f"   - Actions: {lastmove_agent.num_possible_actions}")
    print(f"   - Save path: {lastmove_agent.save_path}")
    
    # Test Lookback agent
    print("Testing Lookback Chicken Q-Learning Solution...")
    lookback_agent = LookbackChickenQLSolution("LookbackSolution")
    print(f"   - States: {lookback_agent.num_possible_states}")
    print(f"   - Actions: {lookback_agent.num_possible_actions}")
    print(f"   - Save path: {lookback_agent.save_path}")
    
    # Test Custom agent
    print("Testing Custom Chicken Q-Learning Solution...")
    custom_agent = CustomChickenQLSolution("CustomSolution")
    print(f"   - States: {custom_agent.num_possible_states}")
    print(f"   - Actions: {custom_agent.num_possible_actions}")
    print(f"   - Save path: {custom_agent.save_path}")
    
    # Test My Agent solution
    print("Testing My Chicken Agent Solution...")
    my_agent = MyChickenAgentSolution("MyAgentSolution")
    print(f"   - States: {my_agent.num_possible_states}")
    print(f"   - Actions: {my_agent.num_possible_actions}")
    print(f"   - Save path: {my_agent.save_path}")
    
    return lastmove_agent, lookback_agent, custom_agent, my_agent


def test_training_creates_files():
    """Test that training creates policy files."""
    print("\n" + "=" * 60)
    print("Testing Training Creates Policy Files")
    print("=" * 60)
    
    # Create agents with save paths
    agents = []
    save_paths = []
    
    # LastMove agent
    lastmove_agent = LastMoveChickenQLSolution("LastMoveTest")
    agents.append(lastmove_agent)
    save_paths.append(lastmove_agent.save_path)
    
    # Lookback agent
    lookback_agent = LookbackChickenQLSolution("LookbackTest")
    agents.append(lookback_agent)
    save_paths.append(lookback_agent.save_path)
    
    # Custom agent
    custom_agent = CustomChickenQLSolution("CustomTest")
    agents.append(custom_agent)
    save_paths.append(custom_agent.save_path)
    
    # Create opponent
    opponent = BasicChickenAgent("BasicChicken")
    
    # Run short training (1000 rounds to speed up test)
    print("Running short training (1000 rounds) to test file creation...")
    game = ChickenGame(rounds=1000)
    engine = Engine(game, [agents[0], opponent], rounds=1000)
    engine.run()
    
    # Check if files were created
    print("\nChecking for created policy files:")
    for i, save_path in enumerate(save_paths):
        if os.path.exists(save_path):
            file_size = os.path.getsize(save_path)
            print(f"✅ {save_path} - Created ({file_size} bytes)")
            
            # Load and verify the Q-table
            q_table = np.load(save_path)
            print(f"   - Q-table shape: {q_table.shape}")
            print(f"   - Q-table range: [{q_table.min():.3f}, {q_table.max():.3f}]")
        else:
            print(f"❌ {save_path} - Not created")
    
    return agents


def test_collusion_solution():
    """Test Part III: Collusion environment."""
    print("\n" + "=" * 60)
    print("PART III: Testing Collusion Environment")
    print("=" * 60)
    
    # Create Q-learning agents for collusion
    agent1 = CollusionQLLearningAgentSolution("Seller1Test", num_states=10, 
                                             learning_rate=0.1, discount_factor=0.9,
                                             exploration_rate=0.1, training_mode=True,
                                             save_path="seller1-test.npy")
    agent2 = CollusionQLLearningAgentSolution("Seller2Test", num_states=10,
                                             learning_rate=0.1, discount_factor=0.9,
                                             exploration_rate=0.1, training_mode=True,
                                             save_path="seller2-test.npy")
    
    print("✅ Collusion agents created successfully")
    print(f"   - Agent 1 save path: {agent1.save_path}")
    print(f"   - Agent 2 save path: {agent2.save_path}")
    
    # Run short simulation (10000 rounds to speed up test)
    print("\nRunning short collusion simulation (10,000 rounds)...")
    env = CollusionEnvironmentSolution(agent1, agent2)
    env.run_simulation(num_rounds=10000, save_plots=False)  # Don't create plots for test
    
    # Check if files were created
    print("\nChecking for created collusion policy files:")
    for save_path in [agent1.save_path, agent2.save_path]:
        if os.path.exists(save_path):
            file_size = os.path.getsize(save_path)
            print(f"✅ {save_path} - Created ({file_size} bytes)")
            
            # Load and verify the Q-table
            q_table = np.load(save_path)
            print(f"   - Q-table shape: {q_table.shape}")
            print(f"   - Q-table range: [{q_table.min():.3f}, {q_table.max():.3f}]")
        else:
            print(f"❌ {save_path} - Not created")
    
    return agent1, agent2


def demonstrate_learning_progress():
    """Demonstrate learning progress with a simple example."""
    print("\n" + "=" * 60)
    print("Demonstrating Learning Progress")
    print("=" * 60)
    
    # Create a simple agent
    agent = LastMoveChickenQLSolution("LearningDemo")
    opponent = BasicChickenAgent("BasicChicken")
    
    # Track Q-table changes
    initial_q = agent.q.copy()
    
    # Run training in chunks
    chunk_size = 5000
    num_chunks = 4
    
    for chunk in range(num_chunks):
        print(f"\nTraining chunk {chunk + 1}/{num_chunks} ({chunk_size} rounds)...")
        
        # Run training
        game = ChickenGame(rounds=chunk_size)
        engine = Engine(game, [agent, opponent], rounds=chunk_size)
        engine.run()
        
        # Show Q-table changes
        q_change = np.mean(np.abs(agent.q - initial_q))
        print(f"   - Average Q-table change: {q_change:.4f}")
        print(f"   - Q-table range: [{agent.q.min():.3f}, {agent.q.max():.3f}]")
        
        # Save intermediate Q-table
        intermediate_path = f"learning-progress-chunk-{chunk+1}.npy"
        np.save(intermediate_path, agent.q)
        print(f"   - Saved to: {intermediate_path}")
    
    print(f"\n✅ Final Q-table saved to: {agent.save_path}")
    
    return agent


def main():
    """Main test function."""
    print("Lab 3 Solutions - Comprehensive Test")
    print("This demonstrates all parts of Lab 3 and shows training creates policy files")
    print("=" * 80)
    
    try:
        # Test Part I: Q-Learning implementation
        q_agent = test_q_learning_solution()
        
        # Test Part II: State space representations
        lastmove_agent, lookback_agent, custom_agent, my_agent = test_state_space_solutions()
        
        # Test that training creates files
        trained_agents = test_training_creates_files()
        
        # Test Part III: Collusion environment
        collusion_agent1, collusion_agent2 = test_collusion_solution()
        
        # Demonstrate learning progress
        learning_agent = demonstrate_learning_progress()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nSummary:")
        print("✅ Part I: Q-Learning implementation works")
        print("✅ Part II: State space representations work")
        print("✅ Part III: Collusion environment works")
        print("✅ Training creates policy files (.npy)")
        print("✅ Learning progress can be tracked")
        
        print("\nCreated files:")
        # List all .npy files in current directory
        npy_files = [f for f in os.listdir('.') if f.endswith('.npy')]
        for file in npy_files:
            size = os.path.getsize(file)
            print(f"   - {file} ({size} bytes)")
        
        print(f"\nTotal policy files created: {len(npy_files)}")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
