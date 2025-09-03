from core.agents.common.base_agent import BaseAgent


class BOSReluctantAgent(BaseAgent):
    """Reluctant to Compromise strategy for Battle of the Sexes."""
    
    def __init__(self, name: str = "BOSReluctant"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
        self.consecutive_lectures = 0  # Count consecutive times opponent went to lecture
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        if self.curr_state == 0:
            # Initial state: always go to concert (STUBBORN)
            return self.STUBBORN
        elif self.curr_state == 1:
            # Compromise state: go to lecture (COMPROMISE)
            return self.COMPROMISE
        else:
            return self.STUBBORN  # Default fallback
    
    def update(self, reward: float, info=None, observation: dict = None, action: dict = None, done: bool = None):
        """
        Update the current state based on the game history.
        """
        self.reward_history.append(reward)
        
        # Get opponent's last action
        opponent_action = self.get_opponent_last_action()
        
        if opponent_action is not None:
            if opponent_action == self.STUBBORN:  # Opponent went to lecture
                self.consecutive_lectures += 1
                if self.consecutive_lectures >= 3:
                    # After 3 consecutive lectures, compromise once
                    self.curr_state = 1
            else:  # Opponent went to concert
                self.consecutive_lectures = 0
                # Go back to being stubborn
                self.curr_state = 0
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Infer opponent's action from reward and my action
        if my_last_action == self.COMPROMISE:
            if my_last_reward == 0:
                return self.COMPROMISE  # Both compromised
            elif my_last_reward == 3:
                return self.STUBBORN     # I compromised, they were stubborn
        elif my_last_action == self.STUBBORN:
            if my_last_reward == 7:
                return self.COMPROMISE   # I was stubborn, they compromised
            elif my_last_reward == 0:
                return self.STUBBORN     # Both were stubborn
        
        return None  # Can't determine
