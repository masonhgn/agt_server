from .base_game import BaseGame, ObsDict, ActionDict, RewardDict, InfoDict, PlayerId
from typing import List, Tuple, cast
import numpy as np


class LemonadeGame(BaseGame):
    """
    Lemonade Stand Game - a 3-player game where players choose positions 0-11 on a circular board.
    
    Payoff structure:
    - If all three players choose the same position: each gets 8 points
    - If two players choose the same position: they each get 6, the third gets 12
    - If all choose different positions: the player in the middle gets the most points
    """
    
    def __init__(self, rounds: int = 1000):
        self.valid_actions = list(range(12))  # Positions 0-11
        self.game_name = "Lemonade Stand"
        self.rounds = rounds
        self.current_round = 0
        self.cumulative_rewards = {0: 0.0, 1: 0.0, 2: 0.0}
        self.metadata = {
            "num_players": 3,
            "num_rounds": rounds,
            "game_name": self.game_name,
            "valid_actions": self.valid_actions
        }
        
    def calculate_utils(self, actions):
        """
        Calculate utilities for all players based on their actions, using the official Lemonade Stand rules:
        - For each of the 12 positions (beachgoers), find the closest stand(s).
        - Each beachgoer buys 2 cups, split among the closest stand(s).
        - Each player's utility is the sum of cups they receive from all positions.
        """
        if len(actions) != 3:
            raise ValueError("Lemonade Stand requires exactly 3 players")
        
        # Handle invalid actions (as before)
        a1, a2, a3 = actions
        if a1 not in self.valid_actions and a2 not in self.valid_actions and a3 not in self.valid_actions:
            return [0, 0, 0]
        elif a1 not in self.valid_actions and a2 not in self.valid_actions:
            return [0, 0, 24]
        elif a1 not in self.valid_actions and a3 not in self.valid_actions:
            return [0, 24, 0]
        elif a2 not in self.valid_actions and a3 not in self.valid_actions:
            return [24, 0, 0]
        elif a1 not in self.valid_actions:
            return [0, 12, 12]
        elif a2 not in self.valid_actions:
            return [12, 0, 12]
        elif a3 not in self.valid_actions:
            return [12, 12, 0]

        # Simulate the 12 beachgoers
        player_positions = [a1, a2, a3]
        utils = [0.0, 0.0, 0.0]
        for beachgoer in range(12):
            # Compute distances to each stand
            dists = [min((beachgoer - pos) % 12, (pos - beachgoer) % 12) for pos in player_positions]
            min_dist = min(dists)
            # Find all players at min_dist
            closest = [i for i, d in enumerate(dists) if d == min_dist]
            # Split 2 cups among closest
            for i in closest:
                utils[i] += 2.0 / len(closest)
        return utils
    
    def get_valid_actions(self):
        """Return the list of valid actions (positions 0-11)."""
        return self.valid_actions.copy()
    
    def get_game_info(self):
        """Return information about the game."""
        return {
            "name": self.game_name,
            "num_players": self.num_players(),
            "valid_actions": self.valid_actions,
            "description": "3-player game where players choose positions 0-11 on a circular board"
        }
    
    def reset(self, seed: int | None = None) -> ObsDict:
        """Reset the game to initial state."""
        if seed is not None:
            import random
            random.seed(seed)
        
        self.current_round = 0
        self.cumulative_rewards = {0: 0.0, 1: 0.0, 2: 0.0}
        
        # Initialize empty observations for all players
        obs = {i: {"valid_actions": self.valid_actions} for i in range(3)}
        return cast(ObsDict, obs)
    
    def players_to_move(self) -> List[PlayerId]:
        """Return the list of players who need to move (all players in simultaneous game)."""
        return cast(List[PlayerId], list(range(3)))
    
    def step(self, actions: ActionDict) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        """Execute one step of the game."""
        # Extract actions in order
        action_list = [actions[i] for i in range(3)]
        
        # Calculate utilities
        utils = self.calculate_utils(action_list)
        
        # Create reward dict
        rewards = {i: float(utils[i]) for i in range(3)}
        
        # Accumulate rewards
        for i in range(3):
            self.cumulative_rewards[i] += rewards[i]
        
        # Increment round counter
        self.current_round += 1
        
        # Create observations (same for all players in this simple game)
        obs = {i: {"valid_actions": self.valid_actions} for i in range(3)}
        
        # Check if game is done
        done = self.current_round >= self.rounds
        
        # Create info dict
        info = {i: {"actions": action_list, "utilities": utils, "round": self.current_round} for i in range(3)}
        
        # Return cumulative rewards if done, individual rewards otherwise
        if done:
            return cast(Tuple[ObsDict, RewardDict, bool, InfoDict], (obs, self.cumulative_rewards, done, info))
        else:
            return cast(Tuple[ObsDict, RewardDict, bool, InfoDict], (obs, rewards, done, info)) 