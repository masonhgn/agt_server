#!/usr/bin/env python3
"""
Student-style tests for Lab 6: Simultaneous Auctions

This test file simulates what a student would implement and test for Lab 6,
including marginal value calculations, local bidding optimization, and auction game mechanics.
"""

import unittest
import sys
import os
import random
from typing import Dict, Set, Callable, Any

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AuctionGame import AuctionGame
from core.agents.lab06.base_auction_agent import BaseAuctionAgent
from stencils.lab06_stencil.sample_valuations import SampleValuations


class StudentMarginalValueAgent(BaseAuctionAgent):
    """
    Student implementation of an agent that uses marginal value calculations.
    This simulates what a student might implement for Lab 6.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.learning_rate = 0.1
        self.exploration_rate = 0.2
        
    def calculate_marginal_value(self, goods: Set[str], selected_good: str, 
                               bids: Dict[str, float], prices: Dict[str, float]) -> float:
        """
        Student implementation of marginal value calculation.
        This is what they would implement in marginal_value.py
        """
        # Determine which goods the bidder would win with current bids
        won_goods = set()
        for good in goods:
            if bids.get(good, 0) >= prices.get(good, 0):
                won_goods.add(good)
        
        # Calculate value with the selected good
        bundle_with_good = won_goods | {selected_good}
        value_with_good = self.valuation_function(bundle_with_good)
        
        # Calculate value without the selected good
        bundle_without_good = won_goods - {selected_good}
        value_without_good = self.valuation_function(bundle_without_good)
        
        # Marginal value is the difference
        marginal_value = value_with_good - value_without_good
        
        return marginal_value
    
    def local_bid_optimization(self, goods: Set[str], prices: Dict[str, float], 
                             num_iterations: int = 50) -> Dict[str, float]:
        """
        Student implementation of local bidding optimization.
        This is what they would implement in localbid.py
        """
        # Initialize bids to zero
        bids = {good: 0.0 for good in goods}
        
        for iteration in range(num_iterations):
            old_bids = bids.copy()
            
            # Update each good's bid to its marginal value
            for good in goods:
                marginal_value = self.calculate_marginal_value(goods, good, bids, prices)
                bids[good] = marginal_value
            
            # Check for convergence (optional)
            if iteration > 0:
                max_change = max(abs(bids[good] - old_bids[good]) for good in goods)
                if max_change < 0.01:  # Small threshold for convergence
                    break
        
        return bids
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """
        Get bids using local bidding optimization with some exploration.
        """
        # Generate price vector if not provided
        if 'prices' not in observation:
            prices = SampleValuations.generate_price_vector()
        else:
            prices = observation['prices']
        
        # Use local bidding optimization
        optimal_bids = self.local_bid_optimization(self.goods, prices)
        
        # Add some exploration
        if random.random() < self.exploration_rate:
            # Randomly adjust some bids
            for good in self.goods:
                if random.random() < 0.3:  # 30% chance to adjust each bid
                    adjustment = random.uniform(-0.1, 0.1) * optimal_bids[good]
                    optimal_bids[good] = max(0, optimal_bids[good] + adjustment)
        
        return optimal_bids
    
    def update(self, observation: Dict[str, Any], action: Dict[str, float], 
               reward: float, done: bool, info: Dict[str, Any]):
        """Update agent with learning from results."""
        super().update(observation, action, reward, done, info)
        
        # Simple learning: adjust exploration rate based on performance
        if len(self.utility_history) > 1:
            recent_utility = self.utility_history[-1]
            if recent_utility > 0:
                self.exploration_rate = max(0.05, self.exploration_rate * 0.95)
            else:
                self.exploration_rate = min(0.5, self.exploration_rate * 1.05)


class StudentTruthfulAgent(BaseAuctionAgent):
    """
    Student implementation of a truthful bidding agent.
    This simulates a simple baseline that students might implement.
    """
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Bid truthfully (marginal values for single items)."""
        bids = {}
        for good in self.goods:
            # Bid the value of the single item
            bids[good] = self.valuation_function({good})
        return bids


class StudentRandomAgent(BaseAuctionAgent):
    """
    Student implementation of a random bidding agent.
    This simulates a simple baseline that students might implement.
    """
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, float]:
        """Bid randomly between 0 and single item value."""
        bids = {}
        for good in self.goods:
            single_value = self.valuation_function({good})
            bids[good] = random.uniform(0, single_value)
        return bids


