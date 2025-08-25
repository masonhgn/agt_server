import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSCompetitionAgent(BaseAgent):
    """Competition agent for Battle of the Sexes."""
    
    def __init__(self, name: str = "BOSComp"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
        self.opponent_pattern = []  # Track opponent's recent actions
        self.cooperation_count = 0  # Count cooperative moves
        self.defection_count = 0    # Count defections
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        # Adaptive strategy for unknown opponents:
        # - Start with COMPROMISE to establish cooperation
        # - Adapt based on opponent's behavior
        # - Use tit-for-tat with forgiveness
        
        if self.curr_state == 0:
            # Initial state: try to cooperate
            return self.COMPROMISE
        elif self.curr_state == 1:
            # Cooperative state: mostly cooperate
            return self.COMPROMISE
        elif self.curr_state == 2:
            # Tit-for-tat state: mirror opponent's last move
            if len(self.opponent_pattern) > 0:
                return self.opponent_pattern[-1]
            else:
                return self.COMPROMISE
        elif self.curr_state == 3:
            # Defensive state: be stubborn
            return self.STUBBORN
        else:
            return self.COMPROMISE  # Default fallback
    
    def update(self, reward: float, info=None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        self.reward_history.append(reward)
        
        # Get opponent's last action
        opponent_action = self.get_opponent_last_action()
        
        if opponent_action is not None:
            # Update opponent pattern
            self.opponent_pattern.append(opponent_action)
            if len(self.opponent_pattern) > 5:
                self.opponent_pattern.pop(0)  # Keep only last 5 moves
            
            # Update cooperation/defection counts
            if opponent_action == self.COMPROMISE:
                self.cooperation_count += 1
            else:
                self.defection_count += 1
            
            # State transition logic
            if self.curr_state == 0:  # Initial state
                if opponent_action == self.COMPROMISE:
                    # Opponent cooperated, stay cooperative
                    self.curr_state = 1
                else:
                    # Opponent defected, switch to tit-for-tat
                    self.curr_state = 2
            
            elif self.curr_state == 1:  # Cooperative state
                if opponent_action == self.STUBBORN:
                    # Opponent defected, switch to tit-for-tat
                    self.curr_state = 2
            
            elif self.curr_state == 2:  # Tit-for-tat state
                # Analyze recent pattern
                if len(self.opponent_pattern) >= 3:
                    recent_defections = sum(1 for a in self.opponent_pattern[-3:] if a == self.STUBBORN)
                    if recent_defections >= 2:
                        # Too many recent defections, go defensive
                        self.curr_state = 3
                    elif recent_defections == 0:
                        # All cooperation recently, go back to cooperative
                        self.curr_state = 1
            
            elif self.curr_state == 3:  # Defensive state
                # Check if opponent has been cooperative recently
                if len(self.opponent_pattern) >= 2:
                    recent_cooperations = sum(1 for a in self.opponent_pattern[-2:] if a == self.COMPROMISE)
                    if recent_cooperations >= 2:
                        # Opponent cooperating, try tit-for-tat
                        self.curr_state = 2
    
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


# TODO: Give your agent a NAME 
name = "BOSCompetitionAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = BOSCompetitionAgent(name)
####################################################


if __name__ == "__main__":
    # Test your agent before submitting
    print("Testing BOS Competition Agent locally...")
    print("=" * 50)
    
    # Create a 1000-round local competition in which your agent competes against itself
    agent1 = BOSCompetitionAgent("Agent1")
    agent2 = BOSCompetitionAgent("Agent2")
    
    # Create game and run
    game = BOSGame(rounds=1000)
    agents = [agent1, agent2]
    
    engine = Engine(game, agents, rounds=1000)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent1.name} statistics:")
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent1.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(agent1.reward_history)}")
    print(f"Average reward: {sum(agent1.reward_history) / len(agent1.reward_history) if agent1.reward_history else 0:.3f}")
    print(f"Final state: {agent1.curr_state}")
    
    print("\nLocal test completed!")
