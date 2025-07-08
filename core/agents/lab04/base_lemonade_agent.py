from core.agents.common.base_agent import BaseAgent
from typing import List, Any


class BaseLemonadeAgent(BaseAgent):
    """
    Base agent for the Lemonade Stand game.
    
    Provides Lemonade Stand specific methods and interfaces.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.valid_actions = list(range(12))  # Positions 0-11
        self.opponent1_action_history: List[int] = []
        self.opponent2_action_history: List[int] = []
        self.opponent1_reward_history: List[float] = []
        self.opponent2_reward_history: List[float] = []
    
    def get_action(self, obs):
        return 0  # Dummy action for test
    
    def update(self, my_action: int, opponent_actions: List[int], 
               my_utility: float, opponent_utilities: List[float]) -> None:
        """
        Update the agent with the results of a round.
        
        Parameters
        ----------
        my_action : int
            The action this agent took
        opponent_actions : List[int]
            Actions taken by opponents
        my_utility : float
            Utility received by this agent
        opponent_utilities : List[float]
            Utilities received by opponents
        """
        # Update histories
        self.action_history.append(my_action)
        self.reward_history.append(my_utility)
        
        if len(opponent_actions) >= 1:
            self.opponent1_action_history.append(opponent_actions[0])
        if len(opponent_actions) >= 2:
            self.opponent2_action_history.append(opponent_actions[1])
        if len(opponent_utilities) >= 1:
            self.opponent1_reward_history.append(opponent_utilities[0])
        if len(opponent_utilities) >= 2:
            self.opponent2_reward_history.append(opponent_utilities[1])
        
        # Call the parent update method
        super().update(my_utility)
    
    def get_opp1_action_history(self) -> List[int]:
        """Get the action history of the first opponent."""
        return self.opponent1_action_history.copy()
    
    def get_opp2_action_history(self) -> List[int]:
        """Get the action history of the second opponent."""
        return self.opponent2_action_history.copy()
    
    def get_opp1_reward_history(self) -> List[float]:
        """Get the reward history of the first opponent."""
        return self.opponent1_reward_history.copy()
    
    def get_opp2_reward_history(self) -> List[float]:
        """Get the reward history of the second opponent."""
        return self.opponent2_reward_history.copy()
    
    def get_opp1_last_action(self) -> int | None:
        """Get the last action of the first opponent."""
        return self.opponent1_action_history[-1] if self.opponent1_action_history else None
    
    def get_opp2_last_action(self) -> int | None:
        """Get the last action of the second opponent."""
        return self.opponent2_action_history[-1] if self.opponent2_action_history else None
    
    def get_opp1_last_reward(self) -> float | None:
        """Get the last reward of the first opponent."""
        return self.opponent1_reward_history[-1] if self.opponent1_reward_history else None
    
    def get_opp2_last_reward(self) -> float | None:
        """Get the last reward of the second opponent."""
        return self.opponent2_reward_history[-1] if self.opponent2_reward_history else None
    
    def calculate_utils(self, a1: int, a2: int, a3: int) -> List[float]:
        """
        Calculate utilities for all three players based on their actions.
        
        Parameters
        ----------
        a1 : int
            Action of player 1
        a2 : int
            Action of player 2
        a3 : int
            Action of player 3
            
        Returns
        -------
        List[float]
            Utilities [u1, u2, u3] for the three players
        """
        # Check for invalid actions
        if a1 not in self.valid_actions and a2 not in self.valid_actions and a3 not in self.valid_actions:
            return [0.0, 0.0, 0.0]
        elif a1 not in self.valid_actions and a2 not in self.valid_actions:
            return [0.0, 0.0, 24.0]
        elif a1 not in self.valid_actions and a3 not in self.valid_actions:
            return [0.0, 24.0, 0.0]
        elif a2 not in self.valid_actions and a3 not in self.valid_actions:
            return [24.0, 0.0, 0.0]
        elif a1 not in self.valid_actions:
            return [0.0, 12.0, 12.0]
        elif a2 not in self.valid_actions:
            return [12.0, 0.0, 12.0]
        elif a3 not in self.valid_actions:
            return [12.0, 12.0, 0.0]
        
        # All actions are valid, calculate payoffs
        if a1 == a2 and a2 == a3:
            # All three choose the same position
            # The distance between all is zero, so all utilities are zero
            return [0.0, 0.0, 0.0]
        elif a1 == a2:
            # Players 1 and 2 choose the same position
            return [6.0, 6.0, 12.0]
        elif a1 == a3:
            # Players 1 and 3 choose the same position
            return [6.0, 12.0, 6.0]
        elif a2 == a3:
            # Players 2 and 3 choose the same position
            return [12.0, 6.0, 6.0]
        else:
            # All choose different positions - middle player gets most points
            actions_list = [a1, a2, a3]
            sorted_actions = sorted(actions_list)
            index_map = {action: index for index, action in enumerate(actions_list)}
            sorted_indices = [index_map[action] for action in sorted_actions]
            
            u1 = sorted_actions[1] - sorted_actions[0]
            u2 = sorted_actions[2] - sorted_actions[1]
            u3 = 12 + sorted_actions[0] - sorted_actions[2]
            
            utils = [0.0, 0.0, 0.0]
            utils[sorted_indices[0]] = u1 + u3
            utils[sorted_indices[1]] = u1 + u2
            utils[sorted_indices[2]] = u2 + u3
            
            return utils
    
    def reset(self) -> None:
        """Reset the agent's internal state for a new game."""
        super().reset()
        self.opponent1_action_history.clear()
        self.opponent2_action_history.clear()
        self.opponent1_reward_history.clear()
        self.opponent2_reward_history.clear() 