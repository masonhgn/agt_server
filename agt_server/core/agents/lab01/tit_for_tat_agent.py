from core.agents.common.base_agent import BaseAgent


class TitForTatAgent(BaseAgent):
    """Tit-for-tat agent for Prisoner's Dilemma.
    
    Cooperates on the first move, then copies the opponent's previous move.
    """
    
    def __init__(self, name: str = "TitForTat"):
        super().__init__(name)
        self.COOPERATE, self.DEFECT = 0, 1
        self.opponent_last_move = None
    
    def get_action(self, obs):
        """Return action based on tit-for-tat strategy."""
        # Get opponent's last move from observation
        opponent_last_move = obs.get("opponent_last_move", None)
        
        if opponent_last_move is None:
            # First move - cooperate
            return self.COOPERATE
        else:
            # Copy opponent's last move
            return opponent_last_move
    
    def update(self, reward: float, info: dict | None = None):
        """Update with the reward received."""
        super().update(reward, info)
