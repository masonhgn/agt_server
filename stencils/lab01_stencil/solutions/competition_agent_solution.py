import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

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
        import random
        if random.random() < 0.7:
            return self.SWERVE
        else:
            return self.CONTINUE
    
    def update(self, reward=None, info=None):
        """
        Updates your agent with the current history, namely your opponent's choice 
        and your agent's utility in the last game.
        
        Args:
            reward: Your agent's utility in the last game
            info: Additional information (may contain opponent's action)
        """
        # TODO: Add any additional state updates your strategy needs
        if reward is not None:
            self.reward_history.append(reward)
        
        # You can access your action history with self.action_history
        # You can access your reward history with self.reward_history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Competition Agent for Lab 01')
    parser.add_argument('--name', type=str, help='Agent name (default: CompetitionAgent_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='chicken', help='Game type (default: chicken)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    
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
        client = AGTClient(server_agent, args.host, args.port, verbose=args.verbose)
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