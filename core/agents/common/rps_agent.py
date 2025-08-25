#!/usr/bin/env python3
"""
RPS agent base class for Rock-Paper-Scissors games.
"""

from core.agents.common.base_agent import BaseAgent


class RPSAgent(BaseAgent):
    """Base class for Rock-Paper-Scissors agents."""
    
    def __init__(self, name: str = "RPSAgent"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        
        # RPS payoff matrix (row player, column player)
        # R\C  R  P  S
        # R    0 -1  1
        # P    1  0 -1
        # S   -1  1  0
        self.payoff_matrix = [
            [0, -1, 1],   # Rock vs Rock, Paper, Scissors
            [1, 0, -1],   # Paper vs Rock, Paper, Scissors
            [-1, 1, 0]    # Scissors vs Rock, Paper, Scissors
        ]
    
    def calculate_utils(self, a1: int, a2: int) -> list[float]:
        """
        Calculate utilities for actions a1 and a2 in RPS.
        
        args:
            a1: action of player 1 (0=Rock, 1=Paper, 2=Scissors)
            a2: action of player 2 (0=Rock, 1=Paper, 2=Scissors)
            
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
            the action to take (0=Rock, 1=Paper, 2=Scissors)
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
        return [1/3, 1/3, 1/3]
    
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
        return [1/3, 1/3, 1/3]
