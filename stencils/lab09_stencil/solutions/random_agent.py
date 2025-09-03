import sys, os
import random
import math
# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent

class RandomAdXAgent(BaseAgent):
    """
    Random agent for Lab 9: Makes random bids within reasonable bounds.
    Demonstrates basic two-day strategy with random bidding.
    """
    
    def __init__(self, name: str = "RandomAdXAgent"):
        super().__init__(name)
        self.campaign_day1 = None
        self.campaign_day2 = None
        self.quality_score = 1.0

    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """Get the agent's action based on the current observation."""
        # Extract day from observation - check both direct and nested locations
        day = 1
        if observation:
            # Check if day is directly in observation
            if "day" in observation:
                day = observation["day"]
            # Check if day is nested under campaign
            elif "campaign" in observation and "day" in observation["campaign"]:
                day = observation["campaign"]["day"]
        
        # Set campaigns from observation if available
        if observation:
            # Check if campaigns are directly in observation
            if "campaign_day1" in observation:
                campaign_dict = observation["campaign_day1"]
                self.campaign_day1 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
            elif "campaign" in observation and "campaign_day1" in observation["campaign"]:
                campaign_dict = observation["campaign"]["campaign_day1"]
                self.campaign_day1 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                
            if "campaign_day2" in observation:
                campaign_dict = observation["campaign_day2"]
                self.campaign_day2 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
            elif "campaign" in observation and "campaign_day2" in observation["campaign"]:
                campaign_dict = observation["campaign"]["campaign_day2"]
                self.campaign_day2 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                
            # Check for quality score in both locations
            if "qc" in observation:
                self.quality_score = observation["qc"]
            elif "campaign" in observation and "qc" in observation["campaign"]:
                self.quality_score = observation["campaign"]["qc"]
        
        return self.get_bid_bundle(day)

    def get_bid_bundle(self, day: int) -> TwoDaysBidBundle:
        """Random bidding strategy for two-day game."""
        if day == 1:
            campaign = self.campaign_day1
            # Random bid between 0.5 and 2.0 for day 1
            base_bid = random.uniform(0.5, 2.0)
            budget_usage = random.uniform(0.6, 0.9)
        elif day == 2:
            campaign = self.campaign_day2
            # Adjust strategy based on quality score
            if self.quality_score > 0.7:
                base_bid = random.uniform(1.0, 2.5)  # More aggressive
                budget_usage = random.uniform(0.7, 1.0)
            else:
                base_bid = random.uniform(0.3, 1.0)  # More conservative
                budget_usage = random.uniform(0.4, 0.7)
        else:
            raise ValueError("Day must be 1 or 2")
            
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                # Add some randomness to individual segment bids
                segment_bid = base_bid * random.uniform(0.8, 1.2)
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=segment_bid,
                    spending_limit=campaign.budget * budget_usage
                ))
        
        return TwoDaysBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )
    
    def get_first_campaign(self) -> Campaign:
        return self.campaign_day1
    
    def get_second_campaign(self) -> Campaign:
        return self.campaign_day2


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "RandomAdXAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "adx_twoday"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = RandomAdXAgent()
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test the random agent locally
        print("Testing RandomAdXAgent locally...")
        print("=" * 50)
        
        try:
            from core.engine import Engine
            from core.game.AdxTwoDayGame import AdxTwoDayGame
            from example_solution import ExampleTwoDaysTwoCampaignsAgent
            from aggressive_agent import AggressiveAdXAgent
            from conservative_agent import ConservativeAdXAgent
            
            print("=== Random Agent Testing Arena ===\n")
            
            # Create the random agent
            random_agent = RandomAdXAgent()
            print(f"Random agent: {random_agent.name}")
            
            # Create opponents
            example_agent = ExampleTwoDaysTwoCampaignsAgent()
            aggressive_agent = AggressiveAdXAgent()
            conservative_agent = ConservativeAdXAgent()
            
            print(f"Opponents: {example_agent.name}, {aggressive_agent.name}, {conservative_agent.name}\n")
            
            # Test against each opponent
            opponents = [example_agent, aggressive_agent, conservative_agent]
            
            for opponent in opponents:
                print(f"Testing against {opponent.name}...")
                
                # Create game with 2 players
                game = AdxTwoDayGame(num_players=2)
                
                # Create engine and run game
                engine = Engine(game, [random_agent, opponent], rounds=1)
                results = engine.run()
                
                print(f"  Random score: {results[0]:.2f}")
                print(f"  {opponent.name} score: {results[1]:.2f}")
                print(f"  Winner: {'Random' if results[0] > results[1] else opponent.name}")
                print()
            
            print("=== Testing Complete ===")
            
        except ImportError as e:
            print(f"Import error: {e}")
            print("Make sure you're running this from the solutions directory")
        except Exception as e:
            print(f"Error during testing: {e}")
            import traceback
            traceback.print_exc()

# Export for server testing
agent_submission = RandomAdXAgent()
