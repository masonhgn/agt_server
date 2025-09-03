from core.agents.lab04.base_lemonade_agent import BaseLemonadeAgent


class StickAgent(BaseLemonadeAgent):
    """A simple agent that always chooses the same position (position 5)."""
    
    def __init__(self, name="StickAgent"):
        super().__init__(name)
        self.position = 5  # Always stick to position 5
    
    def get_action(self, obs):
        """Always return the same position."""
        return self.position
    
    def update(self, reward, info=None):
        """No learning - just stick to the same position."""
        pass 