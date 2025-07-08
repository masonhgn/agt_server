#!/usr/bin/env python3
"""
Comprehensive tests for Lab 6: Simultaneous Auctions

This script tests the auction game implementation, agents, and integration.
"""

from core.game.AuctionGame import AuctionGame
from tests.test_auction_agents import (
    RandomAuctionAgent, TruthfulAuctionAgent, OverBidderAuctionAgent,
    FPAuctionAgent, ZeroBidAuctionAgent
)
from stencils.lab06_stencil.sample_valuations import SampleValuations
import unittest

class TestAuctionGame(unittest.TestCase):
    """Test the auction game implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.goods = {"A", "B", "C"}
        
        def valuation1(bundle):
            return sum(10 for item in bundle)
        
        def valuation2(bundle):
            return sum(15 for item in bundle)
        
        self.valuation_functions = {
            "player1": valuation1,
            "player2": valuation2
        }
        
        self.game = AuctionGame(self.goods, self.valuation_functions, num_rounds=5)
    
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        self.assertEqual(self.game.goods, self.goods)
        self.assertEqual(self.game.valuation_functions, self.valuation_functions)
        self.assertEqual(self.game.kth_price, 1)
        self.assertEqual(self.game.num_players(), 2)
    
    def test_marginal_value_calculation(self):
        """Test marginal value calculation."""
        bids = {"A": 5.0, "B": 8.0, "C": 3.0}
        prices = {"A": 4.0, "B": 6.0, "C": 2.0}
        
        # Player would win A and C with these bids
        mv_a = self.game.calculate_marginal_value(
            self.goods, "A", self.valuation_functions["player1"], bids, prices
        )
        
        # Value with A: 20 (A, C), Value without A: 10 (C), Marginal value: 10
        self.assertEqual(mv_a, 10)
    
    def test_auction_result_computation(self):
        """Test auction result computation."""
        bids = {
            "player1": {"A": 10.0, "B": 5.0, "C": 8.0},
            "player2": {"A": 8.0, "B": 12.0, "C": 6.0}
        }
        
        allocation, payments, prices = self.game.compute_auction_result(bids)
        
        # Player1 should win A and C, Player2 should win B
        self.assertEqual(allocation["A"], "player1")
        self.assertEqual(allocation["B"], "player2")
        self.assertEqual(allocation["C"], "player1")
        
        # Check payments
        self.assertEqual(payments["player1"], 10.0 + 8.0)  # A + C
        self.assertEqual(payments["player2"], 12.0)      # B
    
    def test_utility_calculation(self):
        """Test utility calculation."""
        allocation = {"A": "player1", "B": "player2", "C": "player1"}
        payments = {"player1": 18.0, "player2": 12.0}
        
        utilities = self.game.calculate_utilities(
            allocation, payments, self.valuation_functions
        )
        
        # Player1: value(A,C) = 20, payment = 18, utility = 2
        # Player2: value(B) = 15, payment = 12, utility = 3
        self.assertEqual(utilities["player1"], 2)
        self.assertEqual(utilities["player2"], 3)
    
    def test_game_round(self):
        """Test running a single game round."""
        actions = {
            "player1": {"A": 10.0, "B": 5.0, "C": 8.0},
            "player2": {"A": 8.0, "B": 12.0, "C": 6.0}
        }
        
        results = self.game.run_round(actions)
        
        self.assertIn("allocation", results)
        self.assertIn("payments", results)
        self.assertIn("prices", results)
        self.assertIn("utilities", results)
        self.assertIn("bids", results)
        
        # Check that history was updated
        self.assertEqual(len(self.game.bid_history), 1)
        self.assertEqual(len(self.game.allocation_history), 1)
        self.assertEqual(len(self.game.payment_history), 1)
        self.assertEqual(len(self.game.price_history), 1)
        self.assertEqual(len(self.game.utility_history), 1)


class TestAuctionAgents(unittest.TestCase):
    """Test the auction agents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.goods = {"A", "B", "C"}
        
        def valuation(bundle):
            return sum(10 for item in bundle)
        
        self.valuation_function = valuation
        self.observation = {
            "goods": self.goods,
            "valuation_function": self.valuation_function,
            "kth_price": 1,
            "round": 1
        }
    
    def test_random_agent(self):
        """Test the random auction agent."""
        agent = RandomAuctionAgent("RandomAgent")
        agent.setup(self.goods, self.valuation_function)
        
        action = agent.get_action(self.observation)
        
        self.assertIsInstance(action, dict)
        self.assertEqual(set(action.keys()), self.goods)
        
        # Check that bids are within reasonable range
        for good, bid in action.items():
            self.assertGreaterEqual(bid, 0)
            self.assertLessEqual(bid, 10)  # Max single item value
    
    def test_truthful_agent(self):
        """Test the truthful auction agent."""
        agent = TruthfulAuctionAgent("TruthfulAgent")
        agent.setup(self.goods, self.valuation_function)
        
        action = agent.get_action(self.observation)
        
        self.assertIsInstance(action, dict)
        self.assertEqual(set(action.keys()), self.goods)
        
        # Check that bids equal single item values
        for good, bid in action.items():
            self.assertEqual(bid, 10)  # Single item value
    
    def test_zero_bid_agent(self):
        """Test the zero bid agent."""
        agent = ZeroBidAuctionAgent("ZeroAgent")
        agent.setup(self.goods, self.valuation_function)
        
        action = agent.get_action(self.observation)
        
        self.assertIsInstance(action, dict)
        self.assertEqual(set(action.keys()), self.goods)
        
        # Check that all bids are zero
        for good, bid in action.items():
            self.assertEqual(bid, 0.0)
    
    def test_agent_update(self):
        """Test agent update functionality."""
        agent = TruthfulAuctionAgent("TestAgent")
        agent.setup(self.goods, self.valuation_function)
        
        action = {"A": 10.0, "B": 10.0, "C": 10.0}
        reward = 5.0
        info = {"allocation": {"A": "TestAgent"}, "prices": {"A": 8.0}}
        
        agent.update(self.observation, action, reward, done=False, info=info)
        
        self.assertEqual(len(agent.bid_history), 1)
        self.assertEqual(agent.bid_history[0], action)
        self.assertEqual(len(agent.utility_history), 1)
        self.assertEqual(agent.utility_history[0], reward)


