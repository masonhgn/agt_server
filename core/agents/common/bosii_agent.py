from core.agents.common.base_agent import BaseAgent
from typing import Dict, Any, Optional, List


class BOSIIAgent(BaseAgent):
    """Base class for BOSII agents that handles player type and mood information."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        
        # BOSII-specific state
        self.is_row = None  # Will be set based on player type
        self.current_mood = None  # Column player's current mood
        self.mood_history = []  # Column player's mood history
        self.opponent_action_history = []  # Opponent's action history
        self.opponent_util_history = []  # Opponent's utility history
    
    def _update_metadata(self, opponent_last_move=None, player_type=None, mood=None):
        """
        Update player type and mood information. This is called by subclasses.
        
        Args:
            opponent_last_move: opponent's last action
            player_type: "row" or "column" 
            mood: current mood (GOOD_MOOD or BAD_MOOD) for column player
        """
        # Update player type and mood information
        if player_type is not None:
            self.is_row = (player_type == "row")
        
        if mood is not None and not self.is_row:
            self.current_mood = mood
            self.mood_history.append(mood)
    
    def get_action(self, obs=None, opponent_last_move=None, player_type=None, mood=None):
        """
        Get action from the agent. This method should be overridden by subclasses.
        
        Args:
            obs: observation dict (for engine interface)
            opponent_last_move: opponent's last action (for server interface)
            player_type: "row" or "column" (for server interface)
            mood: current mood (GOOD_MOOD or BAD_MOOD) for column player (for server interface)
        """
        # Handle server interface parameters
        if player_type is not None:
            self._update_metadata(opponent_last_move, player_type, mood)
        
        # Handle engine interface - try to extract info from obs
        elif obs is not None and isinstance(obs, dict):
            # Try to determine player type from obs if available
            if 'player_id' in obs:
                self.is_row = (obs['player_id'] == 0)
            if 'column_mood' in obs and not self.is_row:
                self.current_mood = obs['column_mood']
                self.mood_history.append(obs['column_mood'])
        
        # Subclasses should override this method to implement their strategy
        pass
    
    def update(self, observation: dict = None, action: dict = None, reward: float = None, done: bool = None, info: dict = None):
        """
        Update the agent with the reward and info from the last action.
        """
        # Handle reward format - could be a number or a dict
        if isinstance(reward, dict):
            # If reward is a dict, extract the value for this player
            if self.is_row:
                reward_value = reward.get(0, 0.0)
            else:
                reward_value = reward.get(1, 0.0)
        else:
            reward_value = reward
        
        if reward_value is not None:
            self.reward_history.append(reward_value)
        
        # Update player type and mood information from info
        if info:
            # Determine player type from player_id
            if 'player_id' in info:
                self.is_row = (info['player_id'] == 0)
            
            # Update mood information for column player
            if 'column_mood' in info and not self.is_row:
                self.current_mood = info['column_mood']
                self.mood_history.append(info['column_mood'])
            
            # Update opponent information if available
            if 'opponent_action' in info:
                self.opponent_action_history.append(info['opponent_action'])
            if 'opponent_util' in info:
                self.opponent_util_history.append(info['opponent_util'])
    
    def setup(self):
        """Setup the agent for a new game."""
        super().setup()
        # Reset BOSII-specific state
        self.is_row = None
        self.current_mood = None
        self.mood_history = []
        self.opponent_action_history = []
        self.opponent_util_history = []
    
    def reset(self):
        """Reset the agent for a new game."""
        super().reset()
        # Reset BOSII-specific state
        self.is_row = None
        self.current_mood = None
        self.mood_history = []
        self.opponent_action_history = []
        self.opponent_util_history = []
    
    # Helper methods as specified in the writeup
    
    def is_row_player(self):
        """Return True if this agent is the row player."""
        return self.is_row
    
    def get_mood(self):
        """Return current mood (column player only)."""
        return self.current_mood
    
    def get_action_history(self):
        """Return a list of the player's historical actions over all rounds played in the current matching so far."""
        return self.action_history.copy()
    
    def get_util_history(self):
        """Return a list of the player's historical payoffs over all rounds played in the current matching so far."""
        return self.reward_history.copy()
    
    def get_opp_action_history(self):
        """Return a list of the opponent's historical actions over all rounds played in the current matching so far."""
        return self.opponent_action_history.copy()
    
    def get_opp_util_history(self):
        """Return a list of the opponent player's historical payoffs over all rounds played in the current matching so far."""
        return self.opponent_util_history.copy()
    
    def get_mood_history(self):
        """Return a list of the column player's moods over all rounds played in the current matching so far, if you are the column player or None, if you are the row player."""
        if self.is_row_player():
            return None
        return self.mood_history.copy()
    
    def get_last_action(self):
        """Return the player's actions in the last round if a round has been played, and None otherwise."""
        return self.action_history[-1] if self.action_history else None
    
    def get_last_util(self):
        """Return the player's payoff in the last round if a round has been played, and None otherwise."""
        return self.reward_history[-1] if self.reward_history else None
    
    def get_opp_last_action(self):
        """Return the opponent's action in the last round if a round has been played, and None otherwise."""
        return self.opponent_action_history[-1] if self.opponent_action_history else None
    
    def get_opp_last_util(self):
        """Return the opponent's payoff in the last round if a round has been played, and None otherwise."""
        return self.opponent_util_history[-1] if self.opponent_util_history else None
    
    def get_last_mood(self):
        """Return your last mood in the previous round if you are the column player and a round has been played, and None otherwise."""
        if self.is_row_player():
            return None
        return self.mood_history[-1] if self.mood_history else None
    
    def row_player_calculate_util(self, row_move, col_move):
        """Return the row player's hypothetical utility given action profile (row_move, col_move)."""
        # This is a simplified implementation - in practice, this would use the actual game logic
        if row_move == self.STUBBORN and col_move == self.STUBBORN:
            return 0  # Both stubborn
        elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
            return 7  # Row stubborn, col compromise
        elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
            return 3  # Row compromise, col stubborn
        else:  # Both compromise
            return 0
    
    def col_player_calculate_util(self, row_move, col_move, mood):
        """Return the column player's hypothetical utility given action profile (row_move, col_move) and mood."""
        # This is a simplified implementation - in practice, this would use the actual game logic
        if mood == self.GOOD_MOOD:
            if row_move == self.STUBBORN and col_move == self.STUBBORN:
                return 0  # Both stubborn
            elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
                return 3  # Row stubborn, col compromise
            elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
                return 7  # Row compromise, col stubborn
            else:  # Both compromise
                return 0
        else:  # BAD_MOOD
            if row_move == self.STUBBORN and col_move == self.STUBBORN:
                return 7  # Both stubborn
            elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
                return 0  # Row stubborn, col compromise
            elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
                return 0  # Row compromise, col stubborn
            else:  # Both compromise
                return 3
    
    def col_player_good_mood_prob(self):
        """Return the probability that the column player is in a good mood."""
        return 2/3  # As specified in the writeup
    
    def add_opponent_action(self, action):
        """Add opponent's action to history (called by engine)."""
        self.opponent_action_history.append(action)
    
    def add_opponent_reward(self, reward):
        """Add opponent's reward to history (called by engine)."""
        self.opponent_util_history.append(reward)
