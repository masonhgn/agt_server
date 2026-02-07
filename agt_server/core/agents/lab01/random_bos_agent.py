"""
random agent for battle of the sexes.
"""

import random
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class RandomBOSAgent(BaseAgent):
    """
    agent that plays uniformly random moves in battle of the sexes.

    randomly chooses between compromise (0) and stubborn (1) each round.
    """

    def __init__(self, name: str = "RandomBOS"):
        super().__init__(name)
        self.actions = [0, 1]  # compromise, stubborn

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return a random action: compromise (0) or stubborn (1)."""
        return random.choice(self.actions)

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
