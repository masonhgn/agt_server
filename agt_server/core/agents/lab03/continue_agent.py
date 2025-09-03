from core.agents.common.base_agent import BaseAgent


class ContinueAgent(BaseAgent):
    """Agent that always plays Continue."""
    
    def __init__(self, name: str = "Continue"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Always return Continue (action 1)."""
        action = 1  # Continue
        self.action_history.append(action)
        return action
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """Store the reward received."""
        if reward is not None:
            self.reward_history.append(reward) 