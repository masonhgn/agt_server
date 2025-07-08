# games/repeated_matrix.py
from typing import Dict, Tuple
import numpy as np

from core.game.base_game import BaseGame, ObsDict, ActionDict, RewardDict, InfoDict
from core.stage.MatrixStage import MatrixStage


class MatrixGame(BaseGame):
    """
    Run the same MatrixStage for `rounds` iterations and sum payoffs.
    """

    def __init__(self, payoff_tensor, rounds=1000):
        self.payoff_tensor = payoff_tensor
        self.rounds = rounds
        self.t = 0
        self.stage = self._init_stage() if not hasattr(self, 'stage') or self.stage is None else self.stage
        self.metadata = {}
        self.cumulative_rewards = {0: 0.0, 1: 0.0}

    def _init_stage(self):
        return MatrixStage(self.payoff_tensor)

    # overrides

    def reset(self, seed=None) -> ObsDict:
        self.t = 0
        self.cumulative_rewards = {0: 0.0, 1: 0.0}
        self.stage = MatrixStage(self.payoff_tensor)
        self.metadata["num_players"] = self.stage.n
        return {0: {}, 1: {}} #nothing to see initially

    def players_to_move(self):
        return [0,1]

    def step(
        self,
        actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        obs, rew, _, info = self.stage.step(actions)
        
        # Accumulate rewards
        for player in [0, 1]:
            self.cumulative_rewards[player] += rew[player]
        
        self.t += 1
        done = self.t >= self.rounds
        
        if not done:
            # Create new stage for next round
            self.stage = MatrixStage(self.payoff_tensor)
        
        # Return cumulative rewards for the final round, individual rewards for others
        if done:
            return obs, self.cumulative_rewards, done, info
        else:
            return obs, rew, done, info
