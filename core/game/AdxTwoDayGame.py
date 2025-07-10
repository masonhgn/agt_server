# games/adx_two_day.py
from typing import Tuple, cast, Dict, List
from core.game import ObsDict, ActionDict, RewardDict, InfoDict
from core.game.base_game import BaseGame
from core.stage.AdxOfflineStage import AdxOfflineStage, BidBundle
from dataclasses import dataclass, field
from core.game.market_segment import MarketSegment
from core.game.bid_entry import SimpleBidEntry


class AdxTwoDayGame(BaseGame):
    def __init__(self, rival_sampler=None):
        self.day = 0
        self.qc = 1.0
        self.rival_sampler = rival_sampler
        self.stage = AdxOfflineStage(
            num_players=1, day_idx=0, qc_multiplier=1.0, rival_sampler=rival_sampler
        )
        self.metadata = {"num_players": 1}

    # ---- BaseGame ---------------------------------------------------

    def reset(self, seed=None) -> ObsDict:
        self.day = 0
        self.qc = 1.0
        self.stage = AdxOfflineStage(1, 0, 1.0, self.rival_sampler)
        return cast(ObsDict, {0: {"day": 0}})

    def players_to_move(self):
        return [0]

    def _convert_two_day_bundle_to_bid_bundle(self, two_day_bundle: 'TwoDayBidBundle') -> BidBundle:
        """Convert TwoDayBidBundle to BidBundle format for AdxOfflineStage."""
        bids = {}
        limits = {}
        
        # Convert bid_entries to bids and limits dictionaries
        for entry in two_day_bundle.bid_entries:
            # Convert MarketSegment to segment ID (0-25)
            seg_id = list(MarketSegment).index(entry.market_segment)
            bids[seg_id] = entry.bid
            limits[seg_id] = int(entry.spending_limit / entry.bid) if entry.bid > 0 else 0
        
        # Create BidBundle with dummy values for budget and reach_goal
        # These will be overridden by the stage logic
        return BidBundle(
            bids=bids,
            limits=limits,
            budget=two_day_bundle.day_limit,
            reach_goal=1000  # Default reach goal
        )

    def step(
        self, actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        # Convert TwoDayBidBundle to BidBundle format
        converted_actions = {}
        for player_id, action in actions.items():
            if isinstance(action, TwoDayBidBundle):
                converted_actions[player_id] = self._convert_two_day_bundle_to_bid_bundle(action)
            else:
                converted_actions[player_id] = action
        
        obs, rew, done, info = self.stage.step(converted_actions)

        if self.day == 0:
            # Extract QC from Stage info
            self.qc = info[0]["qc"]
            # Start Day‑2 Stage
            self.day = 1
            self.stage = AdxOfflineStage(
                num_players=1,
                day_idx=1,
                qc_multiplier=self.qc,
                rival_sampler=self.rival_sampler,
            )
            obs = cast(ObsDict, {0: {"day": 1, "qc": self.qc}})
            done = False

        return obs, rew, done, info

# --- TwoDayBidBundle ---
@dataclass
class TwoDayBidBundle:
    day: int
    campaign_id: int
    day_limit: float
    bid_entries: List[SimpleBidEntry]
    # Internal tracking for simulation
    total_spent: float = 0.0
    impressions_won: Dict[MarketSegment, int] = field(default_factory=dict)

    def __post_init__(self):
        for entry in self.bid_entries:
            self.impressions_won[entry.market_segment] = 0