class TestIntegration(unittest.TestCase):
    """Test integration between game and agents."""
    
    def test_game_with_agents(self):
        """Test running a game with multiple agents."""
        goods = {"A", "B"}
        
        def valuation1(bundle):
            return sum(10 for item in bundle)
        
        def valuation2(bundle):
            return sum(15 for item in bundle)
        
        # Create agents
        agent1 = TruthfulAuctionAgent("Agent1")
        agent2 = RandomAuctionAgent("Agent2")
        
        agent1.setup(goods, valuation1)
        agent2.setup(goods, valuation2)
        
        # Create game
        valuation_functions = {"Agent1": valuation1, "Agent2": valuation2}
        game = AuctionGame(goods, valuation_functions, num_rounds=3)
        
        # Run a few rounds
        for round_num in range(3):
            observation = {
                "goods": goods,
                "round": round_num
            }
            
            # Get actions from agents
            action1 = agent1.get_action(observation)
            action2 = agent2.get_action(observation)
            
            actions = {"Agent1": action1, "Agent2": action2}
            
            # Run round
            results = game.run_round(actions)
            
            # Update agents
            agent1.update(observation, action1, results["utilities"]["Agent1"], False, results)
            agent2.update(observation, action2, results["utilities"]["Agent2"], False, results)
        
        # Check that game history was recorded
        self.assertEqual(len(game.bid_history), 3)
        self.assertEqual(len(game.allocation_history), 3)
        self.assertEqual(len(game.utility_history), 3)


def run_comprehensive_tests():
    """Run all comprehensive tests."""
    print("Running comprehensive tests for Lab 6...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAuctionGame))
    suite.addTests(loader.loadTestsFromTestCase(TestAuctionAgents))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1) 