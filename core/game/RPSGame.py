import numpy as np
from core.game.MatrixGame import MatrixGame


class RPSGame(MatrixGame):
    """
    Rock Paper Scissors game implementation.
    
    Actions:
    0 = Rock
    1 = Paper  
    2 = Scissors
    
    Payoff matrix (row player, column player):
    R\C  R  P  S
    R    0 -1  1
    P    1  0 -1
    S   -1  1  0
    """
    
    def __init__(self, rounds: int = 1000):
        # Create the payoff tensor for RPS
        # Shape: (hidden_states=1, actions=3, actions=3, players=2)
        payoff_tensor = np.array([
            # Rock vs Rock, Paper, Scissors
            [[0.0, 0.0], [-1.0, 1.0], [1.0, -1.0]],
            # Paper vs Rock, Paper, Scissors  
            [[1.0, -1.0], [0.0, 0.0], [-1.0, 1.0]],
            # Scissors vs Rock, Paper, Scissors
            [[-1.0, 1.0], [1.0, -1.0], [0.0, 0.0]]
        ])
        
        # Reshape to (1, 3, 3, 2) for the tensor format
        payoff_tensor = payoff_tensor.reshape(1, 3, 3, 2)
        
        action_labels = ["Rock", "Paper", "Scissors"]
        
        super().__init__(payoff_tensor, rounds)
        self.action_labels = action_labels 