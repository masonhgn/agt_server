#!/usr/bin/env python3
"""
State Space Representation Solutions for Lab 3 Part II.
This shows complete implementations of different state space representations for Chicken.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class LastMoveChickenQLSolution(QLearning):
    """Complete solution for LastMove Chicken Q-Learning agent."""
    
    def __init__(self, name: str = "LastMoveChickenQLSolution"):
        # 2 states: opponent's last action (0 or 1)
        # 2 actions: swerve (0) or continue (1)
        super().__init__(name, num_possible_states=2, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="lastmove-q-table-solution.npy")
    
    def determine_state(self):
        """
        COMPLETE IMPLEMENTATION: State is opponent's last action.
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


class LookbackChickenQLSolution(QLearning):
    """Complete solution for Lookback Chicken Q-Learning agent."""
    
    def __init__(self, name: str = "LookbackChickenQLSolution"):
        # 4 states: opponent's last two actions (00, 01, 10, 11)
        # 2 actions: swerve (0) or continue (1)
        super().__init__(name, num_possible_states=4, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="lookback-q-table-solution.npy")
    
    def determine_state(self):
        """
        COMPLETE IMPLEMENTATION: State is opponent's last two actions.
        State 0: opponent swerved twice in a row
        State 1: opponent swerved then continued
        State 2: opponent continued then swerved
        State 3: opponent continued twice in a row
        """
        if len(self.action_history) < 2:
            return 0  # Initial state
        
        # Infer opponent's last two actions from our rewards
        my_last_action = self.action_history[-1]
        my_second_last_action = self.action_history[-2]
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
        
        # Combine into state: 2 * second_last + last
        return 2 * opp_second_last_action + opp_last_action


class CustomChickenQLSolution(QLearning):
    """Complete solution for custom Chicken Q-Learning agent with advanced state representation."""
    
    def __init__(self, name: str = "CustomChickenQLSolution"):
        # 8 states: combination of opponent's last action and my last action
        # This creates a more sophisticated state space
        super().__init__(name, num_possible_states=8, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="custom-q-table-solution.npy")
    
    def determine_state(self):
        """
        COMPLETE IMPLEMENTATION: Advanced state representation.
        State combines opponent's last action and my last action.
        States 0-3: opponent's last action (0 or 1) + my last action (0 or 1)
        States 4-7: additional features based on recent patterns
        """
        if len(self.action_history) < 2:
            return 0  # Initial state
        
        # Get opponent's last action
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Infer opponent's last action
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
        
        # Basic state: 2 * opponent_action + my_action (states 0-3)
        basic_state = 2 * opp_last_action + my_last_action
        
        # Advanced features for states 4-7
        if len(self.action_history) >= 3:
            # Check for patterns in recent history
            recent_actions = self.action_history[-3:]
            if recent_actions == [1, 0, 0]:  # Pattern [1,0,0] detected
                return 4
            elif recent_actions == [0, 1, 0]:  # Pattern [0,1,0] detected
                return 5
            elif recent_actions == [0, 0, 1]:  # Pattern [0,0,1] detected
                return 6
            elif recent_actions == [1, 1, 1]:  # Pattern [1,1,1] detected
                return 7
        
        return basic_state


# Example usage and testing
if __name__ == "__main__":
    print("State Space Representation Solutions")
    print("=" * 50)
    
    # Test LastMove agent
    print("Testing LastMove Chicken Q-Learning Solution...")
    lastmove_agent = LastMoveChickenQLSolution("LastMoveSolution")
    
    # Test Lookback agent
    print("Testing Lookback Chicken Q-Learning Solution...")
    lookback_agent = LookbackChickenQLSolution("LookbackSolution")
    
    # Test Custom agent
    print("Testing Custom Chicken Q-Learning Solution...")
    custom_agent = CustomChickenQLSolution("CustomSolution")
    
    print("\nAll state space solutions created successfully!")
    print("These show complete implementations of different state representations.")
