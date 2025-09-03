# stages/auction_stage.py
from __future__ import annotations

import random
from typing import Dict, List, Tuple, Callable, Any

from core.stage import (
    BaseStage,
    PlayerId,
    ObsDict,
    ActionDict,
    RewardDict,
    InfoDict,
)


class AuctionStage(BaseStage):
    """
    Generic simultaneous second-price auction for `m` goods.

    Parameters
    ----------
    num_players : int
        How many external agents will submit bid dictionaries.
    goods : List[str]
        Identifiers for each good (e.g. ["A", "B", ...]).
    value_fn : Callable[[PlayerId, List[str]], float]
        Function that returns *that player's* valuation for a list of won goods.
        In the single-agent arena you can pass a stub and let the outer Game
        compute utility separately; set `use_value_fn=False` in that case.
    rival_bid_sampler : Callable[[str], float] | None
        Optional sampler for *internal* rival bids.  If provided,
        the Stage will add one extra phantom bidder for each good,
        drawn independently via the sampler.
    use_value_fn : bool
        If False, Stage returns only payments in `info`; reward = 0.
        The calling Game/agent can compute utility later.
    """

    def __init__(
        self,
        num_players: int,
        goods: List[str],
        value_fn: Callable[[PlayerId, List[str]], float] | None = None,
        rival_bid_sampler: Callable[[str], float] | None = None,
        use_value_fn: bool = True,
    ):
        super().__init__(num_players)
        self.goods = goods
        self.m = len(goods)
        self.value_fn = value_fn or (lambda _pid, _bundle: 0.0)
        self.rival_sampler = rival_bid_sampler
        self.use_value_fn = use_value_fn

    # ---------- BaseStage ---------------------------------------------

    def legal_actions(self, _pid) -> Any:
        return f"Dict[str, float] with keys ⊆ {self.goods}"

    def step(
        self, actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        # 1) validation
        self._validate_actions(actions)

        # 2) collect bids per good
        bids_by_good: Dict[str, List[Tuple[float, PlayerId]]] = {g: [] for g in self.goods}
        for pid, bid_dict in actions.items():
            for g, b in bid_dict.items():
                if g not in self.goods:
                    raise ValueError(f"Unknown good {g}")
                bids_by_good[g].append((float(b), pid))

        # optional internal rival bids
        if self.rival_sampler is not None:
            for g in self.goods:
                bids_by_good[g].append((self.rival_sampler(g), "RIVAL"))

        # 3) clear each good
        allocation: Dict[str, PlayerId | None] = {}
        payments: Dict[PlayerId, float] = {pid: 0.0 for pid in actions}
        for g, lst in bids_by_good.items():
            if not lst:
                allocation[g] = None
                continue
            lst.sort(reverse=True)                        # highest first
            price_taker, price = lst[0]                   # top bid
            winner, winner_pid = price_taker, lst[0][1]
            second_price = lst[1][0] if len(lst) > 1 else 0.0
            if winner_pid in payments:                    # ignore RIVAL wins in multi-player
                allocation[g] = winner_pid
                payments[winner_pid] += second_price
            else:
                allocation[g] = None                      # rival won

        # 4) compute reward
        reward: RewardDict = {pid: 0.0 for pid in actions}
        if self.use_value_fn:
            for pid in actions:
                won = [g for g, w in allocation.items() if w == pid]
                reward[pid] = self.value_fn(pid, won) - payments[pid]

        # 5) return
        self._done = True
        obs: ObsDict = {pid: {} for pid in actions}
        info: InfoDict = {pid: {"payments": payments[pid]} for pid in actions}
        info["allocation"] = allocation

        return obs, reward, True, info
