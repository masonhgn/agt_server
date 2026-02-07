"""
base class for rock-paper-scissors agents.

provides common functionality including action constants, payoff matrix,
and default implementations of strategy methods.
"""

import random
from typing import Dict, Any, List
from core.agents.common.base_agent import BaseAgent


class RPSAgent(BaseAgent):
    """
    base class for rock-paper-scissors agents.

    provides action constants (ROCK=0, PAPER=1, SCISSORS=2), the payoff
    matrix, and default implementations of predict/optimize methods.
    """

    def __init__(self, name: str = "RPSAgent"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]

        # payoff matrix: payoff_matrix[my_action][opp_action] = my_reward
        self.payoff_matrix = [
            [0, -1, 1],   # rock vs rock, paper, scissors
            [1, 0, -1],   # paper vs rock, paper, scissors
            [-1, 1, 0]    # scissors vs rock, paper, scissors
        ]

    def calculate_utils(self, a1: int, a2: int) -> List[float]:
        """
        calculate utilities for actions a1 and a2 in rps.

        args:
            a1: action of player 1 (0=rock, 1=paper, 2=scissors)
            a2: action of player 2 (0=rock, 1=paper, 2=scissors)

        returns:
            [u1, u2] where u1 is player 1's utility and u2 is player 2's
        """
        if a1 not in self.actions or a2 not in self.actions:
            return [0.0, 0.0]

        u1 = float(self.payoff_matrix[a1][a2])
        u2 = float(self.payoff_matrix[a2][a1])
        return [u1, u2]

    def get_action(self, observation: Dict[str, Any] = None) -> int:
        """
        get the agent's action. subclasses should override this.

        args:
            observation: current game state observation

        returns:
            the action to take (0=rock, 1=paper, 2=scissors)
        """
        raise NotImplementedError("subclasses must implement get_action")

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """
        update the agent with the reward from the last action.

        args:
            observation: current game state observation
            action: action taken
            reward: reward received from the last action
            done: whether the game is done
            info: additional information
        """
        if reward is not None:
            self.reward_history.append(reward)

    def setup(self):
        """initialize the agent for a new game."""
        pass

    def predict(self) -> List[float]:
        """
        predict opponent's action distribution.

        default implementation returns uniform distribution.
        subclasses should override for fictitious play or other strategies.
        """
        return [1/3, 1/3, 1/3]

    def optimize(self, dist: List[float]) -> int:
        """
        return the best response to a given opponent distribution.

        default implementation returns random action.
        subclasses should override for strategic play.
        """
        return random.choice(self.actions)

    def calc_move_probs(self) -> List[float]:
        """
        calculate this agent's mixed strategy probabilities.

        default implementation returns uniform distribution.
        subclasses should override for exponential weights or other strategies.
        """
        return [1/3, 1/3, 1/3]
