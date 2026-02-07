"""
agent that always plays scissors in rock-paper-scissors.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class ScissorsAgent(BaseAgent):
    """
    deterministic agent that always plays scissors.

    useful as a baseline opponent for testing adaptive strategies.
    """

    def __init__(self, name: str = "Scissors"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return scissors (action 2)."""
        return 2

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
