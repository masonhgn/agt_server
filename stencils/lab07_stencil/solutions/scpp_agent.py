import pickle
import os
import sys
import time
import argparse
import random

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..','..','..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import expected_local_bid

class SCPPAgent(BaseAuctionAgent):
    def setup(self, goods, valuation_function, kth_price=1):
        # NOTE: Many internal methods (e.g. self.get_valuations) aren't available during setup.
        # So we delay any setup that requires those until get_action() is called.
        
        super().setup(goods, valuation_function, kth_price)
        
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
        if os.path.exists(self.distribution_file):
            with open(self.distribution_file, "rb") as f:
                self.learned_distribution = pickle.load(f)
            self.curr_distribution = self.create_independent_histogram()
        else:
            self.initialize_distribution()

    def save_distribution(self):
        """
        Save the learned distribution to disk.
        """
        with open(self.distribution_file, "wb") as f:
            pickle.dump(self.learned_distribution, f)
            
    def create_independent_histogram(self):
        return IndependentHistogram(
            self.goods,
            bucket_sizes=[self.BUCKET_SIZE for _ in range(len(self.goods))],
            max_bids=[100 for _ in range(len(self.goods))]  # Assuming max bid of 100
        )

    def initialize_distribution(self):
        """
        Initialize the learned distribution using the goods and default parameters.
        We assume bucket sizes of 5 and max values of 100 per good.
        """
        self.learned_distribution = self.create_independent_histogram()
        self.curr_distribution = self.learned_distribution.copy()
    
    def get_action(self, observation):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        In RUN mode, load the distribution from disk.
        In TRAIN mode, initialize a new distribution if needed.
        """
        self.load_distribution()

        return self.get_bids()
    
    def get_bids(self):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        """
        # TODO: Implement get_bids method
        # Use expected_local_bid with the learned distribution
        raise NotImplementedError("Implement get_bids method")

    def update(self, observation, action, reward, done, info):
        """Update the agent with the results of the last action."""
        super().update(observation, action, reward, done, info)
        
        # Extract opponent bids from info
        if 'bids' in info:
            other_bids_raw = info['bids']
            # Remove our own bids to get opponent bids
            other_bids = {player: bids for player, bids in other_bids_raw.items() if player != self.name}
            
            predicted_prices = {}
            
            for good in self.goods:
                # Get the highest bid for each good (excluding our own)
                bids_for_good = [bids.get(good, 0) for bids in other_bids.values()]
                if bids_for_good:
                    predicted_prices[good] = max(bids_for_good)
                else:
                    predicted_prices[good] = 0
            
            if predicted_prices:
                # TODO: insert prices into self.curr_distribution
                # TODO: update simulation_count
                raise NotImplementedError("Implement price insertion and simulation count update")
                
                if self.simulation_count % self.NUM_SIMULATIONS_PER_ITERATION == 0:
                    # TODO: Update the learned distribution with the newly gathered data
                    # TODO: Reset the current distribution
                    # TODO: Save the learned distribution to disk (for use in live auction mode)
                    raise NotImplementedError("Implement distribution update and save")


################### SUBMISSION #####################
agent_submission = SCPPAgent("SCPP Agent")
####################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SCPP Agent')
    parser.add_argument('--join_server', action='store_true',
                        help='Connects the agent to the server')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')
    parser.add_argument('--mode', type=str, default='TRAIN',
                        help='Mode: TRAIN or RUN (default: TRAIN)')
    parser.add_argument('--num_rounds', type=int, default=100,
                        help='Number of rounds (default: 100)')

    args = parser.parse_args()
    agent_submission.mode = args.mode
    print(agent_submission.mode)

    if args.join_server:
        print("Server mode not implemented in this version")
    elif args.mode == "TRAIN":
        # TODO: Check for bias
        VALUE_UPPER_BOUND = 100
        VALUE_LOWER_BOUND = 0
        
        # Create a simple training environment
        from core.game.AuctionGame import AuctionGame
        #from core.agents.test_auction_agents import RandomAuctionAgent, TruthfulAuctionAgent
        
        def valuation_function(bundle):
            return sum(10 for item in bundle)
        
        goods = {"A", "B", "C"}
        valuation_functions = {
            "SCPP": valuation_function,
            "Agent_1": valuation_function,
            "Agent_2": valuation_function,
            "Agent_3": valuation_function,
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=args.num_rounds, kth_price=2)
        
        # Set up agents
        agent_submission.setup(goods, valuation_function, 2)
        agents = {
            "Agent_1": SCPPAgent("Agent_1"),
            "Agent_2": SCPPAgent("Agent_2"),
            "Agent_3": SCPPAgent("Agent_3"),
        }
        
        for agent in agents.values():
            agent.setup(goods, valuation_function, 2)
        
        start = time.time()
        
        # Run training rounds
        for round_num in range(args.num_rounds):
            observation = {"goods": goods, "round": round_num}
            
            # Get actions from all agents
            actions = {}
            actions["SCPP"] = agent_submission.get_action(observation)
            for name, agent in agents.items():
                actions[name] = agent.get_action(observation)
            
            # Run round
            results = game.run_round(actions)
            
            # Update agents
            agent_submission.update(observation, actions["SCPP"], results["utilities"]["SCPP"], False, results)
            for name, agent in agents.items():
                agent.update(observation, actions[name], results["utilities"][name], False, results)
        
        end = time.time()
        print(f"{end - start} Seconds Elapsed")
    else:
        # Test mode
        from core.game.AuctionGame import AuctionGame
        from core.agents.test_auction_agents import TruthfulAuctionAgent
        
        def valuation_function(bundle):
            return sum(10 for item in bundle)
        
        goods = {"A", "B", "C"}
        valuation_functions = {
            "SCPP": valuation_function,
            "Agent_1": valuation_function,
            "Agent_2": valuation_function,
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=500, kth_price=2)
        
        # Set up agents
        agent_submission.setup(goods, valuation_function, 2)
        agents = {
            "Agent_1": TruthfulAuctionAgent("Agent_1"),
            "Agent_2": TruthfulAuctionAgent("Agent_2"),
        }
        
        for agent in agents.values():
            agent.setup(goods, valuation_function, 2)
        
        start = time.time()
        
        # Run test rounds
        for round_num in range(500):
            observation = {"goods": goods, "round": round_num}
            
            # Get actions from all agents
            actions = {}
            actions["SCPP"] = agent_submission.get_action(observation)
            for name, agent in agents.items():
                actions[name] = agent.get_action(observation)
            
            # Run round
            results = game.run_round(actions)
            
            # Update agents
            agent_submission.update(observation, actions["SCPP"], results["utilities"]["SCPP"], False, results)
            for name, agent in agents.items():
                agent.update(observation, actions[name], results["utilities"][name], False, results)
        
        end = time.time()
        print(f"{end - start} Seconds Elapsed") 