import sys, os
import math
# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent

class ConservativeAdXAgent(BaseAgent):
    """
    Conservative agent for Lab 9: Prioritizes day 1 profit over quality score.
    This strategy aims for immediate profit but may have limited day 2 opportunities.
    """
    
    def __init__(self, name: str = "ConservativeAdXAgent"):
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
        """Conservative bidding strategy prioritizing day 1 profit."""
        if day == 1:
            campaign = self.campaign_day1
            # Conservative day 1 strategy: low bids to maximize profit
            bid_amount = 0.5  # Low bid to minimize costs
            budget_usage = 0.6  # Use limited budget
        elif day == 2:
            campaign = self.campaign_day2
            # Day 2 strategy: adapt to quality score from day 1
            if self.quality_score > 0.8:
                # Surprisingly good quality score - can be more aggressive
                bid_amount = 1.5
                budget_usage = 0.8
            elif self.quality_score > 0.5:
                # Moderate quality score - moderate strategy
                bid_amount = 1.0
                budget_usage = 0.7
            else:
                # Low quality score - very conservative
                bid_amount = 0.3
                budget_usage = 0.4
        else:
            raise ValueError("Day must be 1 or 2")
            
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=bid_amount,
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


def main():
    """
    Local testing arena for Conservative AdX Agent.
    Run this file directly to test the conservative agent against other agents.
    """
    try:
        from core.engine import Engine
        from core.game.AdxTwoDayGame import AdxTwoDayGame
        from example_solution import ExampleTwoDaysTwoCampaignsAgent
        from random_agent import RandomAdXAgent
        from aggressive_agent import AggressiveAdXAgent
        
        print("=== Conservative Agent Testing Arena ===\n")
        
        # Create the conservative agent
        conservative_agent = ConservativeAdXAgent()
        print(f"Conservative agent: {conservative_agent.name}")
        
        # Create opponents
        example_agent = ExampleTwoDaysTwoCampaignsAgent()
        random_agent = RandomAdXAgent()
        aggressive_agent = AggressiveAdXAgent()
        
        print(f"Opponents: {example_agent.name}, {random_agent.name}, {aggressive_agent.name}\n")
        
        # Test against each opponent
        opponents = [example_agent, random_agent, aggressive_agent]
        
        for opponent in opponents:
            print(f"Testing against {opponent.name}...")
            
            # Create game with 2 players
            game = AdxTwoDayGame(num_players=2)
            
            # Create engine and run game
            engine = Engine(game, [conservative_agent, opponent], rounds=1)
            results = engine.run()
            
            print(f"  Conservative score: {results[0]:.2f}")
            print(f"  {opponent.name} score: {results[1]:.2f}")
            print(f"  Winner: {'Conservative' if results[0] > results[1] else opponent.name}")
            print()
        
        print("=== Testing Complete ===")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running this from the solutions directory")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "ConservativeAdXAgent"  # Agent name
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
            agent = ConservativeAdXAgent()
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test the conservative agent locally
        print("Testing ConservativeAdXAgent locally...")
        print("=" * 50)
        
        try:
            from core.engine import Engine
            from core.game.AdxTwoDayGame import AdxTwoDayGame
            from example_solution import ExampleTwoDaysTwoCampaignsAgent
            from random_agent import RandomAdXAgent
            from aggressive_agent import AggressiveAdXAgent
            
            print("=== Conservative Agent Testing Arena ===\n")
            
            # Create the conservative agent
            conservative_agent = ConservativeAdXAgent()
            print(f"Conservative agent: {conservative_agent.name}")
            
            # Create opponents
            example_agent = ExampleTwoDaysTwoCampaignsAgent()
            random_agent = RandomAdXAgent()
            aggressive_agent = AggressiveAdXAgent()
            
            print(f"Opponents: {example_agent.name}, {random_agent.name}, {aggressive_agent.name}\n")
            
            # Test against each opponent
            opponents = [example_agent, random_agent, aggressive_agent]
            
            for opponent in opponents:
                print(f"Testing against {opponent.name}...")
                
                # Create game with 2 players
                game = AdxTwoDayGame(num_players=2)
                
                # Create engine and run game
                engine = Engine(game, [conservative_agent, opponent], rounds=1)
                results = engine.run()
                
                print(f"  Conservative score: {results[0]:.2f}")
                print(f"  {opponent.name} score: {results[1]:.2f}")
                print(f"  Winner: {'Conservative' if results[0] > results[1] else opponent.name}")
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
agent_submission = ConservativeAdXAgent()
