import random
from core.agents.common.base_agent import BaseAgent

class SimpleRLAgent(BaseAgent):
    """Simple RL-inspired agent that learns from rewards"""
    
    def __init__(self, name: str = "SimpleRLAgent"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
        self.position_weights = [1.0] * 12  # Equal weights initially
        self.learning_rate = 0.1
    
    def get_action(self, observation=None):
        """Choose action based on learned weights"""
        # Convert weights to probabilities
        total_weight = sum(self.position_weights)
        if total_weight == 0:
            return random.choice(self.positions)
        
        probabilities = [w / total_weight for w in self.position_weights]
        
        # Choose position based on probabilities
        return random.choices(self.positions, weights=probabilities)[0]
    
    def update(self, reward: float, info=None):
        """Update weights based on reward"""
        self.reward_history.append(reward)
        
        # Simple learning: if we got a good reward, increase weight for last action
        if hasattr(self, 'last_action') and reward > 0:
            self.position_weights[self.last_action] += self.learning_rate * reward
    
    def _circular_distance(self, pos1, pos2):
        """Calculate circular distance between two positions"""
        direct_distance = abs(pos1 - pos2)
        circular_distance = min(direct_distance, 12 - direct_distance)
        return circular_distance

# Export for the competition
agent_submission = SimpleRLAgent("EveRL")
