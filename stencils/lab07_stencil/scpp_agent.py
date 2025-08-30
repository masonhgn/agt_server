import pickle
import os
import sys
import time
import argparse
import random

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.base_auction_agent import BaseAuctionAgent
from independent_histogram import IndependentHistogram
from local_bid import local_bid

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
        if self.mode == 'RUN':
            self.load_distribution()
        else:  # TRAIN mode
            if self.learned_distribution is None:
                self.initialize_distribution()

        return self.get_bids()
    
    def get_bids(self):
        """
        Compute and return a bid vector by running the LocalBid routine with expected marginal values.
        """
        # Use local_bid with the learned distribution
        return local_bid(
            self.goods,
            self.valuation_function,
            self.learned_distribution,
            self.NUM_ITERATIONS_LOCALBID,
            self.NUM_SAMPLES
        )

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
                # Insert prices into self.curr_distribution
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
    parser.add_argument('--num_rounds', type=int, default=100,
                        help='Number of rounds (default: 100)')

    args = parser.parse_args()
    agent_submission.mode = args.mode
    print(f"Running in {agent_submission.mode} mode")

    if args.mode == "TRAIN":
        # Training mode - self-play (SCPP agents against each other)
        from core.game.AuctionGame import AuctionGame
        
        # Create realistic valuation functions that simulate the original game
        def create_valuation_function(agent_name, valuation_type="complement"):
            """Create a valuation function that matches the original game's behavior."""
            def valuation_function(bundle):
                if not bundle:
                    return 0
                
                # Simulate individual good valuations (in real game these are random per round)
                # For training, we'll use deterministic but realistic values
                # In the real game, these would be randomly generated each round
                base_values = {"A": 20, "B": 25, "C": 30}
                
                # Add some randomness to simulate the original game's random valuations
                random.seed(hash(agent_name) % 1000)  # Deterministic per agent
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
        
        # Create different valuation functions for each agent to simulate the original game
        valuation_functions = {
            "SCPP": create_valuation_function("SCPP", "complement"),
            "Agent_1": create_valuation_function("Agent_1", "complement"),
            "Agent_2": create_valuation_function("Agent_2", "complement"),
            "Agent_3": create_valuation_function("Agent_3", "complement"),
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=args.num_rounds, kth_price=2)
        
        # Set up agents - in training mode, use self-play (SCPP agents against each other)
        agent_submission.setup(goods, valuation_functions["SCPP"], 2)
        agents = {
            "Agent_1": SCPPAgent("Agent_1"),
            "Agent_2": SCPPAgent("Agent_2"),
            "Agent_3": SCPPAgent("Agent_3"),
        }
        
        for name, agent in agents.items():
            agent.setup(goods, valuation_functions[name], 2)
            agent.mode = 'TRAIN'  # All agents in training mode
        
        start = time.time()
        
        # Run training rounds
        for round_num in range(args.num_rounds):
            # Create observation with the agent's specific valuation function
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
        print(f"Training completed in {end - start} seconds")
        print("Learned distribution saved to disk")
        
    else:  # RUN mode
        # Test mode - compete against variety of agents
        from core.game.AuctionGame import AuctionGame
        from core.agents.lab07.marginal_value_agent import MarginalValueAgent
        from core.agents.lab07.random_agent import RandomAgent
        from core.agents.lab07.aggressive_agent import AggressiveAgent
        from core.agents.lab07.conservative_agent import ConservativeAgent
        
        # Create realistic valuation functions for the test scenario
        def create_valuation_function(agent_name, valuation_type="complement"):
            """Create a valuation function that matches the original game's behavior."""
            def valuation_function(bundle):
                if not bundle:
                    return 0
                
                # Simulate individual good valuations (in real game these are random per round)
                # For testing, we'll use deterministic but realistic values
                base_values = {"A": 20, "B": 25, "C": 30}
                
                # Add some randomness to simulate the original game's random valuations
                random.seed(hash(agent_name) % 1000)  # Deterministic per agent
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
        
        # Create different valuation functions for each agent
        valuation_functions = {
            "SCPP": create_valuation_function("SCPP", "complement"),
            "MarginalValue": create_valuation_function("MarginalValue", "complement"),
            "Random": create_valuation_function("Random", "complement"),
            "Aggressive": create_valuation_function("Aggressive", "complement"),
            "Conservative": create_valuation_function("Conservative", "complement"),
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=500, kth_price=2)
        
        # Set up agents - in RUN mode, use variety of different agents
        agent_submission.setup(goods, valuation_functions["SCPP"], 2)
        agents = {
            "MarginalValue": MarginalValueAgent("MarginalValue", bid_fraction=0.8),
            "Random": RandomAgent("Random", min_bid=1.0, max_bid=20.0),
            "Aggressive": AggressiveAgent("Aggressive", bid_multiplier=1.5),
            "Conservative": ConservativeAgent("Conservative", bid_fraction=0.5),
        }
        
        for name, agent in agents.items():
            agent.setup(goods, valuation_functions[name], 2)
        
        start = time.time()
        
        # Run test rounds
        for round_num in range(500):
            # Create observation with the agent's specific valuation function
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
        print(f"Testing completed in {end - start} seconds") 