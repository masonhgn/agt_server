import sys
import os
import asyncio
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.bosii_agent import BOSIIAgent
from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSIICompetitionAgent(BOSIIAgent):
    """Competition agent for Battle of the Sexes with Incomplete Information."""
    
    def __init__(self, name: str = "BOSIIComp"):
        super().__init__(name)
        self.curr_state = 0
        self.opponent_pattern = []  # Track opponent's recent actions
        self.cooperation_count = 0  # Count cooperative moves
        self.defection_count = 0    # Count defections
    
    def get_action(self, obs=None, opponent_last_move=None, player_type=None, mood=None):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        Consider whether you're the row or column player and the mood information.
        """
        # Call parent to handle both interfaces
        super().get_action(obs, opponent_last_move, player_type, mood)
        
        # TODO: Implement your BOSII strategy here
        # Consider:
        # - Are you row or column player? (use self.is_row_player())
        # - What's your current mood (if column player)? (use self.get_mood())
        # - What's the mood history? (use self.get_mood_history())
        # - What's your current state? (use self.curr_state)
        # - What's the opponent's pattern? (use self.opponent_pattern)
        
        # Placeholder implementation - replace with your strategy
        if self.is_row_player():
            # TODO: Implement row player strategy
            return self.COMPROMISE
        else:
            # TODO: Implement column player strategy (consider mood)
            return self.COMPROMISE
    
    def update(self, observation: dict = None, action: dict = None, reward: float = None, done: bool = None, info: dict = None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        # Call parent update method
        super().update(observation, action, reward, done, info)
        
        # TODO: Implement your state transition logic here
        # Update self.curr_state based on the game history
        # Consider:
        # - Opponent's last action (use self.get_opp_last_action())
        # - Opponent's pattern (use self.opponent_pattern)
        # - Cooperation/defection counts (use self.cooperation_count, self.defection_count)
        
        # Placeholder implementation - replace with your logic
        opponent_action = self.get_opp_last_action()
        if opponent_action is not None:
            # TODO: Update opponent pattern and state transitions
            pass
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # TODO: Implement opponent action inference from reward
        # This is a simplified inference - in BOSII it's more complex
        # due to mood-dependent payoffs
        # Consider the payoff matrices for both good and bad moods
        
        # Placeholder implementation - replace with your logic
        return None  # Can't determine
    
    def setup(self):
        """Setup the agent for a new game."""
        super().setup()
        # Reset agent-specific state
        self.curr_state = 0
        self.opponent_pattern = []
        self.cooperation_count = 0
        self.defection_count = 0


# TODO: Give your agent a NAME 
name = "BOSIICompetitionAgent"  # TODO: PLEASE NAME ME D:


################### SUBMISSION #####################
agent_submission = BOSIICompetitionAgent(name)
####################################################


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "BOSIICompetitionAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = BOSIICompetitionAgent(name)
            server_agent = create_adapter(agent, "bosii")
            
            # Connect to server
            await connect_agent_to_server(server_agent, "bosii", name, host, port, verbose)
        
        # Run the async main function
        asyncio.run(main())
        
    else:
        # Test your agent locally
        print("Testing BOSII Competition Agent locally...")
        print("=" * 50)
        
        # Import opponent agent for testing
        try:
            from solutions.BOSIIMoodAwareAgent import BOSIICompetitionAgent as BOSIIMoodAwareAgent
            opponent = BOSIIMoodAwareAgent("MoodAwareAgent")
        except ImportError:
            print("Note: Mood-aware agent not found, using random agent instead")
            from core.agents.lab02.random_bos_agent import RandomBOSAgent
            opponent = RandomBOSAgent("RandomAgent")
        
        # Create agents for testing
        agent = BOSIICompetitionAgent("CompetitionAgent")
        
        # Create arena and run tournament
        from core.local_arena import LocalArena
        from core.game.BOSIIGame import BOSIIGame
        
        agents = [agent, opponent]
        arena = LocalArena(BOSIIGame, agents, num_rounds=100, verbose=True)
        arena.run_tournament()
        
        print("\nLocal test completed!")
