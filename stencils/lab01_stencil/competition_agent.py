import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class CompetitionAgent(BaseAgent):
    def __init__(self, name: str = "Competition"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
    
    def get_action(self, opponent_last_move=None):
        """
        Simple competition strategy using Fictitious Play.
        
        This is a basic implementation that students can replace with their own strategy.
        
        Args:
            opponent_last_move: The opponent's last move (0=rock, 1=paper, 2=scissors, None=first round)
        """
        import random
        
        # For now, use a simple random strategy
        # Students should replace this with their actual implementation
        return random.choice(self.actions)
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Competition Agent for Lab 01')
    parser.add_argument('--name', type=str, help='Agent name (default: CompetitionAgent_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='rps', help='Game type (default: rps)')
    
    args = parser.parse_args()
    
    # Add server directory to path for imports
    server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
    sys.path.insert(0, server_dir)
    
    from client import AGTClient
    from adapters import create_adapter
    
    async def main():
        # Generate unique name if not provided
        if not args.name:
            import random
            agent_name = f"CompetitionAgent_{random.randint(1000, 9999)}"
        else:
            agent_name = args.name
            
        # Create agent
        agent = CompetitionAgent(agent_name)
        
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
agent_submission = CompetitionAgent("CompetitionAgent") 