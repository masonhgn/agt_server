import numpy as np
from core.agents.common.base_agent import BaseAgent


class FictitiousPlayAgent(BaseAgent):
    """Agent that uses fictitious play to learn opponent's strategy."""
    
    def __init__(self, name: str = "FictitiousPlay"):
        super().__init__(name)
        self.actions = [0, 1, 2]  # Rock, Paper, Scissors
        self.opponent_action_counts = [0, 0, 0]  # Count of each action by opponent
    
    def get_action(self, obs):
        """Return the best response to predicted opponent action."""
        # Predict opponent's action distribution
        if sum(self.opponent_action_counts) == 0:
            # No history yet, play randomly
            action = np.random.choice(self.actions)
        else:
            # Use fictitious play to predict opponent's mixed strategy
            opponent_dist = np.array(self.opponent_action_counts) / sum(self.opponent_action_counts)
            
            # Calculate expected payoff for each action
            expected_payoffs = np.zeros(3)
            for my_action in self.actions:
                for opp_action in self.actions:
                    # RPS payoff matrix: my_action vs opp_action
                    if my_action == opp_action:
                        payoff = 0
                    elif (my_action == 0 and opp_action == 2) or \
                         (my_action == 1 and opp_action == 0) or \
                         (my_action == 2 and opp_action == 1):
                        payoff = 1  # Win
                    else:
                        payoff = -1  # Lose
                    
                    expected_payoffs[my_action] += opponent_dist[opp_action] * payoff
            
            # Choose action with highest expected payoff
            action = np.argmax(expected_payoffs)
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float):
        """Store the reward and update opponent action counts."""
        self.reward_history.append(reward)
        
        # Update opponent action counts based on the reward
        # This is a simplified approach - in a real implementation,
        # we'd need to know the opponent's actual action
        # For now, we'll infer it from the reward and our action
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            # Infer opponent's action from reward
            if reward == 0:
                # Tie - opponent played same as us
                opp_action = my_action
            elif reward == 1:
                # We won - opponent played the action we beat
                if my_action == 0:  # Rock beats Scissors
                    opp_action = 2
                elif my_action == 1:  # Paper beats Rock
                    opp_action = 0
                else:  # Scissors beats Paper
                    opp_action = 1
            else:  # reward == -1
                # We lost - opponent played the action that beats us
                if my_action == 0:  # Rock loses to Paper
                    opp_action = 1
                elif my_action == 1:  # Paper loses to Scissors
                    opp_action = 2
                else:  # Scissors loses to Rock
                    opp_action = 0
            
            self.opponent_action_counts[opp_action] += 1 