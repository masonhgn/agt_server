#!/usr/bin/env python3
"""
My Chicken Q-Learning Agent.
Students implement their own state-space representation for Chicken.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class MyChickenAgent(QLearning):
    """Your custom Q-Learning agent for Chicken with your own state representation."""
    
    def __init__(self, name: str = "MyChickenAgent"):
        # TODO: Set the number of states based on your representation
        NUM_POSSIBLE_STATES = 4  # TODO: Adjust this based on your state representation
        
        super().__init__(name, num_possible_states=NUM_POSSIBLE_STATES, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="my-q-table.npy")
    
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
    print("Testing My Chicken Q-Learning Agent...")
    print("=" * 50)
    
    # Import required modules
    from core.engine import Engine
    from core.game.ChickenGame import ChickenGame
    from core.agents.lab03.random_chicken_agent import RandomChickenAgent
    
    # Create agents
    agent = MyChickenAgent("MyAgent")
    opponent = RandomChickenAgent("MysteryAgent")
    
    # Training phase
    print("TRAINING PHASE (20,000 rounds)")
    agent.set_training_mode(True)
    game = ChickenGame(rounds=20000)
    engine = Engine(game, [agent, opponent], rounds=20000)
    engine.run()
    
    # Testing phase
    print("\nTESTING PHASE (300 rounds)")
    agent.set_training_mode(False)
    game = ChickenGame(rounds=300)
    engine = Engine(game, [agent, opponent], rounds=300)
    final_rewards = engine.run()
    
    # Print results
    print(f"\nFinal rewards: {final_rewards}")
    print(f"Agent average reward: {sum(agent.reward_history[-300:]) / 300:.3f}")
    print(f"Agent total reward: {sum(agent.reward_history[-300:])}")
    
    # Print action distribution
    action_counts = [0, 0]
    for action in agent.action_history[-300:]:
        action_counts[action] += 1
    print(f"Action distribution: Swerve={action_counts[0]}, Continue={action_counts[1]}")
    
    print("\nTest completed!")
