import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.chicken_agent import ChickenAgent


class CompetitionAgent(ChickenAgent):
    def setup(self):
        """
        Initializes the agent for each new game they play.
        Called before each new game starts.
        """
        # TODO: Initialize any variables you need for a new game
        # This method is called at the beginning of each new game
        pass
    
    def get_action(self, obs=None):
        """
        Returns your agent's next action for the Chicken game.
        
        Actions:
        0 = Swerve
        1 = Continue
        
        Chicken payoff matrix (row player, column player):
        S\\C  S  C
        S    0  -1
        C    1  -5
        
        Where S = Swerve, C = Continue
        """
        # TODO: Implement your Chicken strategy here
        # You can use any strategy you want, but it should not be uniform random
        
        # For now, using a simple strategy that swerves 70% of the time
        # Students should replace this with their actual implementation
        return self.CONTINUE
        import random
        if random.random() < 0.5:
            return self.SWERVE
        else:
            return self.CONTINUE
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """
        Updates your agent with the current history, namely your opponent's choice 
        and your agent's utility in the last game.
        
        Args:
            obs: Current observation from the game
            actions: Actions taken by all players
            reward: Your agent's utility in the last game
            done: Whether the game is finished
            info: Additional information (may contain opponent's action)
        """
        # TODO: Add any additional state updates your strategy needs
        if reward is not None:
            self.reward_history.append(reward)
        
        # You can access your action history with self.action_history
        # You can access your reward history with self.reward_history


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "FRIENDLY_DUCK"  # Agent name (None for auto-generated)
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "chicken"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Generate unique name if not provided
            if not name:
                import random
                agent_name = f"CompetitionAgent_{random.randint(1000, 9999)}"
            else:
                agent_name = name
                
            # Create agent and adapter
            agent = CompetitionAgent(agent_name)
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, agent_name, host, port, verbose)
        
        # Run the async main function
        asyncio.run(main())
    else:
        # Test your agent locally
        print("Testing Chicken Competition Agent locally...")
        print("=" * 50)
        
        # Import opponent agents and arena for testing
        from core.agents.lab03.swerve_agent import SwerveAgent
        from core.agents.lab03.continue_agent import ContinueAgent
        from core.agents.lab03.random_chicken_agent import RandomChickenAgent
        from core.local_arena import LocalArena
        from core.game.ChickenGame import ChickenGame
        
        # Create agents for testing
        agent = CompetitionAgent("CompetitionAgent")
        '''
        opponent1 = SwerveAgent("SwerveAgent")
        opponent2 = ContinueAgent("ContinueAgent")
        opponent3 = RandomChickenAgent("RandomAgent")
        '''
        opponent1 = CompetitionAgent("CompetitionAgent1")
        opponent2 = CompetitionAgent("CompetitionAgent2")
        opponent3 = CompetitionAgent("CompetitionAgent3")
        
        # Create arena and run tournament
        agents = [agent, opponent1, opponent2, opponent3]
        arena = LocalArena(ChickenGame, agents, num_rounds=1000, verbose=True)
        arena.run_tournament()
        
        print("\nLocal test completed!")

# Export for server testing
agent_submission = CompetitionAgent("CompetitionAgent") 