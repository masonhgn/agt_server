"""
Marginal Value Agent for Lab 7 - bids based on marginal values.
"""

import random
from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class MarginalValueAgent(BaseAuctionAgent):
    """
    An agent that bids based on marginal values.
    This agent calculates the marginal value of each good and bids a fraction of it.
    """
    
    def __init__(self, name="MarginalValueAgent", bid_fraction=0.8):
        super().__init__(name)
        self.bid_fraction = bid_fraction
    
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
    
    def get_action(self, observation):
        """
        Get bids based on marginal values.
        
        Args:
            observation: Dictionary containing goods and valuation function
            
        Returns:
            Dictionary mapping goods to bid amounts
        """
        goods = observation.get("goods", set())
        valuation_function = observation.get("valuation_function", None)
        
        if not goods or not valuation_function:
            # Fallback if no goods or valuation function provided
            return {good: 5.0 for good in goods}
        
        bids = {}
        for good in goods:
            # Calculate marginal value of this good
            # Value with the good
            value_with_good = valuation_function({good})
            # Value without the good (empty bundle)
            value_without_good = valuation_function(set())
            marginal_value = value_with_good - value_without_good
            
            # Bid a fraction of the marginal value
            bids[good] = marginal_value * self.bid_fraction
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)
