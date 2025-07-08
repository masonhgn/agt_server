import random
from core.agents.common.base_agent import BaseAgent


class RandomChickenAgent(BaseAgent):
    """Agent that plays random moves in Chicken."""
    
    def __init__(self, name: str = "RandomChicken"):
        super().__init__(name)
        self.actions = [0, 1]  # Swerve, Continue
    
    def get_action(self, obs):
        """Return a random action."""
        action = random.choice(self.actions)
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, agent_info: dict | None = None):
        """Store the reward received."""
        self.reward_history.append(reward) 