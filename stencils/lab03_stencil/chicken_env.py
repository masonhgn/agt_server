#!/usr/bin/env python3
"""
Chicken game environment for Lab 3.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.ChickenGame import ChickenGame


class ChickenEnv:
    """Chicken game environment wrapper."""
    
    def __init__(self, rounds: int = 100):
        """
        Initialize Chicken environment.
        
        Args:
            rounds: Number of rounds to play
        """
        self.game = ChickenGame(rounds=rounds)
        self.rounds = rounds
    
    def reset(self):
        """Reset the environment for a new game."""
        return self.game.reset()
    
    def step(self, actions):
        """
        Take a step in the environment.
        
        Args:
            actions: Dictionary of player actions
            
        Returns:
            Tuple of (observations, rewards, done, info)
        """
        return self.game.step(actions)
    
    def players_to_move(self):
        """Get list of players who need to move."""
        return self.game.players_to_move()
    
    def is_done(self):
        """Check if the game is done."""
        return self.game.is_done()
