"""
random agent for prisoner's dilemma.
"""

import random
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class RandomPDAgent(BaseAgent):
    """
    agent that plays uniformly random moves in prisoner's dilemma.

    randomly chooses between cooperate (0) and defect (1) each round.
    """

    def __init__(self, name: str = "RandomPD"):
        super().__init__(name)
        self.actions = [0, 1]  # cooperate, defect

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return a random action: cooperate (0) or defect (1)."""
        return random.choice(self.actions)

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
