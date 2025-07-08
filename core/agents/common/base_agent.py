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
        
    @abstractmethod
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """
        get the agent's action based on the current observation.
        
        args:
            observation: current game state observation
            
        returns:
            the action to take
        """
        pass
    
    def update(self, reward: float, info: Dict[str, Any]):
        """
        update the agent with the reward and info from the last action.
        
        args:
            reward: reward received from the last action
            info: additional information from the last action
        """
        self.reward_history.append(reward)
        
    def reset(self):
        """reset the agent for a new game."""
        self.reward_history = []
        self.action_history = []
        self.observation_history = []
        
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
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')" 