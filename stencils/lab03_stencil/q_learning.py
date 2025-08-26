#!/usr/bin/env python3
"""
Q-Learning implementation for Lab 3.
Students implement update_rule() and choose_next_move() methods.
"""

import sys
import os
import numpy as np
import random

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class QLearning(BaseAgent):
    """Q-Learning agent base class."""
    
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
        # Choose initial action
        self.a = self.training_policy.get_move(self.s)
    
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
        TODO: Implement the Q-learning update rule.
        
        Q(s,a) = Q(s,a) + α[r + γ max_{a'} Q(s',a') - Q(s,a)]
        
        Args:
            reward: Reward received from the last action
        """
        # TODO: Implement Q-learning update rule
        # Hint: Use self.s (current state), self.a (current action), 
        #       self.s_prime (next state), and self.q (Q-table)
        raise NotImplementedError
    
    def choose_next_move(self, s_prime: int):
        """
        TODO: Implement exploration-exploitation strategy.
        
        Args:
            s_prime: Next state
            
        Returns:
            Next action to take
        """
        # TODO: Implement exploration-exploitation
        # If in training mode:
        #   - With probability self.exploration_rate: choose random action
        #   - With probability 1 - self.exploration_rate: choose best action
        # If not in training mode:
        #   - Always choose best action
        raise NotImplementedError
    
    def update(self, reward: float, info=None):
        """Update the agent with the reward from the last action."""
        super().update(reward, info)
        
        # Determine next state
        s_prime = self.determine_state()
        
        # Update Q-table
        self.update_rule(reward)
        
        # Choose next action
        self.a = self.choose_next_move(s_prime)
        
        # Update current state
        self.s = s_prime
        
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


# TODO: Give your agent a NAME 
name = "QLearningAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = QLearning(name, num_possible_states=2, num_possible_actions=2,
                            initial_state=0, learning_rate=0.1, discount_factor=0.9,
                            exploration_rate=0.1, training_mode=True, save_path=None)
####################################################


if __name__ == "__main__":
    print("Q-Learning base class created successfully!")
    print("This is a base class - you should implement specific Q-learning agents that inherit from this.")
