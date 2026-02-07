"""
agent that always defects in prisoner's dilemma.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class DefectAgent(BaseAgent):
    """
    deterministic agent that always defects in prisoner's dilemma.

    defect is action 1. this is the dominant strategy in single-shot
    prisoner's dilemma but leads to suboptimal outcomes when both defect.
    """

    def __init__(self, name: str = "Defect"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return defect (action 1)."""
        return 1

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
