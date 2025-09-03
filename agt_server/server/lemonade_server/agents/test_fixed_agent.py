from core.agents.common.base_agent import BaseAgent

class TestFixedAgent(BaseAgent):
    """Simple fixed agent that always chooses position 3 for testing"""
    
    def __init__(self, name: str = "TestFixed"):
        super().__init__(name)
    
    def get_action(self, opponent_positions=None):
        """Always return position 3"""
        return 3
    
    def update(self, reward: float, info=None):
        """Update with reward"""
        self.reward_history.append(reward)

# Export for the competition
agent_submission = TestFixedAgent("TestFixed")
