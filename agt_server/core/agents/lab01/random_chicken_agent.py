"""
random agent for the chicken game.
"""

import random
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class RandomChickenAgent(BaseAgent):
    """
    agent that plays uniformly random moves in the chicken game.

    randomly chooses between swerve (0) and continue (1) each round.
    """

    def __init__(self, name: str = "RandomChicken"):
        super().__init__(name)
        self.actions = [0, 1]  # swerve, continue

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return a random action: swerve (0) or continue (1)."""
        return random.choice(self.actions)

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
