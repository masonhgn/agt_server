import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSIICompetitionAgent(BaseAgent):
    """Competition agent for Incomplete-Information Battle of the Sexes."""
    
    def __init__(self, name: str = "BOSIIComp"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0
        self.is_row = None  # Will be set by the game
        self.current_mood = None  # Will be set by the game
        self.mood_history = []
        self.opponent_action_history = []
        self.opponent_util_history = []
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        # Strategy depends on whether we're the row player (Alice) or column player (Bob)
        if self.is_row_player():
            # Row player strategy (Alice) - incomplete information
            return self._row_player_strategy()
        else:
            # Column player strategy (Bob) - knows his mood
            return self._column_player_strategy()
    
    def _row_player_strategy(self):
        """Strategy for the row player (Alice) who doesn't know Bob's mood."""
        # Simple strategy: mostly compromise, occasionally be stubborn
        # This can be improved with more sophisticated analysis
        
        if len(self.action_history) < 5:
            # Early game: try to cooperate
            return self.COMPROMISE
        else:
            # Analyze opponent's behavior
            recent_actions = self.get_opp_action_history()[-5:]
            if len(recent_actions) >= 3:
                # If opponent has been mostly cooperative, cooperate
                cooperations = sum(1 for a in recent_actions if a == self.COMPROMISE)
                if cooperations >= 3:
                    return self.COMPROMISE
                else:
                    # Be more cautious
                    return self.STUBBORN
            else:
                return self.COMPROMISE
    
    def _column_player_strategy(self):
        """Strategy for the column player (Bob) who knows his mood."""
        my_mood = self.get_mood()
        
        if my_mood == self.GOOD_MOOD:
            # Good mood: prefer to meet Alice
            if len(self.action_history) < 3:
                return self.COMPROMISE  # Start cooperative
            else:
                # Analyze Alice's behavior
                recent_actions = self.get_opp_action_history()[-3:]
                if len(recent_actions) >= 2:
                    cooperations = sum(1 for a in recent_actions if a == self.COMPROMISE)
                    if cooperations >= 2:
                        return self.COMPROMISE  # Alice cooperating, meet her
                    else:
                        return self.STUBBORN  # Alice not cooperating, be stubborn
                else:
                    return self.COMPROMISE
        else:
            # Bad mood: prefer to avoid Alice
            if len(self.action_history) < 3:
                return self.STUBBORN  # Start by avoiding
            else:
                # Even in bad mood, if Alice is very cooperative, might compromise
                recent_actions = self.get_opp_action_history()[-5:]
                if len(recent_actions) >= 4:
                    cooperations = sum(1 for a in recent_actions if a == self.COMPROMISE)
                    if cooperations >= 4:
                        return self.COMPROMISE  # Alice very cooperative, compromise
                    else:
                        return self.STUBBORN  # Avoid Alice
                else:
                    return self.STUBBORN
    
    def update(self, reward: float, agent_info: dict | None = None):
        """
        Update the agent's state based on the game results.
        """
        self.reward_history.append(reward)
        
        # Update opponent information if provided
        if agent_info:
            if 'opponent_action' in agent_info:
                self.opponent_action_history.append(agent_info['opponent_action'])
            if 'opponent_util' in agent_info:
                self.opponent_util_history.append(agent_info['opponent_util'])
            if 'mood' in agent_info and not self.is_row_player():
                self.mood_history.append(agent_info['mood'])
    
    # Helper methods as specified in the writeup
    def is_row_player(self):
        """Returns true if you are the row player (and thus have incomplete information)."""
        return self.is_row
    
    def get_mood(self):
        """Returns your current mood: either self.GOOD_MOOD or self.BAD_MOOD, provided you are the column player."""
        return self.current_mood
    
    def get_action_history(self):
        """Returns a list of the player's historical actions over all rounds played in the current matching so far."""
        return self.action_history.copy()
    
    def get_util_history(self):
        """Returns a list of the player's historical payoffs over all rounds played in the current matching so far."""
        return self.reward_history.copy()
    
    def get_opp_action_history(self):
        """Returns a list of the opponent's historical actions over all rounds played in the current matching so far."""
        return self.opponent_action_history.copy()
    
    def get_opp_util_history(self):
        """Returns a list of the opponent player's historical payoffs over all rounds played in the current matching so far."""
        return self.opponent_util_history.copy()
    
    def get_mood_history(self):
        """Returns a list of the column player's moods over all rounds played in the current matching so far, if you are the column player or None, if you are the row player."""
        return None if self.is_row_player() else self.mood_history.copy()
    
    def get_last_action(self):
        """Returns the player's actions in the last round if a round has been played, and None otherwise."""
        return self.action_history[-1] if self.action_history else None
    
    def get_last_util(self):
        """Returns the player's payoff in the last round if a round has been played, and None otherwise."""
        return self.reward_history[-1] if self.reward_history else None
    
    def get_opp_last_action(self):
        """Returns the opponent's action in the last round if a round has been played, and None otherwise."""
        return self.opponent_action_history[-1] if self.opponent_action_history else None
    
    def get_opp_last_util(self):
        """Returns the opponent's payoff in the last round if a round has been played, and None otherwise."""
        return self.opponent_util_history[-1] if self.opponent_util_history else None
    
    def get_last_mood(self):
        """Returns your last mood in the previous round if you are the column player and a round has been played, and None otherwise."""
        return None if self.is_row_player() else (self.mood_history[-1] if self.mood_history else None)
    
    def row_player_calculate_util(self, row_move, col_move):
        """Returns the row player's hypothetical utility given action profile (row_move, col_move)."""
        # Row player (Alice) always has the same payoffs regardless of mood
        if row_move == self.STUBBORN and col_move == self.STUBBORN:
            return 0  # Both go to lecture
        elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
            return 7  # Alice gets her preferred outcome
        elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
            return 3  # Alice compromises
        else:  # row_move == COMPROMISE and col_move == COMPROMISE
            return 0  # Both compromise
    
    def col_player_calculate_util(self, row_move, col_move, mood):
        """Returns the column player's hypothetical utility, and depending on her mood."""
        if mood == self.GOOD_MOOD:
            # Good mood: prefer to meet Alice
            if row_move == self.STUBBORN and col_move == self.STUBBORN:
                return 0  # Both go to lecture
            elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
                return 3  # Bob compromises
            elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
                return 7  # Bob gets his preferred outcome
            else:  # row_move == COMPROMISE and col_move == COMPROMISE
                return 0  # Both compromise
        else:
            # Bad mood: prefer to avoid Alice
            if row_move == self.STUBBORN and col_move == self.STUBBORN:
                return 7  # Bob avoids Alice and gets high payoff
            elif row_move == self.STUBBORN and col_move == self.COMPROMISE:
                return 0  # Bob compromises but Alice doesn't
            elif row_move == self.COMPROMISE and col_move == self.STUBBORN:
                return 0  # Bob avoids Alice but Alice compromises
            else:  # row_move == COMPROMISE and col_move == COMPROMISE
                return 3  # Both compromise, Bob gets moderate payoff
    
    def col_player_good_mood_prob(self):
        """Returns the probability that the column player is in a good mood."""
        return 2/3  # As specified in the writeup


# TODO: Give your agent a NAME 
name = "BOSIICompetitionAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = BOSIICompetitionAgent(name)
####################################################


if __name__ == "__main__":
    # Test your agent before submitting
    print("Testing BOSII Competition Agent locally...")
    print("=" * 50)
    
    # Create a 100-round local competition in which your agent competes against itself
    agent1 = BOSIICompetitionAgent("Agent1")
    agent2 = BOSIICompetitionAgent("Agent2")
    
    # Create game and run
    game = BOSIIGame(rounds=100)
    agents = [agent1, agent2]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent1.name} statistics:")
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent1.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(agent1.reward_history)}")
    print(f"Average reward: {sum(agent1.reward_history) / len(agent1.reward_history) if agent1.reward_history else 0:.3f}")
    
    print("\nLocal test completed!")
