#!/usr/bin/env python3
"""
Example solution for Lab 1 - Rock Paper Scissors
This shows what a completed implementation looks like and demonstrates the new architecture.
"""

import sys
import os
import numpy as np

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.rps_agent import RPSAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class ExampleFictitiousPlayAgent(RPSAgent):
    """Example implementation of Fictitious Play for RPS using new architecture."""
    
    def __init__(self, name: str = "ExampleFP"):
        super().__init__(name)
        self._is_fictitious_play = True  # Flag to identify this as a Fictitious Play agent
    
    def setup(self):
        """Initialize the agent for a new game."""
        self.opponent_action_counts = [0, 0, 0]
        print(f"{self.name}: Setup called - ready for new game!")
        print(f"{self.name}: Using new architecture - server calls predict() and optimize() directly!")
    
    def get_action(self, obs=None):
        """
        This method is not used in the new architecture.
        The server will call predict() and optimize() directly.
        """
        # For backward compatibility, implement the old way
        dist = self.predict()
        best_move = self.optimize(dist)
        action = self.actions[best_move]
        return action
    
    def update(self, reward=None, info=None):
        """Store the reward and update opponent action counts."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # DEMONSTRATE ALL THE NEW METHODS
        print(f"\n{self.name}: === DEMONSTRATING NEW METHODS ===")
        
        # Test get_opp_action_history()
        opp_actions = self.get_opp_action_history()
        print(f"{self.name}: get_opp_action_history() = {opp_actions}")
        
        # Test get_opp_last_action()
        opp_last_action = self.get_opp_last_action()
        print(f"{self.name}: get_opp_last_action() = {opp_last_action}")
        
        # Test get_opp_last_util()
        opp_last_util = self.get_opp_last_util()
        print(f"{self.name}: get_opp_last_util() = {opp_last_util}")
        
        # Test get_last_action()
        my_last_action = self.get_last_action()
        print(f"{self.name}: get_last_action() = {my_last_action}")
        
        # Test get_last_util()
        my_last_util = self.get_last_util()
        print(f"{self.name}: get_last_util() = {my_last_util}")
        
        # Test get_util_history()
        util_history = self.get_util_history()
        print(f"{self.name}: get_util_history() = {util_history}")
        
        # Test calculate_utils() with different combinations
        print(f"{self.name}: Testing calculate_utils():")
        for a1 in [0, 1, 2]:
            for a2 in [0, 1, 2]:
                utils = self.calculate_utils(a1, a2)
                print(f"{self.name}:   calculate_utils({a1}, {a2}) = {utils}")
        
        # Update opponent action counts using the tracked history
        if len(opp_actions) > 0:
            last_opp_action = opp_actions[-1]
            self.opponent_action_counts[last_opp_action] += 1
            print(f"{self.name}: Updated opponent action counts: {self.opponent_action_counts}")
    
    def predict(self):
        """Predict opponent's next move distribution using the new methods."""
        # Use get_opp_action_history() instead of manual tracking
        opp_actions = self.get_opp_action_history()
        
        if len(opp_actions) == 0:
            # No history yet, assume uniform distribution
            return [1/3, 1/3, 1/3]
        
        # Calculate empirical distribution from opponent's action history
        counts = [0, 0, 0]
        for action in opp_actions:
            counts[action] += 1
        
        total = sum(counts)
        return [count / total for count in counts]
    
    def optimize(self, dist):
        """Find best response to opponent's predicted distribution using calculate_utils."""
        expected_payoffs = []
        
        for my_action in self.actions:
            expected_payoff = 0
            for opp_action in self.actions:
                # Use the new calculate_utils method
                utils = self.calculate_utils(my_action, opp_action)
                my_util = utils[0]  # My utility
                expected_payoff += dist[opp_action] * my_util
            
            expected_payoffs.append(expected_payoff)
        
        return np.argmax(expected_payoffs)


