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
        # Track action history for observations
        self.last_actions = {0: None, 1: None}

    def _init_stage(self):
        return MatrixStage(self.payoff_tensor)

    # overrides

    def reset(self, seed=None) -> ObsDict:
        self.t = 0
        self.cumulative_rewards = {0: 0.0, 1: 0.0}
        self.stage = MatrixStage(self.payoff_tensor)
        self.metadata["num_players"] = self.stage.n
        # Reset action history
        self.last_actions = {0: None, 1: None}
        # Provide basic game information in observations (no opponent action yet)
        return {0: {"round": 0, "opponent_last_action": None}, 1: {"round": 0, "opponent_last_action": None}}

    def players_to_move(self):
        return [0,1]

    def step(
        self,
        actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        # Store current actions for next round's observations
        self.last_actions = actions.copy()
        
        obs, rew, _, info = self.stage.step(actions)
        
        # accumulate rewards
        for player in [0, 1]:
            self.cumulative_rewards[player] += rew[player]
        
        self.t += 1
        done = self.t >= self.rounds
        
        if not done:
            # Create new stage for next round
            self.stage = MatrixStage(self.payoff_tensor)
            # observations with opponent's last action for next round
            obs = {
                0: {"round": self.t, "opponent_last_action": self.last_actions[1]},
                1: {"round": self.t, "opponent_last_action": self.last_actions[0]}
            }
        
        # return awards and actions oflast opponent
        return obs, rew, done, info
