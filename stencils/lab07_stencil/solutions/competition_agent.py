"""
Solution for Competition Agent implementation.
"""

import sys
import os
import time
import random

# Add parent directories to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import expected_local_bid

class CompetitionAgent(BaseAuctionAgent):
    def __init__(self, name: str | None = None):
        """Initialize the competition agent with all required attributes."""
        super().__init__(name)
        
        # Competition agent parameters - initialize these here so they're always available
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        self.bid_history = []
        self.utility_history = []
        self.price_history = []
        self.price_histogram = None  # Will be initialized in setup()
        
    def set_valuations(self, valuations):
        """Override to add debug output when valuations are set."""
        super().set_valuations(valuations)
        print(f"[DEBUG] {self.name}: valuations set to: {self.valuations}")
        
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
        
        print(f"[DEBUG] {self.name}: setup called with goods: {goods}, kth_price: {kth_price}")
        
        # Initialize histogram for price prediction
        self.price_histogram = IndependentHistogram(
            goods,
            bucket_sizes=[5 for _ in range(len(goods))],
            max_bids=[100 for _ in range(len(goods))]
        )
        
        print(f"[DEBUG] {self.name}: setup completed, goods: {self.goods}, valuations: {self.valuations}")

    def get_action(self, observation):
        """
        Advanced competition strategy that combines multiple approaches:
        1. Marginal value bidding with price prediction
        2. Adaptive bidding based on history
        3. Exploration vs exploitation
        """
        goods = observation.get("goods", set())
        
        print(f"[DEBUG] {self.name}: get_action called with goods: {goods}")
        print(f"[DEBUG] {self.name}: current valuations: {self.valuations}")
        print(f"[DEBUG] {self.name}: goods to index mapping: {self._goods_to_index}")
        
        if not goods:
            # This is a major issue - no goods available
            raise ValueError(f"[ERROR] {self.name}: No goods available in observation: {observation}")
        
        # Strategy 1: Marginal value bidding with price prediction
        if random.random() > self.exploration_rate and len(self.price_history) > 10:
            print(f"[DEBUG] {self.name}: Using learned price distribution for bidding")
            # Use learned price distribution for bidding
            bids = expected_local_bid(
                goods,
                self.calculate_valuation,  # Use the agent's internal valuation method
                self.price_histogram,
                num_iterations=50,
                num_samples=30
            )
        else:
            print(f"[DEBUG] {self.name}: Using adaptive bidding strategy")
            # Strategy 2: Adaptive bidding based on history
            bids = self._adaptive_bidding(goods)
        
        # Strategy 3: Add some randomness for exploration
        if random.random() < self.exploration_rate:
            print(f"[DEBUG] {self.name}: Adding exploration randomness")
            for good in bids:
                bids[good] *= random.uniform(0.8, 1.2)
        
        print(f"[DEBUG] {self.name}: Final bids: {bids}")
        return bids
    
    def _adaptive_bidding(self, goods):
        """
        Adaptive bidding strategy based on historical performance.
        """
        bids = {}
        
        for good in goods:
            # Calculate marginal value using the agent's internal valuation method
            value_with_good = self.calculate_valuation({good})
            value_without_good = self.calculate_valuation(set())
            marginal_value = value_with_good - value_without_good
            
            # Adjust bid based on historical performance
            if len(self.utility_history) > 0:
                recent_utility = sum(self.utility_history[-5:]) / min(5, len(self.utility_history))
                if recent_utility < 0:
                    # If losing money, bid more conservatively
                    bid_multiplier = 0.7
                elif recent_utility > 10:
                    # If doing well, bid more aggressively
                    bid_multiplier = 1.1
                else:
                    # Moderate bidding
                    bid_multiplier = 0.9
            else:
                bid_multiplier = 0.9
            
            bids[good] = marginal_value * bid_multiplier
        
        return bids

    def update(self, observation, action, reward, done, info):
        """Update the agent with the results of the last action."""
        super().update(observation, action, reward, done, info)
        
        print(f"[DEBUG] {self.name}: update called with reward: {reward}, done: {done}")
        print(f"[DEBUG] {self.name}: action taken: {action}")
        print(f"[DEBUG] {self.name}: info received: {info}")
        
        # Track utility history
        self.utility_history.append(reward)
        
        # Extract opponent bids from info to update price predictions
        if 'bids' in info:
            other_bids_raw = info['bids']
            other_bids = {player: bids for player, bids in other_bids_raw.items() if player != self.name}
            print(f"[DEBUG] {self.name}: other bids: {other_bids}")
            
            if other_bids:
                predicted_prices = {}
                for good in self.goods:
                    bids_for_good = [bids.get(good, 0) for bids in other_bids.values()]
                    if bids_for_good:
                        predicted_prices[good] = max(bids_for_good)
                    else:
                        predicted_prices[good] = 0
                
                if predicted_prices:
                    self.price_histogram.add_record(predicted_prices)
                    self.price_history.append(predicted_prices)
                    print(f"[DEBUG] {self.name}: predicted prices: {predicted_prices}")
        
        # Update exploration rate based on performance
        if len(self.utility_history) > 20:
            recent_performance = sum(self.utility_history[-10:]) / 10
            if recent_performance < 0:
                # Increase exploration if performing poorly
                self.exploration_rate = min(0.5, self.exploration_rate + 0.01)
            else:
                # Decrease exploration if performing well
                self.exploration_rate = max(0.05, self.exploration_rate - 0.005)

################### SUBMISSION #####################
# Create the agent submission with proper initialization
agent_submission = CompetitionAgent("Competition Agent")
# Ensure all required attributes are set
if not hasattr(agent_submission, 'exploration_rate'):
    agent_submission.exploration_rate = 0.2
if not hasattr(agent_submission, 'learning_rate'):
    agent_submission.learning_rate = 0.1
if not hasattr(agent_submission, 'bid_history'):
    agent_submission.bid_history = []
if not hasattr(agent_submission, 'utility_history'):
    agent_submission.utility_history = []
if not hasattr(agent_submission, 'price_history'):
    agent_submission.price_history = []
if not hasattr(agent_submission, 'price_histogram'):
    agent_submission.price_histogram = None
####################################################

if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    name = "CompetitionAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = CompetitionAgent(name)
            server_agent = create_adapter(agent, "auction")
            
            # Connect to server
            await connect_agent_to_server(server_agent, "auction", name, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Use the proper game infrastructure for local testing
        from core.game.AuctionGame import AuctionGame
        from core.engine import Engine
        from core.agents.lab07.random_agent import RandomAgent
        from core.agents.lab07.marginal_value_agent import MarginalValueAgent
        from core.agents.lab07.aggressive_agent import AggressiveAgent
        from core.agents.lab07.conservative_agent import ConservativeAgent
        
        # Create a simple test environment
        goods = {"A", "B", "C"}
        player_names = ["Competition", "Random", "MarginalValue", "Aggressive", "Conservative"]
        
        # Create agents - these work with the new system
        agents = [
            CompetitionAgent("Competition"),
            RandomAgent("Random", min_bid=1.0, max_bid=20.0),
            MarginalValueAgent("MarginalValue", bid_fraction=0.8),
            AggressiveAgent("Aggressive", bid_multiplier=1.5),
            ConservativeAgent("Conservative", bid_fraction=0.5),
        ]
        
        # Create game with internal valuation handling
        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=100,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )
        
        start = time.time()
        
        # Use the engine to run the game properly
        engine = Engine(game, agents, rounds=100)
        final_rewards = engine.run()
        
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
        
        # Print results
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
        
        print("Success! The new system handles valuations internally without exposing them in main.")