class ExampleExponentialAgent(RPSAgent):
    """Example implementation of Exponential Weights for RPS using new architecture."""
    
    def __init__(self, name: str = "ExampleExp"):
        super().__init__(name)
        self._is_exponential_weights = True  # Flag to identify this as an Exponential Weights agent
    
    def setup(self):
        """Initialize the agent for a new game."""
        self.action_rewards = np.zeros(len(self.actions))
        self.action_counts = [0, 0, 0]
        self.learning_rate = 0.1  # Learning rate for exponential weights
        print(f"{self.name}: Setup called - ready for new game!")
        print(f"{self.name}: Using new architecture - server calls calc_move_probs() directly!")
    
    def get_action(self, obs=None):
        """
        This method is not used in the new architecture.
        The server will call calc_move_probs() directly and sample from the distribution.
        """
        # For backward compatibility, implement the old way
        move_probs = self.calc_move_probs()
        action = np.random.choice(self.actions, p=move_probs)
        return action
    
    def update(self, reward=None, info=None):
        """Update action rewards and counts using the new methods."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # DEMONSTRATE ALL THE NEW METHODS
        print(f"\n{self.name}: === DEMONSTRATING NEW METHODS ===")
        
        # Test get_last_action() and get_last_util() methods
        last_action = self.get_last_action()
        last_util = self.get_last_util()
        
        print(f"{self.name}: get_last_action() = {last_action}")
        print(f"{self.name}: get_last_util() = {last_util}")
        print(f"{self.name}: get_util_history() = {self.get_util_history()}")
        print(f"{self.name}: get_opp_action_history() = {self.get_opp_action_history()}")
        print(f"{self.name}: get_opp_last_action() = {self.get_opp_last_action()}")
        print(f"{self.name}: get_opp_last_util() = {self.get_opp_last_util()}")
        
        # Test calculate_utils()
        print(f"{self.name}: Testing calculate_utils():")
        utils = self.calculate_utils(0, 1)  # Rock vs Paper
        print(f"{self.name}:   calculate_utils(0, 1) = {utils}")
        
        if last_action is not None:
            self.action_rewards[last_action] += last_util
            self.action_counts[last_action] += 1
    
    @staticmethod
    def softmax(x):
        """Compute softmax values for each set of scores in x."""
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)
    
    def calc_move_probs(self):
        """Calculate move probabilities using exponential weights and new methods."""
        # Use get_util_history() instead of manual tracking
        util_history = self.get_util_history()
        
        if len(util_history) == 0:
            # No history yet, return uniform distribution
            return [1/3, 1/3, 1/3]
        
        # Calculate average rewards for each action
        avg_rewards = np.zeros(3)
        for i in range(3):
            if self.action_counts[i] > 0:
                avg_rewards[i] = self.action_rewards[i] / self.action_counts[i]
        
        # Apply exponential weights
        weighted_rewards = self.learning_rate * avg_rewards
        return self.softmax(weighted_rewards)


if __name__ == "__main__":
    print("Example Solutions for Lab 1 - Testing NEW ARCHITECTURE")
    print("=" * 60)
    print("NEW ARCHITECTURE: Server calls predict()/optimize() and calc_move_probs() directly!")
    print("=" * 60)
    
    # Test Fictitious Play
    print("\nTesting Fictitious Play vs Random:")
    print("-" * 40)
    game = RPSGame(rounds=3)  # Very short for demonstration
    agents = [
        ExampleFictitiousPlayAgent("ExampleFP"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=3)
    final_rewards = engine.run()
    
    print(f"\nFinal rewards: {final_rewards}")
    
    # Test Exponential Weights
    print("\nTesting Exponential Weights vs Random:")
    print("-" * 40)
    game = RPSGame(rounds=3)  # Very short for demonstration
    agents = [
        ExampleExponentialAgent("ExampleExp"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=3)
    final_rewards = engine.run()
    
    print(f"\nFinal rewards: {final_rewards}")
    
    print("\n" + "=" * 60)
    print("Example solutions completed!")
    print("NEW ARCHITECTURE SUCCESSFUL:")
    print("- Server calls predict() and optimize() directly for Fictitious Play")
    print("- Server calls calc_move_probs() directly for Exponential Weights")
    print("- All methods work correctly with the new architecture")
    print("Use these as reference for implementing your own agents.")
