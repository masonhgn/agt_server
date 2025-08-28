import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class AuctionCompetitionAgent(BaseAgent):
    """Competition agent for Lab 06 - Simultaneous Auction bidding."""
    
    def __init__(self, name: str = "AuctionCompetition"):
        super().__init__(name)
    
    def get_action(self, valuation_func=None, goods=None):
        """
        TODO: Implement your competition strategy here!
        
        This is where you'll put your best auction bidding implementation.
        You can use any combination of:
        - Marginal value calculation
        - Local bidding algorithm
        - Best response strategies
        - Game theory analysis
        - Or any other approach you think will work well
        
        Args:
            valuation_func: Function that takes a bundle (set) and returns its value
            goods: Set of available goods to bid on
            
        Return a dictionary mapping goods to bid amounts
        """
        # TODO: Fill out your competition strategy
        raise NotImplementedError
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs
    
    def calculate_marginal_value(self, goods, selected_good, valuation_func, bids, prices):
        """
        Helper method to calculate marginal value of a good.
        
        Args:
            goods: Set of all available goods
            selected_good: The good to calculate marginal value for
            valuation_func: Function that takes a bundle and returns its value
            bids: Current bid vector (dict mapping goods to bids)
            prices: Price vector (dict mapping goods to prices)
            
        Returns:
            Marginal value of the selected good
        """
        # Determine which goods you would win with current bids
        won_goods = set()
        for good in goods:
            if bids.get(good, 0) >= prices.get(good, 0):
                won_goods.add(good)
        
        # Value with the selected good
        bundle_with_good = won_goods | {selected_good}
        value_with_good = valuation_func(bundle_with_good)
        
        # Value without the selected good
        bundle_without_good = won_goods - {selected_good}
        value_without_good = valuation_func(bundle_without_good)
        
        # Marginal value is the difference
        marginal_value = value_with_good - value_without_good
        
        return marginal_value


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    name = None  # Agent name (None for auto-generated)
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "auction"  # Game type (hardcoded for this agent)
    
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
                agent_name = f"AuctionCompetition_{random.randint(1000, 9999)}"
            else:
                agent_name = name
                
            # Create agent and adapter
            agent = AuctionCompetitionAgent(agent_name)
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
agent_submission = AuctionCompetitionAgent("AuctionCompetitionAgent")
