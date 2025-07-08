from typing import Dict, Set, Callable, List, Tuple, Any
import random
import itertools
from .base_game import BaseGame, PlayerId, ObsDict, ActionDict, RewardDict, InfoDict


class AuctionGame(BaseGame):
    """
    Simultaneous Sealed Bid Auction Game
    
    Players bid on multiple goods simultaneously. Each good is awarded to the highest bidder,
    who pays their bid amount. Players can have different valuation functions (additive, 
    complement, substitute, etc.).
    """
    
    def __init__(self, goods: Set[str], valuation_functions: Dict[str, Callable], 
                 num_rounds: int = 100, kth_price: int = 1):
        """
        Initialize the auction game.
        
        Args:
            goods: Set of goods available for auction
            valuation_functions: Dict mapping player names to their valuation functions
            num_rounds: Number of rounds to play
            kth_price: Which price to use (1st price = 1, 2nd price = 2, etc.)
        """
        super().__init__()
        self.goods = goods
        self.valuation_functions = valuation_functions
        self.kth_price = kth_price
        self.players = list(valuation_functions.keys())
        self._num_players = len(self.players)
        self.num_rounds = num_rounds
        
        # Game state
        self.current_round = 0
        self.bid_history = []
        self.allocation_history = []
        self.payment_history = []
        self.price_history = []
        self.utility_history = []
        
    def calculate_marginal_value(self, goods: Set[str], selected_good: str, 
                               valuation_function: Callable, bids: Dict[str, float], 
                               prices: Dict[str, float]) -> float:
        """
        Calculate the marginal value of a given good for a bidder.
        
        Args:
            goods: Set of all goods
            selected_good: The good to calculate marginal value for
            valuation_function: The player's valuation function
            bids: Current bid vector
            prices: Current price vector
            
        Returns:
            Marginal value of the selected good
        """
        # Determine which goods the player would win with current bids
        won_goods = set()
        for good in goods:
            if bids.get(good, 0) >= prices.get(good, 0):
                won_goods.add(good)
        
        # Value with the selected good
        bundle_with_good = won_goods | {selected_good}
        value_with_good = valuation_function(bundle_with_good)
        
        # Value without the selected good
        bundle_without_good = won_goods - {selected_good}
        value_without_good = valuation_function(bundle_without_good)
        
        # Marginal value is the difference
        marginal_value = value_with_good - value_without_good
        
        return marginal_value
    
    def compute_auction_result(self, bids: Dict[str, Dict[str, float]]) -> Tuple[Dict[str, str], Dict[str, float], Dict[str, float]]:
        """
        Compute the auction outcome for each good.
        
        Args:
            bids: Dict mapping player names to their bid dictionaries
            
        Returns:
            allocation: Dict mapping goods to winning player names
            payments: Dict mapping player names to their total payments
            prices: Dict mapping goods to their clearing prices
        """
        allocation = {}
        payments = {player: 0.0 for player in self.players}
        prices = {}
        
        for good in self.goods:
            # Collect all valid bids for this good
            bid_tuples = []
            for player, bid_dict in bids.items():
                if bid_dict and good in bid_dict and bid_dict[good] > 0:
                    bid_tuples.append((bid_dict[good], player))
            
            if bid_tuples:
                # Sort bids in descending order
                sorted_bids = sorted(bid_tuples, key=lambda x: x[0], reverse=True)
                winner = sorted_bids[0][1]
                
                # Determine kth highest bid price
                kth_index = min(self.kth_price - 1, len(sorted_bids) - 1)
                kth_bid = sorted_bids[kth_index][0]
                
                allocation[good] = winner
                prices[good] = kth_bid
                payments[winner] += kth_bid
            else:
                allocation[good] = None
                prices[good] = 0.0
        
        return allocation, payments, prices
    
    def calculate_utilities(self, allocation: Dict[str, str], payments: Dict[str, float], 
                          valuation_functions: Dict[str, Callable]) -> Dict[str, float]:
        """
        Calculate utilities for all players.
        
        Args:
            allocation: Dict mapping goods to winning player names
            payments: Dict mapping player names to their total payments
            valuation_functions: Dict mapping player names to their valuation functions
            
        Returns:
            Dict mapping player names to their utilities
        """
        utilities = {}
        
        for player in self.players:
            # Determine which goods this player won
            won_goods = {good for good, winner in allocation.items() if winner == player}
            
            # Calculate value of won goods
            value = valuation_functions[player](won_goods)
            
            # Calculate utility (value - payment)
            utility = value - payments[player]
            utilities[player] = utility
        
        return utilities
    
    def run_round(self, agent_actions: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Run a single round of the auction.
        
        Args:
            agent_actions: Dict mapping player names to their bid dictionaries
            
        Returns:
            Dict containing round results
        """
        # Compute auction outcome
        allocation, payments, prices = self.compute_auction_result(agent_actions)
        
        # Calculate utilities
        utilities = self.calculate_utilities(allocation, payments, self.valuation_functions)
        
        # Store history
        self.bid_history.append(agent_actions)
        self.allocation_history.append(allocation)
        self.payment_history.append(payments)
        self.price_history.append(prices)
        self.utility_history.append(utilities)
        
        # Return round results
        return {
            'allocation': allocation,
            'payments': payments,
            'prices': prices,
            'utilities': utilities,
            'bids': agent_actions
        }
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get the current game state."""
        return {
            'current_round': self.current_round,
            'goods': self.goods,
            'players': self.players,
            'kth_price': self.kth_price,
            'bid_history': self.bid_history,
            'allocation_history': self.allocation_history,
            'payment_history': self.payment_history,
            'price_history': self.price_history,
            'utility_history': self.utility_history
        }
    
    def reset(self, seed: int | None = None) -> ObsDict:
        """Reset the game state."""
        if seed is not None:
            random.seed(seed)
        
        self.current_round = 0
        self.bid_history = []
        self.allocation_history = []
        self.payment_history = []
        self.price_history = []
        self.utility_history = []
        
        # Initialize metadata
        self.metadata = {
            "num_players": self._num_players,
            "goods": self.goods,
            "kth_price": self.kth_price
        }
        
        # Return initial observations
        obs = {}
        for player in self.players:
            obs[player] = {
                "goods": self.goods,
                "valuation_function": self.valuation_functions[player],
                "kth_price": self.kth_price,
                "round": 0
            }
        return obs
    
    def players_to_move(self) -> List[PlayerId]:
        """Return the subset of players whose actions are required now."""
        if self.current_round < self.num_rounds:
            return [player for player in self.players]
        return []
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Advance the game by applying actions."""
        if self.current_round >= self.num_rounds:
            raise ValueError("Game is already finished")
        
        # Convert actions to the expected format
        agent_actions = {str(player): actions[player] for player in self.players}
        
        # Run the round
        results = self.run_round(agent_actions)
        self.current_round += 1
        
        # Prepare observations for next round
        obs = {}
        for player in self.players:
            obs[player] = {
                "goods": self.goods,
                "valuation_function": self.valuation_functions[player],
                "kth_price": self.kth_price,
                "round": self.current_round,
                "last_allocation": results['allocation'],
                "last_prices": results['prices'],
                "last_payments": results['payments']
            }
        
        # Rewards are the utilities from this round
        rewards = results['utilities']
        
        # Check if game is done
        done = self.current_round >= self.num_rounds
        
        # Info contains additional data
        info = {}
        for player in self.players:
            info[player] = {
                "allocation": results['allocation'],
                "prices": results['prices'],
                "payments": results['payments'],
                "bids": results['bids']
            }
        
        return obs, rewards, done, info
    
    def num_players(self) -> int:
        """Get number of players in the game."""
        return self._num_players 