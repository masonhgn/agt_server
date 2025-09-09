#!/usr/bin/env python3
"""
comprehensive tests for lab 9: ad exchange (two day game)

this test suite validates various adx agent implementations and their behavior
in the two-day ad exchange game environment.
"""

import sys
import os
import unittest
from typing import Dict, Any, List, Optional

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.game.AdxTwoDayGame import AdxTwoDayGame, TwoDayBidBundle
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.game.base_game import ActionDict


def get_dummy_campaign(day=1):
    # create a dummy campaign for testing
    return Campaign(
        id=day,
        market_segment=MarketSegment.all_segments()[0],
        reach=1000 * day,
        budget=100.0 * day,
        start_day=day,
        end_day=day
    )

class StudentAdXAgent:
    """student implementation of adx agent for two-day game testing."""
    
    def __init__(self, name: str = "student_agent"):
        self.name = name
        self.campaign_day1: Optional[Campaign] = None
        self.campaign_day2: Optional[Campaign] = None
        self.bid_history = []
    
    def get_bid_bundle(self, day: int) -> TwoDayBidBundle:
        """student bidding strategy: bid 0.5 on all matching segments for each day."""
        if day == 1:
            campaign = self.campaign_day1
        elif day == 2:
            campaign = self.campaign_day2
        else:
            raise ValueError("Day must be 1 or 2")
        
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=0.5,
                    spending_limit=campaign.budget * 0.8  # Use 80% of budget
                ))
        
        self.bid_history.append({
            'day': day,
            'campaign_id': campaign.id,
            'bid_entries': len(bid_entries),
            'total_budget': campaign.budget
        })
        
        return TwoDayBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )


class AdaptiveAdXAgent(StudentAdXAgent):
    def get_bid_bundle(self, day: int) -> TwoDayBidBundle:
        if day == 1:
            campaign = self.campaign_day1
            bid_amount = 1.5
            budget_usage = 0.9
        elif day == 2:
            campaign = self.campaign_day2
            bid_amount = 0.3
            budget_usage = 0.5
        else:
            raise ValueError("Day must be 1 or 2")
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        bid_entries = []
        for segment in MarketSegment.all_segments():
            if MarketSegment.is_subset(campaign.market_segment, segment):
                bid_entries.append(SimpleBidEntry(
                    market_segment=segment,
                    bid=bid_amount,
                    spending_limit=campaign.budget * budget_usage
                ))
        self.bid_history.append({'day': day, 'campaign_id': campaign.id, 'bid_entries': len(bid_entries), 'total_budget': campaign.budget})
        return TwoDayBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )

class ConservativeAdXAgent(StudentAdXAgent):
    def get_bid_bundle(self, day: int) -> TwoDayBidBundle:
        if day == 1:
            campaign = self.campaign_day1
        elif day == 2:
            campaign = self.campaign_day2
        else:
            raise ValueError("Day must be 1 or 2")
        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")
        bid_entries = [SimpleBidEntry(
            market_segment=campaign.market_segment,
            bid=0.1,
            spending_limit=campaign.budget * 0.2
        )]
        self.bid_history.append({'day': day, 'campaign_id': campaign.id, 'bid_entries': 1, 'total_budget': campaign.budget})
        return TwoDayBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )

