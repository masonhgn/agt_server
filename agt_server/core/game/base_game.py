
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Hashable, List, Tuple

PlayerId = Hashable
ObsDict = Dict[PlayerId, Any]
ActionDict = Dict[PlayerId, Any]
RewardDict = Dict[PlayerId, float]
InfoDict = Dict[PlayerId, Dict[str, Any]]

class BaseGame(ABC):


    metadata: Dict[str, Any] #metadata that comes along with games from the config maybe

    @abstractmethod
    def reset(self, seed: int | None = None) -> ObsDict:
        """
        Initialise a fresh match and return the initial per-player observations.
        Must also (re)populate self.metadata.

        Parameters
        ----------
        seed : int | None
            Deterministic seed if the game is stochastic.
        """




    @abstractmethod
    def players_to_move(self) -> List[PlayerId]:
        """
        Return the subset of players whose actions are required *now*.
        For simultaneous-move games this is usually `list(range(n))`.
        For an offline one-shot game (AdX) it might be `[0]` once
        and an empty list while internal simulation rolls.
        """



    @abstractmethod
    def step(
            self,
            actions: ActionDict
        ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """
        Advance the game by applying "actions".

        Returns
        -------
        obs : ObsDict
            New observations for every player.
        reward : RewardDict
            Payoff earned **since the last call** (can be 0 for nonterminal steps).
        done : bool
            True if the whole match is finished.
        info : InfoDict
            Optional extra diagnostics (never used for scoring).
        """










    def num_players(self) -> int:
        """Gets number of players in the game"""
        return self.metadata.get("num_players", 0)

    



