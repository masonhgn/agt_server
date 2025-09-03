import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class BasicBiddingAgent:
    """
    Basic bidding agent for Lab 8: Simple but effective strategy.
    
    This agent implements a straightforward bidding strategy:
    - Bids $1.0 on all market segments that match the campaign
    - Uses the campaign's budget as both day limit and spending limits
    - Focuses on reaching the target audience without overbidding
    """
    def __init__(self):
        self.name = "basic_bidding_agent"
        self.campaign = None  # Will be set by the game environment
    
    def reset(self):
        """Reset the agent for a new game."""
        pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass

    def get_bid_bundle(self) -> OneDayBidBundle:
        """
        Basic bidding strategy: bid $1.0 on all matching segments.
        
        This strategy:
        1. Identifies all market segments that match the campaign target
        2. Bids a moderate amount ($1.0) on each matching segment
        3. Uses the full budget as spending limits to ensure maximum reach
        """
        bid_entries = []
        
        # Iterate through all market segments
        for segment in MarketSegment.all_segments():
            # Check if this segment matches the campaign target
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                # Create a bid entry for this segment
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=1.0,  # Moderate bid amount
                    spending_limit=self.campaign.budget  # Use full budget as limit
                ))
        
        # Create and return the bid bundle
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,  # Total spending limit for the day
            bid_entries=bid_entries
        )


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "BasicBiddingAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "adx_oneday"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = BasicBiddingAgent()
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test the basic bidding agent locally
        print("Testing BasicBiddingAgent locally...")
        print("=" * 50)
        
        # Import opponent agents and AdX arena for testing
        from aggressive_bidding_agent import AggressiveBiddingAgent
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
        agent = BasicBiddingAgent()
        opponent1 = AggressiveBiddingAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]
        
        # Create arena and run tournament
        agents = [agent, opponent1] + random_agents
        arena = AdXLocalArena(agents, num_agents_per_game=10, num_games=10, verbose=True)
        arena.run_tournament()
        
        print("\nLocal test completed!")

# Export for server testing
agent_submission = BasicBiddingAgent()