class TestLab9AdXGame(unittest.TestCase):
    """test suite for lab 9 adx two-day game functionality (single agent)."""
    
    def setUp(self):
        self.game = AdxTwoDayGame()
        self.obs = self.game.reset(seed=42)
        # simulate campaign assignment
        self.campaign_day1 = get_dummy_campaign(day=1)
        self.campaign_day2 = get_dummy_campaign(day=2)
    
    def test_basic_game_setup(self):
        """test that the two-day game can be set up correctly."""
        self.assertIn("day", self.obs[0])
        self.assertEqual(self.obs[0]["day"], 0)
    
    def test_student_agent_basic_functionality(self):
        """test basic functionality of student agent for both days."""
        agent = StudentAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        self.assertIsInstance(bid_bundle_day1, TwoDayBidBundle)
        self.assertEqual(bid_bundle_day1.day, 1)
        self.assertEqual(bid_bundle_day1.campaign_id, agent.campaign_day1.id)
        self.assertEqual(bid_bundle_day1.day_limit, agent.campaign_day1.budget)
        self.assertGreater(len(bid_bundle_day1.bid_entries), 0)
        bid_bundle_day2 = agent.get_bid_bundle(2)
        self.assertIsInstance(bid_bundle_day2, TwoDayBidBundle)
        self.assertEqual(bid_bundle_day2.day, 2)
        self.assertEqual(bid_bundle_day2.campaign_id, agent.campaign_day2.id)
        self.assertEqual(bid_bundle_day2.day_limit, agent.campaign_day2.budget)
        self.assertGreater(len(bid_bundle_day2.bid_entries), 0)
    
    def test_adaptive_agent_behavior(self):
        """test adaptive agent bidding behavior for both days."""
        agent = AdaptiveAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        for entry in bid_bundle_day1.bid_entries:
            self.assertGreaterEqual(entry.bid, 1.5)
            self.assertEqual(entry.spending_limit, agent.campaign_day1.budget * 0.9)
        bid_bundle_day2 = agent.get_bid_bundle(2)
        for entry in bid_bundle_day2.bid_entries:
            self.assertLessEqual(entry.bid, 0.3)
            self.assertEqual(entry.spending_limit, agent.campaign_day2.budget * 0.5)
    
    def test_conservative_agent_behavior(self):
        """test conservative agent bidding behavior for both days."""
        agent = ConservativeAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        self.assertEqual(len(bid_bundle_day1.bid_entries), 1)
        entry_day1 = bid_bundle_day1.bid_entries[0]
        self.assertLessEqual(entry_day1.bid, 0.1)
        self.assertLessEqual(entry_day1.spending_limit, agent.campaign_day1.budget * 0.2)
        bid_bundle_day2 = agent.get_bid_bundle(2)
        self.assertEqual(len(bid_bundle_day2.bid_entries), 1)
        entry_day2 = bid_bundle_day2.bid_entries[0]
        self.assertLessEqual(entry_day2.bid, 0.1)
        self.assertLessEqual(entry_day2.spending_limit, agent.campaign_day2.budget * 0.2)
    
    def test_market_segment_matching_both_days(self):
        """test that market segment matching works correctly for both days."""
        agent = StudentAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        for entry in bid_bundle_day1.bid_entries:
            self.assertTrue(MarketSegment.is_subset(agent.campaign_day1.market_segment, entry.market_segment))
        bid_bundle_day2 = agent.get_bid_bundle(2)
        for entry in bid_bundle_day2.bid_entries:
            self.assertTrue(MarketSegment.is_subset(agent.campaign_day2.market_segment, entry.market_segment))
    
    def test_game_execution_with_student_agent(self):
        """test full two-day game execution with student agent."""
        agent = StudentAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        actions_day1: ActionDict = {0: agent.get_bid_bundle(1)}
        obs, rewards, done, info = self.game.step(actions_day1)
        self.assertIsInstance(rewards, dict)
        self.assertIn(0, rewards)
        # simulate day 2
        actions_day2: ActionDict = {0: agent.get_bid_bundle(2)}
        obs, rewards, done, info = self.game.step(actions_day2)
        self.assertIsInstance(rewards, dict)
        self.assertIn(0, rewards)
    
    def test_campaign_budget_constraints_both_days(self):
        """test that budget constraints are respected for both days."""
        agent = StudentAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        self.assertLessEqual(bid_bundle_day1.day_limit, agent.campaign_day1.budget)
        for entry in bid_bundle_day1.bid_entries:
            self.assertLessEqual(entry.spending_limit, agent.campaign_day1.budget)
        bid_bundle_day2 = agent.get_bid_bundle(2)
        self.assertLessEqual(bid_bundle_day2.day_limit, agent.campaign_day2.budget)
        for entry in bid_bundle_day2.bid_entries:
            self.assertLessEqual(entry.spending_limit, agent.campaign_day2.budget)
    
    def test_bid_entry_validation_both_days(self):
        """test that bid entries are properly validated for both days."""
        agent = StudentAdXAgent()
        agent.campaign_day1 = self.campaign_day1
        agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = agent.get_bid_bundle(1)
        for entry in bid_bundle_day1.bid_entries:
            self.assertGreater(entry.bid, 0)
            self.assertGreater(entry.spending_limit, 0)
            self.assertIsInstance(entry.market_segment, MarketSegment)
        bid_bundle_day2 = agent.get_bid_bundle(2)
        for entry in bid_bundle_day2.bid_entries:
            self.assertGreater(entry.bid, 0)
            self.assertGreater(entry.spending_limit, 0)
            self.assertIsInstance(entry.market_segment, MarketSegment)
    
    def test_agent_error_handling(self):
        """test that agents handle errors gracefully."""
        agent = StudentAdXAgent()
        with self.assertRaises(ValueError):
            agent.get_bid_bundle(1)
        with self.assertRaises(ValueError):
            agent.get_bid_bundle(2)
        agent.campaign_day1 = self.campaign_day1
        with self.assertRaises(ValueError):
            agent.get_bid_bundle(3)
    
    def test_multiple_game_runs(self):
        """test that multiple game runs work correctly."""
        for run in range(3):
            game = AdxTwoDayGame()
            obs = game.reset(seed=42 + run)
            campaign_day1 = get_dummy_campaign(day=1)
            campaign_day2 = get_dummy_campaign(day=2)
            agent = StudentAdXAgent(f"agent_{run}")
            agent.campaign_day1 = campaign_day1
            agent.campaign_day2 = campaign_day2
            actions_day1: ActionDict = {0: agent.get_bid_bundle(1)}
            obs, rewards, done, info = game.step(actions_day1)
            self.assertIsInstance(rewards, dict)
            self.assertIn(0, rewards)
            actions_day2: ActionDict = {0: agent.get_bid_bundle(2)}
            obs, rewards, done, info = game.step(actions_day2)
            self.assertIsInstance(rewards, dict)
            self.assertIn(0, rewards)
    
    def test_day_specific_behavior(self):
        """test that agents behave differently on different days."""
        adaptive_agent = AdaptiveAdXAgent()
        adaptive_agent.campaign_day1 = self.campaign_day1
        adaptive_agent.campaign_day2 = self.campaign_day2
        bid_bundle_day1 = adaptive_agent.get_bid_bundle(1)
        avg_bid_day1 = sum(entry.bid for entry in bid_bundle_day1.bid_entries) / len(bid_bundle_day1.bid_entries)
        bid_bundle_day2 = adaptive_agent.get_bid_bundle(2)
        avg_bid_day2 = sum(entry.bid for entry in bid_bundle_day2.bid_entries) / len(bid_bundle_day2.bid_entries)
        self.assertGreater(avg_bid_day1, avg_bid_day2)


def run_comprehensive_tests():
    """run all comprehensive tests for lab 9."""
    print("=" * 60)
    print("Lab 9: Ad Exchange (Two Day Game) - Comprehensive Tests")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLab9AdXGame)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
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