import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class AuctionExampleAgent(BaseAgent):
    """Example Auction agent for Lab 06 that connects to the server."""
    
    def __init__(self, name: str = "AuctionExample"):
        super().__init__(name)
    
    def get_action(self, valuation_func=None, goods=None):
        """
        Simple auction strategy using marginal value bidding.
        
        This is a basic implementation that students can replace with their own strategy.
        
        Args:
            valuation_func: Function that takes a bundle (set) and returns its value
            goods: Set of available goods to bid on
            
        Returns:
            Dictionary mapping goods to bid amounts
        """
        if not goods or not valuation_func:
            # Fallback if no valuation function or goods provided
            return {"A": 0, "B": 0, "C": 0, "D": 0}
        
        # Simple strategy: bid 80% of the individual good values
        bids = {}
        for good in goods:
            # Calculate value of just this good
            individual_value = valuation_func({good})
            # Bid 80% of the individual value
            bids[good] = int(individual_value * 0.8)
        
        return bids
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auction Example Agent for Lab 06')
    parser.add_argument('--name', type=str, help='Agent name (default: AuctionExample_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='auction', help='Game type (default: auction)')
    
    args = parser.parse_args()
    
    # Generate unique name if not provided
    if not args.name:
        import random
        agent_name = f"AuctionExample_{random.randint(1000, 9999)}"
    else:
        agent_name = args.name
        
    # Create agent
    agent = AuctionExampleAgent(agent_name)
    
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
agent_submission = AuctionExampleAgent("AuctionExampleAgent")
