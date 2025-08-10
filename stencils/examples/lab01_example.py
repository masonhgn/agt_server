#!/usr/bin/env python3
"""
Example solution for Lab 1 - Rock Paper Scissors
This shows what a completed implementation looks like.
"""

import sys
import os
import numpy as np

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class ExampleFictitiousPlayAgent(BaseAgent):
    """Example implementation of Fictitious Play for RPS."""
    
    def __init__(self, name: str = "ExampleFP"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.opponent_action_counts = [0, 0, 0]
    
    def get_action(self, obs):
        """Return the best response to predicted opponent action."""
        dist = self.predict()
        best_move = self.optimize(dist)
        action = self.actions[best_move]
        self.action_history.append(action)
        return action
    
    def update(self, reward, info=None):
        """Store the reward and update opponent action counts."""
        self.reward_history.append(reward)
        
        # Infer opponent's action from reward and our action
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            if reward == 0:
                opp_action = my_action  # Tie
            elif reward == 1:
                # We won - opponent played the action we beat
                if my_action == 0:  # Rock beats Scissors
                    opp_action = 2
                elif my_action == 1:  # Paper beats Rock
                    opp_action = 0
                else:  # Scissors beats Paper
                    opp_action = 1
            else:  # reward == -1
                # We lost - opponent played the action that beats us
                if my_action == 0:  # Rock loses to Paper
                    opp_action = 1
                elif my_action == 1:  # Paper loses to Scissors
                    opp_action = 2
                else:  # Scissors loses to Rock
                    opp_action = 0
            
            self.opponent_action_counts[opp_action] += 1
    
    def predict(self):
        """Predict opponent's next move distribution."""
        if sum(self.opponent_action_counts) == 0:
            # No history yet, assume uniform distribution
            return np.array([1/3, 1/3, 1/3])
        
        # Return empirical distribution of opponent's actions
        total = sum(self.opponent_action_counts)
        return np.array(self.opponent_action_counts) / total
    
    def optimize(self, dist):
        """Find best response to opponent's predicted distribution."""
        expected_payoffs = np.zeros(3)
        
        for my_action in self.actions:
            for opp_action in self.actions:
                # RPS payoff matrix
                if my_action == opp_action:
                    payoff = 0
                elif (my_action == 0 and opp_action == 2) or \
                     (my_action == 1 and opp_action == 0) or \
                     (my_action == 2 and opp_action == 1):
                    payoff = 1  # Win
                else:
                    payoff = -1  # Lose
                
                expected_payoffs[my_action] += dist[opp_action] * payoff
        
        return np.argmax(expected_payoffs)


class ExampleExponentialAgent(BaseAgent):
    """Example implementation of Exponential Weights for RPS."""
    
    def __init__(self, name: str = "ExampleExp"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.action_rewards = np.zeros(len(self.actions))
        self.action_counts = [0, 0, 0]
        self.learning_rate = 0.1  # Learning rate for exponential weights
    
    def get_action(self, obs):
        """Return an action based on exponential weights strategy."""
        move_probs = self.calc_move_probs()
        action = np.random.choice(self.actions, p=move_probs)
        self.action_history.append(action)
        return action
    
    def update(self, reward, info=None):
        """Update action rewards and counts."""
        self.reward_history.append(reward)
        
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
    
    @staticmethod
    def softmax(x):
        """Compute softmax values for each set of scores in x."""
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)
    
    def calc_move_probs(self):
        """Calculate move probabilities using exponential weights."""
        if sum(self.action_counts) == 0:
            # No history yet, return uniform distribution
            return np.array([1/3, 1/3, 1/3])
        
        # Calculate average rewards for each action
        avg_rewards = np.zeros(3)
        for i in range(3):
            if self.action_counts[i] > 0:
                avg_rewards[i] = self.action_rewards[i] / self.action_counts[i]
        
        # Apply exponential weights
        weighted_rewards = self.learning_rate * avg_rewards
        return self.softmax(weighted_rewards)


if __name__ == "__main__":
    print("Example Solutions for Lab 1")
    print("=" * 40)
    
    # Test Fictitious Play
    print("\nTesting Fictitious Play vs Random:")
    game = RPSGame(rounds=100)
    agents = [
        ExampleFictitiousPlayAgent("ExampleFP"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print detailed statistics for FP
    fp_agent = agents[0]
    action_counts = [0, 0, 0]  # Rock, Paper, Scissors
    for action in fp_agent.action_history:
        action_counts[action] += 1
    
    print(f"\n{fp_agent.name} statistics:")
    print(f"Rock: {action_counts[0]}, Paper: {action_counts[1]}, Scissors: {action_counts[2]}")
    print(f"Total reward: {sum(fp_agent.reward_history)}")
    print(f"Average reward: {sum(fp_agent.reward_history) / len(fp_agent.reward_history):.3f}")
    
    # Test Exponential Weights
    print("\nTesting Exponential Weights vs Random:")
    game = RPSGame(rounds=100)
    agents = [
        ExampleExponentialAgent("ExampleExp"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print detailed statistics for EW
    ew_agent = agents[0]
    action_counts = [0, 0, 0]  # Rock, Paper, Scissors
    for action in ew_agent.action_history:
        action_counts[action] += 1
    
    print(f"\n{ew_agent.name} statistics:")
    print(f"Rock: {action_counts[0]}, Paper: {action_counts[1]}, Scissors: {action_counts[2]}")
    print(f"Total reward: {sum(ew_agent.reward_history)}")
    print(f"Average reward: {sum(ew_agent.reward_history) / len(ew_agent.reward_history):.3f}")
    
    # Print action-specific statistics for EW
    print(f"\n{ew_agent.name} action-specific statistics:")
    for i, action_name in enumerate(["Rock", "Paper", "Scissors"]):
        if ew_agent.action_counts[i] > 0:
            avg_reward = ew_agent.action_rewards[i] / ew_agent.action_counts[i]
            print(f"{action_name}: {ew_agent.action_counts[i]} plays, avg reward: {avg_reward:.3f}")
        else:
            print(f"{action_name}: 0 plays")
    
    print("\nExample solutions completed!")
    print("Use these as reference for implementing your own agents.") 