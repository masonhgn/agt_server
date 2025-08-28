import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSIICompetitionAgent(BaseAgent):
    """Competition agent for Battle of the Sexes with Incomplete Information."""
    
    def __init__(self, name: str = "BOSIIComp"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0
        self.is_row = None  # Will be set based on player ID
        self.current_mood = None  # Column player's mood (if column player)
        self.mood_history = []  # Column player's mood history
        self.opponent_action_history = []  # Opponent's action history
        self.opponent_util_history = []  # Opponent's utility history
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        Consider whether you're the row or column player and the mood information.
        """
        # TODO: Implement your strategy here
        # Consider:
        # - Are you row or column player?
        # - What's your current mood (if column player)?
        # - What's the mood history?
        # - What's your current state?
        raise NotImplementedError
    
    def update(self, reward: float, agent_info: dict | None = None):
        """
        Update the agent with the reward and info from the last action.
        """
        self.reward_history.append(reward)
        
        # Update opponent information if available
        if agent_info:
            if 'opponent_action' in agent_info:
                self.opponent_action_history.append(agent_info['opponent_action'])
            if 'opponent_util' in agent_info:
                self.opponent_util_history.append(agent_info['opponent_util'])
            if 'mood' in agent_info and not self.is_row_player():
                self.mood_history.append(agent_info['mood'])
    
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


# TODO: Give your agent a NAME 
name = "BOSIICompetitionAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = BOSIICompetitionAgent(name)
####################################################


if __name__ == "__main__":
    # Test your agent before submitting
    print("Testing BOSII Competition Agent locally...")
    print("=" * 50)
    
    # Create multiple instances for BOSII testing (appropriate since it's a different game type)
    agent = BOSIICompetitionAgent("CompetitionAgent")
    opponent1 = BOSIICompetitionAgent("Agent1")
    opponent2 = BOSIICompetitionAgent("Agent2")
    
    # Create game and run
    game = BOSIIGame(rounds=100)
    agents = [agent, opponent1, opponent2]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent.name} statistics:")
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(agent.reward_history)}")
    print(f"Average reward: {sum(agent.reward_history) / len(agent.reward_history) if agent.reward_history else 0:.3f}")
    print(f"Final state: {agent.curr_state}")
    print(f"Is row player: {agent.is_row_player()}")
    if agent.mood_history:
        print(f"Mood history: {agent.mood_history}")
    
    print("\nLocal test completed!")
