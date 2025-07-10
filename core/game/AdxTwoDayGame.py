# games/adx_two_day.py
from typing import Tuple, cast, Dict, List, Union
from core.game import ObsDict, ActionDict, RewardDict, InfoDict
from core.game.base_game import BaseGame
from core.stage.AdxOfflineStage import AdxOfflineStage, BidBundle
from dataclasses import dataclass, field
from core.game.market_segment import MarketSegment
from core.game.bid_entry import SimpleBidEntry
from core.game.campaign import Campaign
import random


class AdxTwoDayGame(BaseGame):
    def __init__(self, num_players: int = 2, rival_sampler=None):
        super().__init__()
        self._num_players = num_players
        self.day = 0
        self.qc = 1.0
        self.rival_sampler = rival_sampler
        self.stage = AdxOfflineStage(
            num_players=num_players, day_idx=0, qc_multiplier=1.0, rival_sampler=rival_sampler
        )
        self.metadata = {"num_players": num_players}
        self.campaigns_day1: Dict[int, Campaign] = {}
        self.campaigns_day2: Dict[int, Campaign] = {}

    # ---- BaseGame ---------------------------------------------------

    def reset(self, seed=None) -> ObsDict:
        if seed is not None:
            random.seed(seed)
        self.day = 1  # Start with day 1, not day 0
        self.qc = 1.0
        self.stage = AdxOfflineStage(self._num_players, 0, 1.0, self.rival_sampler)
        
        # Generate campaigns for each player
        self.campaigns_day1.clear()
        self.campaigns_day2.clear()
        for player_id in range(self._num_players):
            self.campaigns_day1[player_id] = self._generate_campaign(player_id, day=1)
            self.campaigns_day2[player_id] = self._generate_campaign(player_id, day=2)
        
        obs = {}
        for i in range(self._num_players):
            obs[i] = {
                "day": 1,  # Start with day 1
                "campaign_day1": self._campaign_to_dict(self.campaigns_day1[i]),
                "campaign_day2": self._campaign_to_dict(self.campaigns_day2[i])
            }
        return cast(ObsDict, obs)

    def _generate_campaign(self, player_id: int, day: int) -> Campaign:
        """Generate a campaign for a player on a specific day."""
        # Pick a random segment with at least two attributes
        eligible_segments = [s for s in MarketSegment if len(s.value.split('_')) >= 2]
        segment = random.choice(eligible_segments)
        avg_users = 1000  # Default average users
        reach = int(avg_users * random.choice([0.3, 0.5, 0.7]))
        budget = float(reach)  # $1 per impression
        return Campaign(id=player_id * 10 + day, market_segment=segment, reach=reach, budget=budget)

    def _campaign_to_dict(self, campaign: Campaign) -> Dict:
        """Convert a Campaign object to a dictionary for JSON serialization."""
        return {
            "id": campaign.id,
            "market_segment": campaign.market_segment.value,
            "reach": campaign.reach,
            "budget": campaign.budget
        }

    def players_to_move(self):
        return list(range(self._num_players))

    def _convert_two_day_bundle_to_bid_bundle(self, two_day_bundle: Union['TwoDayBidBundle', Dict]) -> BidBundle:
        """Convert TwoDayBidBundle to BidBundle format for AdxOfflineStage."""
        bids = {}
        limits = {}
        
        # Handle both TwoDayBidBundle objects and dictionaries
        if isinstance(two_day_bundle, dict):
            # Handle dictionary format from client
            bid_entries = two_day_bundle.get('bid_entries', [])
            day_limit = two_day_bundle.get('day_limit', 0)
            
            for entry in bid_entries:
                # Convert market segment string to segment ID
                market_segment_str = entry.get('market_segment', '')
                try:
                    seg_id = list(MarketSegment).index(MarketSegment(market_segment_str))
                except (ValueError, KeyError):
                    # If market segment not found, skip this entry
                    continue
                
                bid = entry.get('bid', 0.0)
                spending_limit = entry.get('spending_limit', 0.0)
                
                bids[seg_id] = bid
                limits[seg_id] = int(spending_limit / bid) if bid > 0 else 0
            
            return BidBundle(
                bids=bids,
                limits=limits,
                budget=day_limit,
                reach_goal=1000  # Default reach goal
            )
        else:
            # Handle TwoDayBidBundle object
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
            # Handle both TwoDayBidBundle objects and dictionaries
            if isinstance(action, dict) or hasattr(action, 'bid_entries'):
                converted_actions[player_id] = self._convert_two_day_bundle_to_bid_bundle(action)
            else:
                converted_actions[player_id] = action
        
        obs, rew, done, info = self.stage.step(converted_actions)

        if self.day == 1:
            # Extract QC from Stage info
            self.qc = info[0]["qc"]
            # Start Day‑2 Stage
            self.day = 2
            self.stage = AdxOfflineStage(
                num_players=self._num_players,
                day_idx=1,
                qc_multiplier=self.qc,
                rival_sampler=self.rival_sampler,
            )
            obs = cast(ObsDict, {i: {
                "day": 2, 
                "qc": self.qc,
                "campaign_day1": self._campaign_to_dict(self.campaigns_day1[i]),
                "campaign_day2": self._campaign_to_dict(self.campaigns_day2[i])
            } for i in range(self._num_players)})
            done = False
        elif self.day == 2:
            # Day 2 is complete, game is done
            done = True

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

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "day": self.day,
            "campaign_id": self.campaign_id,
            "day_limit": self.day_limit,
            "bid_entries": [
                {
                    "market_segment": entry.market_segment.value,
                    "bid": entry.bid,
                    "spending_limit": entry.spending_limit
                }
                for entry in self.bid_entries
            ]
        }
