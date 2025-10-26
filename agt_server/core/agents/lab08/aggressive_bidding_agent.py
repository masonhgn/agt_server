import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.campaign import Campaign
from core.game.market_segment import MarketSegment
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent
class AggressiveBiddingAgent(BaseAgent):
    """
    Aggressive bidding agent for Lab 8: Higher bids to win more auctions.
    
    This agent implements a more aggressive bidding strategy:
    - Bids higher amounts ($2.0) to increase chances of winning auctions
    - Allocates budget more strategically across segments
    - Uses 80% of budget as day limit to leave room for unexpected costs
    """
    def __init__(self, name: str = "AggressiveBiddingAgent"):
        super().__init__(name)
        self.game_title = "adx_oneday"

    
    def reset(self):
        """Reset the agent for a new game."""
        pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass

    def get_action(self, observation: Dict[str, Any]) -> OneDayBidBundle:
        # Convert campaign dictionary to Campaign object if needed
        campaign_data = observation['campaign']
        self.campaign = Campaign.from_dict(campaign_data) if isinstance(campaign_data, dict) else campaign_data
        """
        Aggressive bidding strategy: bid $2.0 on matching segments with budget allocation.
        
        This strategy:
        1. Bids higher amounts to increase auction win probability
        2. Allocates budget strategically across segments
        3. Uses 80% of budget as day limit for safety margin
        """
        bid_entries = []
        
        # Calculate budget allocation
        day_limit = self.campaign.budget * 0.8  # Use 80% of budget as day limit
        
        # Count how many matching segments we have
        matching_segments = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                matching_segments.append(segment)
        
        # Allocate budget evenly across matching segments
        segment_budget = day_limit / len(matching_segments) if matching_segments else 0
        
        # Create bid entries for each matching segment
        for segment in matching_segments:
            bid_entries.append(SimpleBidEntry(
                market_segment=segment,
                bid=2.0,  # Higher bid to win more auctions
                spending_limit=segment_budget  # Allocate budget evenly
            ))
        
        # Create and return the bid bundle
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=day_limit,  # Use 80% of budget as day limit
            bid_entries=bid_entries
        )


