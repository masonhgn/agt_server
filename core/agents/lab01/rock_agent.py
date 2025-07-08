from core.agents.common.base_agent import BaseAgent


class RockAgent(BaseAgent):
    """Agent that always plays Rock."""
    
    def __init__(self, name: str = "Rock"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Always return Rock (action 0)."""
        action = 0  # Rock
        self.action_history.append(action)
        return action
    
    def update(self, reward, info=None):
        """Store the reward received."""
        self.reward_history.append(reward) 