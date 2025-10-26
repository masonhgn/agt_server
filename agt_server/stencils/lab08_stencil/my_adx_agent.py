import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

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

class MyAdXAgent(BaseAgent):
    """
    Your implementation of the AdX One Day agent.
    
    This agent should implement a bidding strategy for the AdX One Day game.
    You will be assigned a campaign with:
    - id: campaign ID
    - market_segment: target demographic (e.g., Female_Old, Male_Young_HighIncome)
    - reach: number of impressions needed to fulfill the campaign
    - budget: total budget available for bidding
    
    Your goal is to bid on market segments to win impressions that match your campaign,
    while staying within your budget and maximizing profit.
    
    Key concepts:
    - Market segments can be 1, 2, or 3 attributes (e.g., Female, Female_Old, Female_Old_HighIncome)
    - You can bid on any segment that matches your campaign (use MarketSegment.is_subset)
    - Second-price sealed-bid auctions determine winners
    - You only get credit for impressions that match your campaign's target segment
    - Profit = (reach_fulfilled / total_reach) * budget - total_spending
    """
    
    def __init__(self, name: str = "MyAdXAgent"):
        super().__init__(name)
        self.game_title = "adx_oneday"
        # TODO: Add any instance variables you need for your strategy

    def reset(self):
        """Reset the agent for a new game."""
        # TODO: Reset any game-specific state variables
        pass
    
    def setup(self):
        """Initialize the agent for a new game."""
        # TODO: Initialize any strategy-specific variables
        pass

    def get_action(self, observation: Dict[str, Any]) -> OneDayBidBundle:
        """
        Return a OneDayBidBundle for your assigned campaign.
        
        This is the main method you need to implement. It should:
        1. Extract your campaign from the observation
        2. Create SimpleBidEntry objects for relevant market segments
        3. Set appropriate bids and spending limits
        4. Return a OneDayBidBundle
        
        Args:
            observation: Dictionary containing your campaign information
            
        Returns:
            OneDayBidBundle: Your bidding strategy for this game
        """
        # Convert campaign dictionary to Campaign object if needed
        campaign_data = observation['campaign']
        self.campaign = Campaign.from_dict(campaign_data) if isinstance(campaign_data, dict) else campaign_data
        
        # TODO: Implement your bidding strategy here
        # 
        # Example strategy (you should replace this with your own):
        # 1. Find all market segments that match your campaign
        # 2. Create bid entries for those segments
        # 3. Set bids and spending limits based on your strategy
        # 4. Return the bid bundle
        
        bid_entries = []
        
        # Example: Bid on all segments that match your campaign
        for segment in MarketSegment.all_segments():
            # Check if this segment matches your campaign target
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                # TODO: Implement your bidding logic here
                # Example: Simple strategy - bid $1.0 on each matching segment
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=1.0,  # TODO: Calculate your bid amount
                    spending_limit=self.campaign.budget  # TODO: Set appropriate spending limit
                ))
        
        # Create and return the bid bundle
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,  # TODO: Set your total day spending limit
            bid_entries=bid_entries
        )


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "MyAdXAgent"  # TODO: Give your agent a unique name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "adx_oneday"  # Game type (hardcoded for this agent)
    
    if server:
        async def main():
            # Create agent and connect to server
            agent = MyAdXAgent()
            
            # Connect to server
            await connect_agent_to_server(agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test your agent locally
        print("Testing MyAdXAgent locally...")
        print("=" * 50)
        
        # Create all agents for testing
        agent = MyAdXAgent(name="MyAdXAgent")
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
agent_submission = MyAdXAgent()