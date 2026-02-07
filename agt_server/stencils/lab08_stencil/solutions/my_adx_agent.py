"""
solution for lab 8 adx one-day competition agent.

implements an aggressive bidding strategy that allocates budget
strategically across matching market segments.
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.game.AdxOneDayGame import OneDayBidBundle, AdxOneDayGame
from core.game.bid_entry import SimpleBidEntry
from core.game.market_segment import MarketSegment
from core.game.campaign import Campaign
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent
from server.connect_stencil import connect_agent_to_server


class MyAdXAgent(BaseAgent):
    """
    Adx one-day competition agent with aggressive bidding strategy.

    bids higher amounts on matching market segments and allocates
    budget evenly across them, using most of the available budget.
    """

    def __init__(self, name: str = "MyAdXAgent"):
        super().__init__(name)
        self.game_title = "adx_oneday"

    def get_action(self, observation: Dict[str, Any]) -> OneDayBidBundle:
        """
        Create bid bundle for the assigned campaign.

        Args:
            observation: dict containing campaign information

        Returns:
            OneDayBidBundle with bids for matching market segments
        """
        campaign_data = observation['campaign']
        campaign = Campaign.from_dict(campaign_data) if isinstance(campaign_data, dict) else campaign_data

        # use 80% of budget as day limit for safety margin
        day_limit = campaign.budget * 0.8

        # find all segments matching the campaign target
        matching_segments = [
            segment for segment in MarketSegment.all_segments()
            if MarketSegment.is_subset(campaign.market_segment, segment)
        ]

        # allocate budget evenly across matching segments
        segment_budget = day_limit / len(matching_segments) if matching_segments else 0

        bid_entries = [
            SimpleBidEntry(
                market_segment=segment,
                bid=2.0,
                spending_limit=segment_budget
            )
            for segment in matching_segments
        ]

        return OneDayBidBundle(
            campaign_id=campaign.id,
            day_limit=day_limit,
            bid_entries=bid_entries
        )


name = "MyAdXAgent"


################### SUBMISSION #####################
agent_submission = MyAdXAgent(name)
####################################################


if __name__ == "__main__":
    # configuration
    server = True
    host = "localhost"
    port = 8080
    verbose = False
    game = "adx_oneday"

    if server:
        async def main():
            agent = MyAdXAgent(name)
            await connect_agent_to_server(agent, game, name, host, port, verbose)

        asyncio.run(main())
    else:
        from core.agents.lab08.random_agent import RandomAdXAgent
        from core.agents.lab08.aggressive_bidding_agent import AggressiveBiddingAgent
        from core.local_arena import LocalArena

        agent = MyAdXAgent(name)
        opponent1 = AggressiveBiddingAgent()
        random_agents = [RandomAdXAgent(f"RandomAgent_{i}") for i in range(8)]

        agents = [agent, opponent1] + random_agents
        arena = LocalArena(
            game_title="adx_oneday",
            game_class=AdxOneDayGame,
            agents=agents,
            num_agents_per_game=10,
            num_rounds=10,
            timeout=30.0,
            save_results=False,
            verbose=True
        )
        arena.run_tournament()

        print("\nLocal test completed!")
