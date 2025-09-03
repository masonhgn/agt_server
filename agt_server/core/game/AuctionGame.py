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
    
    def __init__(self, goods: Set[str], player_names: List[str], 
                 num_rounds: int = 100, kth_price: int = 1, 
                 valuation_type: str = "additive", value_range: Tuple[int, int] = (0, 100)):
        """
        Initialize the auction game.
        
        Args:
            goods: Set of goods available for auction
            player_names: List of player names
            num_rounds: Number of rounds to play
            kth_price: Which price to use (1st price = 1, 2nd price = 2, etc.)
            valuation_type: Type of valuation function ("additive", "complement", "substitute", "randomized")
            value_range: Range for individual good valuations (min, max)
        """
        super().__init__()
        self.goods = goods
        self.players = player_names
        self._num_players = len(self.players)
        self.num_rounds = num_rounds
        self.kth_price = kth_price
        self.valuation_type = valuation_type
        self.value_range = value_range
        
        # Create goods to index mapping
        self._goods_to_index = {good: idx for idx, good in enumerate(goods)}
        self._index_to_goods = {idx: good for good, idx in self._goods_to_index.items()}
        
        # Game state
        self.current_round = 0
        self.bid_history = []
        self.allocation_history = []
        self.payment_history = []
        self.price_history = []
        self.utility_history = []
        
        # Valuation history for each player
        self.valuation_history = {player: [] for player in self.players}
        
        # Current valuations for each player (set each round)
        self.current_valuations = {player: [0] * len(goods) for player in self.players}
        
    def generate_valuations_for_round(self):
        """
        Generate valuations for all players for the current round.
        This mimics the old server's behavior of generating valuations each round.
        """
        from itertools import combinations
        
        for player in self.players:
            # Generate individual good valuations
            valuations = {}
            for good in self.goods:
                valuations[good] = random.randint(self.value_range[0], self.value_range[1])
            
            # Store valuations in the format expected by agents
            for good, value in valuations.items():
                self.current_valuations[player][self._goods_to_index[good]] = value
            
            # Store in history
            self.valuation_history[player].append(valuations)
    
    def calculate_valuation_for_player(self, player: str, bundle: Set[str]) -> float:
        """
        Calculate the valuation for a player's bundle using their current valuations.
        This mimics the old server's calculate_valuation method.
        """
        if not bundle:
            return 0
        
        # Get the player's current valuations
        valuations = self.current_valuations[player]
        
        # Convert bundle to indices and sum base values
        bundle_indices = [self._goods_to_index[good] for good in bundle]
        base_sum = sum(valuations[idx] for idx in bundle_indices)
        
        n = len(bundle)
        
        if self.valuation_type == 'additive':
            return base_sum
        elif self.valuation_type == 'complement':
            return base_sum * (1 + 0.05 * (n - 1)) if n > 0 else 0
        elif self.valuation_type == 'substitute':
            return base_sum * (1 - 0.05 * (n - 1)) if n > 0 else 0
        elif self.valuation_type == 'randomized':
            # For randomized, we need pairwise adjustments
            # This is simplified - in full implementation would need to store pairwise adjustments
            return base_sum
        else:
            return base_sum
    
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
    
    def calculate_utilities(self, allocation: Dict[str, str], payments: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate utilities for all players using their current valuations.
        
        Args:
            allocation: Dict mapping goods to winning player names
            payments: Dict mapping player names to their total payments
            
        Returns:
            Dict mapping player names to their utilities
        """
        utilities = {}
        
        for player in self.players:
            # Determine which goods this player won
            won_goods = {good for good, winner in allocation.items() if winner == player}
            
            # Calculate value of won goods using the game's valuation method
            value = self.calculate_valuation_for_player(player, won_goods)
            
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
        utilities = self.calculate_utilities(allocation, payments)
        
        # Print round results
        print(f"\n=== Round {self.current_round + 1} ===")
        print(f"Bids: {agent_actions}")
        print(f"Allocation: {allocation}")
        print(f"Prices: {prices}")
        print(f"Payments: {payments}")
        print(f"Utilities: {utilities}")
        
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
        
        # Return initial observations (using numeric indices)
        obs = {}
        for i, player in enumerate(self.players):
            obs[i] = {
                "goods": self.goods,
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
        print(f"[GAME DEBUG] AuctionGame.step() called with actions: {actions}", flush=True)
        print(f"[GAME DEBUG] Current round: {self.current_round}, num_rounds: {self.num_rounds}", flush=True)
        
        if self.current_round >= self.num_rounds:
            print(f"[GAME DEBUG] Game already finished, raising error", flush=True)
            raise ValueError("Game is already finished")
        
        # Convert numeric indices to player names for internal processing
        print(f"[GAME DEBUG] Converting agent indices to player names", flush=True)
        agent_actions = {}
        for i, player in enumerate(self.players):
            if i in actions:
                agent_actions[player] = actions[i]
                print(f"[GAME DEBUG] Agent {i} -> Player {player}: {actions[i]}")
            else:
                print(f"[GAME DEBUG] Warning: No action for agent {i}")
        
        print(f"[GAME DEBUG] Converted actions: {agent_actions}", flush=True)
        
        # Run the round
        print(f"[GAME DEBUG] Running round", flush=True)
        results = self.run_round(agent_actions)
        self.current_round += 1
        print(f"[GAME DEBUG] Round completed, current_round now: {self.current_round}", flush=True)
        
        # Prepare observations for next round (using numeric indices)
        print(f"[GAME DEBUG] Preparing observations for next round", flush=True)
        obs = {}
        for i, player in enumerate(self.players):
            obs[i] = {
                "goods": self.goods,
                "kth_price": self.kth_price,
                "round": self.current_round,
                "last_allocation": results['allocation'],
                "last_prices": results['prices'],
                "last_payments": results['payments']
            }
            print(f"[GAME DEBUG] Observation for agent {i}: {obs[i]}")
        
        # Rewards are the utilities from this round (using numeric indices)
        print(f"[GAME DEBUG] Preparing rewards", flush=True)
        rewards = {}
        for i, player in enumerate(self.players):
            rewards[i] = results['utilities'].get(player, 0)
            print(f"[GAME DEBUG] Reward for agent {i} (player {player}): {rewards[i]}")
        
        # Check if game is done
        done = self.current_round >= self.num_rounds
        print(f"[GAME DEBUG] Game done: {done}", flush=True)
        
        # Info contains additional data (using numeric indices)
        print(f"[GAME DEBUG] Preparing info", flush=True)
        info = {}
        for i, player in enumerate(self.players):
            info[i] = {
                "allocation": results['allocation'],
                "prices": results['prices'],
                "payments": results['payments'],
                "bids": results['bids']
            }
            print(f"[GAME DEBUG] Info for agent {i}: {info[i]}")
        
        print(f"[GAME DEBUG] step() returning: obs={obs}, rewards={rewards}, done={done}, info={info}", flush=True)
        return obs, rewards, done, info
    
    def num_players(self) -> int:
        """Get number of players in the game."""
        return self._num_players
    
    def get_player_name(self, index: int) -> str:
        """Get player name by index."""
        if 0 <= index < len(self.players):
            return self.players[index]
        raise IndexError(f"Player index {index} out of range")
    
    def get_player_index(self, player_name: str) -> int:
        """Get player index by name."""
        try:
            return self.players.index(player_name)
        except ValueError:
            raise ValueError(f"Player name '{player_name}' not found") 