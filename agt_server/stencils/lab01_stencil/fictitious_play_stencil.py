import numpy as np
import sys
import os

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.rps_agent import RPSAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class FictitiousPlayAgent(RPSAgent):
    def __init__(self, name: str = "FictitiousPlay"):
        super().__init__(name)
        self._is_fictitious_play = True  # Flag to identify this as a Fictitious Play agent
    
    def setup(self):
        """Initialize the agent for a new game."""
        # TODO: Initialize any variables you need to track opponent's actions
        self.opponent_action_counts = [0, 0, 0]  # Count of each action by opponent
    
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
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """Store the reward and update opponent action counts."""
        if reward is not None:
            self.reward_history.append(reward)
        
        # TODO: Update any variables you need to track opponent's actions
        # HINT: Use self.get_opp_action_history() to get opponent's action history
        opp_actions = self.get_opp_action_history()
        if len(opp_actions) > 0:
            last_opp_action = opp_actions[-1]
            self.opponent_action_counts[last_opp_action] += 1
    
    def predict(self):
        """
        Uses the opponent's previous moves to generate and return a probability distribution
        over the opponent's next move
        """
        # TODO: Return a probability distribution over the opponent's next move
        # HINT: Use self.get_opp_action_history() to build the distribution
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
    agent_name = ...  # TODO: Please give your agent a name
    
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


# Export for server testing
agent_submission = FictitiousPlayAgent("FictitiousPlayAgent")
