from core.agents.common.base_agent import BaseAgent


class CooperateAgent(BaseAgent):
    """Agent that always cooperates in Prisoner's Dilemma."""
    
    def __init__(self, name: str = "Cooperate"):
        super().__init__(name)
        self.COOPERATE = 0
    
    def get_action(self, obs):
        """Always return Cooperate (0)."""
        return self.COOPERATE
