#!/usr/bin/env python3
"""
Chicken agent base class for Chicken games.
"""

from core.agents.common.base_agent import BaseAgent


class ChickenAgent(BaseAgent):
    """Base class for Chicken game agents."""
    
    def __init__(self, name: str = "ChickenAgent"):
        super().__init__(name)
        self.SWERVE, self.CONTINUE = 0, 1
        self.actions = [self.SWERVE, self.CONTINUE]
        
        # Chicken payoff matrix (row player, column player)
        # S\C  S  C
        # S    0  -1
        # C    1  -5
        # Where S = Swerve, C = Continue
        self.payoff_matrix = [
            [0, -1],      # Swerve vs Swerve, Continue
            [1, -5]       # Continue vs Swerve, Continue
        ]
    
    def calculate_utils(self, a1: int, a2: int) -> list[float]:
        """
        Calculate utilities for actions a1 and a2 in Chicken.
        
        args:
            a1: action of player 1 (0=Swerve, 1=Continue)
            a2: action of player 2 (0=Swerve, 1=Continue)
            
        returns:
            [u1, u2] where u1 is player 1's utility and u2 is player 2's utility
        """
        if a1 not in self.actions or a2 not in self.actions:
            return [0, 0]
        
        u1 = self.payoff_matrix[a1][a2]
        u2 = self.payoff_matrix[a2][a1]  # Opponent's utility is the transpose
        return [u1, u2]
    
    def get_action(self, observation=None):
        """
        Get the agent's action. Subclasses should override this.
        
        args:
            observation: current game state observation (optional)
            
        returns:
            the action to take (0=Swerve, 1=Continue)
        """
        raise NotImplementedError("Subclasses must implement get_action")
    
    def update(self, reward=None, info=None):
        """
        Update the agent with the reward from the last action.
        
        args:
            reward: reward received from the last action
            info: additional information (optional)
        """
        if reward is not None:
            self.reward_history.append(reward)
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass
    
    # Default implementations for Lab 1 abstract methods
    def predict(self) -> list[float]:
        """
        Default implementation: predict uniform distribution.
        Subclasses should override this for Fictitious Play.
        """
        return [1/2, 1/2]
    
    def optimize(self, dist: list[float]) -> int:
        """
        Default implementation: return random action.
        Subclasses should override this for Fictitious Play.
        """
        import random
        return random.choice(self.actions)
    
    def calc_move_probs(self) -> list[float]:
        """
        Default implementation: return uniform distribution.
        Subclasses should override this for Exponential Weights.
        """
        return [1/2, 1/2]
