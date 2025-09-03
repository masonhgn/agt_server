from core.agents.common.base_agent import BaseAgent


class StubbornAgent(BaseAgent):
    """Agent that always plays Stubborn."""
    
    def __init__(self, name: str = "Stubborn"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Always return Stubborn (action 1)."""
        action = 1  # Stubborn
        self.action_history.append(action)
        return action
    
    def update(self, observation: dict, action: dict, reward: float, done: bool, info: dict):
        """Store the reward received."""
        self.reward_history.append(reward) 