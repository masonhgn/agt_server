import sys, os
import math
# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent

class AggressiveAdXAgent(BaseAgent):
    """
    Aggressive agent for Lab 9: Prioritizes quality score on day 1 to maximize day 2 budget.
    This strategy sacrifices day 1 profit for better day 2 opportunities.
    """
    
    def __init__(self, name: str = "AggressiveAdXAgent"):
        super().__init__(name)
        self.campaign_day1 = None
        self.campaign_day2 = None
        self.quality_score = 1.0

    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """Get the agent's action based on the current observation."""
        # Debug logging
        print(f"[DEBUG] AggressiveAdXAgent: Received observation: {observation}")
        print(f"[DEBUG] AggressiveAdXAgent: observation type: {type(observation)}")
        print(f"[DEBUG] AggressiveAdXAgent: observation keys: {list(observation.keys()) if observation else 'None'}")
        
        # Extract day from observation - check both direct and nested locations
        day = 1
        if observation:
            # Check if day is directly in observation
            if "day" in observation:
                day = observation["day"]
                print(f"[DEBUG] AggressiveAdXAgent: Found day directly: {day}")
            # Check if day is nested under campaign
            elif "campaign" in observation and "day" in observation["campaign"]:
                day = observation["campaign"]["day"]
                print(f"[DEBUG] AggressiveAdXAgent: Found day in campaign: {day}")
            else:
                print(f"[DEBUG] AggressiveAdXAgent: No day found, using default: {day}")
        
        print(f"[DEBUG] AggressiveAdXAgent: Final day value: {day}")
        
        # Set campaigns from observation if available
        if observation:
            print(f"[DEBUG] AggressiveAdXAgent: Processing observation for campaigns...")
            
            # Check if campaigns are directly in observation
            if "campaign_day1" in observation:
                campaign_dict = observation["campaign_day1"]
                print(f"[DEBUG] AggressiveAdXAgent: Found campaign_day1 directly: {campaign_dict}")
                self.campaign_day1 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                print(f"[DEBUG] AggressiveAdXAgent: Set campaign_day1 from direct observation")
            elif "campaign" in observation and "campaign_day1" in observation["campaign"]:
                campaign_dict = observation["campaign"]["campaign_day1"]
                print(f"[DEBUG] AggressiveAdXAgent: Found campaign_day1 in campaign: {campaign_dict}")
                self.campaign_day1 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                print(f"[DEBUG] AggressiveAdXAgent: Set campaign_day1 from nested observation")
            else:
                print(f"[DEBUG] AggressiveAdXAgent: No campaign_day1 found in observation")
                
            if "campaign_day2" in observation:
                campaign_dict = observation["campaign_day2"]
                print(f"[DEBUG] AggressiveAdXAgent: Found campaign_day2 directly: {campaign_dict}")
                self.campaign_day2 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                print(f"[DEBUG] AggressiveAdXAgent: Set campaign_day2 from direct observation")
            elif "campaign" in observation and "campaign_day2" in observation["campaign"]:
                campaign_dict = observation["campaign"]["campaign_day2"]
                print(f"[DEBUG] AggressiveAdXAgent: Found campaign_day2 in campaign: {campaign_dict}")
                self.campaign_day2 = Campaign(
                    id=campaign_dict["id"],
                    market_segment=MarketSegment(campaign_dict["market_segment"]),
                    reach=campaign_dict["reach"],
                    budget=campaign_dict["budget"]
                )
                print(f"[DEBUG] AggressiveAdXAgent: Set campaign_day2 from nested observation")
            else:
                print(f"[DEBUG] AggressiveAdXAgent: No campaign_day2 found in observation")
                
            # Check for quality score in both locations
            if "qc" in observation:
                self.quality_score = observation["qc"]
                print(f"[DEBUG] AggressiveAdXAgent: Found qc directly: {self.quality_score}")
            elif "campaign" in observation and "qc" in observation["campaign"]:
                self.quality_score = observation["campaign"]["qc"]
                print(f"[DEBUG] AggressiveAdXAgent: Found qc in campaign: {self.quality_score}")
            else:
                print(f"[DEBUG] AggressiveAdXAgent: No qc found, using default: {self.quality_score}")
        
        print(f"[DEBUG] AggressiveAdXAgent: Final state - campaign_day1 is None: {self.campaign_day1 is None}")
        print(f"[DEBUG] AggressiveAdXAgent: Final state - campaign_day2 is None: {self.campaign_day2 is None}")
        if self.campaign_day1:
            print(f"[DEBUG] AggressiveAdXAgent: campaign_day1 details: id={self.campaign_day1.id}, segment={self.campaign_day1.market_segment}, reach={self.campaign_day1.reach}, budget={self.campaign_day1.budget}")
        if self.campaign_day2:
            print(f"[DEBUG] AggressiveAdXAgent: campaign_day2 details: id={self.campaign_day2.id}, segment={self.campaign_day2.market_segment}, reach={self.campaign_day2.reach}, budget={self.campaign_day2.budget}")
        
        return self.get_bid_bundle(day)

    def get_bid_bundle(self, day: int) -> TwoDaysBidBundle:
        """Aggressive bidding strategy prioritizing quality score."""
        if day == 1:
            campaign = self.campaign_day1
            # Aggressive day 1 strategy: high bids to maximize quality score
            bid_amount = 2.5  # High bid to win more impressions
            budget_usage = 0.95  # Use almost all budget
        elif day == 2:
            campaign = self.campaign_day2
            # Day 2 strategy: capitalize on high quality score from day 1
            if self.quality_score > 0.9:
                # Very high quality score - be very aggressive
                bid_amount = 3.0
                budget_usage = 1.0
            elif self.quality_score > 0.7:
                # Good quality score - moderately aggressive
                bid_amount = 2.0
                budget_usage = 0.9
            else:
                # Lower quality score - still aggressive but careful
                bid_amount = 1.5
                budget_usage = 0.8
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
    Local testing arena for Aggressive AdX Agent.
    Run this file directly to test the aggressive agent against other agents.
    """
    try:
        from core.engine import Engine
        from core.game.AdxTwoDayGame import AdxTwoDayGame
        from example_solution import ExampleTwoDaysTwoCampaignsAgent
        from random_agent import RandomAdXAgent
        from conservative_agent import ConservativeAdXAgent
        
        print("=== Aggressive Agent Testing Arena ===\n")
        
        # Create the aggressive agent
        aggressive_agent = AggressiveAdXAgent()
        print(f"Aggressive agent: {aggressive_agent.name}")
        
        # Create opponents
        example_agent = ExampleTwoDaysTwoCampaignsAgent()
        random_agent = RandomAdXAgent()
        conservative_agent = ConservativeAdXAgent()
        
        print(f"Opponents: {example_agent.name}, {random_agent.name}, {conservative_agent.name}\n")
        
        # Test against each opponent
        opponents = [example_agent, random_agent, conservative_agent]
        
        for opponent in opponents:
            print(f"Testing against {opponent.name}...")
            
            # Create game with 2 players
            game = AdxTwoDayGame(num_players=2)
            
            # Create engine and run game
            engine = Engine(game, [aggressive_agent, opponent], rounds=1)
            results = engine.run()
            
            print(f"  Aggressive score: {results[0]:.2f}")
            print(f"  {opponent.name} score: {results[1]:.2f}")
            print(f"  Winner: {'Aggressive' if results[0] > results[1] else opponent.name}")
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
    server = True # Set to True to connect to server, False for local testing
    name = "AggressiveAdXAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = True  # Enable verbose debug output
    game = "adx_twoday"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = AggressiveAdXAgent()
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test the aggressive agent locally
        print("Testing AggressiveAdXAgent locally...")
        print("=" * 50)
        
        try:
            from core.engine import Engine
            from core.game.AdxTwoDayGame import AdxTwoDayGame
            from example_solution import ExampleTwoDaysTwoCampaignsAgent
            from random_agent import RandomAdXAgent
            from conservative_agent import ConservativeAdXAgent
            
            print("=== Aggressive Agent Testing Arena ===\n")
            
            # Create the aggressive agent
            aggressive_agent = AggressiveAdXAgent()
            print(f"Aggressive agent: {aggressive_agent.name}")
            
            # Create opponents
            example_agent = ExampleTwoDaysTwoCampaignsAgent()
            random_agent = RandomAdXAgent()
            conservative_agent = ConservativeAdXAgent()
            
            print(f"Opponents: {example_agent.name}, {random_agent.name}, {conservative_agent.name}\n")
            
            # Test against each opponent
            opponents = [example_agent, random_agent, conservative_agent]
            
            for opponent in opponents:
                print(f"Testing against {opponent.name}...")
                
                # Create game with 2 players
                game = AdxTwoDayGame(num_players=2)
                
                # Create engine and run game
                engine = Engine(game, [aggressive_agent, opponent], rounds=1)
                results = engine.run()
                
                print(f"  Aggressive score: {results[0]:.2f}")
                print(f"  {opponent.name} score: {results[1]:.2f}")
                print(f"  Winner: {'Aggressive' if results[0] > results[1] else opponent.name}")
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
agent_submission = AggressiveAdXAgent()
