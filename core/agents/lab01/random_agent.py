import random
from core.agents.common.rps_agent import RPSAgent


class RandomAgent(RPSAgent):
    """Agent that plays random moves in Rock Paper Scissors."""
    
    def get_action(self, obs=None):
        """Return a random action."""
        action = random.choice(self.actions)
        return action
    
    def update(self, reward=None, info=None):
        """Store the reward received."""
        if reward is not None:
            self.reward_history.append(reward)
    
    def setup(self):
        """Initialize the agent for a new game."""
        pass 