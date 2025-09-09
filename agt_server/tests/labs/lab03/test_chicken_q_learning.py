#!/usr/bin/env python3
"""
Comprehensive student-style test for Chicken Q-Learning.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import numpy as np
from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_chicken_agent import RandomChickenAgent
from core.agents.lab03.swerve_agent import SwerveAgent
from core.agents.lab03.continue_agent import ContinueAgent
from core.agents.common.q_learning import QLearningAgent

# Student implementation of Chicken Q-Learning Agent
class StudentChickenQLearningAgent(QLearningAgent):
    def __init__(self, name: str = "StudentChickenQL", num_states: int = 2, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str | None = None):
        super().__init__(name, num_states, 2, learning_rate, discount_factor, 
                         exploration_rate, training_mode, save_path)
        self.SWERVE, self.CONTINUE = 0, 1
    
    def determine_state(self):
        # Simple state: last opponent action (0 or 1), or 0 if no history
        if len(self.action_history) == 0:
            return 0
        opp_last = self.get_opponent_last_action()
        if opp_last is None:
            return 0
        return opp_last
    
    def get_opponent_last_action(self):
        if len(self.action_history) == 0:
            return None
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        if my_last_action == self.SWERVE:
            if my_last_reward == 0:
                return self.SWERVE
            elif my_last_reward == -1:
                return self.CONTINUE
        elif my_last_action == self.CONTINUE:
            if my_last_reward == 1:
                return self.SWERVE
            elif my_last_reward == -5:
                return self.CONTINUE
        return None

def test_chicken_q_learning():
    print("Comprehensive Chicken Q-Learning Test")
    print("=" * 50)
    
    q_agent = StudentChickenQLearningAgent("TestQL", num_states=2)
    random_agent = RandomChickenAgent("Random")
    swerve_agent = SwerveAgent("Swerve")
    continue_agent = ContinueAgent("Continue")
    
    opponents = [
        ("Random", random_agent),
        ("Swerve", swerve_agent),
        ("Continue", continue_agent)
    ]
    
    for opponent_name, opponent in opponents:
        print(f"\nTesting Q-Learning Agent vs {opponent_name}:")
        game = ChickenGame()
        agents = [q_agent, opponent]
        engine = Engine(game, agents, rounds=100)
        q_agent.reset()
        opponent.reset()
        final_rewards = engine.run()
        print(f"  Final rewards: {final_rewards}")
        print(f"  Q Agent total reward: {sum(q_agent.reward_history)}")
        print(f"  Q Agent average reward: {np.mean(q_agent.reward_history):.3f}")
        action_counts = [0, 0]
        for action in q_agent.action_history:
            action_counts[action] += 1
        print(f"  Swerve: {action_counts[0]}, Continue: {action_counts[1]}")
        print(f"  Q-table shape: {q_agent.get_q_table().shape}")
        assert q_agent.get_q_table().shape == (2, 2), "Q-table shape should be (2, 2)"
        assert len(q_agent.action_history) == 100, "Agent should have played 100 actions"
        assert len(q_agent.reward_history) == 100, "Agent should have 100 rewards"
    
    print("\nPASS: All Chicken Q-Learning tests completed successfully!")

if __name__ == "__main__":
    test_chicken_q_learning() 