import random
from core.agents.common.base_agent import BaseAgent

class TestRandomAgent(BaseAgent):
    """Simple random agent for testing the lemonade server logging"""
    
    def __init__(self, name: str = "TestRandom"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, opponent_positions=None):
        """Return a random position"""
        return random.choice(self.positions)
    
    def update(self, reward: float, info=None):
        """Update with reward"""
        self.reward_history.append(reward)

# Export for the competition
agent_submission = TestRandomAgent("TestRandom")
