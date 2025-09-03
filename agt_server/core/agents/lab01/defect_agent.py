from core.agents.common.base_agent import BaseAgent


class DefectAgent(BaseAgent):
    """Agent that always defects in Prisoner's Dilemma."""
    
    def __init__(self, name: str = "Defect"):
        super().__init__(name)
        self.DEFECT = 1
    
    def get_action(self, obs):
        """Always return Defect (1)."""
        return self.DEFECT
