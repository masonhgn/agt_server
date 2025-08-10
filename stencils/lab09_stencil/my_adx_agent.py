import sys, os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.AdxTwoDayGame import TwoDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class MyAdXAgent:
    """
    Minimal Lab 9 agent stencil. Implement get_bid_bundle(day) to return your TwoDayBidBundle.
    """
    def __init__(self):
        self.name = "TODO: Enter your name or ID here"
        self.campaign_day1 = None  # Will be set by the game environment
        self.campaign_day2 = None  # Will be set by the game environment

    def get_bid_bundle(self, day: int) -> TwoDayBidBundle:
        """
        Return a TwoDayBidBundle for your assigned campaign on the given day (1 or 2).
        """
        raise NotImplementedError("Implement your bidding strategy here.") 