#!/usr/bin/env python3
"""
Aggressive Chicken Q-Learning Agent Solution.
This agent is designed to be more aggressive and Continue more often.
"""

import sys
import os
import asyncio
import argparse
import numpy as np

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class AggressiveChickenAgent(QLearning):
    """Aggressive Chicken Q-Learning agent that tends to Continue more often."""
    
    def __init__(self, name: str = "AggressiveChickenAgent"):
        # 4 states: based on my last 2 actions (2^2 = 4)
        # This focuses on my own behavior patterns and encourages more Continue
        NUM_POSSIBLE_STATES = 4
        
        super().__init__(name, num_possible_states=NUM_POSSIBLE_STATES, num_possible_actions=2,
                        initial_state=0, learning_rate=0.15, discount_factor=0.98,
                        exploration_rate=0.2, training_mode=True, save_path="aggressive-q-table.npy")
    
    def determine_state(self):
        """
        AGGRESSIVE IMPLEMENTATION: Focus on my own action patterns.
        
        This state representation tracks:
        - My last 2 actions (4 combinations: 00, 01, 10, 11)
        
        This encourages the agent to develop its own aggressive patterns
        rather than just reacting to the opponent. The agent will learn
        to Continue more when it has recently Continued (state 11, 10)
        and to be more aggressive in general.
        """
        if len(self.action_history) < 2:
            return 0  # Initial state
        
        # Get my last two actions
        my_last_action = self.action_history[-1]
        my_second_last_action = self.action_history[-2]
        
        # Convert to state: 2 * second_last + last
        state = 2 * my_second_last_action + my_last_action
        return state


# Example agent name
name = "AggressiveChickenAgent"


################### SUBMISSION #####################
agent_submission = AggressiveChickenAgent(name)
####################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aggressive Chicken Q-Learning Agent Solution')
    parser.add_argument('--mode', type=str, default='TRAIN', choices=['TRAIN', 'RUN'],
                        help='Mode: TRAIN or RUN (default: TRAIN)')

    args = parser.parse_args()
    
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    agent_name = "aggresso"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "chicken"  # Game type (hardcoded for this agent)
    num_rounds = 20000  # Number of rounds for training
    
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
            agent = AggressiveChickenAgent(agent_name)
            agent.set_training_mode(False)  # Set to RUN mode for server competition
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
            agent = AggressiveChickenAgent(agent_name)
            agent.set_training_mode(True)
            
            from core.engine import Engine
            from core.game.ChickenGame import ChickenGame
            from core.agents.lab03.random_chicken_agent import RandomChickenAgent
            from core.agents.lab03.swerve_agent import SwerveAgent
            from core.agents.lab03.continue_agent import ContinueAgent
            
            # Create training environment with SwerveAgent to make aggression pay off
            agents = [
                agent,
                SwerveAgent("SwerveAgent")
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
            agent = AggressiveChickenAgent(agent_name)
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
        print("python stencils/lab03_stencil/solutions/my_agent_aggressive.py --server --mode RUN")
