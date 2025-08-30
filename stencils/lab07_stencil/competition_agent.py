import sys
import os
import time
import random

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.agents.base_auction_agent import BaseAuctionAgent

class CompetitionAgent(BaseAuctionAgent):
    def setup(self, goods, valuation_function, kth_price=1):
        super().setup(goods, valuation_function, kth_price)
        pass

    def get_action(self, observation):
        # ??? 
        raise NotImplementedError
        
    def update(self, observation, action, reward, done, info):
        super().update(observation, action, reward, done, info)
        pass

################### SUBMISSION #####################
# agent_submission = CompetitionAgent(???)
agent_submission = CompetitionAgent("Competition Agent")
####################################################

if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = "CompetitionAgent"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from connect_stencil import connect_agent_to_server
        from adapters import create_adapter
        
        async def main():
            # Create agent and adapter
            agent = CompetitionAgent(name)
            server_agent = create_adapter(agent, "auction")
            
            # Connect to server
            await connect_agent_to_server(server_agent, host, port, verbose)
        
        # Run the async main function
        import asyncio
        asyncio.run(main())
    else:
        # Create a simple test environment
        from core.game.AuctionGame import AuctionGame
        from core.agents.test_auction_agents import RandomAuctionAgent
        
        # Create realistic valuation functions that simulate the original game
        def create_valuation_function(agent_name, valuation_type="complement"):
            """Create a valuation function that matches the original game's behavior."""
            def valuation_function(bundle):
                if not bundle:
                    return 0
                
                # Simulate individual good valuations (in real game these are random per round)
                # For testing, we'll use deterministic but realistic values
                base_values = {"A": 20, "B": 25, "C": 30}
                
                # Add some randomness to simulate the original game's random valuations
                random.seed(hash(agent_name) % 1000)  # Deterministic per agent
                adjusted_values = {good: base_values[good] + random.randint(-5, 5) for good in base_values}
                
                base_sum = sum(adjusted_values.get(good, 0) for good in bundle)
                n = len(bundle)
                
                if valuation_type == 'additive':
                    return base_sum
                elif valuation_type == 'complement':
                    return base_sum * (1 + 0.05 * (n - 1)) if n > 0 else 0
                elif valuation_type == 'substitute':
                    return base_sum * (1 - 0.05 * (n - 1)) if n > 0 else 0
                else:
                    return base_sum
            
            return valuation_function
        
        goods = {"A", "B", "C"}
        
        # Create different valuation functions for each agent
        valuation_functions = {
            "Competition": create_valuation_function("Competition", "complement"),
            "Agent_1": create_valuation_function("Agent_1", "complement"),
            "Agent_2": create_valuation_function("Agent_2", "complement"),
            "Agent_3": create_valuation_function("Agent_3", "complement"),
            "Agent_4": create_valuation_function("Agent_4", "complement"),
            "Agent_5": create_valuation_function("Agent_5", "complement"),
            "Agent_6": create_valuation_function("Agent_6", "complement"),
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=100, kth_price=1)
        
        # Set up agents
        agent_submission.setup(goods, valuation_functions["Competition"], 1)
        agents = {
            "Agent_1": CompetitionAgent("Agent_1"),
            "Agent_2": CompetitionAgent("Agent_2"),
            "Agent_3": CompetitionAgent("Agent_3"),
            "Agent_4": CompetitionAgent("Agent_4"),
            "Agent_5": CompetitionAgent("Agent_5"),
            "Agent_6": CompetitionAgent("Agent_6"),
        }
        
        for name, agent in agents.items():
            agent.setup(goods, valuation_functions[name], 1)
        
        start = time.time()
        
        # Run test rounds
        for round_num in range(100):
            # Create observation with the agent's specific valuation function
            observation = {"goods": goods, "round": round_num}
            
            # Get actions from all agents
            actions = {}
            actions["Competition"] = agent_submission.get_action(observation)
            for name, agent in agents.items():
                actions[name] = agent.get_action(observation)
            
            # Run round
            results = game.run_round(actions)
            
            # Update agents
            agent_submission.update(observation, actions["Competition"], results["utilities"]["Competition"], False, results)
            for name, agent in agents.items():
                agent.update(observation, actions[name], results["utilities"][name], False, results)
        
        end = time.time()
        print(f"{end - start} Seconds Elapsed") 