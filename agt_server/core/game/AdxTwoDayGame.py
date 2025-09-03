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
        print(f"[GAME DEBUG] AdxTwoDayGame.reset() called with seed: {seed}", flush=True)
        if seed is not None:
            random.seed(seed)
        self.day = 1  # Start with day 1, not day 0
        self.qc = 1.0
        print(f"[GAME DEBUG] Creating initial AdxOfflineStage for day 1", flush=True)
        self.stage = AdxOfflineStage(self._num_players, 0, 1.0, self.rival_sampler)
        
        # Generate campaigns for each player
        self.campaigns_day1.clear()
        self.campaigns_day2.clear()
        for player_id in range(self._num_players):
            self.campaigns_day1[player_id] = self._generate_campaign(player_id, day=1)
            self.campaigns_day2[player_id] = self._generate_campaign(player_id, day=2)
            print(f"[GAME DEBUG] Generated campaigns for player {player_id}:", flush=True)
            print(f"[GAME DEBUG]   Day 1: {self._campaign_to_dict(self.campaigns_day1[player_id])}", flush=True)
            print(f"[GAME DEBUG]   Day 2: {self._campaign_to_dict(self.campaigns_day2[player_id])}", flush=True)
        
        obs = {}
        for i in range(self._num_players):
            obs[i] = {
                "day": 1,  # Start with day 1
                "campaign_day1": self._campaign_to_dict(self.campaigns_day1[i]),
                "campaign_day2": self._campaign_to_dict(self.campaigns_day2[i])
            }
        print(f"[GAME DEBUG] reset() returning observations: {obs}", flush=True)
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

    def _convert_two_day_bundle_to_bid_bundle(self, two_day_bundle: Union['TwoDaysBidBundle', Dict], campaign: Campaign = None) -> BidBundle:
        """Convert TwoDayBidBundle to BidBundle format for AdxOfflineStage."""
        print(f"[GAME DEBUG] _convert_two_day_bundle_to_bid_bundle called with: {two_day_bundle}", flush=True)
        print(f"[GAME DEBUG] Campaign: {campaign}", flush=True)
        
        bids = {}
        limits = {}
        
        # Handle both TwoDayBidBundle objects and dictionaries
        if isinstance(two_day_bundle, dict):
            print(f"[GAME DEBUG] Processing dictionary format", flush=True)
            # Handle dictionary format from client
            bid_entries = two_day_bundle.get('bid_entries', [])
            day_limit = two_day_bundle.get('day_limit', 0)
            print(f"[GAME DEBUG] Dictionary: bid_entries={bid_entries}, day_limit={day_limit}", flush=True)
            
            for entry in bid_entries:
                # Convert market segment string to segment ID
                market_segment_str = entry.get('market_segment', '')
                try:
                    seg_id = list(MarketSegment).index(MarketSegment(market_segment_str))
                    print(f"[GAME DEBUG] Market segment '{market_segment_str}' -> segment ID {seg_id}", flush=True)
                except (ValueError, KeyError) as e:
                    print(f"[GAME DEBUG] Warning: Market segment '{market_segment_str}' not found, skipping: {e}", flush=True)
                    # If market segment not found, skip this entry
                    continue
                
                bid = entry.get('bid', 0.0)
                spending_limit = entry.get('spending_limit', 0.0)
                
                bids[seg_id] = bid
                limits[seg_id] = int(spending_limit / bid) if bid > 0 else 0
                print(f"[GAME DEBUG] Entry: bid={bid}, spending_limit={spending_limit}, limit_impressions={limits[seg_id]}", flush=True)
            
            reach_goal = campaign.reach if campaign else 1000
            result = BidBundle(
                bids=bids,
                limits=limits,
                budget=day_limit,
                reach_goal=reach_goal
            )
            print(f"[GAME DEBUG] Dictionary conversion result: {result}", flush=True)
            return result
        else:
            print(f"[GAME DEBUG] Processing TwoDaysBidBundle object", flush=True)
            # Handle TwoDaysBidBundle object
            # Convert bid_entries to bids and limits dictionaries
            for entry in two_day_bundle.bid_entries:
                # Convert MarketSegment to segment ID (0-25)
                seg_id = list(MarketSegment).index(entry.market_segment)
                bids[seg_id] = entry.bid
                limits[seg_id] = int(entry.spending_limit / entry.bid) if entry.bid > 0 else 0
                print(f"[GAME DEBUG] Entry: segment={entry.market_segment}, bid={entry.bid}, spending_limit={entry.spending_limit}, limit_impressions={limits[seg_id]}", flush=True)
            
            # Create BidBundle with campaign reach goal
            reach_goal = campaign.reach if campaign else 1000
            result = BidBundle(
                bids=bids,
                limits=limits,
                budget=two_day_bundle.day_limit,
                reach_goal=reach_goal
            )
            print(f"[GAME DEBUG] Object conversion result: {result}", flush=True)
            return result

    def step(
        self, actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        print(f"[GAME DEBUG] AdxTwoDayGame.step() called with actions: {actions}", flush=True)
        print(f"[GAME DEBUG] Current day: {self.day}, num_players: {self._num_players}", flush=True)
        
        # Convert TwoDayBidBundle to BidBundle format
        converted_actions = {}
        for player_id, action in actions.items():
            print(f"[GAME DEBUG] Processing action for player {player_id}: {action}", flush=True)
            
            # Get the appropriate campaign for this day
            if self.day == 1:
                campaign = self.campaigns_day1[player_id]
                print(f"[GAME DEBUG] Player {player_id} day 1 campaign: {self._campaign_to_dict(campaign)}", flush=True)
            else:  # day == 2
                campaign = self.campaigns_day2[player_id]
                print(f"[GAME DEBUG] Player {player_id} day 2 campaign: {self._campaign_to_dict(campaign)}", flush=True)
            
            # Handle both TwoDayBidBundle objects and dictionaries
            if isinstance(action, dict) or hasattr(action, 'bid_entries'):
                converted_action = self._convert_two_day_bundle_to_bid_bundle(action, campaign)
                converted_actions[player_id] = converted_action
                print(f"[GAME DEBUG] Player {player_id} converted action: {converted_action}", flush=True)
            else:
                converted_actions[player_id] = action
                print(f"[GAME DEBUG] Player {player_id} action used as-is: {action}", flush=True)
        
        print(f"[GAME DEBUG] Calling stage.step() with converted actions: {converted_actions}", flush=True)
        obs, rew, done, info = self.stage.step(converted_actions)
        print(f"[GAME DEBUG] Stage.step() returned: obs={obs}, rew={rew}, done={done}, info={info}", flush=True)

        if self.day == 1:
            print(f"[GAME DEBUG] Day 1 complete, extracting QC from info[0]: {info[0] if info else 'No info'}", flush=True)
            # Extract QC from Stage info
            self.qc = info[0]["qc"] if info and 0 in info and "qc" in info[0] else 1.0
            print(f"[GAME DEBUG] QC extracted: {self.qc}", flush=True)
            
            # Start Day‑2 Stage
            self.day = 2
            print(f"[GAME DEBUG] Starting Day 2, creating new AdxOfflineStage", flush=True)
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
            print(f"[GAME DEBUG] Day 2 observations prepared: {obs}", flush=True)
            done = False
        elif self.day == 2:
            print(f"[GAME DEBUG] Day 2 complete, game finished", flush=True)
            # Day 2 is complete, game is done
            done = True

        print(f"[GAME DEBUG] step() returning: obs={obs}, rew={rew}, done={done}, info={info}", flush=True)
        return obs, rew, done, info

# --- TwoDaysBidBundle ---
@dataclass
class TwoDaysBidBundle:
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
