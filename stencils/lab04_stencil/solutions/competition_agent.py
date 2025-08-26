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
    parser = argparse.ArgumentParser(description='Lemonade Competition Agent for Lab 04')
    parser.add_argument('--name', type=str, help='Agent name (default: LemonadeCompetition_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='lemonade', help='Game type (default: lemonade)')
    
    args = parser.parse_args()
    
    # Generate unique name if not provided
    if not args.name:
        import random
        agent_name = f"LemonadeCompetition_{random.randint(1000, 9999)}"
    else:
        agent_name = args.name
        
    # Create agent
    agent = LemonadeCompetitionAgent(agent_name)
    
    # Add server directory to path for imports
    server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
    sys.path.insert(0, server_dir)
    
    from client import AGTClient
    from adapters import create_adapter
    
    async def main():
        # Create adapter for server communication
        server_agent = create_adapter(agent, args.game)
        
        print(f"Starting {agent.name} for {args.game} game...")
        print(f"Connecting to server at {args.host}:{args.port}")
        
        # Create client and connect
        client = AGTClient(server_agent, args.host, args.port)
        await client.connect()
        
        if client.connected:
            print("Connected to server!")
            print(f"Joining {args.game} game...")
            
            if await client.join_game(args.game):
                print("Joined game successfully!")
                print("Waiting for tournament to start...")
                await client.run()
            else:
                print("Failed to join game")
        else:
            print("Failed to connect to server")
    
    # Run the async main function
    asyncio.run(main())

# Export for server testing
agent_submission = LemonadeCompetitionAgent("LemonadeCompetitionAgent")
