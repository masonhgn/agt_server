import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class ExampleAdXAgent:
    """
    Example solution for Lab 8: bids $1 on all matching segments, uses full budget as limits.
    """
    def __init__(self):
        self.name = "example_solution"
        self.campaign = None  # Will be set by the game environment

    # NOTE: self.campaign is set by the game environment before get_bid_bundle is called.
    def get_bid_bundle(self) -> OneDayBidBundle:
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=1.0,
                    spending_limit=self.campaign.budget
                ))
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,
            bid_entries=bid_entries
        ) 