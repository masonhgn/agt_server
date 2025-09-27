# games/adx_one_day.py
from typing import Dict, List, Optional, Tuple, Any
import random
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.game.bid_entry import SimpleBidEntry
from dataclasses import dataclass, field
from core.game.base_game import BaseGame
from core.game import ObsDict, ActionDict, RewardDict, InfoDict

# --- OneDayBidBundle ---
@dataclass
class OneDayBidBundle:
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

# --- AdxOneDayGame ---
class AdxOneDayGame(BaseGame):
    """
    TAC AdX Game (One-Day Variant).
    Each agent is assigned a campaign and submits a OneDayBidBundle before the day starts.
    The game simulates user arrivals and second-price auctions for each impression.
    """
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

    def __init__(self, num_agents: int = 10):
        super().__init__()
        self.num_agents = num_agents
        self.campaigns: Dict[int, Campaign] = {}
        self.bid_bundles: Dict[int, OneDayBidBundle] = {}
        self.user_arrivals: List[MarketSegment] = []
        self.agent_campaigns: Dict[int, Campaign] = {}
        self._generate_user_arrivals()
        self.metadata = {"num_players": num_agents}

    def reset(self, seed: Optional[int] = None) -> Dict[int, Dict]:
        if seed is not None:
            random.seed(seed)
        self.campaigns.clear()
        self.bid_bundles.clear()
        self.agent_campaigns.clear()
        for agent_id in range(self.num_agents):
            campaign = self._generate_campaign(agent_id)
            self.campaigns[campaign.id] = campaign
            self.agent_campaigns[agent_id] = campaign
        self._generate_user_arrivals()
        obs = {}
        for agent_id in range(self.num_agents):
            campaign = self.agent_campaigns[agent_id]
            obs[agent_id] = {
                "campaign": campaign,
                "day": 1,
                "total_users": self.TOTAL_USERS
            }
        return obs

    def step(self, actions: Dict[int, OneDayBidBundle]) -> Tuple[Dict, Dict, bool, Dict]:
        self._validate_actions(actions)
        self.bid_bundles = actions
        self._run_auctions()
        rewards = {}
        info = {}
        for agent_id in range(self.num_agents):
            campaign = self.agent_campaigns[agent_id]
            bundle = self.bid_bundles[agent_id]
            total_impressions = 0
            for entry in bundle.bid_entries:
                if MarketSegment.is_subset(campaign.market_segment, entry.market_segment):
                    total_impressions += bundle.impressions_won.get(entry.market_segment, 0)
            reach_fulfilled = min(total_impressions, campaign.reach)
            profit = (reach_fulfilled / campaign.reach) * campaign.budget - bundle.total_spent
            rewards[agent_id] = profit
            info[agent_id] = {
                "impressions": total_impressions,
                "reach_fulfilled": reach_fulfilled,
                "total_spent": bundle.total_spent
            }
        done = True
        obs = {}
        return obs, rewards, done, info

    def players_to_move(self) -> List[int]:
        """Return the subset of players whose actions are required now."""
        return list(range(self.num_agents))

    def num_players(self) -> int:
        """Get number of players in the game."""
        return self.num_agents

    def get_game_state(self) -> Dict[str, Any]:
        """Get the current game state."""
        return {
            "num_agents": self.num_agents,
            "campaigns": self.campaigns,
            "bid_bundles": self.bid_bundles,
            "agent_campaigns": self.agent_campaigns
        }

    def _generate_campaign(self, agent_id: int) -> Campaign:
        # Pick a random segment with at least two attributes
        eligible_segments = [s for s in MarketSegment if len(s.value.split('_')) >= 2]
        segment = random.choice(eligible_segments)
        avg_users = self.USER_FREQUENCIES.get(segment, 1000)
        reach = int(avg_users * random.choice(self.REACH_FACTORS))
        budget = float(reach)  # $1 per impression
        return Campaign(id=agent_id, market_segment=segment, reach=reach, budget=budget)

    def _generate_user_arrivals(self):
        self.user_arrivals = []
        for segment, count in self.USER_FREQUENCIES.items():
            self.user_arrivals.extend([segment] * count)
        random.shuffle(self.user_arrivals)

    def _validate_actions(self, actions: Dict[int, OneDayBidBundle]):
        if set(actions.keys()) != set(range(self.num_agents)):
            raise ValueError("Actions must be provided for all agents.")
        for agent_id, bundle in actions.items():
            if bundle.campaign_id != self.agent_campaigns[agent_id].id:
                raise ValueError(f"Agent {agent_id} campaign_id mismatch.")

    def _run_auctions(self):
        # For each user, run a second-price auction
        for user_segment in self.user_arrivals:
            bids = []
            for agent_id, bundle in self.bid_bundles.items():
                for entry in bundle.bid_entries:
                    if MarketSegment.is_subset(entry.market_segment, user_segment):
                        # Check spending limits - use actual spending, not bid amount
                        # We need to track actual prices paid per segment
                        segment_spent = getattr(bundle, 'segment_spending', {}).get(entry.market_segment, 0.0)
                        if segment_spent < entry.spending_limit and bundle.total_spent < bundle.day_limit:
                            bids.append((agent_id, entry.bid, entry.market_segment))
            if not bids:
                continue
            # Find highest and second-highest bid
            bids.sort(key=lambda x: x[1], reverse=True)
            winner_id, win_bid, win_segment = bids[0]
            price = bids[1][1] if len(bids) > 1 else 0.0
            # Update winner's stats
            bundle = self.bid_bundles[winner_id]
            bundle.impressions_won[win_segment] += 1
            bundle.total_spent += price
            
            # Track spending per segment for proper limit enforcement
            if not hasattr(bundle, 'segment_spending'):
                bundle.segment_spending = {}
            bundle.segment_spending[win_segment] = bundle.segment_spending.get(win_segment, 0.0) + price
