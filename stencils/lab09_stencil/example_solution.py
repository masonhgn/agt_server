import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

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