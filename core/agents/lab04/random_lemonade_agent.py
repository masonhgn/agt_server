from core.agents.lab04.base_lemonade_agent import BaseLemonadeAgent
import random


class RandomLemonadeAgent(BaseLemonadeAgent):
    """A random agent that chooses random positions for the Lemonade Stand game."""
    
    def __init__(self, name="RandomLemonadeAgent"):
        super().__init__(name)
    
    def get_action(self, obs):
        """Choose a random position from 0-11."""
        valid_actions = obs.get("valid_actions", list(range(12)))
        return random.choice(valid_actions)
    
    def update(self, reward, info=None):
        """No learning - just random choices."""
        pass 