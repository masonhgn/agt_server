from __future__ import annotations

import math
from typing import List, Tuple, Dict

from core.stage.BaseStage import BaseStage, PlayerId, ObsDict, ActionDict, RewardDict, InfoDict


class SpatialStage(BaseStage):
    """
    Three-player Lemonade Stand on a 12-position circle.
    Action = integer in [0, 11]   (clock positions)
    Pay-off rule:
        - Customers are uniformly distributed on the circumference.
        - Each customer buys from the *closest* stand; ties are split equally.
        - With discrete spots this reduces to:
            reward[p] = 0.5 * (gap_left + gap_right)
            where gap_* are arc lengths (# spots) between adjacent stands.
    """

    POSITIONS = list(range(12))

    def __init__(self, num_players: int = 3):
        super().__init__(num_players)
        if self.n != 3:
            raise ValueError("Classic Lemonade variant expects exactly 3 players")
        self._actions: Dict[PlayerId, int] = {}





    # overrides

    def legal_actions(self, player_id = None):
        return self.POSITIONS

    def step(
        self, actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        # Validate
        self._validate_actions(actions, expected_players=[0, 1, 2])

        self._actions = {pid: int(a) % 12 for pid, a in actions.items()}  # ensure 0-11
        # Compute clockwise sorted order of (pos, pid)
        ordered: List[Tuple[int, PlayerId]] = sorted(
            ((pos, pid) for pid, pos in self._actions.items()), key=lambda t: t[0]
        )

        # Append first entry + 12 to simplify wrap-around gap calc
        extended = ordered + [(ordered[0][0] + 12, ordered[0][1])]

        # Gaps and rewards
        reward: RewardDict = {pid: 0.0 for pid in actions}
        for i in range(3):
            pos_curr, pid_curr = extended[i]
            pos_next, _ = extended[i + 1]
            gap = pos_next - pos_curr
            # Each of the two adjacent players shares half the gap
            reward[pid_curr] += gap / 2.0

        self._done = True
        obs: ObsDict = {pid: {} for pid in actions}
        info: InfoDict = {"positions": self._actions}

        return obs, reward, True, info