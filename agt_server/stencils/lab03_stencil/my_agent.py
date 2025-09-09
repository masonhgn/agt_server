#!/usr/bin/env python3
"""
My Chicken Q-Learning Agent for Competition.
This is your competition agent for the Chicken game.
"""

import sys
import os
import asyncio
import argparse

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class MyChickenAgent(QLearning):
    """Your competition Q-Learning agent for Chicken."""
    
    def __init__(self, name: str = "MyChickenAgent"):
        # TODO: Set the number of states based on your representation
        NUM_POSSIBLE_STATES = 4  # TODO: Adjust this based on your state representation
        
        super().__init__(name, num_possible_states=NUM_POSSIBLE_STATES, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="q-table.npy")
    
    def determine_state(self):
        """
        TODO: Implement your own state-space representation.
        
        This is where you define how to represent the game state as an MDP.
        Your representation can be:
        - Basic and low-level: incorporating previous k states/actions
        - Feature-based: summarizing game history into features
        - Pattern-based: detecting specific patterns in opponent behavior
        
        Returns:
            int: State index (0 to num_possible_states - 1)
        """
        # TODO: Implement your state representation
        # Hint: Use self.get_action_history(), self.get_opponent_last_action(), etc.
        raise NotImplementedError("Implement your state representation here")


# TODO: Give your agent a NAME 
name = "MyChickenAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = MyChickenAgent(name)
####################################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My Chicken Q-Learning Agent')
    parser.add_argument('--mode', type=str, default='TRAIN', choices=['TRAIN', 'RUN'],
                        help='Mode: TRAIN or RUN (default: TRAIN)')

    args = parser.parse_args()
    
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    agent_name = name  # Agent name
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
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = MyChickenAgent(agent_name)
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
            agent = MyChickenAgent(agent_name)
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
            agent = MyChickenAgent(agent_name)
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
        print("python stencils/lab03_stencil/my_agent.py --server --mode RUN")
