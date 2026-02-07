import sys
import os
import asyncio
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent
from server.connect_stencil import connect_agent_to_server


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
        
        # TODO: Implement your competition strategy here
        # Use self.curr_state to determine which action to take
        # This is for the competition where you don't know the opponent's strategy
        raise NotImplementedError
    
    def update(self, observation=None, action=None, reward=None, done=None, info=None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        if reward is not None:
            self.reward_history.append(reward)
        
        # TODO: Implement your state transition logic here
        # Use self.get_last_action() and self.get_opponent_last_action() 
        # to determine how to update self.curr_state
        
        # TODO: Implement your state transition logic here
        # Use self.get_last_action() and self.get_opponent_last_action() 
        # to determine how to update self.curr_state
        raise NotImplementedError
    
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
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "BOSCompetitionAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        async def main():
            agent = BOSCompetitionAgent(name)
            await connect_agent_to_server(agent, "bos", name, host, port, verbose)

        asyncio.run(main())
        
    else:
        # Test your agent locally
        print("Testing BOS Competition Agent locally...")
        print("=" * 50)

        agent = BOSCompetitionAgent("CompetitionAgent")
        opponent = RandomBOSAgent("RandomAgent")

        agents = [agent, opponent]
        game_instance = BOSGame(rounds=1000)
        engine = Engine(game_instance, agents, rounds=1000)
        final_rewards = engine.run()

        for i, a in enumerate(agents):
            print(f"{a.name}: {final_rewards[i]:.2f}")

        print("\nLocal test completed!")
