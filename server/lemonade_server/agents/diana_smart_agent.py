import random
from core.agents.common.base_agent import BaseAgent

class SmartAgent(BaseAgent):
    """Smart agent that tries to position away from opponents"""
    
    def __init__(self, name: str = "SmartAgent"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, observation=None):
        """Try to find a good position away from opponents"""
        # For now, just choose a fixed position (position 0)
        # In a real implementation, this would analyze opponent positions
        return 0
    
    def update(self, reward: float, info=None):
        """Update with reward"""
        self.reward_history.append(reward)
    
    def _circular_distance(self, pos1, pos2):
        """Calculate circular distance between two positions"""
        direct_distance = abs(pos1 - pos2)
        circular_distance = min(direct_distance, 12 - direct_distance)
        return circular_distance

# Export for the competition
agent_submission = SmartAgent("DianaSmart")
