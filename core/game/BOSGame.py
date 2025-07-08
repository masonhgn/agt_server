import numpy as np
from core.game.MatrixGame import MatrixGame


class BOSGame(MatrixGame):
    """
    Battle of the Sexes game implementation (Complete Information).
    
    Actions:
    0 = Compromise/Cooperative
    1 = Stubborn
    
    Payoff matrix (row player, column player):
    C\S  C  S
    C    0  3
    S    7  0
    
    Where C = Compromise, S = Stubborn
    """
    
    def __init__(self, rounds: int = 1000):
        # Create the payoff tensor for BOS
        # Shape: (hidden_states=1, actions=2, actions=2, players=2)
        payoff_tensor = np.array([
            # Compromise vs Compromise, Stubborn
            [[0.0, 0.0], [3.0, 7.0]],
            # Stubborn vs Compromise, Stubborn
            [[7.0, 3.0], [0.0, 0.0]]
        ])
        
        # Reshape to (1, 2, 2, 2) for the tensor format
        payoff_tensor = payoff_tensor.reshape(1, 2, 2, 2)
        
        action_labels = ["Compromise", "Stubborn"]
        
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels 