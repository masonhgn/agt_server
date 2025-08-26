#!/usr/bin/env python3
"""
Complete Solution for my_agent.py - Lab 3 Part II.
This shows the implementation of determine_state() for custom state representation.
"""

import sys
import os

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


# Example usage and testing
if __name__ == "__main__":
    print("My Chicken Agent Solution - Complete Implementation")
    print("=" * 60)
    
    # Test the agent
    agent = MyChickenAgentSolution("MyAgentSolution")
    print(f"Agent created successfully")
    print(f"   - States: {agent.num_possible_states}")
    print(f"   - Actions: {agent.num_possible_actions}")
    print(f"   - Save path: {agent.save_path}")
    
    print("\nThis shows a complete implementation of determine_state()")
    print("for a custom state representation that combines both")
    print("opponent's and my own recent action history.")
