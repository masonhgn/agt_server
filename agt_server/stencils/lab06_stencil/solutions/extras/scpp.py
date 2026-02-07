"""
solution for scpp agent implementation.

uses local_bid with learned price estimates from opponent bid history.
"""

import pickle
import os
import sys
import time
import argparse

TRAINING_ROUNDS = 1000
TESTING_ROUNDS = 100

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from local_bid import local_bid


class SCPPAgent(BaseAuctionAgent):
    def setup(self, goods=None, kth_price=1):
        super().setup(goods, kth_price)
        if goods is None:
            return

        self.mode = 'TRAIN'
        self.simulation_count = 0
        self.NUM_ITERATIONS_LOCALBID = 100
        self.ALPHA = 0.1

        self.price_file = f"learned_price_{self.name}.pkl"
        self.learned_prices = None

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
        self.learned_prices = {g: 0.0 for g in self.goods}

    def get_action(self, observation=None):
        self.load_prices()
        return self.get_bids()

    def get_bids(self):
        """compute bid vector using local_bid with learned price estimates."""
        bids = local_bid(
            self.goods,
            self.calculate_valuation,
            self.learned_prices,
            num_iterations=self.NUM_ITERATIONS_LOCALBID,
        )
        return bids

    def update(self, observation, action, reward, done, info):
        """update learned prices from opponent bid history."""
        super().update(observation, action, reward, done, info)

        if 'bids' not in info:
            return

        other_bids_raw = info['bids']
        other_bids = {player: bids for player, bids in other_bids_raw.items() if player != self.name}

        if not other_bids:
            return

        # estimate clearing prices as max opponent bid per good
        observed_prices = {}
        for good in self.goods:
            bids_for_good = [bids.get(good, 0) for bids in other_bids.values()]
            observed_prices[good] = max(bids_for_good) if bids_for_good else 0

        # exponential moving average update
        if self.learned_prices is None:
            self.initialize_prices()

        for good in self.goods:
            self.learned_prices[good] = (
                (1 - self.ALPHA) * self.learned_prices[good]
                + self.ALPHA * observed_prices[good]
            )

        self.simulation_count += 1
        # periodically save to disk
        if self.simulation_count % 100 == 0:
            self.save_prices()


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
        from core.game.AuctionGame import AuctionGame
        from core.engine import Engine

        goods = {"A", "B", "C"}
        player_names = ["SCPP", "SCPP_1", "SCPP_2", "SCPP_3"]

        agents = [
            agent_submission,
            SCPPAgent("SCPP_1"),
            SCPPAgent("SCPP_2"),
            SCPPAgent("SCPP_3"),
        ]
        for agent in agents:
            if hasattr(agent, 'mode'):
                agent.mode = 'TRAIN'

        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=TRAINING_ROUNDS,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )

        start = time.time()
        engine = Engine(game, agents, rounds=TRAINING_ROUNDS)
        final_rewards = engine.run()

        print(f"Training completed in {time.time() - start:.1f} seconds")
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")

    else:
        from core.game.AuctionGame import AuctionGame
        from core.engine import Engine
        from core.agents.lab07.random_agent import RandomAgent
        from core.agents.lab07.marginal_value_agent import MarginalValueAgent
        from core.agents.lab07.aggressive_agent import AggressiveAgent
        from core.agents.lab07.conservative_agent import ConservativeAgent

        goods = {"A", "B", "C"}
        player_names = ["SCPP", "MarginalValue", "Random", "Aggressive", "Conservative"]

        agents = [
            SCPPAgent("SCPP"),
            MarginalValueAgent("MarginalValue", bid_fraction=0.8),
            RandomAgent("Random", min_bid=1.0, max_bid=20.0),
            AggressiveAgent("Aggressive", bid_multiplier=1.5),
            ConservativeAgent("Conservative", bid_fraction=0.5),
        ]
        for agent in agents:
            if hasattr(agent, 'mode'):
                agent.mode = 'RUN'

        game = AuctionGame(
            goods=goods,
            player_names=player_names,
            num_rounds=TESTING_ROUNDS,
            kth_price=1,
            valuation_type="additive",
            value_range=(10, 50)
        )

        start = time.time()
        engine = Engine(game, agents, rounds=TESTING_ROUNDS)
        final_rewards = engine.run()

        print(f"Testing completed in {time.time() - start:.1f} seconds")
        for i, agent in enumerate(agents):
            print(f"{agent.name}: {final_rewards[i]:.2f}")
