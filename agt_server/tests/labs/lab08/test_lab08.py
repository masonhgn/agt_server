#!/usr/bin/env python3
"""
comprehensive tests for lab 8: ad exchange (one day game)

this test suite validates various adx agent implementations and their behavior
in the one-day ad exchange game environment.
"""

import sys
import os
import unittest
from typing import Dict, Any, List

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.game.AdxOneDayGame import AdxOneDayGame, OneDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign


class StudentAdXAgent:
    """student implementation of adx agent for testing."""
    
    def __init__(self, name: str = "student_agent"):
        self.name = name
        self.campaign = None
        self.bid_history = []
    
    def get_bid_bundle(self) -> OneDayBidBundle:
        """student bidding strategy: bid 0.5 on all matching segments."""
        if self.campaign is None:
            raise ValueError("Campaign not set")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=0.5,
                    spending_limit=self.campaign.budget * 0.8  # Use 80% of budget
                ))
        
        self.bid_history.append({
            'campaign_id': self.campaign.id,
            'bid_entries': len(bid_entries),
            'total_budget': self.campaign.budget
        })
        
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,
            bid_entries=bid_entries
        )


class AggressiveAdXAgent:
    """aggressive bidding agent for testing."""
    
    def __init__(self, name: str = "aggressive_agent"):
        self.name = name
        self.campaign = None
    
    def get_bid_bundle(self) -> OneDayBidBundle:
        """aggressive strategy: bid high on all segments."""
        if self.campaign is None:
            raise ValueError("Campaign not set")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(self.campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=2.0,  # High bid
                    spending_limit=self.campaign.budget
                ))
        
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,
            bid_entries=bid_entries
        )


class ConservativeAdXAgent:
    """conservative bidding agent for testing."""
    
    def __init__(self, name: str = "conservative_agent"):
        self.name = name
        self.campaign = None
    
    def get_bid_bundle(self) -> OneDayBidBundle:
        """conservative strategy: bid low on few segments."""
        if self.campaign is None:
            raise ValueError("Campaign not set")
        
        bid_entries = []
        # Only bid on the exact market segment
        bid_entries.append(SimpleBidEntry(
            market_segment=self.campaign.market_segment,
            bid=0.1,  # Low bid
            spending_limit=self.campaign.budget * 0.3  # Use only 30% of budget
        ))
        
        return OneDayBidBundle(
            campaign_id=self.campaign.id,
            day_limit=self.campaign.budget,
            bid_entries=bid_entries
        )


