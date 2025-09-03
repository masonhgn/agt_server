import random
from core.agents.common.base_agent import BaseAgent

class RandomAgent(BaseAgent):
    """Simple random agent that chooses positions randomly"""
    
    def __init__(self, name: str = "RandomAgent"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, observation=None):
        """Return a random position"""
        return random.choice(self.positions)
    
    def update(self, reward: float, info=None):
        """Update with reward (not used in this simple agent)"""
        self.reward_history.append(reward)

# Export for the competition
agent_submission = RandomAgent("BobRandom")
