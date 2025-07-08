import numpy as np
from core.game.MatrixGame import MatrixGame


class ChickenGame(MatrixGame):
    """
    Chicken game implementation.
    
    Actions:
    0 = Swerve
    1 = Continue
    
    Payoff matrix (row player, column player):
    S\C  S  C
    S    0  -1
    C    1  -5
    
    Where S = Swerve, C = Continue
    """
    
    def __init__(self, rounds: int = 1000):
        # Create the payoff tensor for Chicken
        # Shape: (hidden_states=1, actions=2, actions=2, players=2)
        payoff_tensor = np.array([
            # Swerve vs Swerve, Continue
            [[0.0, 0.0], [-1.0, 1.0]],
            # Continue vs Swerve, Continue
            [[1.0, -1.0], [-5.0, -5.0]]
        ])
        
        # Reshape to (1, 2, 2, 2) for the tensor format
        payoff_tensor = payoff_tensor.reshape(1, 2, 2, 2)
        
        action_labels = ["Swerve", "Continue"]
        
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels 