"""
Conservative Agent for Lab 7 - bids conservatively low amounts.
"""

import random
from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class ConservativeAgent(BaseAuctionAgent):
    """
    A conservative agent that bids low amounts to minimize payments.
    This agent is useful for testing against conservative opponents.
    """
    
    def __init__(self, name="ConservativeAgent", bid_fraction=0.5):
        super().__init__(name)
        self.bid_fraction = bid_fraction
    
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
    
    def get_action(self, observation):
        """
        Get conservative bids for each good.
        
        Args:
            observation: Dictionary containing goods and valuation function
            
        Returns:
            Dictionary mapping goods to conservative bid amounts
        """
        goods = observation.get("goods", set())
        valuation_function = observation.get("valuation_function", None)
        
        if not goods or not valuation_function:
            # Fallback if no goods or valuation function provided
            return {good: 3.0 for good in goods}
        
        bids = {}
        for good in goods:
            # Calculate value of this good
            value = valuation_function({good})
            
            # Bid conservatively (lower than the value)
            bids[good] = value * self.bid_fraction
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)
