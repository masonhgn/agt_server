# stages/matrix_stage.py
import numpy as np
from typing import Sequence

from core.stage.BaseStage import BaseStage, ObsDict, RewardDict, InfoDict, ActionDict, PlayerId


class MatrixStage(BaseStage):
    """
    Payoff tensor shape:  (hidden_states, A, A, num_players)
      - For PD/RPS hidden_states = 1  (use shape (1, A, A, 2))
      - Pass `hidden_idx` at instantiation if you want a mood-specific matrix.
    """

    def __init__(
        self,
        payoff_tensor: np.ndarray, #payoff matrix
        hidden_idx: int = 0, #if there is a hidden part like in moody BoS
        action_labels: Sequence[str] | None = None, #all actions in an easily readable form
    ):
        super().__init__(num_players=2) # there are 2 expected players in a matrix game (row and column player)
        self.tensor = payoff_tensor #payoff matrix
        self.h = hidden_idx
        self.action_labels = action_labels or list(range(payoff_tensor.shape[1]))



    #overrides

    def legal_actions(self, player_id: PlayerId = None):
        #we don't need a player id here because the legal actions are the same for both players
        return self.action_labels

    def step(self, actions: ActionDict):
        # Validate and unpack
        # there are 2 expected players in a matrix game (row and column player)
        self._validate_actions(actions, expected_players=[0,1]) 
        a0, a1 = actions[0], actions[1]

        # Payoffs from tensor
        r0, r1 = self.tensor[self.h, a0, a1]
        reward: RewardDict = {0: float(r0), 1: float(r1)}

        # One-shot stage ends immediately
        self._done = True
        obs: ObsDict = {0: {"round_complete": True}, 1: {"round_complete": True}} #indicate round is complete
        info: InfoDict = {}

        return obs, reward, True, info
