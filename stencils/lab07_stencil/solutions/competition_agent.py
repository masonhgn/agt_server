import sys
import os
import time
import argparse

# Add parent directory to path to import from core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.agents.lab06.base_auction_agent import BaseAuctionAgent

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
    #### DO NOT TOUCH THIS #####
    parser = argparse.ArgumentParser(description='My Agent')
    parser.add_argument('--join_server', action='store_true',
                        help='Connects the agent to the server')
    parser.add_argument('--ip', type=str, default='127.0.0.1',
                        help='IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port number (default: 8080)')

    args = parser.parse_args()

    if args.join_server:
        print("Server mode not implemented in this version")
    else:
        # Create a simple test environment
        from core.game.AuctionGame import AuctionGame
        # from core.agents.test_auction_agents import RandomAuctionAgent
        
        def valuation_function(bundle):
            return sum(10 for item in bundle)
        
        goods = {"A", "B", "C"}
        valuation_functions = {
            "Competition": valuation_function,
            "Agent_1": valuation_function,
            "Agent_2": valuation_function,
            "Agent_3": valuation_function,
            "Agent_4": valuation_function,
            "Agent_5": valuation_function,
            "Agent_6": valuation_function,
        }
        
        game = AuctionGame(goods, valuation_functions, num_rounds=100, kth_price=1)
        
        # Set up agents
        agent_submission.setup(goods, valuation_function, 1)
        agents = {
            "Agent_1": CompetitionAgent("Agent_1"),
            "Agent_2": CompetitionAgent("Agent_2"),
            "Agent_3": CompetitionAgent("Agent_3"),
            "Agent_4": CompetitionAgent("Agent_4"),
            "Agent_5": CompetitionAgent("Agent_5"),
            "Agent_6": CompetitionAgent("Agent_6"),
        }
        
        for agent in agents.values():
            agent.setup(goods, valuation_function, 1)
        
        start = time.time()
        
        # Run test rounds
        for round_num in range(100):
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