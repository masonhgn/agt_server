from core.agents.lab04.base_lemonade_agent import BaseLemonadeAgent


class AlwaysStayAgent(BaseLemonadeAgent):
    """An agent that always chooses position 0 for the Lemonade Stand game."""
    
    def __init__(self, name="AlwaysStayAgent"):
        super().__init__(name)
        self.position = 0  # Always stay at position 0
    
    def get_action(self, obs):
        """Always return position 0."""
        return self.position
    
    def update(self, reward):
        """No learning - just stay at the same position."""
        pass 