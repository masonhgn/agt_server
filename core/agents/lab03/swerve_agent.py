from core.agents.common.base_agent import BaseAgent


class SwerveAgent(BaseAgent):
    """Agent that always plays Swerve."""
    
    def __init__(self, name: str = "Swerve"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Always return Swerve (action 0)."""
        action = 0  # Swerve
        self.action_history.append(action)
        return action
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """Store the reward received."""
        if reward is not None:
            self.reward_history.append(reward) 