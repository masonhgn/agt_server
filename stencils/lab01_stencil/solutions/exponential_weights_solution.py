import numpy as np
import sys
import os

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..','..'))

from core.agents.common.rps_agent import RPSAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class ExponentialAgent(RPSAgent):
    def __init__(self, name: str = "Exponential"):
        super().__init__(name)
        self._is_exponential_weights = True  # Flag to identify this as an Exponential Weights agent
    
    def setup(self):
        """Initialize the agent for a new game."""
        self.action_rewards = np.zeros(len(self.actions))  # Cumulative rewards for each action
        self.action_counts = [0, 0, 0]  # Number of times each action was played
    
    def get_action(self, obs=None):
        """
        This method is not used in the new architecture.
        The server will call calc_move_probs() directly and sample from the distribution.
        """
        # For backward compatibility, implement the old way
        move_probs = self.calc_move_probs()
        action = np.random.choice(self.actions, p=move_probs)
        return action
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """Update action rewards and counts."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # Update the reward for the last action taken
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
    
    @staticmethod
    def softmax(x):
        """Compute softmax values for each set of scores in x."""
        # Shifting values to avoid nan issues (due to underflow)
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)
    
    def calc_move_probs(self):
        """
        Uses your historical average rewards to generate a probability distribution 
        over your next move using the Exponential Weights strategy
        """
        # TODO: Calculate the average reward for each action over time and return the softmax of it
        # HINT: Use self.action_rewards and self.action_counts to compute averages
        # HINT: Use self.softmax() to convert averages to probabilities
        
        # Calculate average rewards for each action
        avg_rewards = np.zeros(len(self.actions))
        for i in range(len(self.actions)):
            if self.action_counts[i] > 0:
                avg_rewards[i] = self.action_rewards[i] / self.action_counts[i]
            else:
                # If action hasn't been played yet, give it a small positive value to encourage exploration
                avg_rewards[i] = 0.1
        
        # Apply softmax to get probability distribution
        return self.softmax(avg_rewards)


if __name__ == "__main__":
    # TODO: Give your agent a name
    agent_name = "YourName_Exponential"
    
    # Create agents
    agent = ExponentialAgent(agent_name)
    opponent = RandomAgent("Random")
    
    # Create game and run
    game = RPSGame(rounds=1000)
    agents = [agent, opponent]
    
    engine = Engine(game, agents, rounds=1000)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent.name} statistics:")
    action_counts = [0, 0, 0]  # Rock, Paper, Scissors
    for action in agent.action_history:
        action_counts[action] += 1
    print(f"Rock: {action_counts[0]}, Paper: {action_counts[1]}, Scissors: {action_counts[2]}")
    print(f"Total reward: {sum(agent.reward_history)}")
    print(f"Average reward: {sum(agent.reward_history) / len(agent.reward_history) if agent.reward_history else 0:.3f}")
    
    # Print action-specific statistics
    print(f"\nAction-specific statistics:")
    for i, action_name in enumerate(["Rock", "Paper", "Scissors"]):
        if agent.action_counts[i] > 0:
            avg_reward = agent.action_rewards[i] / agent.action_counts[i]
            print(f"{action_name}: {agent.action_counts[i]} plays, avg reward: {avg_reward:.3f}")
        else:
            print(f"{action_name}: 0 plays") 