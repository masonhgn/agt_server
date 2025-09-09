import sys
import os
import time
import random

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import expected_local_bid

class CompetitionAgent(BaseAuctionAgent):
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
        
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
        # TODO: Implement your competition strategy here
        # You can use any combination of:
        # - Marginal value calculation with price prediction
        # - Local bidding algorithm
        # - Best response strategies
        # - Game theory analysis
        # - Or any other approach you think will work well
        raise NotImplementedError("Implement your competition strategy")
    
    def _adaptive_bidding(self, goods):
        """
        Adaptive bidding strategy based on historical performance.
        """
        # TODO: Implement adaptive bidding based on historical performance
        # Consider:
        # - Recent utility performance
        # - Price prediction from histogram
        # - Marginal value calculations
        raise NotImplementedError("Implement adaptive bidding strategy")

    def update(self, observation, action, reward, done, info):
        """Update the agent with the results of the last action."""
        super().update(observation, action, reward, done, info)
        
        # TODO: Implement the update logic for learning
        # 1. Track utility history
        # 2. Extract opponent bids from info to update price predictions
        # 3. Update exploration rate based on performance
        raise NotImplementedError("Implement update method")

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
        
        engine = Engine(game, agents, rounds=100)
        final_rewards = engine.run()
        
        end = time.time()
        print(f"{end - start} SECONDS")
        
        # print results
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
        
