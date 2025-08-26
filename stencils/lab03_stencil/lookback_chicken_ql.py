#!/usr/bin/env python3
"""
Lookback Chicken Q-Learning Agent.
State space representing the opponent's past two actions.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class LookbackChickenQL(QLearning):
    """Q-Learning agent with state space based on opponent's last two actions."""
    
    def __init__(self, name: str = "LookbackChickenQL"):
        # 4 states: opponent's last two actions (00, 01, 10, 11)
        # 2 actions: swerve (0) or continue (1)
        super().__init__(name, num_possible_states=4, num_possible_actions=2,
                        initial_state=0, learning_rate=0.05, discount_factor=0.90,
                        exploration_rate=0.05, training_mode=True, save_path="lookback-q-table.npy")
    
    def determine_state(self):
        """
        State is opponent's last two actions.
        State 0: opponent swerved twice in a row
        State 1: opponent swerved then continued
        State 2: opponent continued then swerved
        State 3: opponent continued twice in a row
        """
        if len(self.action_history) < 2:
            return 0  # Initial state
        
        # Infer opponent's last two actions from our rewards
        my_last_action = self.action_history[-1]
        my_second_last_action = self.action_history[-2]
        my_last_reward = self.reward_history[-1]
        my_second_last_reward = self.reward_history[-2]
        
        # Chicken payoff matrix (row player, column player):
        # S\C  S  C
        # S    0  -1
        # C    1  -5
        
        # Determine opponent's last action
        if my_last_action == 0:  # I swerved
            if my_last_reward == 0:
                opp_last_action = 0  # Opponent also swerved
            elif my_last_reward == -1:
                opp_last_action = 1  # Opponent continued
            else:
                opp_last_action = 0  # Default
        else:  # I continued
            if my_last_reward == 1:
                opp_last_action = 0  # Opponent swerved
            elif my_last_reward == -5:
                opp_last_action = 1  # Opponent also continued
            else:
                opp_last_action = 0  # Default
        
        # Determine opponent's second-to-last action
        if my_second_last_action == 0:  # I swerved
            if my_second_last_reward == 0:
                opp_second_last_action = 0  # Opponent also swerved
            elif my_second_last_reward == -1:
                opp_second_last_action = 1  # Opponent continued
            else:
                opp_second_last_action = 0  # Default
        else:  # I continued
            if my_second_last_reward == 1:
                opp_second_last_action = 0  # Opponent swerved
            elif my_second_last_reward == -5:
                opp_second_last_action = 1  # Opponent also continued
            else:
                opp_second_last_action = 0  # Default
        
        # Combine into state: 2 * second_last + last
        return 2 * opp_second_last_action + opp_last_action


# TODO: Give your agent a NAME 
name = "LookbackChickenQL"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = LookbackChickenQL(name)
####################################################


if __name__ == "__main__":
    print("Testing Lookback Chicken Q-Learning Agent...")
    print("=" * 50)
    
    # Import required modules
    from core.engine import Engine
    from core.game.ChickenGame import ChickenGame
    from basic_chicken_agent import BasicChickenAgent
    
    # Create agents
    agent = LookbackChickenQL("LookbackQL")
    opponent = BasicChickenAgent("BasicChicken")
    
    # Training phase
    print("TRAINING PHASE (20,000 rounds)")
    agent.set_training_mode(True)
    game = ChickenGame(rounds=20000)
    engine = Engine(game, [agent, opponent], rounds=20000)
    engine.run()
    
    # Testing phase
    print("\nTESTING PHASE (300 rounds)")
    agent.set_training_mode(False)
    game = ChickenGame(rounds=300)
    engine = Engine(game, [agent, opponent], rounds=300)
    final_rewards = engine.run()
    
    # Print results
    print(f"\nFinal rewards: {final_rewards}")
    print(f"Agent average reward: {sum(agent.reward_history[-300:]) / 300:.3f}")
    print(f"Agent total reward: {sum(agent.reward_history[-300:])}")
    
    # Print action distribution
    action_counts = [0, 0]
    for action in agent.action_history[-300:]:
        action_counts[action] += 1
    print(f"Action distribution: Swerve={action_counts[0]}, Continue={action_counts[1]}")
    
    print("\nTest completed!")
