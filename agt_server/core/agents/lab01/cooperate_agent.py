"""
agent that always cooperates in prisoner's dilemma.
"""

from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class CooperateAgent(BaseAgent):
    """
    deterministic agent that always cooperates in prisoner's dilemma.

    cooperate is action 0. this agent will be exploited by defectors
    but achieves mutual cooperation against other cooperators.
    """

    def __init__(self, name: str = "Cooperate"):
        super().__init__(name)

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """always return cooperate (action 0)."""
        return 0

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
