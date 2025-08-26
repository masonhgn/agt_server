#!/usr/bin/env python3
"""
Q-Learning base class for Lab 4 - Lemonade Stand Game.
"""

import sys
import os
import numpy as np
import random

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class QLearning(BaseAgent):
    """Q-Learning agent base class for Lemonade Stand Game."""
    
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
        
        # Initialize Q-table optimistically (as suggested in writeup)
        self.q = np.full((num_possible_states, num_possible_actions), 12.0)
        
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
        Q-learning update rule.
        
        Q(s,a) = Q(s,a) + α[r + γ max_{a'} Q(s',a') - Q(s,a)]
        
        Args:
            reward: Reward received from the last action
        """
        # Determine next state
        s_prime = self.determine_state()
        
        # Q-learning update
        max_q_next = np.max(self.q[s_prime])
        self.q[self.s][self.a] = self.q[self.s][self.a] + self.learning_rate * (
            reward + self.discount_factor * max_q_next - self.q[self.s][self.a]
        )
        
        # Update current state and choose next action
        self.s = s_prime
        self.a = self.choose_next_move(s_prime)
        
        # Save Q-table if path is specified
        if self.save_path:
            np.save(self.save_path, self.q)
    
    def choose_next_move(self, s_prime: int):
        """
        Exploration-exploitation strategy.
        
        Args:
            s_prime: Next state
            
        Returns:
            Next action to take
        """
        if self.training_mode:
            # With probability exploration_rate, choose random action
            if random.random() < self.exploration_rate:
                return self.training_policy.get_move(s_prime)
            else:
                # Choose best action
                return np.argmax(self.q[s_prime])
        else:
            # Always choose best action when not training
            return np.argmax(self.q[s_prime])
    
    def update(self, reward: float, info=None):
        """Update the agent with the reward from the last action."""
        super().update(reward, info)
        self.update_rule(reward)
    
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
