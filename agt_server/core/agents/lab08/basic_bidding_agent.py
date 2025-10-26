import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle, AdxOneDayGame
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from typing import Dict, Any
from server.connect_stencil import connect_agent_to_server
from core.agents.lab08.random_agent import RandomAdXAgent
from core.agents.lab08.aggressive_bidding_agent import AggressiveBiddingAgent
from core.local_arena import LocalArena
from core.agents.common.base_agent import BaseAgent
class BasicBiddingAgent(BaseAgent):
    """
    Basic bidding agent for Lab 8: Simple but effective strategy.
    
    This agent implements a straightforward bidding strategy:
    - Bids $1.0 on all market segments that match the campaign
    - Uses the campaign's budget as both day limit and spending limits
    - Focuses on reaching the target audience without overbidding
    """
    def __init__(self, name: str = "BasicBiddingAgent"):
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

        async def main():
            # Create agent and adapter
            agent = BasicBiddingAgent()
            
            # Connect to server
            await connect_agent_to_server(agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test the basic bidding agent locally
        print("Testing BasicBiddingAgent locally...")
        print("=" * 50)
        

        
        
        # Create all agents for testing
        agent = BasicBiddingAgent(name="BasicBiddingAgent")
        opponent1 = AggressiveBiddingAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]
        
        # Create arena and run tournament
        agents = [agent, opponent1] + random_agents
        arena = LocalArena(
            game_title="adx_oneday",
            game_class=AdxOneDayGame,
            agents=agents,
            num_agents_per_game=10,
            num_rounds=10,
            timeout=30.0,
            save_results=False,
            verbose=True
        )
        arena.run_tournament()
        
        print("\nLocal test completed!")

# Export for server testing
agent_submission = BasicBiddingAgent()
