import random
from core.agents.common.base_agent import BaseAgent


class RandomPDAgent(BaseAgent):
    """Random agent for Prisoner's Dilemma."""
    
    def __init__(self, name: str = "RandomPD"):
        super().__init__(name)
        self.COOPERATE, self.DEFECT = 0, 1
        self.actions = [self.COOPERATE, self.DEFECT]
    
    def get_action(self, obs):
        """Return a random action: Cooperate (0) or Defect (1)."""
        return random.choice(self.actions)
