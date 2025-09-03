from core.agents.common.base_agent import BaseAgent

class RandomBOSAgent(BaseAgent):
    def get_action(self, obs):
        return 0  # Dummy action for test 