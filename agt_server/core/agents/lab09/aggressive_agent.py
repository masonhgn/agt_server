import sys, os
import math
# Add the core directory to the path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

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
        print(day, self.campaign_day1)
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






# Export for server testing
agent_submission = AggressiveAdXAgent()
