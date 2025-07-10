#!/usr/bin/env python3
"""
Example solutions for Lab 3 - Q-Learning and Collusion
This shows what completed implementations look like.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import numpy as np
from core.agents.common.q_learning import QLearningAgent
from core.engine import Engine
from core.game.ChickenGame import ChickenGame
from core.agents.lab03.random_chicken_agent import RandomChickenAgent


class ExampleChickenQLearningAgent(QLearningAgent):
    """Example implementation of Q-Learning for Chicken game."""
    
    def __init__(self, name: str = "ExampleChickenQL", num_states: int = 2, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str | None = None):
        super().__init__(name, num_states, 2, learning_rate, discount_factor, 
                        exploration_rate, training_mode, save_path)
        self.SWERVE, self.CONTINUE = 0, 1
    
    def determine_state(self):
        """
        Simple state representation: opponent's last action.
        State 0: Opponent swerved last time
        State 1: Opponent continued last time
        """
        if len(self.action_history) == 0:
            return 0  # Initial state
        
        opp_last_action = self.get_opponent_last_action()
        if opp_last_action is None:
            return 0  # Default to state 0 if can't determine
        
        return opp_last_action  # State = opponent's last action
    
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

    def update(self, reward, info=None):
        super().update(reward, info)
        pass


class ExampleCollusionQLearningAgent(QLearningAgent):
    """Example implementation of Q-Learning for collusion environment."""
    
    def __init__(self, name: str = "ExampleCollusionQL", num_states: int = 10, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str | None = None):
        super().__init__(name, num_states, 10, learning_rate, discount_factor, 
                        exploration_rate, training_mode, save_path)
        
        # Pricing parameters
        self.price_range = np.linspace(1.0, 2.0, 10)  # 10 price levels
        self.bertrand_price = 1.45  # Competitive price
        self.monopoly_price = 1.95  # Collusive price
        
        # Market parameters
        self.a_i = 2.0  # Product quality
        self.a_0 = 1.0  # Outside option
        self.mu = 0.5   # Price sensitivity
        self.c_i = 1.0  # Marginal cost
    
    def determine_state(self):
        """
        State representation: opponent's last price level.
        This creates 10 states, one for each possible opponent price.
        """
        if len(self.action_history) == 0:
            return 0  # Initial state
        
        # For simplicity, assume we can observe opponent's last action
        # In practice, this would be inferred from market outcomes
        if hasattr(self, 'opponent_last_action'):
            return self.opponent_last_action
        else:
            return 0  # Default state
    
    def get_price(self, action):
        """Convert action to price."""
        return self.price_range[action]
    
    def calculate_demand(self, my_price, opponent_price):
        """Calculate demand given prices."""
        prices = np.array([my_price, opponent_price])
        demand = np.exp((self.a_i - prices) / self.mu) / (
            np.sum(np.exp((self.a_i - prices) / self.mu)) + np.exp(self.a_0 / self.mu)
        )
        return demand[0]  # Return my demand
    
    def calculate_profit(self, my_price, opponent_price):
        """Calculate profit given prices."""
        demand = self.calculate_demand(my_price, opponent_price)
        return (my_price - self.c_i) * demand

    def update(self, reward, info=None):
        super().update(reward, info)
        pass


class ContinueAgent(object):
    def __init__(self, name="ContinueAgent"):
        self.name = name
    
    def get_action(self, state):
        # Always continue (swerve)
        return 1  # Continue action in Chicken game
    
    def update(self, reward, info=None):
        pass



class SwerveAgent:
    def __init__(self):
        self.name = "SwerveAgent"
    
    def get_action(self, state):
        # Always swerve
        return 0  # Swerve action in Chicken game
    
    def update(self, reward, info=None):
        pass


def test_chicken_q_learning():
    """Test Q-Learning in Chicken game."""
    print("Testing Q-Learning in Chicken Game")
    print("=" * 50)
    
    # Create agents
    q_agent = ExampleChickenQLearningAgent(
        "ExampleChickenQL", num_states=2, learning_rate=0.1, 
        discount_factor=0.9, exploration_rate=0.1, training_mode=True
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
    
    # Analyze learned strategy
    q_table = q_agent.get_q_table()
    print(f"\nLearned Strategy Analysis:")
    for state in range(2):
        best_action = np.argmax(q_table[state])
        action_name = "Swerve" if best_action == 0 else "Continue"
        state_name = "Opponent Swerved" if state == 0 else "Opponent Continued"
        print(f"  {state_name}: Best action = {action_name}")


def test_collusion_environment():
    """Test Q-Learning in collusion environment."""
    print("\nTesting Q-Learning in Collusion Environment")
    print("=" * 50)
    
    # Create agents
    agent1 = ExampleCollusionQLearningAgent(
        "ExampleCollusionQL1", num_states=10, learning_rate=0.1,
        discount_factor=0.9, exploration_rate=0.1, training_mode=True
    )
    agent2 = ExampleCollusionQLearningAgent(
        "ExampleCollusionQL2", num_states=10, learning_rate=0.1,
        discount_factor=0.9, exploration_rate=0.1, training_mode=True
    )
    
    # Run simple simulation
    print("Running collusion simulation...")
    
    # Initialize with random prices
    action1 = np.random.randint(0, 10)
    action2 = np.random.randint(0, 10)
    
    price_history = []
    profit_history = []
    
    for round_num in range(100):
        # Agents choose actions
        agent1.current_action = action1
        agent2.current_action = action2
        
        # Get prices
        price1 = agent1.get_price(action1)
        price2 = agent2.get_price(action2)
        
        # Calculate profits
        profit1 = agent1.calculate_profit(price1, price2)
        profit2 = agent2.calculate_profit(price2, price1)
        
        # Update agents
        agent1.update(profit1)
        agent2.update(profit2)
        
        # Store history
        price_history.append([price1, price2])
        profit_history.append([profit1, profit2])
        
        # Get next actions
        action1 = agent1.current_action
        action2 = agent2.current_action
        
        # Print progress
        if round_num % 20 == 0:
            avg_price1 = np.mean([p[0] for p in price_history[-20:]])
            avg_price2 = np.mean([p[1] for p in price_history[-20:]])
            print(f"Round {round_num}: Avg prices = ({avg_price1:.3f}, {avg_price2:.3f})")
    
    # Print final statistics
    print(f"\nFinal Statistics:")
    print(f"Agent 1 - Final Q-table shape: {agent1.get_q_table().shape}")
    print(f"Agent 2 - Final Q-table shape: {agent2.get_q_table().shape}")
    
    final_prices = price_history[-20:]
    avg_price1 = np.mean([p[0] for p in final_prices])
    avg_price2 = np.mean([p[1] for p in final_prices])
    
    print(f"Final 20 rounds average prices:")
    print(f"  Agent 1: {avg_price1:.3f}")
    print(f"  Agent 2: {avg_price2:.3f}")
    print(f"  Bertrand price: {agent1.bertrand_price:.3f}")
    print(f"  Monopoly price: {agent1.monopoly_price:.3f}")
    
    if avg_price1 > agent1.bertrand_price and avg_price2 > agent1.bertrand_price:
        print("PASS: Evidence of collusion detected!")
    else:
        print("FAIL: No clear evidence of collusion")
    
    # Show learned pricing strategies
    print(f"\nLearned Pricing Strategies:")
    q_table1 = agent1.get_q_table()
    q_table2 = agent2.get_q_table()
    
    for state in range(min(5, agent1.num_states)):  # Show first 5 states
        best_price1 = agent1.price_range[np.argmax(q_table1[state])]
        best_price2 = agent2.price_range[np.argmax(q_table2[state])]
        print(f"  State {state}: Agent 1 best price = {best_price1:.3f}, Agent 2 best price = {best_price2:.3f}")


if __name__ == "__main__":
    print("Example Solutions for Lab 3")
    print("=" * 40)
    
    test_chicken_q_learning()
    test_collusion_environment()
    
    print("\nExample solutions completed!")
    print("Use these as reference for implementing your own agents.")
    print("\nKey insights:")
    print("1. State representation is crucial for Q-Learning performance")
    print("2. Q-Learning can discover optimal strategies in competitive games")
    print("3. Collusion can emerge naturally from Q-Learning in pricing games")
    print("4. The exploration rate affects how quickly agents learn") 