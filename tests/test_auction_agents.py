from typing import Dict, Set, Callable, Any
import random
from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class RandomAuctionAgent(BaseAuctionAgent):
    """Random auction agent that bids randomly between 0 and the item's value."""
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Get random bids for all goods."""
        bids = {}
        single_valuations = self.get_single_item_valuations()
        
        for good in self.goods:
            max_bid = single_valuations[good]
            bids[good] = random.uniform(0, max_bid)
        
        return bids


class TruthfulAuctionAgent(BaseAuctionAgent):
    """Truthful auction agent that bids exactly the marginal value of each good."""
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Get truthful bids (marginal values) for all goods."""
        bids = {}
        single_valuations = self.get_single_item_valuations()
        
        for good in self.goods:
            bids[good] = single_valuations[good]
        
        return bids


class OverBidderAuctionAgent(BaseAuctionAgent):
    """Over-bidding agent that bids above the item's value."""
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Get over-bids for all goods."""
        bids = {}
        single_valuations = self.get_single_item_valuations()
        
        for good in self.goods:
            max_bid = single_valuations[good]
            bids[good] = random.uniform(max_bid, 2 * max_bid)
        
        return bids


class FPAuctionAgent(BaseAuctionAgent):
    """First-price auction agent that bids 6/7 of the item's value."""
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Get first-price bids (6/7 of value) for all goods."""
        bids = {}
        single_valuations = self.get_single_item_valuations()
        
        for good in self.goods:
            bids[good] = (6/7) * single_valuations[good]
        
        return bids


class ZeroBidAuctionAgent(BaseAuctionAgent):
    """Agent that always bids zero."""
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Get zero bids for all goods."""
        bids = {}
        for good in self.goods:
            bids[good] = 0.0
        return bids 