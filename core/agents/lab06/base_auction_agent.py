from abc import ABC, abstractmethod
from typing import Dict, Set, Callable, Any, Optional
import random



class BaseAuctionAgent(ABC):
    """
    Base class for auction agents.
    
    Auction agents participate in simultaneous sealed bid auctions.
    They receive valuations for goods and must submit bids.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize the auction agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name or f"AuctionAgent_{random.randint(1000, 9999)}"
        self.goods = set()
        self.valuation_function = None
        self.kth_price = 1
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = []
        
    def setup(self, goods: Set[str], valuation_function: Callable, kth_price: int = 1):
        """
        Set up the agent with game parameters.
        
        Args:
            goods: Set of goods available for auction
            valuation_function: Function that takes a bundle and returns its value
            kth_price: Which price to use (1st price = 1, 2nd price = 2, etc.)
        """
        self.goods = goods
        self.valuation_function = valuation_function
        self.kth_price = kth_price
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = []
        
    @abstractmethod
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """
        Get the agent's action (bids) for the current round.
        
        Args:
            observation: Current game observation containing:
                - goods: Set of goods
                - valuation_function: The agent's valuation function
                - kth_price: Which price to use
                - round: Current round number
                - last_allocation: Previous round's allocation (if any)
                - last_prices: Previous round's prices (if any)
                - last_payments: Previous round's payments (if any)
                
        Returns:
            Dict mapping goods to bid amounts
        """
        pass
    
    def update(self, observation: Dict[str, Any], action: Dict[str, float], 
               reward: float, done: bool, info: Dict[str, Any]):
        """
        Update the agent with the results of the last action.
        
        Args:
            observation: Current game observation
            action: The action taken by this agent
            reward: The reward received
            done: Whether the game is finished
            info: Additional information about the round
        """
        self.current_round = observation.get('round', self.current_round)
        self.bid_history.append(action)
        self.utility_history.append(reward)
        
        if 'allocation' in info:
            self.allocation_history.append(info['allocation'])
        if 'prices' in info:
            self.price_history.append(info['prices'])
    
    def get_valuation(self, bundle: Set[str]) -> float:
        """
        Get the valuation for a bundle of goods.
        
        Args:
            bundle: Set of goods to value
            
        Returns:
            Value of the bundle
        """
        if self.valuation_function is None:
            raise ValueError("Agent not set up with valuation function")
        return self.valuation_function(bundle)
    
    def get_single_item_valuations(self) -> Dict[str, float]:
        """
        Get valuations for individual goods.
        
        Returns:
            Dict mapping goods to their individual values
        """
        if self.valuation_function is None:
            raise ValueError("Agent not set up with valuation function")
        
        valuations = {}
        for good in self.goods:
            valuations[good] = self.valuation_function({good})
        return valuations
    
    def reset(self):
        """Reset the agent's internal state."""
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = [] 