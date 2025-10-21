# games/adx_two_day.py
from typing import Tuple, cast, Dict, List, Optional
from core.game import ObsDict, ActionDict, RewardDict, InfoDict
from core.game.base_game import BaseGame
from core.stage.AdxTwoDayStage import AdxTwoDayStage, TwoDaysBidBundle
from core.game.campaign import Campaign
import random


class AdxTwoDayGame(BaseGame):
    """
    Two-day TAC AdX Game.
    
    This game runs over two consecutive days:
    - Day 1: Agents bid with base budgets
    - Day 2: Agents bid with QC-adjusted budgets based on Day 1 performance
    
    The game uses AdxTwoDayStage to handle the actual auction logic.
    """
    
    def __init__(self, num_players: int = 2, rival_sampler=None):
        super().__init__()
        self._num_players = num_players
        self.rival_sampler = rival_sampler
        self.stage = AdxTwoDayStage(num_players, rival_sampler)
        self.metadata = {"num_players": num_players}

    def reset(self, seed: Optional[int] = None) -> ObsDict:
        """Reset the game for a new tournament."""
        if seed is not None:
            random.seed(seed)
        
        # Create new stage instance
        self.stage = AdxTwoDayStage(self._num_players, self.rival_sampler)
        
        # Prepare initial observations for day 1
        obs = {}
        for i in range(self._num_players):
            obs[i] = {
                "day": 1,
                "campaign_day1": self._campaign_to_dict(self.stage.get_campaigns_day1()[i]),
                "campaign_day2": self._campaign_to_dict(self.stage.get_campaigns_day2()[i])
            }
        
        return cast(ObsDict, obs)

    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Execute one step of the game."""
        #delegate to stage
        return self.stage.step(actions)

    def players_to_move(self) -> List[int]:
        """Return the subset of players whose actions are required now."""
        return list(range(self._num_players))

    def num_players(self) -> int:
        """Get number of players in the game."""
        return self._num_players

    def get_game_state(self) -> Dict[str, any]:
        """Get the current game state."""
        return {
            "num_players": self._num_players,
            "current_day": self.stage.current_day,
            "qc_multiplier": self.stage.qc_multiplier,
            "campaigns_day1": self.stage.get_campaigns_day1(),
            "campaigns_day2": self.stage.get_campaigns_day2()
        }

    def _campaign_to_dict(self, campaign: Campaign) -> Dict:
        """Convert Campaign to dictionary for JSON serialization."""
        return {
            "id": campaign.id,
            "market_segment": campaign.market_segment.value,
            "reach": campaign.reach,
            "budget": campaign.budget
        }