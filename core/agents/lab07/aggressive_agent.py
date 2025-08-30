"""
Aggressive Agent for Lab 7 - bids aggressively high amounts.
"""

import random
from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class AggressiveAgent(BaseAuctionAgent):
    """
    An aggressive agent that bids high amounts to try to win goods.
    This agent is useful for testing against aggressive opponents.
    """
    
    def __init__(self, name="AggressiveAgent", bid_multiplier=1.5):
        super().__init__(name)
        self.bid_multiplier = bid_multiplier
    
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
    
    def get_action(self, observation):
        """
        Get aggressive bids for each good.
        
        Args:
            observation: Dictionary containing goods and valuation function
            
        Returns:
            Dictionary mapping goods to aggressive bid amounts
        """
        goods = observation.get("goods", set())
        valuation_function = observation.get("valuation_function", None)
        
        if not goods or not valuation_function:
            # Fallback if no goods or valuation function provided
            return {good: 15.0 for good in goods}
        
        bids = {}
        for good in goods:
            # Calculate value of this good
            value = valuation_function({good})
            
            # Bid aggressively (higher than the value)
            bids[good] = value * self.bid_multiplier
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)
