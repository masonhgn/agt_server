"""
agent that always compromises in battle of the sexes.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class CompromiseAgent(BaseAgent):
    """
    deterministic agent that always plays compromise in battle of the sexes.

    compromise is action 0. both players compromising leads to coordination
    on one outcome.
    """

    def __init__(self, name: str = "Compromise"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return compromise (action 0)."""
        return 0

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
