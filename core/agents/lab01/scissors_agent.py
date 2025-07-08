from core.agents.common.base_agent import BaseAgent

class ScissorsAgent(BaseAgent):
    def get_action(self, obs):
        return 2  # Always play 'scissors' 

    def update(self, reward, info=None):
        self.reward_history.append(reward) 