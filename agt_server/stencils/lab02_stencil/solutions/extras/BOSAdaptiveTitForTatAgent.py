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
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        # TODO: Implement your competition strategy here
        # Use self.curr_state to determine which action to take
        # This is for the competition where you don't know the opponent's strategy
        
        # Simple implementation for testing
        import random
        return random.choice([self.STUBBORN, self.COMPROMISE])
    
    def update(self, reward: float, info=None, observation: dict = None, action: dict = None, done: bool = None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        self.reward_history.append(reward)
        
        # TODO: Implement your state transition logic here
        # Use self.get_last_action() and self.get_opponent_last_action() 
        # to determine how to update self.curr_state
        
        # Simple implementation for testing
        pass
    
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
    
    # Import opponent agents for testing
    try:
        from ..bos_punitive import BOSPunitiveAgent
        from ..bos_reluctant import BOSReluctantAgent
    except ImportError:
        print("Note: Opponent agents not found, using random agents instead")
        from core.agents.lab02.random_bos_agent import RandomBOSAgent
        BOSPunitiveAgent = RandomBOSAgent
        BOSReluctantAgent = RandomBOSAgent
    
    # Create agents for testing
    agent = BOSCompetitionAgent("CompetitionAgent")
    opponent1 = BOSPunitiveAgent("PunitiveAgent")
    opponent2 = BOSReluctantAgent("ReluctantAgent")
    
    # Create game and run
    game = BOSGame(rounds=1000)
    agents = [agent, opponent1, opponent2]
    
    engine = Engine(game, agents, rounds=1000)
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
    
    print("\nLocal test completed!")
