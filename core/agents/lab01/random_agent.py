import random
from core.agents.common.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    """Agent that plays random moves in Rock Paper Scissors."""
    
    def __init__(self, name: str = "Random"):
        super().__init__(name)
        self.actions = [0, 1, 2]  # Rock, Paper, Scissors
    
    def get_action(self, obs):
        """Return a random action."""
        action = random.choice(self.actions)
        self.action_history.append(action)
        return action
    
    def update(self, reward, info=None):
        """Store the reward received."""
        self.reward_history.append(reward) 