
from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
import random
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class RandomAdXAgent(BaseAgent):
    def __init__(self, name: str = "RandomAgent"):
        super().__init__(name)
        self.game_title = "adx_oneday"
    
    def reset(self):
        """Reset the agent for a new game."""
        pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass
    
    def get_action(self, observation: Dict[str, Any]) -> OneDayBidBundle:
        self.campaign = observation['campaign']
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=random.uniform(0.5, 2.0),  # Random bid between 0.5 and 2.0
                    spending_limit=self.campaign.budget * random.uniform(0.5, 1.0)
                ))
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget * random.uniform(0.5, 1.0),
            bid_entries=bid_entries
        )