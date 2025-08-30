"""
Random Agent for Lab 7 - bids random amounts.
"""

import random
from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class RandomAgent(BaseAuctionAgent):
    """
    A random agent that bids random amounts.
    This agent is useful for testing and training scenarios.
    """
    
    def __init__(self, name="RandomAgent", min_bid=1.0, max_bid=20.0):
        super().__init__(name)
        self.min_bid = min_bid
        self.max_bid = max_bid
    
    def setup(self, goods, valuation_function, kth_price=1):
        super().setup(goods, valuation_function, kth_price)
    
    def get_action(self, observation):
        """
        Get random bids for each good.
        
        Args:
            observation: Dictionary containing goods
            
        Returns:
            Dictionary mapping goods to random bid amounts
        """
        goods = observation.get("goods", set())
        
        if not goods:
            # Fallback if no goods provided
            return {"A": random.uniform(self.min_bid, self.max_bid), 
                   "B": random.uniform(self.min_bid, self.max_bid)}
        
        bids = {}
        for good in goods:
            # Random bid between min_bid and max_bid
            bids[good] = random.uniform(self.min_bid, self.max_bid)
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)
