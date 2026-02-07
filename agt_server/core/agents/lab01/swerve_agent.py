"""
agent that always swerves in the chicken game.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class SwerveAgent(BaseAgent):
    """
    deterministic agent that always swerves in the chicken game.

    swerve is action 0. this agent avoids crashes but may be exploited
    by aggressive opponents who always continue.
    """

    def __init__(self, name: str = "Swerve"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return swerve (action 0)."""
        return 0

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
