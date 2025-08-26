#!/usr/bin/env python3
"""
Complete Collusion Environment Solution for Lab 3 Part III.
This shows the implementation of determine_state() for the market game.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from q_learning import QLearning


class CollusionQLearningAgentSolution(QLearning):
    """Complete Q-Learning agent solution for collusion environment."""
    
    def __init__(self, name: str = "CollusionQLSolution", num_states: int = 10, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9,
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str = None):
        super().__init__(name, num_states, 10, 0, learning_rate, discount_factor, 
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
        
        # Track opponent's price history
        self.opponent_price_history = []
    
    def determine_state(self):
        """
        COMPLETE IMPLEMENTATION: State representation for collusion environment.
        
        State 0-9: opponent's last price level (discretized)
        This creates a simple but effective state space for learning collusive behavior.
        """
        if len(self.action_history) == 0:
            return 0  # Initial state
        
        # For this example, we'll use a simple state representation
        # based on the opponent's last price level
        if len(self.opponent_price_history) > 0:
            last_opponent_price = self.opponent_price_history[-1]
            # Discretize the price into 10 states
            price_index = int((last_opponent_price - 1.0) / 0.1)
            price_index = max(0, min(9, price_index))  # Clamp to [0, 9]
            return price_index
        
        return 0  # Default state
    
    def get_price(self, action):
        """Convert action to price."""
        return self.price_range[action]
    
    def calculate_demand(self, my_price, opponent_price):
        """Calculate demand given prices using logit demand equation."""
        # Logit demand equation from writeup:
        # qi = exp((ai - pi) / μ) / (Σ exp((aj - pj) / μ) + exp(a0 / μ))
        
        numerator = np.exp((self.a_i - my_price) / self.mu)
        denominator = (np.exp((self.a_i - my_price) / self.mu) + 
                      np.exp((self.a_i - opponent_price) / self.mu) + 
                      np.exp(self.a_0 / self.mu))
        
        return numerator / denominator
    
    def calculate_profit(self, my_price, opponent_price):
        """Calculate profit given prices."""
        demand = self.calculate_demand(my_price, opponent_price)
        return (my_price - self.c_i) * demand
    
    def update_opponent_price(self, opponent_price):
        """Update opponent's price history."""
        self.opponent_price_history.append(opponent_price)


class CollusionEnvironmentSolution:
    """Complete environment solution for studying collusion in pricing games."""
    
    def __init__(self, agent1: CollusionQLearningAgentSolution, agent2: CollusionQLearningAgentSolution):
        self.agent1 = agent1
        self.agent2 = agent2
        self.price_history = []
        self.profit_history = []
    
    def run_simulation(self, num_rounds: int = 1000000, save_plots: bool = True):
        """Run the collusion simulation."""
        print(f"Running collusion simulation for {num_rounds} rounds...")
        
        # Initialize with random prices
        action1 = np.random.randint(0, 10)
        action2 = np.random.randint(0, 10)
        
        for round_num in range(num_rounds):
            # Agents choose actions
            self.agent1.a = action1
            self.agent2.a = action2
            
            # Get prices
            price1 = self.agent1.get_price(action1)
            price2 = self.agent2.get_price(action2)
            
            # Calculate profits
            profit1 = self.agent1.calculate_profit(price1, price2)
            profit2 = self.agent2.calculate_profit(price2, price1)
            
            # Update agents
            self.agent1.update_opponent_price(price2)
            self.agent2.update_opponent_price(price1)
            
            # Update Q-learning agents
            self.agent1.update(profit1)
            self.agent2.update(profit2)
            
            # Store history
            self.price_history.append([price1, price2])
            self.profit_history.append([profit1, profit2])
            
            # Choose next actions
            action1 = self.agent1.get_action()
            action2 = self.agent2.get_action()
            
            # Print progress
            if round_num % 100000 == 0:
                print(f"Round {round_num}: Prices = ({price1:.2f}, {price2:.2f}), "
                      f"Profits = ({profit1:.3f}, {profit2:.3f})")
        
        # Create plots
        if save_plots:
            self.create_plots()
    
    def create_plots(self):
        """Create plots showing collusion behavior."""
        price_history = np.array(self.price_history)
        profit_history = np.array(self.profit_history)
        
        # Plot 1: Price trajectories
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(price_history[:, 0], label='Seller 1', alpha=0.7)
        plt.plot(price_history[:, 1], label='Seller 2', alpha=0.7)
        plt.axhline(y=self.agent1.bertrand_price, color='r', linestyle='--', 
                   label='Bertrand Equilibrium')
        plt.axhline(y=self.agent1.monopoly_price, color='g', linestyle='--', 
                   label='Monopoly Price')
        plt.xlabel('Round')
        plt.ylabel('Price')
        plt.title('Price Trajectories (Solution)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot 2: Price war example (last 1000 rounds)
        plt.subplot(1, 2, 2)
        last_1000 = price_history[-1000:]
        plt.plot(last_1000[:, 0], label='Seller 1', alpha=0.7)
        plt.plot(last_1000[:, 1], label='Seller 2', alpha=0.7)
        plt.axhline(y=self.agent1.bertrand_price, color='r', linestyle='--', 
                   label='Bertrand Equilibrium')
        plt.xlabel('Round (last 1000)')
        plt.ylabel('Price')
        plt.title('Price War Example (Solution)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('collusion_results_solution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Solution plots saved as 'collusion_results_solution.png'")


def main():
    """Main function to run collusion simulation with complete solution."""
    print("Lab 3 Part III: Collusion in Market Games - Complete Solution")
    print("=" * 60)
    
    # Create Q-learning agents with complete implementations
    agent1 = CollusionQLearningAgentSolution("Seller1Solution", num_states=10, 
                                            learning_rate=0.1, discount_factor=0.9,
                                            exploration_rate=0.1, training_mode=True,
                                            save_path="seller1-q-table-solution.npy")
    agent2 = CollusionQLearningAgentSolution("Seller2Solution", num_states=10,
                                            learning_rate=0.1, discount_factor=0.9,
                                            exploration_rate=0.1, training_mode=True,
                                            save_path="seller2-q-table-solution.npy")
    
    # Create environment and run simulation
    env = CollusionEnvironmentSolution(agent1, agent2)
    env.run_simulation(num_rounds=1000000, save_plots=True)
    
    print("\nCollusion simulation completed!")
    print("Check the generated plots to see collusion behavior.")
    print("Q-tables saved as 'seller1-q-table-solution.npy' and 'seller2-q-table-solution.npy'")


if __name__ == "__main__":
    main()
