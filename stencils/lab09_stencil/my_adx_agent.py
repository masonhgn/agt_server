import sys, os
import math
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent

class MyTwoDaysTwoCampaignsAgent(BaseAgent):
    """
    Lab 9: TAC AdX Game (Two-Day Variant) Agent
    
    This agent competes in AdX auctions over two consecutive days.
    The budget for the second day's campaign depends on the quality score
    achieved on the first day.
    
    Quality Score Formula (corrected implementation):
    QC(x) = (2/a) * (arctan(a * (x/R - b)) - arctan(-b)) + 1
    where a = 4.08577, b = 3.08577, x = impressions achieved, R = campaign reach
    
    Note: The +1 offset is required for the formula to produce the expected behavior
    (QC(0) ≈ 0.89, QC(R) ≈ 0.90, QC(∞) ≈ 1.38)
    """
    
    def __init__(self):
        super().__init__("TODO: Enter your name or ID here")
        self.campaign_day1 = None  # Will be set by the game environment
        self.campaign_day2 = None  # Will be set by the game environment
        self.quality_score = 1.0  # Quality score from day 1 (affects day 2 budget)

    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """
        Get the agent's action based on the current observation.
        For AdX games, this returns a bid bundle for the current day.
        """
        # Extract day from observation
        day = observation.get("day", 1) if observation else 1
        
        # Set campaigns from observation if available
        if observation:
            if "campaign_day1" in observation:
                campaign_dict = observation["campaign_day1"]
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
            if "qc" in observation:
                self.quality_score = observation["qc"]
        
        return self.get_bid_bundle(day)

    def get_bid_bundle(self, day: int) -> TwoDaysBidBundle:
        """
        Return a TwoDaysBidBundle for your assigned campaign on the given day (1 or 2).
        
        Parameters:
        - day: The day for which to create bids (1 or 2)
        
        Returns:
        - TwoDaysBidBundle containing all bids for the specified day
        """
        if day == 1:
            campaign = self.campaign_day1
        elif day == 2:
            campaign = self.campaign_day2
        else:
            raise ValueError("Day must be 1 or 2")
            
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        
        # TODO: Implement your bidding strategy here
        # This is where you should implement your agent's logic for:
        # 1. Deciding how much to bid on each market segment
        # 2. Setting spending limits for each segment
        # 3. Balancing day 1 performance vs quality score for day 2
        
        # TODO: Replace this placeholder implementation with your strategy
        raise NotImplementedError("Implement your bidding strategy here")
    
    def calculate_quality_score(self, impressions_achieved: int, campaign_reach: int) -> float:
        """
        Calculate quality score using the formula from the writeup.
        
        QC(x) = (2/a) * (arctan(a * (x/R - b)) - arctan(-b)) + 1
        where a = 4.08577, b = 3.08577
        
        Parameters:
        - impressions_achieved: Number of impressions acquired (x)
        - campaign_reach: Campaign's reach goal (R)
        
        Returns:
        - Quality score between 0 and 1.38442
        """
        a = 4.08577
        b = 3.08577
        x = impressions_achieved
        R = campaign_reach
        
        if R == 0:
            return 0.0
            
        x_over_R = x / R
        quality_score = (2 / a) * (math.atan(a * (x_over_R - b)) - math.atan(-b)) + 1
        
        return max(0.0, quality_score)  # Ensure non-negative
    
    def get_first_campaign(self) -> Campaign:
        """Get the campaign assigned for the first day."""
        return self.campaign_day1
    
    def get_second_campaign(self) -> Campaign:
        """Get the campaign assigned for the second day."""
        return self.campaign_day2


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = ...  # TODO: Please give your agent a name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "adx_two_day"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Generate unique name if not provided
            if not name:
                import random
                agent_name = f"MyTwoDaysTwoCampaignsAgent_{random.randint(1000, 9999)}"
            else:
                agent_name = name
                
            # Create agent and adapter
            agent = MyTwoDaysTwoCampaignsAgent()
            agent.name = agent_name
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, agent_name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Test your agent locally
        print("Testing MyTwoDaysTwoCampaignsAgent locally...")
        print("=" * 50)
        
        try:
            from core.engine import Engine
            from core.game.AdxTwoDayGame import AdxTwoDayGame
            from solutions.example_solution import ExampleTwoDaysTwoCampaignsAgent
            from solutions.random_agent import RandomAdXAgent
            from solutions.aggressive_agent import AggressiveAdXAgent
            from solutions.conservative_agent import ConservativeAdXAgent
            
            print("=== Lab 9: AdX Two-Day Game Testing Arena ===\n")
            
            # Create your agent
            my_agent = MyTwoDaysTwoCampaignsAgent()
            print(f"Your agent: {my_agent.name}")
            
            # Create example opponents
            example_agent = ExampleTwoDaysTwoCampaignsAgent()
            random_agent = RandomAdXAgent()
            aggressive_agent = AggressiveAdXAgent()
            conservative_agent = ConservativeAdXAgent()
            
            print(f"Opponents: {example_agent.name}, {random_agent.name}, {aggressive_agent.name}, {conservative_agent.name}\n")
            
            # Test against each opponent
            opponents = [example_agent, random_agent, aggressive_agent, conservative_agent]
            
            for opponent in opponents:
                print(f"Testing against {opponent.name}...")
                
                # Create game with 2 players
                game = AdxTwoDayGame(num_players=2)
                
                # Create engine and run game
                engine = Engine(game, [my_agent, opponent], rounds=1)
                results = engine.run()
                
                print(f"  Your score: {results[0]:.2f}")
                print(f"  {opponent.name} score: {results[1]:.2f}")
                print(f"  Winner: {'You' if results[0] > results[1] else opponent.name}")
                print()
            
            print("=== Testing Complete ===")
            
        except ImportError as e:
            print(f"Import error: {e}")
            print("Make sure you're running this from the lab09_stencil directory")
        except Exception as e:
            print(f"Error during testing: {e}")
            import traceback
            traceback.print_exc()

# Export for server testing
agent_submission = MyTwoDaysTwoCampaignsAgent("MyTwoDaysTwoCampaignsAgent") 