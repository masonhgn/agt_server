"""
random agent for rock-paper-scissors.
"""

import random
from typing import Dict, Any
from core.agents.common.rps_agent import RPSAgent


class RandomAgent(RPSAgent):
    """
    agent that plays uniformly random moves in rock-paper-scissors.

    useful as a baseline for measuring performance of learning agents.
    expected reward against any opponent is 0 in the long run.
    """

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return a uniformly random action."""
        return random.choice(self.actions)

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)

    def setup(self):
        """initialize the agent for a new game."""
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
