"""
solution for lab 9 adx two-day competition agent.

implements an aggressive bidding strategy across two days,
prioritizing quality score on day 1 to maximize day 2 budget.
"""

import sys
import os
import math
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxTwoDayGame import TwoDaysBidBundle, AdxTwoDayGame
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from core.agents.common.base_agent import BaseAgent
from server.connect_stencil import connect_agent_to_server


class MyTwoDaysTwoCampaignsAgent(BaseAgent):
    """
    Adx two-day competition agent with quality-score-aware strategy.

    day 1: bids aggressively to maximize quality score.
    day 2: adjusts aggressiveness based on achieved quality score.
    """

    def __init__(self, name: str = "MyTwoDaysAdxAgent"):
        super().__init__(name)
        self.campaign_day1 = None
        self.campaign_day2 = None
        self.quality_score = 1.0
        self.game_title = "adx_twoday"

    def get_action(self, observation: dict = None) -> TwoDaysBidBundle:
        """
        Create bid bundle based on current observation.

        Args:
            observation: dict with day, campaign info, and quality score

        Returns:
            TwoDaysBidBundle for the current day
        """
        day = observation["day"]
        if day == 1:
            self.campaign_day1 = Campaign.from_dict(observation["campaign_day1"])
        elif day == 2:
            self.campaign_day2 = Campaign.from_dict(observation["campaign_day2"])

        # extract quality score from observation
        if "qc" in observation:
            self.quality_score = observation["qc"]
        elif "campaign" in observation and "qc" in observation["campaign"]:
            self.quality_score = observation["campaign"]["qc"]

        return self._get_bid_bundle(day)

    def _get_bid_bundle(self, day: int) -> TwoDaysBidBundle:
        """
        Build bid bundle for the given day.

        Args:
            day: 1 or 2

        Returns:
            TwoDaysBidBundle with bids for matching segments
        """
        if day == 1:
            campaign = self.campaign_day1
            # aggressive day 1: high bids to maximize quality score
            bid_amount = 2.5
            budget_usage = 0.95
        elif day == 2:
            campaign = self.campaign_day2
            # day 2: adjust based on quality score
            if self.quality_score > 0.9:
                bid_amount = 3.0
                budget_usage = 1.0
            elif self.quality_score > 0.7:
                bid_amount = 2.0
                budget_usage = 0.9
            else:
                bid_amount = 1.5
                budget_usage = 0.8
        else:
            raise ValueError("Day must be 1 or 2")

        if campaign is None:
            raise ValueError(f"Campaign is not set for day {day}")

        bid_entries = [
            SimpleBidEntry(
                market_segment=segment,
                bid=bid_amount,
                spending_limit=campaign.budget * budget_usage
            )
            for segment in MarketSegment.all_segments()
            if MarketSegment.is_subset(campaign.market_segment, segment)
        ]

        return TwoDaysBidBundle(
            day=day,
            campaign_id=campaign.id,
            day_limit=campaign.budget,
            bid_entries=bid_entries
        )

    def calculate_quality_score(self, impressions_achieved: int, campaign_reach: int) -> float:
        """
        Calculate quality score using the formula from the writeup.

        QC(x) = (2/a) * (arctan(a * (x/R - b)) - arctan(-b))
        where a = 4.08577, b = 3.08577

        Args:
            impressions_achieved: number of impressions acquired (x)
            campaign_reach: campaign's reach goal (R)

        Returns:
            quality score (non-negative)
        """
        a = 4.08577
        b = 3.08577

        if campaign_reach == 0:
            return 0.0

        x_over_r = impressions_achieved / campaign_reach
        quality_score = (2 / a) * (math.atan(a * x_over_r - b) - math.atan(-b))

        return max(0.0, quality_score)


name = "MyTwoDaysAdxAgent"


################### SUBMISSION #####################
agent_submission = MyTwoDaysTwoCampaignsAgent(name)
####################################################


if __name__ == "__main__":
    # configuration
    server = True
    host = "localhost"
    port = 8080
    verbose = False
    game = "adx_twoday"

    if server:
        async def main():
            agent = MyTwoDaysTwoCampaignsAgent(name)
            await connect_agent_to_server(agent, game, name, host, port, verbose)

        asyncio.run(main())
    else:
        from core.agents.lab09.aggressive_agent import AggressiveAdXAgent
        from core.agents.lab09.random_agent import RandomAdXAgent
        from core.local_arena import LocalArena

        agent = MyTwoDaysTwoCampaignsAgent(name)
        opponent1 = AggressiveAdXAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]

        agents = [agent, opponent1] + random_agents
        arena = LocalArena(
            game_title="adx_twoday",
            game_class=AdxTwoDayGame,
            agents=agents,
            num_agents_per_game=10,
            num_rounds=10,
            timeout=30.0,
            save_results=False,
            verbose=True
        )
        arena.run_tournament()

        print("\nLocal test completed!")
