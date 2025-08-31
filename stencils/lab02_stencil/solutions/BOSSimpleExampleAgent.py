import sys
import os
import asyncio
import argparse

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.base_agent import BaseAgent


class BOSExampleAgent(BaseAgent):
    """Example BOS agent for Lab 02 that connects to the server."""
    
    def __init__(self, name: str = "BOSExample"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
    
    def get_action(self, opponent_last_move=None):
        """
        Simple BOS strategy using a finite state machine.
        
        This is a basic implementation that students can replace with their own strategy.
        
        Args:
            opponent_last_move: The opponent's last move (0=compromise, 1=stubborn, None=first round)
        """
        import random
        
        # Simple state machine: alternate between compromise and stubborn
        if self.curr_state == 0:
            action = self.COMPROMISE
        else:
            action = self.STUBBORN
            
        # Update state for next round
        self.curr_state = (self.curr_state + 1) % 2
        
        return action
    
    def update(self, reward: float, info=None, observation: dict = None, action: dict = None, done: bool = None):
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
        if my_last_action == self.COMPROMISE:
            if my_last_reward == 0:
                return self.COMPROMISE  # Both compromised
            elif my_last_reward == 3:
                return self.STUBBORN     # I compromised, they were stubborn
        elif my_last_action == self.STUBBORN:
            if my_last_reward == 7:
                return self.COMPROMISE   # I was stubborn, they compromised
            elif my_last_reward == 0:
                return self.STUBBORN     # Both were stubborn
        
        return None  # Can't determine


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BOS Example Agent for Lab 02')
    parser.add_argument('--name', type=str, help='Agent name (default: BOSExample_<random>)')
    parser.add_argument('--host', type=str, default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8080, help='Server port')
    parser.add_argument('--game', type=str, default='bos', help='Game type (default: bos)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose debug output')
    
    args = parser.parse_args()
    
    # Generate unique name if not provided
    if not args.name:
        import random
        agent_name = f"BOSExample_{random.randint(1000, 9999)}"
    else:
        agent_name = args.name
        
    # Create agent
    agent = BOSExampleAgent(agent_name)
    
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
agent_submission = BOSExampleAgent("BOSExampleAgent")
