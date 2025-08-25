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

from core.agents.common.rps_agent import RPSAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class ExampleFictitiousPlayAgent(RPSAgent):
    """Example implementation of Fictitious Play for RPS."""
    
    def setup(self):
        """Initialize the agent for a new game."""
        self.opponent_action_counts = [0, 0, 0]
        print(f"{self.name}: Setup called - ready for new game!")
    
    def get_action(self, obs=None):
        """Return the best response to predicted opponent action."""
        dist = self.predict()
        best_move = self.optimize(dist)
        action = self.actions[best_move]
        return action
    
    def update(self, reward=None, info=None):
        """Store the reward and update opponent action counts."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # Use the new get_opp_action_history() method
        opp_actions = self.get_opp_action_history()
        if len(opp_actions) > 0:
            last_opp_action = opp_actions[-1]
            self.opponent_action_counts[last_opp_action] += 1
            
            # Demonstrate using the new methods
            print(f"{self.name}: Last opponent action: {last_opp_action}")
            print(f"{self.name}: My last action: {self.get_last_action()}")
            print(f"{self.name}: My last utility: {self.get_last_util()}")
            print(f"{self.name}: Opponent action history length: {len(opp_actions)}")
    
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
    """Example implementation of Exponential Weights for RPS."""
    
    def setup(self):
        """Initialize the agent for a new game."""
        self.action_rewards = np.zeros(len(self.actions))
        self.action_counts = [0, 0, 0]
        self.learning_rate = 0.1  # Learning rate for exponential weights
        print(f"{self.name}: Setup called - ready for new game!")
    
    def get_action(self, obs=None):
        """Return an action based on exponential weights strategy."""
        move_probs = self.calc_move_probs()
        action = np.random.choice(self.actions, p=move_probs)
        return action
    
    def update(self, reward=None, info=None):
        """Update action rewards and counts using the new methods."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # Use get_last_action() and get_last_util() methods
        last_action = self.get_last_action()
        last_util = self.get_last_util()
        
        if last_action is not None:
            self.action_rewards[last_action] += last_util
            self.action_counts[last_action] += 1
            
            # Demonstrate using the new methods
            print(f"{self.name}: Last action: {last_action}")
            print(f"{self.name}: Last utility: {last_util}")
            print(f"{self.name}: Total utilities: {sum(self.get_util_history())}")
    
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


class ExampleChickenAgent(RPSAgent):
    """Example implementation for Chicken game (using RPS for testing)."""
    
    def setup(self):
        """Initialize the agent for a new game."""
        print(f"{self.name}: Setup called - ready for Chicken game!")
    
    def get_action(self, obs=None):
        """Return an action for Chicken game."""
        # Simple strategy: swerve 70% of the time
        import random
        if random.random() < 0.7:
            return 0  # Swerve
        else:
            return 1  # Continue
    
    def update(self, reward=None, info=None):
        """Update with reward and demonstrate new methods."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # Demonstrate all the new methods
        print(f"{self.name}: Action history: {self.get_action_history()}")
        print(f"{self.name}: Utility history: {self.get_util_history()}")
        print(f"{self.name}: Opponent action history: {self.get_opp_action_history()}")
        print(f"{self.name}: Opponent utility history: {self.get_opp_reward_history()}")
        
        # Test calculate_utils method
        utils = self.calculate_utils(0, 1)  # Swerve vs Continue
        print(f"{self.name}: calculate_utils(0, 1) = {utils}")


if __name__ == "__main__":
    print("Example Solutions for Lab 1 - Testing New Methods")
    print("=" * 60)
    
    # Test Fictitious Play
    print("\nTesting Fictitious Play vs Random:")
    print("-" * 40)
    game = RPSGame(rounds=10)  # Shorter for demonstration
    agents = [
        ExampleFictitiousPlayAgent("ExampleFP"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=10)
    final_rewards = engine.run()
    
    print(f"\nFinal rewards: {final_rewards}")
    
    # Test Exponential Weights
    print("\nTesting Exponential Weights vs Random:")
    print("-" * 40)
    game = RPSGame(rounds=10)  # Shorter for demonstration
    agents = [
        ExampleExponentialAgent("ExampleExp"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=10)
    final_rewards = engine.run()
    
    print(f"\nFinal rewards: {final_rewards}")
    
    # Test Chicken Agent
    print("\nTesting Chicken Agent vs Random:")
    print("-" * 40)
    game = RPSGame(rounds=5)  # Very short for demonstration
    agents = [
        ExampleChickenAgent("ExampleChicken"),
        RandomAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=5)
    final_rewards = engine.run()
    
    print(f"\nFinal rewards: {final_rewards}")
    
    print("\n" + "=" * 60)
    print("Example solutions completed!")
    print("All new methods have been demonstrated:")
    print("- calculate_utils(a1, a2)")
    print("- get_opp_action_history()")
    print("- get_util_history()")
    print("- get_last_util()")
    print("- get_last_action()")
    print("- get_opp_last_action()")
    print("- get_opp_last_util()")
    print("- setup()")
    print("Use these as reference for implementing your own agents.") 