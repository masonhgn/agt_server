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
import random


class ExampleNRLAgent(BaseLemonadeAgent):
    """
    Example non-reinforcement learning agent using Fictitious Play.
    
    This agent tracks opponent action frequencies and plays a best response
    to the empirical distribution of opponent actions.
    """
    
    def setup(self):
        """Initialize opponent action frequency tracking."""
        self.opp1_frequencies = np.zeros(12)
        self.opp2_frequencies = np.zeros(12)
        self.alpha = 0.8  # Decay factor for old observations
    
    def get_action(self, obs):
        """Choose action using Fictitious Play strategy."""
        # If we have no history, choose randomly
        if len(self.get_opp1_action_history()) == 0:
            return random.randint(0, 11)
        
        # Update frequency estimates with decay
        self.opp1_frequencies *= self.alpha
        self.opp2_frequencies *= self.alpha
        
        # Add latest observations
        opp1_last = self.get_opp1_last_action()
        opp2_last = self.get_opp2_last_action()
        
        if opp1_last is not None:
            self.opp1_frequencies[opp1_last] += 1
        if opp2_last is not None:
            self.opp2_frequencies[opp2_last] += 1
        
        # Calculate expected opponent positions
        opp1_exp = int(np.argmax(self.opp1_frequencies))
        opp2_exp = int(np.argmax(self.opp2_frequencies))
        
        # Find the best response: position between opponents
        if opp1_exp == opp2_exp:
            # If opponents are at same position, go to opposite side
            return (opp1_exp + 6) % 12
        else:
            # Find middle position between opponents
            pos1, pos2 = min(opp1_exp, opp2_exp), max(opp1_exp, opp2_exp)
            if pos2 - pos1 <= 6:
                # Opponents are close, go to middle
                return (pos1 + pos2) // 2
            else:
                # Opponents are far apart, go to opposite side of closer one
                return (pos1 + 6) % 12
    
    def update(self, reward):
        """No additional learning needed for this strategy."""
        pass


class ExampleRLAgent(QLearningAgent, BaseLemonadeAgent):
    """
    Example reinforcement learning agent using Q-Learning.
    
    This agent uses the last actions of both opponents as the state
    representation and learns optimal responses through Q-Learning.
    """
    
    def __init__(self, name, num_possible_states, num_possible_actions, initial_state, 
                 learning_rate, discount_factor, exploration_rate, training_mode, save_path=None):
        QLearningAgent.__init__(self, name, num_possible_states, num_possible_actions,
                               learning_rate, discount_factor, exploration_rate, training_mode, save_path)
        BaseLemonadeAgent.__init__(self, name)
    
    def determine_state(self):
        """
        Determine state based on last opponent actions.
        
        State = opp1_last_action * 12 + opp2_last_action
        This gives us 144 possible states (12 * 12)
        """
        opp1_last = self.get_opp1_last_action()
        opp2_last = self.get_opp2_last_action()
        
        # If we don't have opponent history yet, use initial state
        if opp1_last is None or opp2_last is None:
            return 0
        
        # Create state from opponent positions
        state = opp1_last * 12 + opp2_last
        return state


# Example usage
if __name__ == "__main__":
    from core.game.LemonadeGame import LemonadeGame
    
    print("Testing Example Non-RL Agent...")
    print("=" * 50)
    
    # Test non-RL agent
    nrl_agent = ExampleNRLAgent("ExampleNRL")
    arena = LocalArena(
        game_class=LemonadeGame,
        agents=[
            nrl_agent,
            StickAgent("Stick1"),
            RandomLemonadeAgent("Random1"),
            AlwaysStayAgent("Stay1"),
            RandomLemonadeAgent("Random2")
        ],
        num_rounds=1000,
        timeout=10
    )
    
    results = arena.run_tournament()
    
    print("Non-RL Agent Results:")
    for _, row in results.iterrows():
        if row['Agent'] == "ExampleNRL":
            print(f"  Total Score: {row['Total Score']:.2f}")
            print(f"  Average Score: {row['Average Score']:.2f}")
            print(f"  Wins: {row['Wins']}")
            break
    
    print("\n" + "=" * 50)
    print("Testing Example RL Agent...")
    print("=" * 50)
    
    # Test RL agent
    rl_agent = ExampleRLAgent("ExampleRL", 144, 12, 0, 0.05, 0.90, 0.05, False, "example-qtable.npy")
    
    # Training phase
    print("Training phase...")
    rl_agent.set_training_mode(True)
    training_arena = LocalArena(
        game_class=LemonadeGame,
        agents=[
            rl_agent,
            StickAgent("Stick1"),
            RandomLemonadeAgent("Random1"),
            AlwaysStayAgent("Stay1"),
            RandomLemonadeAgent("Random2")
        ],
        num_rounds=50000,
        timeout=1,
        verbose=False
    )
    
    training_results = training_arena.run_tournament()
    
    # Testing phase
    print("Testing phase...")
    rl_agent.set_training_mode(False)
    test_arena = LocalArena(
        game_class=LemonadeGame,
        agents=[
            rl_agent,
            StickAgent("Stick1"),
            RandomLemonadeAgent("Random1"),
            AlwaysStayAgent("Stay1"),
            RandomLemonadeAgent("Random2")
        ],
        num_rounds=1000,
        timeout=10
    )
    
    test_results = test_arena.run_tournament()
    
    print("RL Agent Results:")
    for _, row in test_results.iterrows():
        if row['Agent'] == "ExampleRL":
            print(f"  Total Score: {row['Total Score']:.2f}")
            print(f"  Average Score: {row['Average Score']:.2f}")
            print(f"  Wins: {row['Wins']}")
            break 