#!/usr/bin/env python3
"""
base agent class for agt agents.

this module provides the base class that all agt agents should inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseAgent(ABC):
    """base class for all agt agents."""
    
    def __init__(self, name: str):
        """
        initialize the agent.
        
        args:
            name: name of the agent
        """
        self.name = name
        self.reward_history = []
        self.action_history = []
        self.observation_history = []
        self.opp_action_history = []  # Track opponent's actions
        self.opp_reward_history = []  # Track opponent's rewards
        self.game_round = 0  # Current round number
        
    @abstractmethod
    def get_action(self, observation: Dict[str, Any] = None) -> Any:
        """
        get the agent's action based on the current observation.
        
        args:
            observation: current game state observation (optional for backward compatibility)
            
        returns:
            the action to take
        """
        pass
    
    def update(self, observation: Dict[str, Any] = None, action: Any = None, reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """
        update the agent with the observation, action, reward, done status, and info from the last action.
        
        args:
            observation: current game state observation (optional for backward compatibility)
            action: action taken by this agent (optional for backward compatibility)
            reward: reward received from the last action (optional for backward compatibility)
            done: whether the game is done (optional for backward compatibility)
            info: additional information from the last action (optional for backward compatibility)
        """
        if observation is not None:
            self.observation_history.append(observation)
        if action is not None:
            self.action_history.append(action)
        if reward is not None:
            self.reward_history.append(reward)
        
    def setup(self):
        """
        Initialize the agent for a new game.
        Called at the beginning of each new game.
        """
        pass
        
    def reset(self):
        """reset the agent for a new game."""
        self.reward_history = []
        self.action_history = []
        self.observation_history = []
        self.opp_action_history = []
        self.opp_reward_history = []
        self.game_round = 0
        
    def get_statistics(self) -> Dict[str, Any]:
        """
        get statistics about the agent's performance.
        
        returns:
            dictionary containing agent statistics
        """
        stats = {
            "name": self.name,
            "total_reward": sum(self.reward_history),
            "average_reward": sum(self.reward_history) / len(self.reward_history) if self.reward_history else 0,
            "num_actions": len(self.action_history),
            "num_observations": len(self.observation_history)
        }
        
        return stats
    
    def get_last_action(self) -> Any:
        """Get the last action taken by this agent."""
        return self.action_history[-1] if self.action_history else None
    
    def get_last_reward(self) -> float | None:
        """Get the last reward received by this agent."""
        return self.reward_history[-1] if self.reward_history else None
    
    def get_action_history(self) -> List[Any]:
        """Get the complete action history."""
        return self.action_history.copy()
    
    def get_reward_history(self) -> List[float]:
        """Get the complete reward history."""
        return self.reward_history.copy()
    
    # New methods for Lab 1 compatibility
    def get_util_history(self) -> List[float]:
        """Get the complete utility history (alias for reward_history)."""
        return self.reward_history.copy()
    
    def get_last_util(self) -> float | None:
        """Get the last utility received (alias for last_reward)."""
        return self.reward_history[-1] if self.reward_history else None
    
    def get_opp_action_history(self) -> List[Any]:
        """Get the complete opponent action history."""
        return self.opp_action_history.copy()
    
    def get_opp_reward_history(self) -> List[float]:
        """Get the complete opponent reward history."""
        return self.opp_reward_history.copy()
    
    def get_opp_last_action(self) -> Any:
        """Get the opponent's last action."""
        return self.opp_action_history[-1] if self.opp_action_history else None
    
    def get_opp_last_util(self) -> float | None:
        """Get the opponent's last utility."""
        return self.opp_reward_history[-1] if self.opp_reward_history else None
    
    def calculate_utils(self, a1: Any, a2: Any) -> List[float]:
        """
        Calculate utilities for actions a1 and a2.
        This is a placeholder - subclasses should override this.
        
        args:
            a1: action of player 1
            a2: action of player 2
            
        returns:
            [u1, u2] where u1 is player 1's utility and u2 is player 2's utility
        """
        # Default implementation - subclasses should override
        return [0, 0]
    
    def add_opponent_action(self, action: Any):
        """Add opponent's action to history."""
        self.opp_action_history.append(action)
    
    def add_opponent_reward(self, reward: float):
        """Add opponent's reward to history."""
        self.opp_reward_history.append(reward)
    
    # Optional methods for Lab 1 - these have default implementations for non-Lab1 agents
    def predict(self) -> List[float]:
        """
        Predict opponent's next move distribution.
        This method will be called directly by the server for Fictitious Play agents.
        Default implementation for non-Lab1 agents.
        
        returns:
            probability distribution over opponent's next move
        """
        # Default implementation - Lab 1 agents should override this
        raise NotImplementedError("predict() method not implemented - this agent is not a Lab 1 Fictitious Play agent")
    
    def optimize(self, dist: List[float]) -> Any:
        """
        Find best response to opponent's predicted distribution.
        This method will be called directly by the server for Fictitious Play agents.
        Default implementation for non-Lab1 agents.
        
        args:
            dist: probability distribution over opponent's next move
            
        returns:
            the best action to take
        """
        # Default implementation - Lab 1 agents should override this
        raise NotImplementedError("optimize() method not implemented - this agent is not a Lab 1 Fictitious Play agent")
    
    def calc_move_probs(self) -> List[float]:
        """
        Calculate move probabilities using Exponential Weights strategy.
        This method will be called directly by the server for Exponential Weights agents.
        Default implementation for non-Lab1 agents.
        
        returns:
            probability distribution over your next move
        """
        # Default implementation - Lab 1 agents should override this
        raise NotImplementedError("calc_move_probs() method not implemented - this agent is not a Lab 1 Exponential Weights agent")
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')" 