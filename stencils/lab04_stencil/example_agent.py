import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class LemonadeExampleAgent(BaseAgent):
    """Example Lemonade agent for Lab 04 that connects to the server."""
    
    def __init__(self, name: str = "LemonadeExample"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
    
    def get_action(self, opponent_positions=None):
        """
        Simple Lemonade strategy using positioning.
        
        This is a basic implementation that students can replace with their own strategy.
        
        Args:
            opponent_positions: List of opponent positions (e.g., [3, 7] for 2 opponents)
        """
        import random
        
        # Simple strategy: find a position away from opponents
        if not opponent_positions or len(opponent_positions) == 0:
            # No opponents or first round, choose randomly
            return random.choice(self.positions)
        
        # Find a position that maximizes distance from opponents
        best_position = 0
        max_min_distance = 0
        
        for pos in self.positions:
            # Calculate minimum distance to any opponent
            min_distance = min(self._circular_distance(pos, opp_pos) for opp_pos in opponent_positions)
            
            if min_distance > max_min_distance:
                max_min_distance = min_distance
                best_position = pos
        
        return best_position
    
    def _circular_distance(self, pos1, pos2):
        """Calculate circular distance between two positions on a 12-position circle."""
        direct_distance = abs(pos1 - pos2)
        circular_distance = min(direct_distance, 12 - direct_distance)
        return circular_distance
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lemonade Example Agent for Lab 04')
    parser.add_argument('--name', type=str, help='Agent name (default: LemonadeExample_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='lemonade', help='Game type (default: lemonade)')
    
    args = parser.parse_args()
    
    # Generate unique name if not provided
    if not args.name:
        import random
        agent_name = f"LemonadeExample_{random.randint(1000, 9999)}"
    else:
        agent_name = args.name
        
    # Create agent
    agent = LemonadeExampleAgent(agent_name)
    
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
agent_submission = LemonadeExampleAgent("LemonadeExampleAgent")
