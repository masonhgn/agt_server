import sys, os
import random
import math
# Add the core directory to the path
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

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
        self.name = name
        self.campaign_day1 = None
        self.campaign_day2 = None
        self.quality_score = 1.0






    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """Get the agent's action based on the current observation."""
        day = observation["day"]
        if day == 1:
            self.campaign_day1 = Campaign.from_dict(observation["campaign_day1"])
        elif day == 2:
            self.campaign_day2 = Campaign.from_dict(observation["campaign_day2"])
                
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
        print(day, self.campaign_day1)
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                ##randomness
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




# Export for server testing
agent_submission = RandomAdXAgent()
