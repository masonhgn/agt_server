#!/usr/bin/env python3
"""
Complete Q-Learning Solution for Lab 3 Part I.
This shows the implementation of update_rule() and choose_next_move() methods.
"""

import sys
import os
import numpy as np
import random

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class QLearningSolution(BaseAgent):
    """Complete Q-Learning implementation with all methods implemented."""
    
    def __init__(self, name: str, num_possible_states: int, num_possible_actions: int, 
                 initial_state: int, learning_rate: float, discount_factor: float, 
                 exploration_rate: float, training_mode: bool, save_path: str = None):
        super().__init__(name)
        self.num_possible_states = num_possible_states
        self.num_possible_actions = num_possible_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.training_mode = training_mode
        self.save_path = save_path
        
        # Current state and action
        self.s = initial_state
        self.a = None
        
        # Initialize Q-table
        self.q = np.zeros((num_possible_states, num_possible_actions))
        
        # Training policy (uniform random by default)
        self.training_policy = UniformPolicy(num_possible_actions)
        
        # Load saved Q-table if it exists
        if save_path and os.path.isfile(save_path):
            self.q = np.load(save_path)
    
    def setup(self):
        """Initialize for a new game."""
        # Initialize state and action according to Q-learning pseudocode
        self.s = self.determine_state()  # Initialize current state
        self.a = self.choose_next_move(self.s)  # Choose initial action
    
    def get_action(self, obs=None):
        """Get the current action."""
        return self.a
    
    def determine_state(self):
        """
        Determine the current state based on game history.
        Subclasses should override this method.
        """
        raise NotImplementedError("Subclasses must implement determine_state()")
    
    def update_rule(self, reward: float):
        """
        COMPLETE IMPLEMENTATION: Q-learning update rule.
        
        Q(s,a) = Q(s,a) + α[r + γ max_{a'} Q(s',a') - Q(s,a)]
        
        Args:
            reward: Reward received from the last action
        """
        # Step 1: Determine the next state
        s_prime = self.determine_state()
        
        # Step 2: Find the maximum Q-value for the next state
        max_q_next = np.max(self.q[s_prime])
        
        # Step 3: Apply the Q-learning update rule
        # Q(s,a) = Q(s,a) + α[r + γ max_{a'} Q(s',a') - Q(s,a)]
        self.q[self.s, self.a] = self.q[self.s, self.a] + self.learning_rate * (
            reward + self.discount_factor * max_q_next - self.q[self.s, self.a]
        )
        
        # Step 4: Update current state for next iteration
        self.s = s_prime
    
    def choose_next_move(self, s_prime: int):
        """
        COMPLETE IMPLEMENTATION: Exploration-exploitation strategy.
        
        Args:
            s_prime: Next state
            
        Returns:
            Next action to take
        """
        if self.training_mode:
            # Exploration-exploitation trade-off
            if np.random.random() < self.exploration_rate:
                # Exploration: choose random action
                return np.random.randint(0, self.num_possible_actions)
            else:
                # Exploitation: choose best action
                return np.argmax(self.q[s_prime])
        else:
            # Pure exploitation: always choose best action
            return np.argmax(self.q[s_prime])
    
    def update(self, reward: float, info=None):
        """Update the agent with the reward from the last action."""
        super().update(reward, info)
        
        # Update Q-table using the Q-learning update rule
        self.update_rule(reward)
        
        # Choose next action based on current state
        self.a = self.choose_next_move(self.s)
        
        # Save Q-table if path is specified
        if self.save_path:
            np.save(self.save_path, self.q)
    
    def set_training_mode(self, training_mode: bool):
        """Set whether the agent is in training mode."""
        self.training_mode = training_mode


class UniformPolicy:
    """Uniform random policy for exploration."""
    
    def __init__(self, num_actions: int):
        self.num_actions = num_actions
    
    def get_move(self, state: int) -> int:
        """Return a random action."""
        return random.randint(0, self.num_actions - 1)


class IFixedPolicy:
    """Interface for fixed policies."""
    
    def get_move(self, state: int) -> int:
        """Return an action for the given state."""
        raise NotImplementedError("Subclasses must implement get_move()")


# Example usage
if __name__ == "__main__":
    print("Q-Learning Solution - Complete Implementation")
    print("This shows how to implement update_rule() and choose_next_move()")
    print("Students should use this as a reference for their implementations.")
