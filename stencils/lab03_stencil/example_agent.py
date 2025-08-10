import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class ChickenExampleAgent(BaseAgent):
    """Example Chicken agent for Lab 03 that connects to the server."""
    
    def __init__(self, name: str = "ChickenExample"):
        super().__init__(name)
        self.SWERVE, self.CONTINUE = 0, 1
        self.actions = [self.SWERVE, self.CONTINUE]
    
    def get_action(self, opponent_last_move=None):
        """
        Simple Chicken strategy using Q-Learning concepts.
        
        This is a basic implementation that students can replace with their own strategy.
        
        Args:
            opponent_last_move: The opponent's last move (0=swerve, 1=continue, None=first round)
        """
        import random
        
        # Simple strategy: swerve if opponent continued last time, otherwise random
        if opponent_last_move == self.CONTINUE:
            # Opponent was aggressive last time, be more cautious
            return self.SWERVE
        else:
            # Opponent was cooperative or first round, be more aggressive
            return random.choice([self.SWERVE, self.CONTINUE])
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Infer opponent's action from reward and my action
        if my_last_action == self.SWERVE:
            if my_last_reward == 0:
                return self.SWERVE  # Both swerved
            elif my_last_reward == -1:
                return self.CONTINUE  # I swerved, they continued
        elif my_last_action == self.CONTINUE:
            if my_last_reward == 1:
                return self.SWERVE  # I continued, they swerved
            elif my_last_reward == -5:
                return self.CONTINUE  # Both continued
        
        return None  # Can't determine


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chicken Example Agent for Lab 03')
    parser.add_argument('--name', type=str, help='Agent name (default: ChickenExample_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='chicken', help='Game type (default: chicken)')
    
    args = parser.parse_args()
    
    # Generate unique name if not provided
    if not args.name:
        import random
        agent_name = f"ChickenExample_{random.randint(1000, 9999)}"
    else:
        agent_name = args.name
        
    # Create agent
    agent = ChickenExampleAgent(agent_name)
    
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
agent_submission = ChickenExampleAgent("ChickenExampleAgent")
