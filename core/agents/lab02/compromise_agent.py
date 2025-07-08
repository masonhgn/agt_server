from core.agents.common.base_agent import BaseAgent


class CompromiseAgent(BaseAgent):
    """Agent that always plays Compromise."""
    
    def __init__(self, name: str = "Compromise"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Always return Compromise (action 0)."""
        action = 0  # Compromise
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, agent_info: dict | None = None):
        """Store the reward received."""
        self.reward_history.append(reward) 