class TestLab06StudentStyle(unittest.TestCase):
    """Comprehensive student-style tests for Lab 6."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.goods = {"A", "B", "C", "D"}
        
        # Student valuation functions
        def additive_valuation(bundle):
            """Simple additive valuation."""
            values = {"A": 10, "B": 15, "C": 20, "D": 25}
            return sum(values.get(item, 0) for item in bundle)
        
        def complement_valuation(bundle):
            """Complement valuation with synergy."""
            base_value = additive_valuation(bundle)
            if len(bundle) > 1:
                return base_value * (1.1 ** (len(bundle) - 1))
            return base_value
        
        def substitute_valuation(bundle):
            """Substitute valuation with diminishing returns."""
            base_value = additive_valuation(bundle)
            if len(bundle) > 1:
                return base_value * (0.9 ** (len(bundle) - 1))
            return base_value
        
        self.valuation_functions = {
            "additive": additive_valuation,
            "complement": complement_valuation,
            "substitute": substitute_valuation
        }
    
    def test_marginal_value_calculation(self):
        """Test student marginal value calculation."""
        agent = StudentMarginalValueAgent("TestAgent")
        agent.setup(self.goods, self.valuation_functions["additive"])
        
        # Test case 1: No goods won
        bids = {"A": 5, "B": 5, "C": 5, "D": 5}
        prices = {"A": 10, "B": 15, "C": 20, "D": 25}
        
        mv_a = agent.calculate_marginal_value(self.goods, "A", bids, prices)
        self.assertEqual(mv_a, 10, "Marginal value should equal single item value when no goods won")
        
        # Test case 2: Some goods won
        bids = {"A": 15, "B": 5, "C": 25, "D": 5}
        prices = {"A": 10, "B": 15, "C": 20, "D": 25}
        
        mv_a = agent.calculate_marginal_value(self.goods, "A", bids, prices)
        # Would win A and C, so marginal value of A is value(A,C) - value(C) = 30 - 20 = 10
        self.assertEqual(mv_a, 10, "Marginal value calculation incorrect")
        
        # Test case 3: All goods won
        bids = {"A": 15, "B": 20, "C": 25, "D": 30}
        prices = {"A": 10, "B": 15, "C": 20, "D": 25}
        
        mv_a = agent.calculate_marginal_value(self.goods, "A", bids, prices)
        # Would win all goods, so marginal value of A is value(all) - value(B,C,D) = 70 - 60 = 10
        self.assertEqual(mv_a, 10, "Marginal value calculation incorrect for all goods won")
    
    def test_local_bidding_optimization(self):
        """Test student local bidding optimization."""
        agent = StudentMarginalValueAgent("TestAgent")
        agent.setup(self.goods, self.valuation_functions["additive"])
        
        prices = {"A": 8, "B": 12, "C": 18, "D": 22}
        
        optimized_bids = agent.local_bid_optimization(self.goods, prices, num_iterations=20)
        
        # Check that bids are reasonable
        self.assertIsInstance(optimized_bids, dict)
        self.assertEqual(set(optimized_bids.keys()), self.goods)
        
        for good, bid in optimized_bids.items():
            self.assertGreaterEqual(bid, 0, "Bids should be non-negative")
            # Bids should be close to single item values for additive valuation
            single_value = self.valuation_functions["additive"]({good})
            self.assertLessEqual(bid, single_value * 1.5, "Bids should not be too high")
    
    def test_agent_action_generation(self):
        """Test that agents can generate valid actions."""
        agents = {
            "marginal": StudentMarginalValueAgent("MarginalAgent"),
            "truthful": StudentTruthfulAgent("TruthfulAgent"),
            "random": StudentRandomAgent("RandomAgent")
        }
        
        for name, agent in agents.items():
            agent.setup(self.goods, self.valuation_functions["additive"])
            
            observation = {
                "goods": self.goods,
                "round": 1,
                "prices": {"A": 8, "B": 12, "C": 18, "D": 22}
            }
            
            action = agent.get_action(observation)
            
            # Check action structure
            self.assertIsInstance(action, dict)
            self.assertEqual(set(action.keys()), self.goods)
            
            for good, bid in action.items():
                self.assertGreaterEqual(bid, 0, f"Bid for {good} should be non-negative")
    
    def test_auction_game_with_student_agents(self):
        """Test running an auction game with student agents."""
        # Create student agents
        agent1 = StudentMarginalValueAgent("Student1")
        agent2 = StudentTruthfulAgent("Student2")
        agent3 = StudentRandomAgent("Student3")
        
        # Set up agents
        agent1.setup(self.goods, self.valuation_functions["additive"])
        agent2.setup(self.goods, self.valuation_functions["complement"])
        agent3.setup(self.goods, self.valuation_functions["substitute"])
        
        # Create game
        valuation_functions = {
            "Student1": self.valuation_functions["additive"],
            "Student2": self.valuation_functions["complement"],
            "Student3": self.valuation_functions["substitute"]
        }
        
        game = AuctionGame(self.goods, valuation_functions, num_rounds=5)
        
        # Run multiple rounds
        for round_num in range(5):
            observation = {
                "goods": self.goods,
                "round": round_num,
                "prices": SampleValuations.generate_price_vector()
            }
            
            # Get actions from agents
            action1 = agent1.get_action(observation)
            action2 = agent2.get_action(observation)
            action3 = agent3.get_action(observation)
            
            actions = {
                "Student1": action1,
                "Student2": action2,
                "Student3": action3
            }
            
            # Run round
            results = game.run_round(actions)
            
            # Update agents
            agent1.update(observation, action1, results["utilities"]["Student1"], False, results)
            agent2.update(observation, action2, results["utilities"]["Student2"], False, results)
            agent3.update(observation, action3, results["utilities"]["Student3"], False, results)
        
        # Check that game history was recorded
        self.assertEqual(len(game.bid_history), 5, "Game should have recorded 5 rounds of bids")
        self.assertEqual(len(game.allocation_history), 5, "Game should have recorded 5 rounds of allocations")
        self.assertEqual(len(game.utility_history), 5, "Game should have recorded 5 rounds of utilities")
        
        # Check that agent history was recorded
        self.assertEqual(len(agent1.bid_history), 5, "Agent1 should have recorded 5 rounds of bids")
        self.assertEqual(len(agent1.utility_history), 5, "Agent1 should have recorded 5 rounds of utilities")
    
    def test_learning_behavior(self):
        """Test that the marginal value agent shows learning behavior."""
        agent = StudentMarginalValueAgent("LearningAgent")
        agent.setup(self.goods, self.valuation_functions["additive"])
        
        # Track exploration rate changes
        initial_exploration = agent.exploration_rate
        exploration_changes = []
        
        # Run multiple rounds with feedback
        for round_num in range(10):
            observation = {
                "goods": self.goods,
                "round": round_num,
                "prices": {"A": 8, "B": 12, "C": 18, "D": 22}
            }
            
            action = agent.get_action(observation)
            
            # Simulate positive reward for good performance
            reward = sum(action.values()) / 10  # Simple reward based on bid levels
            
            info = {
                "allocation": {"A": "LearningAgent", "C": "LearningAgent"},
                "prices": observation["prices"]
            }
            
            agent.update(observation, action, reward, False, info)
            exploration_changes.append(agent.exploration_rate)
        
        # Check that exploration rate changed (learning occurred)
        self.assertNotEqual(exploration_changes[0], exploration_changes[-1], 
                           "Exploration rate should change during learning")
        
        # Check that agent has history
        self.assertEqual(len(agent.bid_history), 10, "Agent should have recorded 10 rounds of bids")
        self.assertEqual(len(agent.utility_history), 10, "Agent should have recorded 10 rounds of utilities")
    
    def test_different_valuation_types(self):
        """Test agents with different valuation function types."""
        agents = {
            "additive": StudentMarginalValueAgent("AdditiveAgent"),
            "complement": StudentMarginalValueAgent("ComplementAgent"),
            "substitute": StudentMarginalValueAgent("SubstituteAgent")
        }
        
        # Set up agents with different valuations
        agents["additive"].setup(self.goods, self.valuation_functions["additive"])
        agents["complement"].setup(self.goods, self.valuation_functions["complement"])
        agents["substitute"].setup(self.goods, self.valuation_functions["substitute"])
        
        prices = {"A": 8, "B": 12, "C": 18, "D": 22}
        
        # Test that all agents can generate actions
        for name, agent in agents.items():
            observation = {"goods": self.goods, "round": 1, "prices": prices}
            action = agent.get_action(observation)
            
            self.assertIsInstance(action, dict)
            self.assertEqual(set(action.keys()), self.goods)
            
            # Check that bids are reasonable for each valuation type
            for good, bid in action.items():
                self.assertGreaterEqual(bid, 0, f"Bid for {good} should be non-negative")
                
                # For additive valuation, bids should be close to single item values
                if name == "additive":
                    single_value = self.valuation_functions["additive"]({good})
                    self.assertLessEqual(bid, single_value * 1.2, 
                                       f"Additive agent bid for {good} should not be too high")
    
    def test_edge_cases(self):
        """Test edge cases that students should handle."""
        agent = StudentMarginalValueAgent("EdgeCaseAgent")
        agent.setup(self.goods, self.valuation_functions["additive"])
        
        # Test with empty bundle
        empty_bundle = set()
        value = agent.get_valuation(empty_bundle)
        self.assertEqual(value, 0, "Empty bundle should have zero value")
        
        # Test with single item
        single_bundle = {"A"}
        value = agent.get_valuation(single_bundle)
        self.assertEqual(value, 10, "Single item A should have value 10")
        
        # Test with all items
        all_bundle = {"A", "B", "C", "D"}
        value = agent.get_valuation(all_bundle)
        self.assertEqual(value, 70, "All items should have value 70")
        
        # Test marginal value with zero bids
        zero_bids = {"A": 0, "B": 0, "C": 0, "D": 0}
        prices = {"A": 1, "B": 1, "C": 1, "D": 1}
        
        mv_a = agent.calculate_marginal_value(self.goods, "A", zero_bids, prices)
        self.assertEqual(mv_a, 10, "Marginal value of A should be 10 when no goods won")


def run_student_style_tests():
    """Run all student-style tests for Lab 6."""
    print("Running student-style tests for Lab 6...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestLab06StudentStyle))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_student_style_tests()
    sys.exit(0 if success else 1) 