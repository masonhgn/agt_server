"""
Solution for Competition Agent implementation.
"""

import sys
import os
import time
import random

# Add parent directories to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import local_bid

class CompetitionAgent(BaseAuctionAgent):
    def setup(self, goods, valuation_function, kth_price=1):
        super().setup(goods, valuation_function, kth_price)
        
        # Competition agent parameters
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        self.bid_history = []
        self.utility_history = []
        self.price_history = []
        
        # Initialize histogram for price prediction
        self.price_histogram = IndependentHistogram(
            goods,
            bucket_sizes=[5 for _ in range(len(goods))],
            max_bids=[100 for _ in range(len(goods))]
        )

    def get_action(self, observation):
        """
        Advanced competition strategy that combines multiple approaches:
        1. Marginal value bidding with price prediction
        2. Adaptive bidding based on history
        3. Exploration vs exploitation
        """
        goods = observation.get("goods", set())
        valuation_function = observation.get("valuation_function", None)
        
        if not goods or not valuation_function:
            # Fallback strategy
            return {good: 10.0 for good in goods}
        
        # Strategy 1: Marginal value bidding with price prediction
        if random.random() > self.exploration_rate and len(self.price_history) > 10:
            # Use learned price distribution for bidding
            bids = local_bid(
                goods,
                valuation_function,
                self.price_histogram,
                num_iterations=50,
                num_samples=30
            )
        else:
            # Strategy 2: Adaptive bidding based on history
            bids = self._adaptive_bidding(goods, valuation_function)
        
        # Strategy 3: Add some randomness for exploration
        if random.random() < self.exploration_rate:
            for good in bids:
                bids[good] *= random.uniform(0.8, 1.2)
        
        return bids
    
    def _adaptive_bidding(self, goods, valuation_function):
        """
        Adaptive bidding strategy based on historical performance.
        """
        bids = {}
        
        for good in goods:
            # Calculate marginal value
            value_with_good = valuation_function({good})
            value_without_good = valuation_function(set())
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
        super().update(observation, action, reward, done, info)
        
        # Store history
        self.bid_history.append(action)
        self.utility_history.append(reward)
        
        # Update price prediction from opponent bids
        if 'bids' in info:
            other_bids_raw = info['bids']
            other_bids = {player: bids for player, bids in other_bids_raw.items() if player != self.name}
            
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
agent_submission = CompetitionAgent("Competition Agent")
####################################################

if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "CompetitionAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = CompetitionAgent(name)
            server_agent = create_adapter(agent, "auction")
            
            # Connect to server
            await connect_agent_to_server(server_agent, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Create a simple test environment
        from core.game.AuctionGame import AuctionGame
        from core.agents.lab07.random_agent import RandomAgent
        
        # Create realistic valuation functions
        def create_valuation_function(agent_name, valuation_type="complement"):
            def valuation_function(bundle):
                if not bundle:
                    return 0
                
                base_values = {"A": 20, "B": 25, "C": 30}
                random.seed(hash(agent_name) % 1000)
                adjusted_values = {good: base_values[good] + random.randint(-5, 5) for good in base_values}
                
                base_sum = sum(adjusted_values.get(good, 0) for good in bundle)
                n = len(bundle)
                
                if valuation_type == 'additive':
                    return base_sum
                elif valuation_type == 'complement':
                    return base_sum * (1 + 0.05 * (n - 1)) if n > 0 else 0
                elif valuation_type == 'substitute':
                    return base_sum * (1 - 0.05 * (n - 1)) if n > 0 else 0
                else:
                    return base_sum
            
            return valuation_function
        
        goods = {"A", "B", "C"}
        valuation_functions = {
            "Competition": create_valuation_function("Competition", "complement"),
            "Agent_1": create_valuation_function("Agent_1", "complement"),
            "Agent_2": create_valuation_function("Agent_2", "complement"),
            "Agent_3": create_valuation_function("Agent_3", "complement"),
            "Agent_4": create_valuation_function("Agent_4", "complement"),
            "Agent_5": create_valuation_function("Agent_5", "complement"),
            "Agent_6": create_valuation_function("Agent_6", "complement"),
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=100, kth_price=1)
        
        # Set up agents
        agent_submission.setup(goods, valuation_functions["Competition"], 1)
        agents = {
            "Agent_1": CompetitionAgent("Agent_1"),
            "Agent_2": CompetitionAgent("Agent_2"),
            "Agent_3": CompetitionAgent("Agent_3"),
            "Agent_4": CompetitionAgent("Agent_4"),
            "Agent_5": CompetitionAgent("Agent_5"),
            "Agent_6": CompetitionAgent("Agent_6"),
        }
        
        for name, agent in agents.items():
            agent.setup(goods, valuation_functions[name], 1)
        
        start = time.time()
        
        # Run test rounds
        for round_num in range(100):
            observation = {"goods": goods, "round": round_num}
            
            actions = {}
            actions["Competition"] = agent_submission.get_action(observation)
            for name, agent in agents.items():
                actions[name] = agent.get_action(observation)
            
            results = game.run_round(actions)
            
            agent_submission.update(observation, actions["Competition"], results["utilities"]["Competition"], False, results)
            for name, agent in agents.items():
                agent.update(observation, actions[name], results["utilities"][name], False, results)
        
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
