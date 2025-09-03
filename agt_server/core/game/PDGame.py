import numpy as np
from core.game.MatrixGame import MatrixGame


class PDGame(MatrixGame):
    """
    Prisoner's Dilemma game implementation.
    
    Actions:
    0 = Cooperate
    1 = Defect
    
    Payoff matrix (row player, column player):
    C\\D  C    D
    C   -1   -3
    D    0   -2
    
    Where C = Cooperate, D = Defect
    """
    
    def __init__(self, rounds: int = 1000):
        # Create the payoff tensor for Prisoner's Dilemma
        # Shape: (hidden_states=1, actions=2, actions=2, players=2)
        payoff_tensor = np.array([
            # Cooperate vs Cooperate, Defect
            [[-1.0, -1.0], [-3.0, 0.0]],
            # Defect vs Cooperate, Defect
            [[0.0, -3.0], [-2.0, -2.0]]
        ])
        
        # Reshape to (1, 2, 2, 2) for the tensor format
        payoff_tensor = payoff_tensor.reshape(1, 2, 2, 2)
        
        action_labels = ["Cooperate", "Defect"]
        
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels
