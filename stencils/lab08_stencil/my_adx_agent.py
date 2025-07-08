import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game.AdxOneDayGame import OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment

class MyAdXAgent:
    """
    Minimal Lab 8 agent stencil. Implement get_bid_bundle to return your OneDayBidBundle.
    """
    def __init__(self):
        self.name = "TODO: Enter your name or ID here"
        self.campaign = None  # Will be set by the game environment

    def get_bid_bundle(self) -> OneDayBidBundle:
        """
        Return a OneDayBidBundle for your assigned campaign.
        """
        raise NotImplementedError("Implement your bidding strategy here.") 