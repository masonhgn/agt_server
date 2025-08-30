from abc import ABC, abstractmethod
from typing import Dict, Set, Callable, Any
import random


class BaseAuctionAgent(ABC):
    """
    Base class for auction agents.
    
    Auction agents participate in simultaneous sealed bid auctions.
    They receive valuations for goods and must submit bids.
    """
    
    def __init__(self, name: str | None = None):
        """
        Initialize the auction agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name or f"AuctionAgent_{random.randint(1000, 9999)}"
        self.goods = set()
        self.kth_price = 1
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = []
        
        # Valuation-related attributes (like old server)
        self.valuations = []  # Will be set by the game each round
        self.valuation_type = "additive"
        self._goods_to_index = {}
        self._index_to_goods = {}
        
    def setup(self, goods: Set[str], kth_price: int = 1):
        """
        Set up the agent with game parameters.
        
        Args:
            goods: Set of goods available for auction
            kth_price: Which price to use (1st price = 1, 2nd price = 2, etc.)
        """
        self.goods = goods
        self.kth_price = kth_price
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = []
        
        # Initialize valuation-related attributes
        self.valuations = [0] * len(goods)
        self._goods_to_index = {good: idx for idx, good in enumerate(goods)}
        self._index_to_goods = {idx: good for good, idx in self._goods_to_index.items()}
        
    def set_valuations(self, valuations: list):
        """
        Set the agent's valuations for the current round.
        This is called by the game each round.
        
        Args:
            valuations: List of valuations for each good (in order)
        """
        self.valuations = valuations.copy()
        
    def calculate_valuation(self, bundle: Set[str]) -> float:
        """
        Calculate the valuation for a bundle of goods.
        This mimics the old server's calculate_valuation method.
        
        Args:
            bundle: Set of goods to value
            
        Returns:
            Value of the bundle
        """
        if not bundle:
            return 0
        
        # Convert goods to indices and sum base values
        bundle_indices = [self._goods_to_index[good] for good in bundle]
        base_sum = sum(self.valuations[idx] for idx in bundle_indices)
        
        n = len(bundle)
        
        if self.valuation_type == 'additive':
            return base_sum
        elif self.valuation_type == 'complement':
            return base_sum * (1 + 0.05 * (n - 1)) if n > 0 else 0
        elif self.valuation_type == 'substitute':
            return base_sum * (1 - 0.05 * (n - 1)) if n > 0 else 0
        else:
            return base_sum
    
    def get_valuation(self, good: str) -> float:
        """
        Get the valuation for a specific good.
        
        Args:
            good: Name of the good
            
        Returns:
            Value of the good
        """
        return self.valuations[self._goods_to_index[good]]
    
    def get_single_item_valuations(self) -> Dict[str, float]:
        """
        Get valuations for individual goods.
        
        Returns:
            Dict mapping goods to their individual values
        """
        valuations = {}
        for good in self.goods:
            valuations[good] = self.get_valuation(good)
        return valuations
        
    @abstractmethod
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """
        Get the agent's action (bids) for the current round.
        
        Args:
            observation: Current game observation containing:
                - goods: Set of goods
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
    
    def reset(self):
        """Reset the agent's internal state."""
        self.current_round = 0
        self.bid_history = []
        self.utility_history = []
        self.allocation_history = []
        self.price_history = []
        self.valuations = [0] * len(self.goods) if self.goods else [] 