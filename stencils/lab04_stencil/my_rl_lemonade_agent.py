import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.common.q_learning import QLearningAgent
from core.local_arena import LocalArena
from core.agents.lab04.base_lemonade_agent import BaseLemonadeAgent
from core.agents.lab04.stick_agent import StickAgent
from core.agents.lab04.random_lemonade_agent import RandomLemonadeAgent
from core.agents.lab04.always_stay_agent import AlwaysStayAgent
import numpy as np


class MyRLAgent(QLearningAgent):
    """
    Your reinforcement learning agent for the Lemonade Stand game.
    
    This agent uses Q-Learning to learn optimal strategies through experience.
    You need to implement the state determination logic.
    """
    
    def __init__(self, name, num_possible_states, num_possible_actions, initial_state, 
                 learning_rate, discount_factor, exploration_rate, training_mode, save_path=None):
        super().__init__(name, num_possible_states, num_possible_actions,
                         learning_rate, discount_factor, exploration_rate, training_mode, save_path)
        
        # You can add additional initialization here if needed
        pass

    def determine_state(self):
        """
        Determine the current state based on the game history.
        
        This is the key method you need to implement. The state should capture
        the relevant information for making decisions.
        
        Returns:
        --------
        int
            The current state (must be between 0 and num_possible_states - 1)
        """
        # TODO: Implement state determination logic
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
        
        # Example: Simple state based on last opponent actions
        # opp1_last = self.get_opp1_last_action()
        # opp2_last = self.get_opp2_last_action()
        # if opp1_last is None or opp2_last is None:
        #     return 0  # Initial state
        # return opp1_last * 12 + opp2_last  # State based on opponent positions
        
        raise NotImplementedError("You need to implement the determine_state method!")

    def get_action(self, obs):
        return 0  # Dummy action for test


# TODO: Give your agent a NAME 
name = "MyRLAgent"  # TODO: PLEASE NAME ME D:


# TODO: Determine how many states that your agent will be using
# This depends on your state representation in determine_state()
NUM_POSSIBLE_STATES = 144  # Example: 12 * 12 for opponent positions
INITIAL_STATE = 0


# Lemonade Stand has 12 possible actions [0 - 11]
NUM_POSSIBLE_ACTIONS = 12
LEARNING_RATE = 0.05
DISCOUNT_FACTOR = 0.90
EXPLORATION_RATE = 0.05

################### SUBMISSION #####################
rl_agent_submission = MyRLAgent(name, NUM_POSSIBLE_STATES, NUM_POSSIBLE_ACTIONS, INITIAL_STATE, 
                                LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, False, "my-qtable.npy")
####################################################


if __name__ == "__main__":
    from core.game.LemonadeGame import LemonadeGame
    
    # Training phase
    print("TRAINING PHASE")
    print("=" * 50)
    rl_agent_submission.set_training_mode(True)
    
    if rl_agent_submission.training_mode:
        training_arena = LocalArena(
            game_class=LemonadeGame,
            agents=[
                rl_agent_submission,
                StickAgent("Stick1"),
                RandomLemonadeAgent("Random1"),
                AlwaysStayAgent("Stay1"),
                RandomLemonadeAgent("Random2")
            ],
            num_rounds=100000,  # More rounds for training
            timeout=1,
            verbose=False
        )
        
        training_results = training_arena.run_tournament()
        print("Training completed!")
        # Find our agent's score
        for _, row in training_results.iterrows():
            if row['Agent'] == name:
                print(f"Training score: {row['Total Score']:.2f}")
                break
        else:
            print("Training score: N/A")
    
    # Testing phase
    print("\nTESTING PHASE")
    print("=" * 50)
    rl_agent_submission.set_training_mode(False)
    
    test_arena = LocalArena(
        game_class=LemonadeGame,
        agents=[
            rl_agent_submission,
            StickAgent("Stick1"),
            RandomLemonadeAgent("Random1"),
            AlwaysStayAgent("Stay1"),
            RandomLemonadeAgent("Random2")
        ],
        num_rounds=1000,
        timeout=10
    )
    
    test_results = test_arena.run_tournament()
    
    # Print results
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    for _, row in test_results.iterrows():
        print(f"{row['Agent']}:")
        print(f"  Total Score: {row['Total Score']:.2f}")
        print(f"  Average Score: {row['Average Score']:.2f}")
        print(f"  Wins: {row['Wins']}")
        print() 