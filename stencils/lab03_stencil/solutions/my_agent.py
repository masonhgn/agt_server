#!/usr/bin/env python3
"""
Complete Solution for my_agent.py - Lab 3 Part II.
This shows the implementation of determine_state() for custom state representation.
"""

import sys
import os
import asyncio
import argparse
import numpy as np

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class MyChickenAgentSolution(QLearning):
    """Complete solution for custom Chicken Q-Learning agent with advanced state representation."""
    
    def __init__(self, name: str = "MyChickenAgentSolution"):
        # 16 states: combination of opponent's last 2 actions and my last 2 actions
        # This creates a sophisticated state space for better learning
        NUM_POSSIBLE_STATES = 16
        
        super().__init__(name, num_possible_states=NUM_POSSIBLE_STATES, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="my-agent-q-table-solution.npy")
    
    def determine_state(self):
        """
        COMPLETE IMPLEMENTATION: Advanced state-space representation.
        
        This state representation combines:
        - Opponent's last 2 actions (4 combinations: 00, 01, 10, 11)
        - My last 2 actions (4 combinations: 00, 01, 10, 11)
        
        Total states: 4 * 4 = 16 states
        
        This allows the agent to learn patterns in both its own and opponent's behavior.
        """
        if len(self.action_history) < 2:
            return 0  # Initial state
        
        # Get my last two actions
        my_last_action = self.action_history[-1]
        my_second_last_action = self.action_history[-2]
        
        # Infer opponent's last two actions from rewards
        my_last_reward = self.reward_history[-1]
        my_second_last_reward = self.reward_history[-2]
        
        # Chicken payoff matrix (row player, column player):
        # S\C  S  C
        # S    0  -1
        # C    1  -5
        
        # Determine opponent's last action
        if my_last_action == 0:  # I swerved
            if my_last_reward == 0:
                opp_last_action = 0  # Opponent also swerved
            elif my_last_reward == -1:
                opp_last_action = 1  # Opponent continued
            else:
                opp_last_action = 0  # Default
        else:  # I continued
            if my_last_reward == 1:
                opp_last_action = 0  # Opponent swerved
            elif my_last_reward == -5:
                opp_last_action = 1  # Opponent also continued
            else:
                opp_last_action = 0  # Default
        
        # Determine opponent's second-to-last action
        if my_second_last_action == 0:  # I swerved
            if my_second_last_reward == 0:
                opp_second_last_action = 0  # Opponent also swerved
            elif my_second_last_reward == -1:
                opp_second_last_action = 1  # Opponent continued
            else:
                opp_second_last_action = 0  # Default
        else:  # I continued
            if my_second_last_reward == 1:
                opp_second_last_action = 0  # Opponent swerved
            elif my_second_last_reward == -5:
                opp_second_last_action = 1  # Opponent also continued
            else:
                opp_second_last_action = 0  # Default
        
        # Combine into state: 4 * opponent_pattern + my_pattern
        # opponent_pattern: 2 * opp_second_last + opp_last (0-3)
        # my_pattern: 2 * my_second_last + my_last (0-3)
        opponent_pattern = 2 * opp_second_last_action + opp_last_action
        my_pattern = 2 * my_second_last_action + my_last_action
        
        state = 4 * opponent_pattern + my_pattern
        return state


# Example agent name
name = "MyChickenAgentSolution"


################### SUBMISSION #####################
agent_submission = MyChickenAgentSolution(name)
####################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My Chicken Q-Learning Agent Solution')
    parser.add_argument('--mode', type=str, default='TRAIN', choices=['TRAIN', 'RUN'],
                        help='Mode: TRAIN or RUN (default: TRAIN)')

    args = parser.parse_args()
    
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    agent_name = "WHATEVS"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "chicken"  # Game type (hardcoded for this agent)
    num_rounds = 200000  # Number of rounds for training
    
    print(f"Running in {args.mode} mode")
    
    if server:
        # Server mode - connect to competition server
        print(f"Connecting to server at {host}:{port}")
        
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = MyChickenAgentSolution(agent_name)
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, agent_name, host, port, verbose)
        
        # Run the async main function
        asyncio.run(main())
        
    else:
        # Local testing mode
        if args.mode == "TRAIN":
            # Training mode - train the agent
            print("TRAINING PHASE")
            print("=" * 50)
            
            # Create agent for training
            agent = MyChickenAgentSolution(agent_name)
            agent.set_training_mode(True)
            
            from core.engine import Engine
            from core.game.ChickenGame import ChickenGame
            from core.agents.lab03.random_chicken_agent import RandomChickenAgent
            
            # Create training environment with only 2 agents (Chicken game expects 2 players)
            agents = [
                agent,
                RandomChickenAgent("RandomAgent")
            ]
            
            game = ChickenGame(rounds=num_rounds)
            engine = Engine(game, agents, rounds=num_rounds)
            final_rewards = engine.run()
            
            print("Training completed!")
            print(f"Final rewards: {final_rewards}")
            print(f"Agent average reward: {sum(agent.reward_history[-1000:]) / 1000:.3f}")
            print(f"Agent total reward: {sum(agent.reward_history[-1000:])}")
            
            # Debug: Check Q-table state after training
            print(f"Q-table shape: {agent.q.shape}")
            print(f"Q-table sum: {np.sum(agent.q)}")
            print(f"Q-table max: {np.max(agent.q)}")
            print(f"Q-table min: {np.min(agent.q)}")
            
            # Show Q-values for first few states
            print("\nQ-table values (first 5 states):")
            for state in range(min(5, agent.num_possible_states)):
                swerve_q = agent.q[state, 0]
                continue_q = agent.q[state, 1]
                print(f"State {state}: Swerve={swerve_q:.3f}, Continue={continue_q:.3f}")
            
            # Test a few action choices
            for state in range(min(5, agent.num_possible_states)):
                action = agent.choose_next_move(state)
                print(f"State {state} -> Action {action} (Swerve)" if action == 0 else f"State {state} -> Action {action} (Continue)")
            
            # Print action distribution
            action_counts = [0, 0]
            for action in agent.action_history[-1000:]:
                action_counts[action] += 1
            print(f"Action distribution: Swerve={action_counts[0]}, Continue={action_counts[1]}")
            
        else:  # RUN mode
            # Testing mode - evaluate the trained agent
            print("TESTING PHASE")
            print("=" * 50)
            
            # Create agent for testing (load trained Q-table)
            agent = MyChickenAgentSolution(agent_name)
            agent.set_training_mode(False)
            
            from core.engine import Engine
            from core.game.ChickenGame import ChickenGame
            from core.agents.lab03.random_chicken_agent import RandomChickenAgent
            
            # Create testing environment with only 2 agents (Chicken game expects 2 players)
            agents = [
                agent,
                RandomChickenAgent("RandomAgent")
            ]
            
            game = ChickenGame(rounds=1000)
            engine = Engine(game, agents, rounds=1000)
            final_rewards = engine.run()
            
            print("Testing completed!")
            print(f"Final rewards: {final_rewards}")
            print(f"Agent average reward: {sum(agent.reward_history[-1000:]) / 1000:.3f}")
            print(f"Agent total reward: {sum(agent.reward_history[-1000:])}")
            
            # Print action distribution
            action_counts = [0, 0]
            for action in agent.action_history[-1000:]:
                action_counts[action] += 1
            print(f"Action distribution: Swerve={action_counts[0]}, Continue={action_counts[1]}")
        
        print("\nLocal test completed!")
        print("\nTo connect to server for competition, use:")
        print("python stencils/lab03_stencil/solutions/my_agent.py --server --mode RUN")
