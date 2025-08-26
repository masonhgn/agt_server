import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class MyLemonadeAgent(BaseAgent):
    """
    Your main competition agent for the Lemonade Stand game.
    
    This is the agent that will be submitted for the competition.
    You can implement any strategy you like here.
    """
    
    def __init__(self, name: str = "MyLemonadeAgent"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, opponent_positions=None):
        """
        Choose your next action based on the current game state.
        
        Parameters:
        -----------
        opponent_positions : list, optional
            List of opponent positions (e.g., [3, 7] for 2 opponents)
            
        Returns:
        --------
        int
            Your chosen position (0-11)
        """
        # TODO: Implement your competition strategy here!
        # You can use any combination of:
        # - Fictitious Play
        # - Best Response
        # - Pattern recognition
        # - Game theory analysis
        # - Q-Learning
        # - Or any other approach you think will work well
        
        raise NotImplementedError("Implement your competition strategy here!")
    
    def update(self, reward: float, info=None):
        """
        Update your agent's internal state with the reward received.
        
        Parameters:
        -----------
        reward : float
            The reward received from the last action
        info : dict, optional
            Additional information from the game
        """
        # Update reward history
        self.reward_history.append(reward)
        
        # TODO: Add any additional state updates your strategy needs
        pass
    
    def _circular_distance(self, pos1, pos2):
        """Helper method to calculate circular distance between two positions."""
        direct_distance = abs(pos1 - pos2)
        circular_distance = min(direct_distance, 12 - direct_distance)
        return circular_distance


# TODO: Give your agent a NAME 
name = "MyLemonadeAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = MyLemonadeAgent(name)
####################################################


if __name__ == "__main__":
    # Test your agent locally
    from core.game.LemonadeGame import LemonadeGame
    from core.engine import Engine
    
    print("Testing MyLemonadeAgent locally...")
    print("=" * 50)
    
    # Create a simple test with 3 copies of your agent
    agents = [MyLemonadeAgent(f"TestAgent_{i}") for i in range(3)]
    game = LemonadeGame(rounds=1000)
    engine = Engine(game, agents)
    
    print("Running 1000-round local competition...")
    final_rewards = engine.run()
    
    print("Final rewards:")
    for i, reward in enumerate(final_rewards):
        print(f"Agent {i}: {reward:.2f}")
    
    print("\nLocal test completed!")
