"""
fictitious play agent for rock-paper-scissors.

implements the fictitious play algorithm which assumes the opponent
plays a fixed mixed strategy and best-responds to the empirical distribution.
"""

from typing import Dict, Any, List
import numpy as np
from core.agents.common.base_agent import BaseAgent


class FictitiousPlayAgent(BaseAgent):
    """
    agent that uses fictitious play to learn opponent's strategy.

    tracks opponent's action frequencies and plays the best response
    to their empirical distribution. converges to nash equilibrium
    in two-player zero-sum games.
    """

    def __init__(self, name: str = "FictitiousPlay"):
        super().__init__(name)
        self.actions = [0, 1, 2]  # rock, paper, scissors
        self.opponent_action_counts = [0, 0, 0]
        # rps payoff matrix: payoff[my_action][opp_action] = my_reward
        self.payoff_matrix = [
            [0, -1, 1],   # rock vs rock, paper, scissors
            [1, 0, -1],   # paper vs rock, paper, scissors
            [-1, 1, 0]    # scissors vs rock, paper, scissors
        ]

    def get_action(self, obs: Dict[str, Any] = None) -> int:
        """return the best response to predicted opponent distribution."""
        total_observations = sum(self.opponent_action_counts)

        if total_observations == 0:
            # no history yet, play randomly
            return int(np.random.choice(self.actions))

        # compute opponent's empirical distribution
        opponent_dist = np.array(self.opponent_action_counts) / total_observations

        # calculate expected payoff for each action
        expected_payoffs = np.zeros(3)
        for my_action in self.actions:
            for opp_action in self.actions:
                expected_payoffs[my_action] += (
                    opponent_dist[opp_action] * self.payoff_matrix[my_action][opp_action]
                )

        # choose action with highest expected payoff (break ties randomly)
        max_payoff = np.max(expected_payoffs)
        best_actions = [a for a in self.actions if expected_payoffs[a] == max_payoff]
        return int(np.random.choice(best_actions))

    def update(self, observation: Dict[str, Any] = None, action: Any = None,
               reward: float = None, done: bool = None, info: Dict[str, Any] = None):
        """update opponent action counts based on reward inference."""
        if reward is not None:
            self.reward_history.append(reward)

        # infer opponent's action from our action and reward
        if action is not None and reward is not None:
            opp_action = self._infer_opponent_action(action, reward)
            if opp_action is not None:
                self.opponent_action_counts[opp_action] += 1

    def _infer_opponent_action(self, my_action: int, reward: float) -> int:
        """
        infer opponent's action from our action and the reward received.

        in rps, the reward uniquely determines what the opponent played.
        """
        if reward == 0:
            # tie - opponent played same as us
            return my_action
        elif reward == 1:
            # we won - opponent played the action we beat
            # rock beats scissors, paper beats rock, scissors beats paper
            return (my_action + 2) % 3
        else:
            # we lost - opponent played the action that beats us
            # paper beats rock, scissors beats paper, rock beats scissors
            return (my_action + 1) % 3

    def reset(self):
        """reset the agent for a new game."""
        super().reset()
        self.opponent_action_counts = [0, 0, 0]

    def predict(self) -> List[float]:
        """return the predicted opponent distribution."""
        total = sum(self.opponent_action_counts)
        if total == 0:
            return [1/3, 1/3, 1/3]
        return [c / total for c in self.opponent_action_counts]

    def optimize(self, dist: List[float]) -> int:
        """return the best response to a given opponent distribution."""
        expected_payoffs = np.zeros(3)
        for my_action in self.actions:
            for opp_action in self.actions:
                expected_payoffs[my_action] += (
                    dist[opp_action] * self.payoff_matrix[my_action][opp_action]
                )
        return int(np.argmax(expected_payoffs))
