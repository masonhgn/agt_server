"""
Test auction agents for lab 7 solutions.

These are simple agents used for testing and training the SCPP agent.
"""

import random
import sys
import os

# Add parent directories to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent


class TruthfulAuctionAgent(BaseAuctionAgent):
    """
    A truthful auction agent that bids its true marginal values.
    
    This agent calculates the marginal value of each good and bids that amount.
    It's called "truthful" because it bids what it actually values each good at.
    """
    
    def __init__(self, name="TruthfulAuctionAgent"):
        super().__init__(name)
    
    def get_action(self, observation):
        """
        Get truthful bids based on marginal values.
        
        Args:
            observation: Dictionary containing goods and valuation function
            
        Returns:
            Dictionary mapping goods to bid amounts
        """
        goods = observation.get("goods", set())
        valuation_function = observation.get("valuation_function", None)
        
        if not goods:
            # This is a major issue - no goods available
            raise ValueError(f"[ERROR] {self.name}: No goods available in observation: {observation}")
        
        if not valuation_function:
            # This is a major issue - no valuation function provided
            raise ValueError(f"[ERROR] {self.name}: No valuation function provided in observation: {observation}")
        
        bids = {}
        for good in goods:
            # Calculate marginal value of this good
            # Value with the good
            value_with_good = valuation_function({good})
            # Value without the good (empty bundle)
            value_without_good = valuation_function(set())
            # Marginal value is the difference
            marginal_value = value_with_good - value_without_good
            bids[good] = marginal_value
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)


class RandomAuctionAgent(BaseAuctionAgent):
    """
    A random auction agent that bids random amounts.
    
    This agent is useful for testing and training scenarios.
    """
    
    def __init__(self, name="RandomAuctionAgent"):
        super().__init__(name)
    
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
            # This is a major issue - no goods available
            raise ValueError(f"[ERROR] {self.name}: No goods available in observation: {observation}")
        
        bids = {}
        for good in goods:
            # Random bid between 1 and 10
            bids[good] = random.uniform(1.0, 10.0)
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)


class MarginalValueAuctionAgent(BaseAuctionAgent):
    """
    An auction agent that bids based on marginal values.
    
    This agent calculates marginal values and bids a fraction of them.
    """
    
    def __init__(self, name="MarginalValueAuctionAgent", bid_fraction=0.8):
        super().__init__(name)
        self.bid_fraction = bid_fraction
    
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
        
        if not goods:
            # This is a major issue - no goods available
            raise ValueError(f"[ERROR] {self.name}: No goods available in observation: {observation}")
        
        if not valuation_function:
            # This is a major issue - no valuation function provided
            raise ValueError(f"[ERROR] {self.name}: No valuation function provided in observation: {observation}")
        
        bids = {}
        for good in goods:
            # Calculate marginal value of this good
            value_with_good = valuation_function({good})
            value_without_good = valuation_function(set())
            marginal_value = value_with_good - value_without_good
            
            # Bid a fraction of the marginal value
            bids[good] = marginal_value * self.bid_fraction
        
        return bids
    
    def update(self, observation, action, reward, done, info):
        """Update the agent with results."""
        super().update(observation, action, reward, done, info)
