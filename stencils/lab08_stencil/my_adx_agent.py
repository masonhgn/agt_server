import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class MyOneDayAgent:
    """
    Your implementation of the AdX One Day agent.
    
    This class should implement the get_bid_bundle() method to return your OneDayBidBundle.
    The writeup describes this as MyOneDayAgent.java that extends OneDayAgent.
    
    Your agent will be assigned a campaign at the beginning of the game.
    You can access it via self.campaign which contains:
    - id: campaign ID
    - market_segment: target demographic (e.g., Female_Old)
    - reach: number of impressions needed
    - budget: total budget available
    """
    def __init__(self):
        self.name = "TODO: Enter your name or ID here"
        self.campaign = None  # Will be set by the game environment

    def get_bid_bundle(self) -> OneDayBidBundle:
        """
        Return a OneDayBidBundle for your assigned campaign.
        
        This method should:
        1. Create SimpleBidEntry objects for relevant market segments
        2. Set appropriate bids and spending limits
        3. Return a OneDayBidBundle with your campaign ID, day limit, and bid entries
        
        Example (from writeup):
        - Create SimpleBidEntry for campaign's market segment
        - Add bid entries to a list
        - Create OneDayBidBundle with campaign ID, budget as day limit, and bid entries
        
        Helper functions (equivalent to Java writeup):
        - MarketSegment.all_segments() - iterate over all market segments
        - MarketSegment.is_subset(campaign_segment, user_segment) - check if user segment matches campaign
        """
        raise NotImplementedError("Implement your bidding strategy here.")

# For compatibility with existing code
MyAdXAgent = MyOneDayAgent


if __name__ == "__main__":
    # Test your agent locally
    print("Testing MyOneDayAgent locally...")
    print("=" * 50)
    
    # Import opponent agents and AdX arena for testing
    from solutions.basic_bidding_agent import BasicBiddingAgent
    from solutions.aggressive_bidding_agent import AggressiveBiddingAgent
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
    agent = MyOneDayAgent()
    opponent1 = BasicBiddingAgent()
    opponent2 = AggressiveBiddingAgent()
    random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(7)]
    
    # Create arena and run tournament
    agents = [agent, opponent1, opponent2] + random_agents
    arena = AdXLocalArena(agents, num_agents_per_game=10, num_games=10, verbose=True)
    arena.run_tournament()
    
    print("\nLocal test completed!")

# Export for server testing
agent_submission = MyOneDayAgent("MyOneDayAgent") 