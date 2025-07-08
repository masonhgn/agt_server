# stages/price_stage.py
from __future__ import annotations

from typing import Callable, Dict, Tuple, Any

from core.stage import (
    BaseStage,
    PlayerId,
    ObsDict,
    ActionDict,
    RewardDict,
    InfoDict,
)


class PriceStage(BaseStage):
    """
    Two-seller price-posting market (Lab 3).
    This is part III (the final part) of lab 3.

    Parameters
    ----------
    demand_fn : Callable[[float, float], Tuple[float, float]]
        Function that returns *quantities sold* (q0, q1) given the posted
        prices (p0, p1).  Default is symmetric linear demand:
            q0 = max(0, a - b*p0 + c*p1)
            q1 = max(0, a - b*p1 + c*p0)
        with (a, b, c) chosen below.
    cost : float
        Constant unit cost c_u for both sellers.
    price_grid : Tuple[float, float, float]
        (p_min, p_max, step) — allowed discrete prices.
    """

    def __init__(
        self,
        demand_fn: Callable[[float, float], Tuple[float, float]] | None = None,
        cost: float = 0.0,
        price_grid: Tuple[float, float, float] = (0.0, 10.0, 0.5),
    ):
        super().__init__(num_players=2)
        self.cost = cost
        self.grid = price_grid
        if demand_fn is None:
            a, b, c = 20.0, 1.0, 0.5

            def lin_demand(p0: float, p1: float):
                q0 = max(0.0, a - b * p0 + c * p1)
                q1 = max(0.0, a - b * p1 + c * p0)
                return q0, q1

            self.demand_fn = lin_demand
        else:
            self.demand_fn = demand_fn

    # ---------------- BaseStage overrides -----------------------------

    def legal_actions(self, _pid: PlayerId) -> Any:
        p_min, p_max, step = self.grid
        return [round(p_min + i * step, 4) for i in range(int((p_max - p_min) / step) + 1)]

    def step(
        self,
        actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        
        #validate actions
        self._validate_actions(actions, expected_players=[0, 1])
        p0, p1 = float(actions[0]), float(actions[1])

        # quantities via demand_fn
        q0, q1 = self.demand_fn(p0, p1)

        # profit = (price - cost) * quantity
        r0 = (p0 - self.cost) * q0
        r1 = (p1 - self.cost) * q1
        reward: RewardDict = {0: r0, 1: r1}

        self._done = True
        obs: ObsDict = {0: {"p_opp": p1}, 1: {"p_opp": p0}}
        info: InfoDict = {"quantities": (q0, q1)}

        return obs, reward, True, info
