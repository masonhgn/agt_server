import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSFiniteStateAgent2(BaseAgent):
    """Finite State Machine agent to counter the 'punitive' strategy."""
    
    def __init__(self, name: str = "BOSFSM2"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
        self.break_count = 0  # Count how many times we've broken compromise
        self.consecutive_compromises = 0  # Track consecutive compromises
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        # Strategy to counter "punitive":
        # - Start with COMPROMISE to establish cooperation
        # - If opponent retaliates, be more careful
        # - Try to maintain cooperation while avoiding triggering retaliation
        
        if self.curr_state == 0:
            # Initial state: try to cooperate
            return self.COMPROMISE
        elif self.curr_state == 1:
            # Cautious state: mostly cooperate, occasionally be stubborn
            if self.consecutive_compromises >= 3:
                return self.STUBBORN  # Break pattern occasionally
            else:
                return self.COMPROMISE
        elif self.curr_state == 2:
            # Defensive state: be stubborn to avoid further retaliation
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
            if self.curr_state == 0:  # Initial state
                if opponent_action == self.STUBBORN:  # Opponent retaliated
                    self.break_count += 1
                    if self.break_count >= 2:
                        # Too many breaks, go defensive
                        self.curr_state = 2
                    else:
                        # Be more cautious
                        self.curr_state = 1
                else:  # Opponent cooperated
                    self.consecutive_compromises += 1
            
            elif self.curr_state == 1:  # Cautious state
                if opponent_action == self.STUBBORN:  # Opponent retaliated again
                    self.break_count += 1
                    if self.break_count >= 2:
                        # Go defensive
                        self.curr_state = 2
                else:  # Opponent cooperated
                    self.consecutive_compromises += 1
                    if self.consecutive_compromises >= 5:
                        # Reset to initial state if cooperation is stable
                        self.curr_state = 0
                        self.break_count = 0
                        self.consecutive_compromises = 0
            
            # State 2 (defensive) doesn't change easily
    
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
name = "BOSFiniteStateAgent2"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = BOSFiniteStateAgent2(name)
####################################################


if __name__ == "__main__":
    # Test your agent against the punitive strategy
    print("Testing BOS Finite State Agent 2...")
    print("=" * 50)
    
    # Import the punitive agent (assuming it exists)
    try:
        from core.agents.lab02.bos_punitive import BOSPunitiveAgent
        opponent = BOSPunitiveAgent("Punitive")
    except ImportError:
        # Fallback to random agent if punitive agent doesn't exist
        opponent = RandomBOSAgent("Random")
        print("Note: Using Random agent as fallback (BOSPunitiveAgent not found)")
    
    # Create agents
    agent = BOSFiniteStateAgent2("Agent1")
    
    # Create game and run
    game = BOSGame(rounds=100)
    agents = [agent, opponent]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent.name} statistics:")
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(agent.reward_history)}")
    print(f"Average reward: {sum(agent.reward_history) / len(agent.reward_history) if agent.reward_history else 0:.3f}")
    print(f"Final state: {agent.curr_state}")
    
    print("\nTest completed!")
