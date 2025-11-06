# stages/adx_two_day_stage.py
from __future__ import annotations
import math
import numpy as np
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional

from core.stage.BaseStage import BaseStage
from core.game import PlayerId, ObsDict, ActionDict, RewardDict, InfoDict
from core.game.market_segment import MarketSegment
from core.game.bid_entry import SimpleBidEntry
from core.game.campaign import Campaign


@dataclass
class TwoDaysBidBundle:
    """Bid bundle for 2-day ADX game."""
    day: int
    campaign_id: int
    day_limit: float
    bid_entries: List[SimpleBidEntry]
    # Internal tracking for simulation
    total_spent: float = 0.0
    impressions_won: Dict[MarketSegment, int] = field(default_factory=dict)
    segment_spending: Dict[MarketSegment, float] = field(default_factory=dict)

    def __post_init__(self):
        for entry in self.bid_entries:
            self.impressions_won[entry.market_segment] = 0
            self.segment_spending[entry.market_segment] = 0.0

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
            ],
            "total_spent": self.total_spent,
            "impressions_won": {segment.value: count for segment, count in self.impressions_won.items()},
            "segment_spending": {segment.value: amount for segment, amount in self.segment_spending.items()}
        }
    

    @classmethod
    def from_dict(cls, data: dict) -> 'TwoDaysBidBundle':
        """Create from dictionary."""
        # Convert bid_entries back to SimpleBidEntry objects
        bid_entries = []
        for entry_data in data['bid_entries']:
            bid_entries.append(SimpleBidEntry.from_dict(entry_data))
        
        # Convert impressions_won and segment_spending back to MarketSegment keys
        impressions_won = {}
        for segment_str, count in data['impressions_won'].items():
            impressions_won[MarketSegment(segment_str)] = count
            
        segment_spending = {}
        for segment_str, amount in data['segment_spending'].items():
            segment_spending[MarketSegment(segment_str)] = amount
        
        return cls(
            day=data['day'],
            campaign_id=data['campaign_id'],
            day_limit=data['day_limit'],
            bid_entries=bid_entries,
            total_spent=data['total_spent'],
            impressions_won=impressions_won,
            segment_spending=segment_spending
        )
    
    


