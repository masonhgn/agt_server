import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class LemonadeCompetitionAgent(BaseAgent):
    """Competition agent for Lab 04 - Lemonade Stand positioning game."""
    
    def __init__(self, name: str = "LemonadeCompetition"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, opponent_positions=None):
        """
        TODO: Implement your competition strategy here!
        
        This is where you'll put your best Lemonade Stand agent implementation.
        You can use any combination of:
        - Fictitious Play
        - Best Response
        - Pattern recognition
        - Game theory analysis
        - Q-Learning
        - Or any other approach you think will work well
        
        Args:
            opponent_positions: List of opponent positions (e.g., [3, 7] for 2 opponents)
            
        Return an integer from 0-11 representing your chosen position
        """
        # TODO: Fill out your competition strategy
        raise NotImplementedError
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs
    
    def _circular_distance(self, pos1, pos2):
        """Helper method to calculate circular distance between two positions."""
        direct_distance = abs(pos1 - pos2)
        circular_distance = min(direct_distance, 12 - direct_distance)
        return circular_distance


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    name = None  # Agent name (None for auto-generated)
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "lemonade"  # Game type (hardcoded for this agent)
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Generate unique name if not provided
            if not name:
                import random
                agent_name = f"LemonadeCompetition_{random.randint(1000, 9999)}"
            else:
                agent_name = name
                
            # Create agent and adapter
            agent = LemonadeCompetitionAgent(agent_name)
            server_agent = create_adapter(agent, game)
            
            # Connect to server
            await connect_agent_to_server(server_agent, game, agent_name, host, port, verbose)
        
        # Run the async main function
        asyncio.run(main())
    else:
        # Local testing logic here
        print("Running local test...")
        # TODO: Add local testing code
        print("Local test completed!")

# Export for server testing
agent_submission = LemonadeCompetitionAgent("LemonadeCompetitionAgent")
