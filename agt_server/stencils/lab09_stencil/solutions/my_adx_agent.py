import sys, os
import math
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..','..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent
from core.agents.lab09.aggressive_agent import AggressiveAdXAgent
from core.agents.lab09.random_agent import RandomAdXAgent
from server.connect_stencil import connect_agent_to_server

from core.local_arena import LocalArena
from core.game.AdxTwoDayGame import AdxTwoDayGame

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
    
    def __init__(self, name: str = "MyTwoDaysAdxAgent"):
        super().__init__("TODO: Enter your name or ID here")
        self.campaign_day1 = None  # Will be set by the game environment
        self.campaign_day2 = None  # Will be set by the game environment
        self.quality_score = 1.0  # Quality score from day 1 (affects day 2 budget)
        self.game_title = "adx_twoday"





    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """Get the agent's action based on the current observation."""

        self.campaign_day1 = Campaign.from_dict(observation["campaign_day1"])
        self.campaign_day2 = Campaign.from_dict(observation["campaign_day2"])
        day = observation["day"]
                
        # Check for quality score in both locations
        if "qc" in observation:
            self.quality_score = observation["qc"]
            # print(f"[DEBUG] AggressiveAdXAgent: Found qc directly: {self.quality_score}")
        elif "campaign" in observation and "qc" in observation["campaign"]:
            self.quality_score = observation["campaign"]["qc"]
            # print(f"[DEBUG] AggressiveAdXAgent: Found qc in campaign: {self.quality_score}")
        else:
            print(f"[DEBUG] AggressiveAdXAgent: No qc found, using default: {self.quality_score}")
        
        # print(f"[DEBUG] AggressiveAdXAgent: Final state - campaign_day1 is None: {self.campaign_day1 is None}")
        # print(f"[DEBUG] AggressiveAdXAgent: Final state - campaign_day2 is None: {self.campaign_day2 is None}")
        if self.campaign_day1:
            print(f"[DEBUG] AggressiveAdXAgent: campaign_day1 details: id={self.campaign_day1.id}, segment={self.campaign_day1.market_segment}, reach={self.campaign_day1.reach}, budget={self.campaign_day1.budget}")
        if self.campaign_day2:
            print(f"[DEBUG] AggressiveAdXAgent: campaign_day2 details: id={self.campaign_day2.id}, segment={self.campaign_day2.market_segment}, reach={self.campaign_day2.reach}, budget={self.campaign_day2.budget}")
        
        return self.get_bid_bundle(day)
    












    def get_bid_bundle(self, day: int) -> TwoDaysBidBundle:
        """
        Return a TwoDaysBidBundle for your assigned campaign on the given day (1 or 2).
        
        Parameters:
        - day: The day for which to create bids (1 or 2)
        
        Returns:
        - TwoDaysBidBundle containing all bids for the specified day
        """
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
    server = True  # Set to True to connect to server, False for local testing
    name = "MyBiddingAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "adx_twoday"  # Game type (hardcoded for this agent)
    
    if server:

        async def main():
            # Create agent and adapter
            agent = MyTwoDaysTwoCampaignsAgent(name=name)
            

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
        agent = MyTwoDaysTwoCampaignsAgent(name="MyTestAgent")
        opponent1 = AggressiveAdXAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]
        
        # Create arena and run tournament
        agents = [agent, opponent1] + random_agents
        arena = LocalArena(
            game_title="adx_twoday",
            game_class=AdxTwoDayGame,
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
agent_submission = MyTwoDaysTwoCampaignsAgent()

