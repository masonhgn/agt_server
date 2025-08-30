import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class AggressiveBiddingAgent:
    """
    Aggressive bidding agent for Lab 8: Higher bids to win more auctions.
    
    This agent implements a more aggressive bidding strategy:
    - Bids higher amounts ($2.0) to increase chances of winning auctions
    - Allocates budget more strategically across segments
    - Uses 80% of budget as day limit to leave room for unexpected costs
    """
    def __init__(self):
        self.name = "aggressive_bidding_agent"
        self.campaign = None  # Will be set by the game environment
    
    def reset(self):
        """Reset the agent for a new game."""
        pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass

    def get_bid_bundle(self) -> OneDayBidBundle:
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


if __name__ == "__main__":
    # Test the aggressive bidding agent locally
    print("Testing AggressiveBiddingAgent locally...")
    print("=" * 50)
    
    # Import opponent agents and AdX arena for testing
    from basic_bidding_agent import BasicBiddingAgent
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from adx_local_arena import AdXLocalArena
    import random
    
    # Create additional random agents for a full tournament
    class RandomAdXAgent:
        def __init__(self, name):
            self.name = name
            self.campaign = None
        
        def reset(self):
            """Reset the agent for a new game."""
            pass
        
        def setup(self):
            """Initialize the agent for a new game."""
            pass
        
        def get_bid_bundle(self) -> OneDayBidBundle:
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
    
    # Create all agents for testing
    agent = AggressiveBiddingAgent()
    opponent1 = BasicBiddingAgent()
    random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]
    
    # Create arena and run tournament
    agents = [agent, opponent1] + random_agents
    arena = AdXLocalArena(agents, num_agents_per_game=10, num_games=10, verbose=True)
    arena.run_tournament()
    
    print("\nLocal test completed!")

# Export for server testing
agent_submission = AggressiveBiddingAgent()
