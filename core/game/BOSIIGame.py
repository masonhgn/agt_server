import numpy as np
from core.game.base_game import BaseGame, ObsDict, ActionDict, RewardDict, InfoDict
from core.stage.BaseStage import BaseStage


class BOSIIStage(BaseStage):
    """
    Single stage of Battle of the Sexes with Incomplete Information.
    
    The column player has a mood (GOOD_MOOD or BAD_MOOD) that affects payoffs.
    Row player doesn't know the column player's mood.
    """
    
    def __init__(self):
        super().__init__(num_players=2)
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        
        # Payoff matrices for different moods
        self.payoffs = {
            self.GOOD_MOOD: np.array([
                # Compromise vs Compromise, Stubborn
                [[0.0, 0.0], [3.0, 7.0]],
                # Stubborn vs Compromise, Stubborn  
                [[7.0, 3.0], [0.0, 0.0]]
            ]),
            self.BAD_MOOD: np.array([
                # Compromise vs Compromise, Stubborn
                [[0.0, 3.0], [3.0, 0.0]],
                # Stubborn vs Compromise, Stubborn
                [[7.0, 0.0], [0.0, 7.0]]
            ])
        }
        
        self.action_labels = ["Compromise", "Stubborn"]
        self.column_mood = None  # Will be set when stage starts
    
    def legal_actions(self, player_id):
        return self.action_labels
    
    def set_column_mood(self, mood):
        """Set the column player's mood for this stage."""
        self.column_mood = mood
    
    def step(self, actions: ActionDict) -> tuple[ObsDict, RewardDict, bool, InfoDict]:
        # Validate actions
        self._validate_actions(actions, expected_players=[0, 1])
        row_action, col_action = actions[0], actions[1]
        
        # Get payoffs based on column player's mood
        payoffs = self.payoffs[self.column_mood]  # type: ignore
        row_reward, col_reward = payoffs[row_action, col_action]
        
        reward: RewardDict = {0: float(row_reward), 1: float(col_reward)}
        
        # Stage ends immediately
        self._done = True
        obs: ObsDict = {0: {}, 1: {}}  # No observations needed
        info: InfoDict = {
            0: {"column_mood": self.column_mood},  # Row player gets mood info
            1: {"column_mood": self.column_mood}   # Column player knows their mood
        }
        
        return obs, reward, True, info


class BOSIIGame(BaseGame):
    """
    Battle of the Sexes with Incomplete Information game.
    
    The column player (player 1) has a mood that changes each round:
    - GOOD_MOOD (probability 2/3): Standard BOS payoffs
    - BAD_MOOD (probability 1/3): Modified payoffs
    
    The row player (player 0) doesn't know the column player's mood.
    """
    
    def __init__(self, rounds: int = 1000):
        self.rounds = rounds
        self.t = 0
        self.stage = None
        self.metadata = {"num_players": 2}
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        
        # Column player mood probabilities
        self.good_mood_prob = 2/3
        self.bad_mood_prob = 1/3
    
    def reset(self, seed=None) -> ObsDict:
        self.t = 0
        if seed is not None:
            np.random.seed(seed)
        return {0: {}, 1: {}}
    
    def players_to_move(self):
        return [0, 1]
    
    def step(self, actions: ActionDict) -> tuple[ObsDict, RewardDict, bool, InfoDict]:
        # Create new stage with random column mood
        self.stage = BOSIIStage()
        column_mood = np.random.choice(
            [self.GOOD_MOOD, self.BAD_MOOD], 
            p=[self.good_mood_prob, self.bad_mood_prob]
        )
        self.stage.set_column_mood(column_mood)
        
        # Run the stage
        obs, reward, _, info = self.stage.step(actions)
        
        self.t += 1
        done = self.t >= self.rounds
        
        return obs, reward, done, info 