class AdxTwoDayStage(BaseStage):
    """
    Two-day TAC-AdX simulation stage.
    
    This stage handles both days of the ADX game:
    - Day 1: Initial bidding with base budget
    - Day 2: Bidding with QC-adjusted budget based on Day 1 performance
    
    Parameters
    ----------
    num_players : int
        Number of players in the game
    rival_sampler : callable, optional
        Function: seg_id → rival CPM bid distribution sampler
    n_auctions : int
        Number of impression auctions per day (default: 10,000)
    """

    # User arrival frequencies for each market segment
    USER_FREQUENCIES = {
        MarketSegment.MALE_YOUNG_LOW_INCOME: 1836,
        MarketSegment.MALE_YOUNG_HIGH_INCOME: 517,
        MarketSegment.MALE_OLD_LOW_INCOME: 1795,
        MarketSegment.MALE_OLD_HIGH_INCOME: 808,
        MarketSegment.FEMALE_YOUNG_LOW_INCOME: 1980,
        MarketSegment.FEMALE_YOUNG_HIGH_INCOME: 256,
        MarketSegment.FEMALE_OLD_LOW_INCOME: 2401,
        MarketSegment.FEMALE_OLD_HIGH_INCOME: 407,
    }
    TOTAL_USERS = 10000
    REACH_FACTORS = [0.3, 0.5, 0.7]

    def __init__(
        self,
        num_players: int,
        rival_sampler=None,
        n_auctions: int = 10_000,
    ):
        super().__init__(num_players)
        self.rival_sampler = rival_sampler or self._default_rival_sampler
        self.n_auctions = n_auctions
        
        # Game state
        self.current_day = 1
        self.qc_multiplier = 1.0
        self.campaigns_day1: Dict[int, Campaign] = {}
        self.campaigns_day2: Dict[int, Campaign] = {}
        self.bid_bundles: Dict[int, TwoDaysBidBundle] = {}
        self.user_arrivals: List[MarketSegment] = []
        
        # Generate campaigns and user arrivals
        self._generate_campaigns()
        self._generate_user_arrivals()

    def legal_actions(self, player_id: PlayerId) -> str:
        """Return description of legal actions."""
        return "TwoDaysBidBundle with day, campaign_id, day_limit, and bid_entries"

    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Execute one day of the ADX game."""
        print(f"[ADX_TWO_DAY] Day {self.current_day} step called with {len(actions)} actions")
        
        # Validate actions
        self._validate_actions(actions, list(range(self.n)))
        
        # Store bid bundles
        self.bid_bundles = actions
        
        # Run auction simulation for current day
        self._run_auctions()
        
        # Calculate rewards and info
        rewards, info = self._calculate_results()
        
        # Check if we need to transition to day 2
        if self.current_day == 1:
            # Calculate QC multiplier for day 2
            self.qc_multiplier = self._calculate_qc_multiplier(info)
            print(f"[ADX_TWO_DAY] Day 1 complete, QC multiplier: {self.qc_multiplier}")
            
            # Prepare day 2 observations
            obs = self._prepare_day2_observations()
            self.current_day = 2
            done = False
        else:
            # Day 2 complete, game finished
            obs = {pid: {'none':'none'} for pid in range(self.n)}
            done = True
            self._done = True
            print(f"[ADX_TWO_DAY] Day 2 complete, game finished")
        
        return obs, rewards, done, info

    def _generate_campaigns(self):
        """Generate campaigns for both days."""
        self.campaigns_day1.clear()
        self.campaigns_day2.clear()
        
        for player_id in range(self.n):
            # Generate day 1 campaign
            self.campaigns_day1[player_id] = self._generate_campaign(player_id, day=1)
            # Generate day 2 campaign  
            self.campaigns_day2[player_id] = self._generate_campaign(player_id, day=2)

    def _generate_campaign(self, player_id: int, day: int) -> Campaign:
        """Generate a campaign for a specific player and day."""
        # Pick a random segment with at least two attributes
        eligible_segments = [s for s in MarketSegment if len(s.value.split('_')) >= 2]
        segment = random.choice(eligible_segments)
        avg_users = self.USER_FREQUENCIES.get(segment, 1000)
        reach = int(avg_users * random.choice(self.REACH_FACTORS))
        
        budget = float(reach) if day == 1 else float(reach) * self.qc_multiplier
        return Campaign(id=player_id * 10 + day, market_segment=segment, reach=reach, budget=budget)

    def _generate_user_arrivals(self):
        """Generate user arrival sequence for the day."""
        self.user_arrivals = []
        for segment, count in self.USER_FREQUENCIES.items():
            self.user_arrivals.extend([segment] * count)
        random.shuffle(self.user_arrivals)

    def _run_auctions(self):
        """Run the auction simulation for the current day."""
        print(f"[ADX_TWO_DAY] Running {self.n_auctions} auctions for day {self.current_day}")
        
        # Regenerate user arrivals for each day
        self._generate_user_arrivals()
        
        # Run auctions
        for auction_num, user_segment in enumerate(self.user_arrivals[:self.n_auctions]):
            self._run_single_auction(user_segment, auction_num)







    def _run_single_auction(self, user_segment: MarketSegment, auction_num: int):
        """Run a single auction for a user segment."""
        # Get rival price
        rival_price = self.rival_sampler(user_segment)
        
        # Find best bid from agents
        best_agent_id, best_bid = None, -1.0
        for agent_id, bundle in self.bid_bundles.items():
            for entry in bundle.bid_entries:
                if MarketSegment.is_subset(entry.market_segment, user_segment):
                    # Check spending limits
                    segment_spent = bundle.segment_spending.get(entry.market_segment, 0.0)
                    if (segment_spent < entry.spending_limit and 
                        bundle.total_spent < bundle.day_limit):
                        if entry.bid > best_bid:
                            best_agent_id, best_bid = agent_id, entry.bid
        
        # Award impression if we have a winner
        if best_agent_id is not None and best_bid > rival_price:
            bundle = self.bid_bundles[best_agent_id]
            price_paid = rival_price / 1000.0  # CPM to per-impression
            
            # Update bundle stats
            bundle.total_spent += price_paid
            bundle.impressions_won[user_segment] += 1
            bundle.segment_spending[user_segment] += price_paid

    def _calculate_results(self) -> Tuple[RewardDict, InfoDict]:
        """Calculate rewards and info for all players."""
        rewards = {}
        info = {}
        
        for agent_id in range(self.n):
            bundle = self.bid_bundles[agent_id]
            campaign = self.campaigns_day1[agent_id] if self.current_day == 1 else self.campaigns_day2[agent_id]
            
            # Calculate total impressions that match campaign target
            total_impressions = 0
            for entry in bundle.bid_entries:
                if MarketSegment.is_subset(campaign.market_segment, entry.market_segment):
                    total_impressions += bundle.impressions_won.get(entry.market_segment, 0)
            
            # Calculate reach fulfillment and profit
            reach_fulfilled = min(total_impressions, campaign.reach)
            profit = (reach_fulfilled / campaign.reach) * campaign.budget - bundle.total_spent
            
            rewards[agent_id] = profit
            info[agent_id] = {
                "impressions": total_impressions,
                "reach_fulfilled": reach_fulfilled,
                "total_spent": bundle.total_spent,
                "campaign_id": campaign.id
            }
            
            # Add QC score for day 1
            if self.current_day == 1:
                qc_score = self._calculate_quality_score(reach_fulfilled, campaign.reach)
                info[agent_id]["qc"] = qc_score
        
        return rewards, info

    def _calculate_quality_score(self, reach_achieved: int, reach_goal: int) -> float:
        """Calculate quality score using the TAC formula."""
        if reach_goal == 0:
            return 0.0
            
        a = 4.08577
        b = 3.08577
        x = reach_achieved
        R = reach_goal
        
        x_over_R = x / R
        quality_score = (2 / a) * (math.atan(a * (x_over_R - b)) - math.atan(-b)) + 1
        
        return max(0.0, quality_score)

    def _calculate_qc_multiplier(self, info: InfoDict) -> float:
        """Calculate QC multiplier for day 2 based on day 1 performance."""
        # Use the QC score from the first player (they should all be similar)
        if info and 0 in info and "qc" in info[0]:
            return info[0]["qc"]
        return 1.0

    def _prepare_day2_observations(self) -> ObsDict:
        """Prepare observations for day 2."""
        obs = {}
        for i in range(self.n):
            obs[i] = {
                "day": 2,
                "qc": self.qc_multiplier,
                "campaign_day1": self._campaign_to_dict(self.campaigns_day1[i]),
                "campaign_day2": self._campaign_to_dict(self.campaigns_day2[i])
            }
        return obs

    def _campaign_to_dict(self, campaign: Campaign) -> Dict:
        """Convert Campaign to dictionary for JSON serialization."""
        return {
            "id": campaign.id,
            "market_segment": campaign.market_segment.value,
            "reach": campaign.reach,
            "budget": campaign.budget
        }

    def _default_rival_sampler(self, segment: MarketSegment) -> float:
        """Default rival price sampler."""
        # Simple uniform distribution for now
        return random.uniform(0.0, 10.0)

    def get_campaigns_day1(self) -> Dict[int, Campaign]:
        """Get day 1 campaigns."""
        return self.campaigns_day1

    def get_campaigns_day2(self) -> Dict[int, Campaign]:
        """Get day 2 campaigns."""
        return self.campaigns_day2
