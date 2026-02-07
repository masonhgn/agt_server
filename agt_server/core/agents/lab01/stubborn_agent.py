"""
agent that always plays stubborn in battle of the sexes.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class StubbornAgent(BaseAgent):
    """
    deterministic agent that always plays stubborn in battle of the sexes.

    stubborn is action 1. being stubborn when opponent compromises leads
    to a favorable outcome, but mutual stubbornness leads to miscoordination.
    """

    def __init__(self, name: str = "Stubborn"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return stubborn (action 1)."""
        return 1

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
