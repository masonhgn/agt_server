from core.agents.common.base_agent import BaseAgent

class PaperAgent(BaseAgent):
    def get_action(self, obs):
        return 1  # Always play 'paper' 

    def update(self, reward, info=None):
        self.reward_history.append(reward) 