class TestLab8AdXGame(unittest.TestCase):
    """test suite for lab 8 adx game functionality."""
    
    def setUp(self):
        """set up test environment."""
        self.game = AdxOneDayGame(num_agents=2)
        self.obs = self.game.reset(seed=42)
    
    def test_basic_game_setup(self):
        """test that the game can be set up correctly."""
        self.assertEqual(len(self.obs), 2)
        self.assertIn("campaign", self.obs[0])
        self.assertIn("campaign", self.obs[1])
        
        # Check that campaigns have required attributes
        campaign = self.obs[0]["campaign"]
        self.assertIsInstance(campaign, Campaign)
        self.assertIsNotNone(campaign.id)
        self.assertIsNotNone(campaign.budget)
        self.assertIsNotNone(campaign.market_segment)
    
    def test_student_agent_basic_functionality(self):
        """test basic functionality of student agent."""
        agent = StudentAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        self.assertIsInstance(bid_bundle, OneDayBidBundle)
        self.assertEqual(bid_bundle.campaign_id, agent.campaign.id)
        self.assertEqual(bid_bundle.day_limit, agent.campaign.budget)
        self.assertGreater(len(bid_bundle.bid_entries), 0)
        
        # Check that all bid entries are valid
        for entry in bid_bundle.bid_entries:
            self.assertIsInstance(entry, SimpleBidEntry)
            self.assertGreater(entry.bid, 0)
            self.assertLessEqual(entry.spending_limit, agent.campaign.budget)
    
    def test_aggressive_agent_behavior(self):
        """test aggressive agent bidding behavior."""
        agent = AggressiveAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        # Check that aggressive agent bids high
        for entry in bid_bundle.bid_entries:
            self.assertGreaterEqual(entry.bid, 2.0)
            self.assertEqual(entry.spending_limit, agent.campaign.budget)
    
    def test_conservative_agent_behavior(self):
        """test conservative agent bidding behavior."""
        agent = ConservativeAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        # Check that conservative agent bids low and uses limited budget
        self.assertEqual(len(bid_bundle.bid_entries), 1)
        entry = bid_bundle.bid_entries[0]
        self.assertLessEqual(entry.bid, 0.1)
        self.assertLessEqual(entry.spending_limit, agent.campaign.budget * 0.3)
    
    def test_market_segment_matching(self):
        """test that market segment matching works correctly."""
        agent = StudentAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        # Check that all bid entries match the campaign's market segment
        for entry in bid_bundle.bid_entries:
            self.assertTrue(
                MarketSegment.is_subset(agent.campaign.market_segment, entry.market_segment)
            )
    
    def test_game_execution_with_student_agents(self):
        """test full game execution with student agents."""
        agents = [StudentAdXAgent("student1"), StudentAdXAgent("student2")]
        
        # Assign campaigns to agents
        for i, agent in enumerate(agents):
            agent.campaign = self.obs[i]["campaign"]
        
        # Collect bid bundles
        actions = {}
        for i, agent in enumerate(agents):
            actions[i] = agent.get_bid_bundle()
        
        # Run the game
        obs, rewards, done, info = self.game.step(actions)
        
        # Check results
        self.assertIsInstance(rewards, dict)
        self.assertIn(0, rewards)
        self.assertIn(1, rewards)
        
        # Check that agents have bid history
        for agent in agents:
            self.assertGreater(len(agent.bid_history), 0)
    
    def test_game_execution_with_mixed_agents(self):
        """test game execution with different agent types."""
        agents = [AggressiveAdXAgent(), ConservativeAdXAgent()]
        
        # Assign campaigns to agents
        for i, agent in enumerate(agents):
            agent.campaign = self.obs[i]["campaign"]
        
        # Collect bid bundles
        actions = {}
        for i, agent in enumerate(agents):
            actions[i] = agent.get_bid_bundle()
        
        # Run the game
        obs, rewards, done, info = self.game.step(actions)
        
        # Check that game completed successfully
        self.assertIsInstance(rewards, dict)
        self.assertEqual(len(rewards), 2)
    
    def test_campaign_budget_constraints(self):
        """test that budget constraints are respected."""
        agent = StudentAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        # Check that day limit doesn't exceed budget
        self.assertLessEqual(bid_bundle.day_limit, agent.campaign.budget)
        
        # Check that individual spending limits don't exceed budget
        for entry in bid_bundle.bid_entries:
            self.assertLessEqual(entry.spending_limit, agent.campaign.budget)
    
    def test_bid_entry_validation(self):
        """test that bid entries are properly validated."""
        agent = StudentAdXAgent()
        agent.campaign = self.obs[0]["campaign"]
        
        bid_bundle = agent.get_bid_bundle()
        
        for entry in bid_bundle.bid_entries:
            # Check that bid is positive
            self.assertGreater(entry.bid, 0)
            
            # Check that spending limit is positive
            self.assertGreater(entry.spending_limit, 0)
            
            # Check that market segment is valid
            self.assertIsInstance(entry.market_segment, MarketSegment)
    





    def test_agent_error_handling(self):
        """test that agents handle errors gracefully."""
        agent = StudentAdXAgent()
        
        # Test that agent raises error when campaign is not set
        with self.assertRaises(ValueError):
            agent.get_bid_bundle()
    

    
    def test_multiple_game_runs(self):
        """test that multiple game runs work correctly."""
        for run in range(3):
            game = AdxOneDayGame(num_agents=2)
            obs = game.reset(seed=42 + run)
            
            agents = [StudentAdXAgent(f"agent_{run}_{i}") for i in range(2)]
            
            # Assign campaigns and run game
            for i, agent in enumerate(agents):
                agent.campaign = obs[i]["campaign"]
            
            actions = {i: agent.get_bid_bundle() for i, agent in enumerate(agents)}
            obs, rewards, done, info = game.step(actions)
            
            # Verify game completed
            self.assertIsInstance(rewards, dict)
            self.assertEqual(len(rewards), 2)


def run_comprehensive_tests():
    """run all comprehensive tests for lab 8."""
    print("=" * 60)
    print("Lab 8: Ad Exchange (One Day Game) - Comprehensive Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLab8AdXGame)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("PASS: All tests passed!")
        return True
    else:
        print("FAIL: Some tests failed. Check output above for details.")
        return False


def main():
    """main function to run tests."""
    success = run_comprehensive_tests()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 