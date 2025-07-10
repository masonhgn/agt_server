from typing import Dict, Tuple

from core.game import ObsDict, ActionDict, RewardDict, InfoDict, BaseGame
from core.stage.PriceStage import PriceStage


class MarketGame(BaseGame):
    """
    One long price-posting Stage (20,000+ learning rounds happen
    *outside* in the RL agent; this Game is a single atomic episode).
    """

    def __init__(self, price_stage: PriceStage | None = None):
        self.stage = price_stage or PriceStage()
        self.metadata: Dict[str, int] = {"num_players": 2}



    def reset(self, seed=None) -> ObsDict:
        self.stage._done = False   # one fresh stage – no rounds counter
        return {0: {}, 1: {}}

    def players_to_move(self):
        return [0, 1]

    def step(
        self,
        actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        return self.stage.step(actions)