"""
agent that always continues in the chicken game.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class ContinueAgent(BaseAgent):
    """
    deterministic agent that always continues in the chicken game.

    continue is action 1. this aggressive strategy wins when opponent
    swerves but leads to crashes (-5, -5) when both continue.
    """

    def __init__(self, name: str = "Continue"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return continue (action 1)."""
        return 1

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
