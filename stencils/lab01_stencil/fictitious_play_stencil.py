import numpy as np
import sys
import os

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class FictitiousPlayAgent(BaseAgent):
    def __init__(self, name: str = "FictitiousPlay"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.opponent_action_counts = [0, 0, 0]  # Count of each action by opponent
    
    def get_action(self, obs):
        """Return the best response to predicted opponent action."""
        dist = self.predict()
        best_move = self.optimize(dist)
        action = self.actions[best_move]
        self.action_history.append(action)
        return action
    
    def update(self, reward: float):
        """Store the reward and update opponent action counts."""
        self.reward_history.append(reward)
        
        # Update opponent action counts based on the reward
        # This is a simplified approach - in a real implementation,
        # we'd need to know the opponent's actual action
        # For now, we'll infer it from the reward and our action
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            # Infer opponent's action from reward
            if reward == 0:
                # Tie - opponent played same as us
                opp_action = my_action
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
        """
        Uses the opponent's previous moves to generate and return a probability distribution
        over the opponent's next move
        """
        # TODO: Return a probability distribution over the opponent's next move
        # HINT: Use self.opponent_action_counts to build the distribution
        raise NotImplementedError
    
    def optimize(self, dist):
        """
        Given the distribution over the opponent's next move (output of predict) and knowledge of the payoffs,
        Return the best move according to FP (Fictitious Play).
        Please return one of [self.ROCK, self.PAPER, self.SCISSORS]
        """
        # TODO: Calculate the expected payoff of each action and return the action with the highest payoff
        # HINT: Use the RPS payoff matrix and the opponent's predicted distribution
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: Give your agent a name
    agent_name = "YourName_FictitiousPlay"
    
    # Create agents
    agent = FictitiousPlayAgent(agent_name)
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