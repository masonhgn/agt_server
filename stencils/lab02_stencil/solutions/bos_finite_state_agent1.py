import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSFiniteStateAgent1(BaseAgent):
    """Finite State Machine agent to counter the 'reluctant to compromise' strategy."""
    
    def __init__(self, name: str = "BOSFSM1"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
        self.consecutive_compromises = 0  # Track consecutive compromises
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        Strategy to counter "reluctant to compromise":
        - The reluctant agent goes to concert (STUBBORN) most of the time
        - Only compromises after 3 consecutive lectures from opponent
        - So we should go to lecture (COMPROMISE) to force them to compromise
        """
        if self.curr_state == 0:
            # Initial state: start with compromise to establish cooperation
            return self.COMPROMISE
        elif self.curr_state == 1:
            # Cooperative state: continue compromising
            return self.COMPROMISE
        elif self.curr_state == 2:
            # Exploitation state: be stubborn to exploit their compromise
            return self.STUBBORN
        elif self.curr_state == 3:
            # Reset state: go back to compromise
            return self.COMPROMISE
        else:
            return self.COMPROMISE  # Default fallback
    
    def update(self, reward: float, info=None, observation: dict = None, action: dict = None, done: bool = None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        self.reward_history.append(reward)
        
        # Get opponent's last action
        opponent_action = self.get_opponent_last_action()
        
        if opponent_action is not None:
            if opponent_action == self.COMPROMISE:
                # Opponent compromised
                self.consecutive_compromises += 1
                if self.curr_state == 0:
                    # Initial state: opponent cooperated, stay cooperative
                    self.curr_state = 1
                elif self.curr_state == 1:
                    # Cooperative state: continue cooperating
                    pass
                elif self.curr_state == 2:
                    # Exploitation state: opponent compromised, exploit
                    pass
                elif self.curr_state == 3:
                    # Reset state: back to cooperative
                    self.curr_state = 1
            else:
                # Opponent was stubborn
                self.consecutive_compromises = 0
                if self.curr_state == 0:
                    # Initial state: opponent was stubborn, try exploitation
                    self.curr_state = 2
                elif self.curr_state == 1:
                    # Cooperative state: opponent was stubborn, try exploitation
                    self.curr_state = 2
                elif self.curr_state == 2:
                    # Exploitation state: opponent was stubborn, try reset
                    self.curr_state = 3
                elif self.curr_state == 3:
                    # Reset state: opponent was stubborn, try exploitation again
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


# Agent name for submission
name = "BOSFiniteStateAgent1"


################### SUBMISSION #####################
agent_submission = BOSFiniteStateAgent1(name)
####################################################


if __name__ == "__main__":
    # Test your agent against the reluctant strategy
    print("Testing BOS Finite State Agent 1...")
    print("=" * 50)
    
    # Import the reluctant agent
    try:
        from bos_reluctant import BOSReluctantAgent
        opponent = BOSReluctantAgent("Reluctant")
    except ImportError:
        # Fallback to random agent if reluctant agent doesn't exist
        opponent = RandomBOSAgent("Random")
        print("Note: Using Random agent as fallback (BOSReluctantAgent not found)")
    
    # Create agents
    agent = BOSFiniteStateAgent1("Agent1")
    
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
