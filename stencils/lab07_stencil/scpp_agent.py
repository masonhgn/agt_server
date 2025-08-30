import pickle
import os
import sys
import time
import argparse
import random

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import local_bid

class SCPPAgent(BaseAuctionAgent):
    def setup(self, goods, kth_price=1):
        # NOTE: Many internal methods (e.g. self.get_valuations) aren't available during setup.
        # So we delay any setup that requires those until get_action() is called.
        
        super().setup(goods, kth_price)
        
        self.mode = 'TRAIN'
        
        self.simulation_count = 0
        self.NUM_ITERATIONS = 100
        self.NUM_SIMULATIONS_PER_ITERATION = 10
        self.ALPHA = 0.1
        self.NUM_ITERATIONS_LOCALBID = 100
        self.NUM_SAMPLES = 50
        self.BUCKET_SIZE = 5
        self.distribution_file = f"learned_distribution_{self.name}.pkl"

        self.learned_distribution = None
        self.curr_distribution = None

    def load_distribution(self):
        """
        Load the learned distribution from disk, if it exists.
        """
        # TODO: Implement distribution loading from disk
        raise NotImplementedError("Implement load_distribution method")

    def save_distribution(self):
        """
        Save the learned distribution to disk.
        """
        # TODO: Implement distribution saving to disk
        raise NotImplementedError("Implement save_distribution method")
            
    def create_independent_histogram(self):
        # TODO: Create and return an IndependentHistogram instance
        # Use self.BUCKET_SIZE and appropriate max_bids values
        raise NotImplementedError("Implement create_independent_histogram method")

    def initialize_distribution(self):
        """
        Initialize the learned distribution using the goods and default parameters.
        We assume bucket sizes of 5 and max values of 100 per good.
        """
        # TODO: Initialize self.learned_distribution and self.curr_distribution
        raise NotImplementedError("Implement initialize_distribution method")
    
    def get_action(self, observation):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        In RUN mode, load the distribution from disk.
        In TRAIN mode, initialize a new distribution if needed.
        """
        # TODO: Implement the main action logic
        # 1. Handle RUN vs TRAIN mode
        # 2. Call get_bids() to get the actual bids
        raise NotImplementedError("Implement get_action method")
    
    def get_bids(self):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        """
        # TODO: Use local_bid with the learned distribution
        # The valuation function is now accessed through self.calculate_valuation
        raise NotImplementedError("Implement get_bids method")

    def update(self, observation, action, reward, done, info):
        """Update the agent with the results of the last action."""
        super().update(observation, action, reward, done, info)
        
        # TODO: Implement the update logic for learning
        # 1. Extract opponent bids from info
        # 2. Update price predictions
        # 3. Update the learned distribution periodically
        raise NotImplementedError("Implement update method")


################### SUBMISSION #####################
agent_submission = SCPPAgent("SCPP Agent")
####################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SCPP Agent')
    parser.add_argument('--mode', type=str, default='TRAIN', choices=['TRAIN', 'RUN'],
                        help='Mode: TRAIN or RUN (default: TRAIN)')
    parser.add_argument('--num_rounds', type=int, default=100,
                        help='Number of rounds (default: 100)')

    args = parser.parse_args()
    agent_submission.mode = args.mode
    print(f"Running in {agent_submission.mode} mode")

    if args.mode == "TRAIN":
        # Training mode - self-play (SCPP agents against each other)
        # Use the proper game infrastructure instead of manual testing
        from core.game.AuctionGame import AuctionGame
        from core.engine import Engine
        from core.agents.lab07.random_agent import RandomAgent
        from core.agents.lab07.marginal_value_agent import MarginalValueAgent
        
        # Create a simple test environment
        goods = {"A", "B", "C"}
        player_names = ["SCPP_1", "SCPP_2", "SCPP_3", "Random"]
        
        # Create agents for training
        agents = [
            SCPPAgent("SCPP_1"),
            SCPPAgent("SCPP_2"),
            SCPPAgent("SCPP_3"),
            RandomAgent("Random", min_bid=1.0, max_bid=20.0),
        ]
        
        # Set all agents to training mode
        for agent in agents:
            if hasattr(agent, 'mode'):
                agent.mode = 'TRAIN'
        
        # Create game with internal valuation handling
        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=args.num_rounds,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )
        
        start = time.time()
        
        # Use the engine to run the game properly
        engine = Engine(game, agents, rounds=args.num_rounds)
        final_rewards = engine.run()
        
        end = time.time()
        print(f"Training completed in {end - start} seconds")
        print("Learned distribution saved to disk")
        
        # Print results
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
        
    else:  # RUN mode
        # Test mode - compete against variety of agents
        from core.game.AuctionGame import AuctionGame
        from core.engine import Engine
        from core.agents.lab07.random_agent import RandomAgent
        from core.agents.lab07.marginal_value_agent import MarginalValueAgent
        from core.agents.lab07.aggressive_agent import AggressiveAgent
        from core.agents.lab07.conservative_agent import ConservativeAgent
        
        # Create a simple test environment
        goods = {"A", "B", "C"}
        player_names = ["SCPP", "MarginalValue", "Random", "Aggressive", "Conservative"]
        
        # Create agents for testing
        agents = [
            SCPPAgent("SCPP"),
            MarginalValueAgent("MarginalValue", bid_fraction=0.8),
            RandomAgent("Random", min_bid=1.0, max_bid=20.0),
            AggressiveAgent("Aggressive", bid_multiplier=1.5),
            ConservativeAgent("Conservative", bid_fraction=0.5),
        ]
        
        # Set all agents to run mode
        for agent in agents:
            if hasattr(agent, 'mode'):
                agent.mode = 'RUN'
        
        # Create game with internal valuation handling
        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=500,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )
        
        start = time.time()
        
        # Use the engine to run the game properly
        engine = Engine(game, agents, rounds=500)
        final_rewards = engine.run()
        
        end = time.time()
        print(f"Testing completed in {end - start} seconds")
        
        # Print results
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
        
        