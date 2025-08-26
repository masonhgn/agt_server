#!/usr/bin/env python3
"""
Collusion Environment stencil.
Demonstrates how Q-learners can learn collusive strategies in competitive settings.
"""

import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import matplotlib.pyplot as plt
from core.agents.common.q_learning import QLearningAgent
from core.agents.common.base_agent import BaseAgent


class CollusionQLearningAgent(QLearningAgent):
    """Q-Learning agent for collusion environment."""
    
    def __init__(self, name: str = "CollusionQL", num_states: int = 10, 
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
        Determine the current state based on market conditions.
        
        TODO: Implement your state representation here.
        
        Some examples:
        1. Opponent's last price level (10 states)
        2. Market price difference (discretized)
        3. Price trend (increasing/decreasing)
        
        Returns:
            int: State index (0 to num_states - 1)
        """
        # TODO: Implement your state representation
        # Hint: Use self.get_action_history() and opponent's price history
        raise NotImplementedError
    
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

    def get_action(self, obs):
        return 0  # Dummy action for test


class CollusionEnvironment:
    """Environment for studying collusion in pricing games."""
    
    def __init__(self, agent1: CollusionQLearningAgent, agent2: CollusionQLearningAgent):
        self.agent1 = agent1
        self.agent2 = agent2
        self.price_history = []
        self.profit_history = []
    
    def run_simulation(self, num_rounds: int = 1000, save_plots: bool = True):
        """Run the collusion simulation."""
        print(f"Running collusion simulation for {num_rounds} rounds...")
        
        # Initialize with random prices
        action1 = np.random.randint(0, 10)
        action2 = np.random.randint(0, 10)
        
        for round_num in range(num_rounds):
            # Agents choose actions
            self.agent1.current_action = action1
            self.agent2.current_action = action2
            
            # Get prices
            price1 = self.agent1.get_price(action1)
            price2 = self.agent2.get_price(action2)
            
            # Calculate profits
            profit1 = self.agent1.calculate_profit(price1, price2)
            profit2 = self.agent2.calculate_profit(price2, price1)
            
            # Update agents
            self.agent1.update(profit1)
            self.agent2.update(profit2)
            
            # Store history
            self.price_history.append([price1, price2])
            self.profit_history.append([profit1, profit2])
            
            # Get next actions
            action1 = self.agent1.current_action
            action2 = self.agent2.current_action
            
            # Print progress
            if round_num % 100 == 0:
                avg_price1 = np.mean([p[0] for p in self.price_history[-100:]])
                avg_price2 = np.mean([p[1] for p in self.price_history[-100:]])
                print(f"Round {round_num}: Avg prices = ({avg_price1:.3f}, {avg_price2:.3f})")
        
        # Generate plots
        if save_plots:
            self._generate_plots()
        
        return self.price_history, self.profit_history
    
    def _generate_plots(self):
        """Generate plots showing price evolution and collusion."""
        prices = np.array(self.price_history)
        profits = np.array(self.profit_history)
        
        # Price trajectory
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(prices[:, 0], label='Agent 1 Price', alpha=0.7)
        plt.plot(prices[:, 1], label='Agent 2 Price', alpha=0.7)
        plt.axhline(y=self.agent1.bertrand_price, color='red', linestyle='--', label='Bertrand Price')
        plt.axhline(y=self.agent1.monopoly_price, color='green', linestyle='--', label='Monopoly Price')
        plt.xlabel('Round')
        plt.ylabel('Price')
        plt.title('Price Evolution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Profit trajectory
        plt.subplot(2, 2, 2)
        plt.plot(profits[:, 0], label='Agent 1 Profit', alpha=0.7)
        plt.plot(profits[:, 1], label='Agent 2 Profit', alpha=0.7)
        plt.xlabel('Round')
        plt.ylabel('Profit')
        plt.title('Profit Evolution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Price distribution
        plt.subplot(2, 2, 3)
        plt.hist(prices[:, 0], bins=20, alpha=0.7, label='Agent 1', density=True)
        plt.hist(prices[:, 1], bins=20, alpha=0.7, label='Agent 2', density=True)
        plt.axvline(x=self.agent1.bertrand_price, color='red', linestyle='--', label='Bertrand')
        plt.axvline(x=self.agent1.monopoly_price, color='green', linestyle='--', label='Monopoly')
        plt.xlabel('Price')
        plt.ylabel('Density')
        plt.title('Price Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Q-table visualization
        plt.subplot(2, 2, 4)
        q_table1 = self.agent1.get_q_table()
        q_table2 = self.agent2.get_q_table()
        
        # Show average Q-values for each price level
        avg_q1 = np.mean(q_table1, axis=0)
        avg_q2 = np.mean(q_table2, axis=0)
        
        plt.plot(self.agent1.price_range, avg_q1, 'o-', label='Agent 1 Q-values')
        plt.plot(self.agent2.price_range, avg_q2, 's-', label='Agent 2 Q-values')
        plt.xlabel('Price')
        plt.ylabel('Average Q-value')
        plt.title('Q-values by Price Level')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('collusion_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Plots saved as 'collusion_results.png'")


if __name__ == "__main__":
    # TODO: Give your agents names
    agent1_name = "YourName_CollusionQL1"
    agent2_name = "YourName_CollusionQL2"
    
    # Q-Learning parameters
    num_states = 10  # TODO: Adjust based on your state representation
    learning_rate = 0.1
    discount_factor = 0.9
    exploration_rate = 0.1
    training_mode = True
    
    # Create agents
    agent1 = CollusionQLearningAgent(
        agent1_name, num_states, learning_rate, discount_factor, 
        exploration_rate, training_mode
    )
    agent2 = CollusionQLearningAgent(
        agent2_name, num_states, learning_rate, discount_factor, 
        exploration_rate, training_mode
    )
    
    # Create environment and run simulation
    env = CollusionEnvironment(agent1, agent2)
    price_history, profit_history = env.run_simulation(num_rounds=1000)
    
    # Print final statistics
    print(f"\nFinal Statistics:")
    print(f"Agent 1 - Final Q-table shape: {agent1.get_q_table().shape}")
    print(f"Agent 2 - Final Q-table shape: {agent2.get_q_table().shape}")
    
    final_prices = price_history[-100:]
    avg_price1 = np.mean([p[0] for p in final_prices])
    avg_price2 = np.mean([p[1] for p in final_prices])
    
    print(f"Final 100 rounds average prices:")
    print(f"  Agent 1: {avg_price1:.3f}")
    print(f"  Agent 2: {avg_price2:.3f}")
    print(f"  Bertrand price: {agent1.bertrand_price:.3f}")
    print(f"  Monopoly price: {agent1.monopoly_price:.3f}")
    
    if avg_price1 > agent1.bertrand_price and avg_price2 > agent1.bertrand_price:
        print("PASS: Evidence of collusion detected!")
    else:
        print("FAIL: No clear evidence of collusion") 