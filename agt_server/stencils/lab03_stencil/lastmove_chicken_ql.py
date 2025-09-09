#!/usr/bin/env python3
"""
Last Move Chicken Q-Learning Agent.
State space of size 2, where each state corresponds only to the opponent's last action.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class LastMoveChickenQL(QLearning):
    """Q-Learning agent with state space based on opponent's last action."""
    
    def __init__(self, name: str = "LastMoveChickenQL"):
        # 2 states: opponent's last action (0 or 1)
        # 2 actions: swerve (0) or continue (1)
        super().__init__(name, num_possible_states=2, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="lastmove-q-table.npy")
    
    def determine_state(self):
        """
        State is opponent's last action.
        State 0: opponent swerved last time
        State 1: opponent continued last time
        """
        if len(self.action_history) == 0:
            return 0  # Initial state
        
        # Infer opponent's last action from our reward
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Chicken payoff matrix (row player, column player):
        # S\C  S  C
        # S    0  -1
        # C    1  -5
        
        if my_last_action == 0:  # I swerved
            if my_last_reward == 0:
                return 0  # Opponent also swerved
            elif my_last_reward == -1:
                return 1  # Opponent continued
        elif my_last_action == 1:  # I continued
            if my_last_reward == 1:
                return 0  # Opponent swerved
            elif my_last_reward == -5:
                return 1  # Opponent also continued
        
        return 0  # Default to state 0 if can't determine


# TODO: Give your agent a NAME 
name = "LastMoveChickenQL"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = LastMoveChickenQL(name)
####################################################


if __name__ == "__main__":
    print("Testing Last Move Chicken Q-Learning Agent...")
    print("=" * 50)
    
    # Import required modules
    from core.engine import Engine
    from core.game.ChickenGame import ChickenGame
    from basic_chicken_agent import BasicChickenAgent
    
    # Create agents
    agent = LastMoveChickenQL("LastMoveQL")
    opponent = BasicChickenAgent("BasicChicken")
    
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
