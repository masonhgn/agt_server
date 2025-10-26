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
    campaign_id: int # campaign id of the agent
    day_limit: float # total budget for the day
    bid_entries: List[SimpleBidEntry] # list of bid entries for the day
    # Internal tracking for simulation
    total_spent: float = 0.0
    impressions_won: Dict[MarketSegment, int] = field(default_factory=dict)
    segment_spending: Dict[MarketSegment, float] = field(default_factory=dict)

    def __post_init__(self):
        for entry in self.bid_entries:
            self.impressions_won[entry.market_segment] = 0
            self.segment_spending[entry.market_segment] = 0.0
    
    def to_dict(self) -> dict:
        """Convert OneDayBidBundle to dictionary for JSON serialization."""
        return {
            "campaign_id": self.campaign_id,
            "day_limit": self.day_limit,
            "bid_entries": [entry.to_dict() for entry in self.bid_entries],
            "total_spent": self.total_spent,
            "impressions_won": {segment.value: count for segment, count in self.impressions_won.items()},
            "segment_spending": {segment.value: amount for segment, amount in self.segment_spending.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'OneDayBidBundle':
        """Create OneDayBidBundle from dictionary."""
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
            campaign_id=data['campaign_id'],
            day_limit=data['day_limit'],
            bid_entries=bid_entries,
            total_spent=data['total_spent'],
            impressions_won=impressions_won,
            segment_spending=segment_spending
        )

# --- AdxOneDayGame ---
class AdxOneDayGame(BaseGame):
    """
    TAC AdX Game (One-Day Variant)
    Each agent is assigned a campaign and submits a OneDayBidBundle before the day starts.
    The game simulates user arrivals and second-price auctions for each impression.
    """
    USER_FREQUENCIES = {
        # 3-attribute segments (most specific)
        MarketSegment.MALE_YOUNG_LOW_INCOME: 1836,
        MarketSegment.MALE_YOUNG_HIGH_INCOME: 517,
        MarketSegment.MALE_OLD_LOW_INCOME: 1795,
        MarketSegment.MALE_OLD_HIGH_INCOME: 808,
        MarketSegment.FEMALE_YOUNG_LOW_INCOME: 1980,
        MarketSegment.FEMALE_YOUNG_HIGH_INCOME: 256,
        MarketSegment.FEMALE_OLD_LOW_INCOME: 2401,
        MarketSegment.FEMALE_OLD_HIGH_INCOME: 407,
        # 2-attribute segments
        MarketSegment.MALE_YOUNG: 200,
        MarketSegment.MALE_OLD: 150,
        MarketSegment.MALE_LOW_INCOME: 180,
        MarketSegment.MALE_HIGH_INCOME: 120,
        MarketSegment.FEMALE_YOUNG: 220,
        MarketSegment.FEMALE_OLD: 170,
        MarketSegment.FEMALE_LOW_INCOME: 200,
        MarketSegment.FEMALE_HIGH_INCOME: 130,
        MarketSegment.YOUNG_LOW_INCOME: 190,
        MarketSegment.YOUNG_HIGH_INCOME: 110,
        MarketSegment.OLD_LOW_INCOME: 160,
        MarketSegment.OLD_HIGH_INCOME: 100,
        # 1-attribute segments (most general)
        MarketSegment.MALE: 100,
        MarketSegment.FEMALE: 120,
        MarketSegment.YOUNG: 80,
        MarketSegment.OLD: 70,
        MarketSegment.LOW_INCOME: 90,
        MarketSegment.HIGH_INCOME: 60,
    }
    TOTAL_USERS = 12450
    REACH_FACTORS = [0.3, 0.5, 0.7]

    def __init__(self, num_agents: int = 10):
        super().__init__()
        self.num_agents = num_agents
        self.campaigns: Dict[int, Campaign] = {}
        self.bid_bundles: Dict[int, OneDayBidBundle] = {}
        self.user_arrivals: List[MarketSegment] = [] #the actual user segments that will arrive that agents can bid on
        self.agent_campaigns: Dict[int, Campaign] = {} #the campaign of each agent, which will determine the market segment they want to bid on
        self._generate_user_arrivals()
        self.metadata = {"num_players": num_agents}

    def reset(self, seed: Optional[int] = None) -> Dict[int, Dict]:
        if seed is not None:
            random.seed(seed)
        self.campaigns.clear()
        self.bid_bundles.clear()
        self.agent_campaigns.clear()


        # generate the campaigns for each agent
        for agent_id in range(self.num_agents):
            campaign = self._generate_campaign(agent_id)
            self.campaigns[campaign.id] = campaign
            self.agent_campaigns[agent_id] = campaign

        #generate all user arrivals (market segments)
        self._generate_user_arrivals()
        obs = {}
        for agent_id in range(self.num_agents):
            campaign = self.agent_campaigns[agent_id]
            obs[agent_id] = {
                "campaign": campaign.to_dict(),
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
            try:
                # Get campaign with error handling
                if agent_id not in self.agent_campaigns:
                    print("=" * 80)
                    print("CRITICAL ERROR: MISSING CAMPAIGN DATA")
                    print(f"Agent {agent_id} not found in agent_campaigns!")
                    print(f"Available campaigns: {list(self.agent_campaigns.keys())}")
                    print(f"Expected agents: {list(range(self.num_agents))}")
                    print("=" * 80)
                    # Set default values to continue tournament
                    rewards[agent_id] = 0.0
                    info[agent_id] = {
                        "impressions": 0,
                        "reach_fulfilled": 0,
                        "total_spent": 0,
                        "error": "Missing campaign data"
                    }
                    continue
                
                campaign = self.agent_campaigns[agent_id] #get the campaign of this agent
                
                # Get bundle with error handling
                if agent_id not in self.bid_bundles:
                    print("=" * 80)
                    print("CRITICAL ERROR: MISSING BID BUNDLE DATA")
                    print(f"Agent {agent_id} not found in bid_bundles!")
                    print(f"Available bundles: {list(self.bid_bundles.keys())}")
                    print(f"Expected agents: {list(range(self.num_agents))}")
                    print("=" * 80)
                    # Set default values to continue tournament
                    rewards[agent_id] = 0.0
                    info[agent_id] = {
                        "impressions": 0,
                        "reach_fulfilled": 0,
                        "total_spent": 0,
                        "error": "Missing bid bundle data"
                    }
                    continue
                
                bundle = self.bid_bundles[agent_id] #get the bid bundle of this agent
                total_impressions = 0 #counter for total impressions won by this agent
                for entry in bundle.bid_entries: #traverse all bid entries of the bundle this agent submitted

                    #make sure that the bid entry matches the campaign otherwise they shouldn't profit from this bid
                    if MarketSegment.matches_campaign(entry.market_segment, campaign.market_segment):
                        total_impressions += bundle.impressions_won.get(entry.market_segment, 0)
                reach_fulfilled = min(total_impressions, campaign.reach) #if they won more impressions than their reach, then they only get paid for their reach
                
                # Handle division by zero for campaign.reach
                if campaign.reach == 0:
                    print("=" * 80)
                    print("CRITICAL WARNING: DIVISION BY ZERO PREVENTED")
                    print(f"Agent {agent_id} has campaign with reach=0!")
                    print(f"Campaign: {campaign}")
                    print("Setting profit to 0 to prevent crash")
                    print("=" * 80)
                    profit = 0.0
                else:
                    profit = (reach_fulfilled / campaign.reach) * campaign.budget - bundle.total_spent
                rewards[agent_id] = profit
                info[agent_id] = { #the infoset sent back to the agent
                    "impressions": total_impressions,
                    "reach_fulfilled": reach_fulfilled,
                    "total_spent": bundle.total_spent
                }
            except Exception as e:
                print("=" * 80)
                print("CRITICAL ERROR: UNEXPECTED EXCEPTION")
                print(f"Error processing agent {agent_id}: {e}")
                print(f"Exception type: {type(e).__name__}")
                print("=" * 80)
                # Set default values to continue tournament
                rewards[agent_id] = 0.0
                info[agent_id] = {
                    "impressions": 0,
                    "reach_fulfilled": 0,
                    "total_spent": 0,
                    "error": f"Exception: {str(e)}"
                }
        done = True
        obs = {} #this can be empty because this is only a one-day game and therefore we won't need to step() again
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
        total_auctions = 0
        successful_auctions = 0
        for user_segment in self.user_arrivals:
            total_auctions += 1
            bids = []

            #traverse all agents and their bid bundles to see if they can bid on this user segment
            '''
            for example, if the user segment is FEMALE, then the agent can bid on the FEMALE_YOUNG_LOW_INCOME, 
            FEMALE_YOUNG_HIGH_INCOME, FEMALE_OLD_LOW_INCOME, FEMALE_OLD_HIGH_INCOME segments

            '''
  
            for agent_id, bundle in self.bid_bundles.items():
                for entry in bundle.bid_entries:
                    if MarketSegment.can_serve(entry.market_segment, user_segment):
                        # Check spending limits - use actual spending, not bid amount
                        # We need to track actual prices paid per segment
                        segment_spent = getattr(bundle, 'segment_spending', {}).get(entry.market_segment, 0.0)
                        if segment_spent < entry.spending_limit and bundle.total_spent < bundle.day_limit:
                            bids.append((agent_id, entry.bid, entry.market_segment))
            if not bids:
                continue
            # Find highest and second-highest bid
            # Sort by bid amount (descending), then randomly for ties
            bids.sort(key=lambda x: (x[1], random.random()), reverse=True)
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
            successful_auctions += 1
        
