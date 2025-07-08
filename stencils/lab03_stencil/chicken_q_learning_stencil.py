#!/usr/bin/env python3
"""
Q-Learning stencil for Chicken game.
Students implement the determine_state() method to define state representation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.common.q_learning import QLearningAgent
from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_chicken_agent import RandomChickenAgent


class ChickenQLearningAgent(QLearningAgent):
    """Q-Learning agent for Chicken game."""
    
    def __init__(self, name: str = "ChickenQL", num_states: int = 2, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str | None = None):
        super().__init__(name, num_states, 2, learning_rate, discount_factor, 
                        exploration_rate, training_mode, save_path)
        self.SWERVE, self.CONTINUE = 0, 1
    
    def determine_state(self):
        """
        Determine the current state based on game history.
        
        TODO: Implement your state representation here.
        
        Some examples:
        1. Last Move: State = opponent's last action (2 states)
        2. Lookback: State = last 2 opponent actions (4 states)
        3. History: State = last N opponent actions (2^N states)
        
        Returns:
            int: State index (0 to num_states - 1)
        """
        # TODO: Implement your state representation
        # Hint: Use self.get_action_history() and self.get_opponent_last_action()
        raise NotImplementedError
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Infer opponent's action from reward and my action
        if my_last_action == self.SWERVE:
            if my_last_reward == 0:
                return self.SWERVE  # Both swerved
            elif my_last_reward == -1:
                return self.CONTINUE  # I swerved, they continued
        elif my_last_action == self.CONTINUE:
            if my_last_reward == 1:
                return self.SWERVE  # I continued, they swerved
            elif my_last_reward == -5:
                return self.CONTINUE  # Both continued
        
        return None  # Can't determine

    def get_action(self, obs):
        return 0  # Dummy action for test


if __name__ == "__main__":
    # TODO: Give your agent a name
    agent_name = "YourName_ChickenQL"
    
    # Q-Learning parameters
    num_states = 2  # TODO: Adjust based on your state representation
    learning_rate = 0.1
    discount_factor = 0.9
    exploration_rate = 0.1
    training_mode = True
    
    # Create agents
    q_agent = ChickenQLearningAgent(
        agent_name, num_states, learning_rate, discount_factor, 
        exploration_rate, training_mode
    )
    opponent = RandomChickenAgent("Random")
    
    # Create game and run
    game = ChickenGame(rounds=100)
    agents = {0: q_agent, 1: opponent}
    
    engine = Engine(game, timeout=1.0)
    final_rewards = engine.run(agents)
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{q_agent.name} statistics:")
    action_counts = [0, 0]  # Swerve, Continue
    for action in q_agent.action_history:
        action_counts[action] += 1
    
    print(f"Swerve: {action_counts[0]}, Continue: {action_counts[1]}")
    print(f"Total reward: {sum(q_agent.reward_history)}")
    print(f"Average reward: {sum(q_agent.reward_history) / len(q_agent.reward_history) if q_agent.reward_history else 0:.3f}")
    
    # Print Q-table
    print(f"\nQ-table:")
    print(q_agent.get_q_table()) 