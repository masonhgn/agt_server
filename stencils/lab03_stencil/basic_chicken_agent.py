#!/usr/bin/env python3
"""
Basic Chicken Agent that plays actions [1,0,0] in sequence.
This is used as a simple opponent for Q-learning training.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class BasicChickenAgent(BaseAgent):
    """Basic Chicken agent that plays actions [1,0,0] in sequence."""
    
    def __init__(self, name: str = "BasicChicken"):
        super().__init__(name)
        self.SWERVE, self.CONTINUE = 0, 1
        self.actions = [self.SWERVE, self.CONTINUE]
        self.round_count = 0
    
    def setup(self):
        """Initialize for a new game."""
        self.round_count = 0
    
    def get_action(self, obs=None):
        """
        Play actions [1,0,0] in sequence, repeating.
        
        Returns:
            0 (Swerve) or 1 (Continue) based on the pattern
        """
        # Pattern: [1,0,0] repeated
        pattern = [1, 0, 0]
        action = pattern[self.round_count % len(pattern)]
        self.round_count += 1
        return action
    
    def update(self, reward: float, info=None):
        """Update with reward from last action."""
        super().update(reward, info)


# Agent instance for testing
basic_chicken_agent = BasicChickenAgent("BasicChicken")


if __name__ == "__main__":
    print("Basic Chicken Agent created successfully!")
    print("This agent plays actions [1,0,0] in sequence, repeating.")
