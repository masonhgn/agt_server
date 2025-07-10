import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import numpy as np

from core.game.AdxTwoDayGame import TwoDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class ExampleAdXAgent:
    """
    Example solution for Lab 9: bids $1 on all matching segments, uses full budget as limits.
    """
    def __init__(self):
        self.name = "example_solution"
        self.campaign_day1 = None  # Will be set by the game environment
        self.campaign_day2 = None  # Will be set by the game environment

    # NOTE: campaign_day1 and campaign_day2 are set by the game environment before get_bid_bundle is called.
    def get_bid_bundle(self, day: int) -> TwoDayBidBundle:
        if day == 1:
            campaign = self.campaign_day1
        elif day == 2:
            campaign = self.campaign_day2
        else:
            raise ValueError("Day must be 1 or 2")
        if campaign is None:
            raise ValueError("Campaign is not set for the given day.")
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=1.0,
                    spending_limit=campaign.budget
                ))
        return TwoDayBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )
    
    def update(self, reward, info=None):
        pass

class ExampleTwoDayAgent:
    def __init__(self):
        self.name = "ExampleTwoDayAgent"
    
    def get_action(self, state):
        # Simple two-day strategy
        return {"campaign_id": "test", "day1_bid": 1.0, "day2_bid": 1.5}
    
    def update(self, reward, info=None):
        pass 