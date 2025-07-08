import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        Consider whether you're the row or column player and the mood information.
        """
        # Determine if we're row or column player based on player ID
        if self.is_row is None:
            # This is a simplified way to determine player type
            # In a real implementation, this would come from the game
            self.is_row = True  # Assume row player for now
        
        # TODO: Implement your strategy here
        # Consider:
        # - Are you row or column player?
        # - What's your current mood (if column player)?
        # - What's the mood history?
        # - What's your current state?
        raise NotImplementedError
    
    def update(self, reward: float, agent_info: dict | None = None):
        """
        Minimal update for testing: just store the reward received.
        """
        self.reward_history.append(reward)
    
    def is_row_player(self):
        """Return True if this agent is the row player."""
        return self.is_row
    
    def get_mood(self):
        """Return current mood (column player only)."""
        return self.current_mood
    
    def get_last_mood(self):
        """Return mood from last round (column player only)."""
        return self.mood_history[-1] if self.mood_history else None
    
    def get_mood_history(self):
        """Return complete mood history (column player only)."""
        return self.mood_history.copy()
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # This is a simplified inference - in BOSII it's more complex
        # due to mood-dependent payoffs
        if my_last_action == self.COMPROMISE:
            if my_last_reward == 0:
                return self.COMPROMISE  # Both compromised
            elif my_last_reward == 3:
                return self.STUBBORN     # I compromised, they were stubborn
        elif my_last_action == self.STUBBORN:
            if my_last_reward == 7:
                return self.COMPROMISE   # I was stubborn, they compromised
            elif my_last_reward == 0:
                return self.STUBBORN     # Both were stubborn
        
        return None  # Can't determine


if __name__ == "__main__":
    # TODO: Give your agent a name
    agent_name = "YourName_BOSIIComp"
    
    # Create agents
    agent = BOSIICompetitionAgent(agent_name)
    opponent = RandomBOSAgent("Random")
    
    # Create game and run
    game = BOSIIGame(rounds=100)
    agents = [agent, opponent]
    
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