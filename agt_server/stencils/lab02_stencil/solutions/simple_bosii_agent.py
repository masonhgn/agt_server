import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.bosii_agent import BOSIIAgent
from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class SimpleBOSIIAgent(BOSIIAgent):
    """Simple BOSII agent for testing purposes."""
    
    def __init__(self, name: str = "SimpleBOSII"):
        super().__init__(name)
    
    def get_action(self, obs=None, opponent_last_move=None, player_type=None, mood=None):
        """
        Simple strategy: 
        - Row player: Always compromise
        - Column player: Compromise in good mood, stubborn in bad mood
        """
        # Call parent to handle both interfaces
        super().get_action(obs, opponent_last_move, player_type, mood)
        
        if self.is_row_player():
            # Row player: always compromise
            return self.COMPROMISE
        else:
            # Column player: mood-dependent strategy
            if self.get_mood() == self.GOOD_MOOD:
                return self.COMPROMISE
            else:
                return self.STUBBORN
    

    



if __name__ == "__main__":
    # Test the simple BOSII agent
    print("Testing Simple BOSII Agent locally...")
    print("=" * 50)
    
    # Create agents for testing
    agent = SimpleBOSIIAgent("SimpleBOSII")
    opponent = RandomBOSAgent("RandomAgent")
    
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
    print(f"Is row player: {agent.is_row_player()}")
    if agent.mood_history:
        print(f"Mood history: {agent.mood_history}")
    
    print("\nLocal test completed!")
