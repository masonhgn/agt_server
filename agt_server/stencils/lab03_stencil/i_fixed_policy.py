#!/usr/bin/env python3
"""
Interface for fixed policies.
"""

from abc import ABC, abstractmethod


class IFixedPolicy(ABC):
    """Interface for fixed policies."""
    
    @abstractmethod
    def get_move(self, state: int) -> int:
        """
        Return an action for the given state.
        
        Args:
            state: Current state
            
        Returns:
            Action to take
        """
        pass
