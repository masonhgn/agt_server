#!/usr/bin/env python3
"""
Uniform random policy implementation.
"""

import random
from i_fixed_policy import IFixedPolicy


class UniformPolicy(IFixedPolicy):
    """Uniform random policy that chooses actions randomly."""
    
    def __init__(self, num_actions: int):
        """
        Initialize uniform policy.
        
        Args:
            num_actions: Number of possible actions
        """
        self.num_actions = num_actions
    
    def get_move(self, state: int) -> int:
        """
        Return a random action.
        
        Args:
            state: Current state (ignored for uniform policy)
            
        Returns:
            Random action from 0 to num_actions - 1
        """
        return random.randint(0, self.num_actions - 1)
