import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.local_arena import LocalArena
from core.agents.lab04.base_lemonade_agent import BaseLemonadeAgent
from core.agents.lab04.stick_agent import StickAgent
from core.agents.lab04.random_lemonade_agent import RandomLemonadeAgent
from core.agents.lab04.always_stay_agent import AlwaysStayAgent
import random


class MyNRLAgent(BaseLemonadeAgent):
    """
    Your non-reinforcement learning agent for the Lemonade Stand game.
    
    Implement your strategy here using techniques like:
    - Fictitious Play
    - Best Response
    - Pattern recognition
    - Game theory analysis
    """
    
    def __init__(self, name):
        super().__init__(name)

    def setup(self):
        """
        Initialize your agent's internal state.
        Called once at the beginning of each game.
        """
        # TODO: Initialize any variables you need
        pass

    def get_action(self, obs):
        """
        Choose your next action based on the current observation.
        
        Parameters:
        -----------
        obs : dict
            Observation containing 'valid_actions' list
            
        Returns:
        --------
        int
            Your chosen position (0-11)
        """
        # TODO: Implement your strategy here
        # You have access to:
        # - self.get_action_history() - Your previous actions
        # - self.get_util_history() - Your previous utilities
        # - self.get_opp1_action_history() - First opponent's actions
        # - self.get_opp2_action_history() - Second opponent's actions
        # - self.get_opp1_util_history() - First opponent's utilities
        # - self.get_opp2_util_history() - Second opponent's utilities
        # - self.get_last_action() - Your last action
        # - self.get_last_util() - Your last utility
        # - self.get_opp1_last_action() - First opponent's last action
        # - self.get_opp2_last_action() - Second opponent's last action
        # - self.calculate_utils(a1, a2, a3) - Calculate utilities for three actions
        
        raise NotImplementedError("You need to implement the get_action method!")

    def update(self, reward):
        """
        Update your agent's internal state with the reward received.
        
        Parameters:
        -----------
        reward : float
            The reward received from the last action
        """
        # TODO: Update your agent's internal state if needed
        pass


# TODO: Give your agent a NAME 
name = "MyNRLAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
nrl_agent_submission = MyNRLAgent(name)
####################################################


if __name__ == "__main__":
    # Test your agent against some opponents
    from core.game.LemonadeGame import LemonadeGame
    
    arena = LocalArena(
        game_class=LemonadeGame,
        agents=[
            nrl_agent_submission,
            AlwaysStayAgent("Stay1"),
            RandomLemonadeAgent("Random2")
        ],
        num_rounds=1000,
        timeout=10
    )
    
    print("Testing Non-RL Lemonade Agent...")
    results = arena.run_tournament()
    
    # Print results
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    for _, row in results.iterrows():
        print(f"{row['Agent']}:")
        print(f"  Total Score: {row['Total Score']:.2f}")
        print(f"  Average Score: {row['Average Score']:.2f}")
        print(f"  Wins: {row['Wins']}")
        print() 