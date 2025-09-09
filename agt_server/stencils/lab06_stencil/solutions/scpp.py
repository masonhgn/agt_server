"""
Solution for SCPP Agent implementation.
"""

import pickle
import os
import sys
import time
import argparse
import random


TRAINING_ROUNDS = 1000  # umber of rounds for training games
TESTING_ROUNDS = 100   # number of rounds for testing games

# Add parent directories to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from local_bid import local_bid

class SCPPAgent(BaseAuctionAgent):
    def setup(self, goods, kth_price=1):
        super().setup(goods, kth_price)
        
        self.mode = 'TRAIN'
        
        self.simulation_count = 0
        # Local bid algorithm parameters
        self.NUM_ITERATIONS_LOCALBID = 100  # Number of iterations for local bid optimization
        self.NUM_SAMPLES = 50              # Number of samples for marginal value estimation
        
        # Distribution learning parameters
        self.NUM_SIMULATIONS_PER_ITERATION = 100  # Update distribution every N simulations
        self.ALPHA = 0.1                          # Learning rate for distribution updates
        self.BUCKET_SIZE = 5                      # Histogram bucket size

        self.price_file = f"learned_price_{self.name}.pkl"

        self.learned_prices = None  # persistent point estimate
        self.curr_obs = []   


    def load_prices(self):
        if os.path.exists(self.price_file):
            with open(self.price_file, "rb") as f:
                self.learned_prices = pickle.load(f)
        else:
            self.initialize_prices()

    def save_prices(self):
        with open(self.price_file, "wb") as f:
            pickle.dump(self.learned_prices, f)

    def initialize_prices(self):
        # start with all-zero prices
        self.learned_prices = {g: 0.0 for g in self.goods}

    def get_action(self):
            self.valuation_function = self.calculate_valuation
            self.load_prices()
            return self.get_bids()
    
    def get_bids(self):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        """
        # Use local_bid with the learned distribution
        # The valuation function is now accessed through self.calculate_valuation
        
        bids = local_bid(
            self.goods,
            self.valuation_function,
            self.learned_prices,
            num_iterations=self.num_iterations_localbid,
        )
        return bids

    def update(self, observation, action, reward, done, info):
        #print('update called')
        """Update the agent with the results of the last action."""
        super().update(observation, action, reward, done, info)
        
        # Extract opponent bids from info
        if 'bids' in info:
            other_bids_raw = info['bids']
            # Remove our own bids to get opponent bids
            other_bids = {player: bids for player, bids in other_bids_raw.items() if player != self.name}
            #print(other_bids_raw)
            predicted_prices = {}
            
            for good in self.goods:
                # Get the highest bid for each good (excluding our own)
                bids_for_good = [bids.get(good, 0) for bids in other_bids.values()]
                if bids_for_good:
                    predicted_prices[good] = max(bids_for_good)
                else:
                    predicted_prices[good] = 0
            
            # Insert prices into self.curr_distribution (ONCE, outside the loop)
            self.curr_distribution.add_record(predicted_prices)
            self.simulation_count += 1
            
            if self.simulation_count % self.NUM_SIMULATIONS_PER_ITERATION == 0:
                # Update the learned distribution with the newly gathered data
                self.learned_distribution.update(self.curr_distribution, self.ALPHA)
                # Reset the current distribution
                self.curr_distribution = self.create_independent_histogram()
                # Save the learned distribution to disk (for use in live auction mode)
                self.save_distribution()


################### SUBMISSION #####################
agent_submission = SCPPAgent("SCPP Agent")
####################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SCPP Agent')
    parser.add_argument('--mode', type=str, default='TRAIN', choices=['TRAIN', 'RUN'],
                        help='Mode: TRAIN or RUN (default: TRAIN)')

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
        player_names = ["SCPP", "SCPP_1", "SCPP_2", "SCPP_3"]
        
        # Create agents for training
        agents = [
            agent_submission,
            SCPPAgent("SCPP_1"),
            SCPPAgent("SCPP_2"),
            SCPPAgent("SCPP_3"),
        ]
        
        # Set all agents to training mode
        for agent in agents:
            if hasattr(agent, 'mode'):
                agent.mode = 'TRAIN'
        
        # Create game with internal valuation handling
        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=TRAINING_ROUNDS,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )
        
        start = time.time()
        
        # Use the engine to run the game properly
        engine = Engine(game, agents, rounds=TRAINING_ROUNDS)
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
            num_rounds=TESTING_ROUNDS,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )
        
        start = time.time()
        
        # Use the engine to run the game properly
        engine = Engine(game, agents, rounds=TESTING_ROUNDS)
        final_rewards = engine.run()
        
        end = time.time()
        print(f"Testing completed in {end - start} seconds")
        
        # Print results
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
        

