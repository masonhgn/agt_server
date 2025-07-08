import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game.AdxTwoDayGame import AdxTwoDayGame
from stencils.lab09_stencil.my_adx_agent import MyAdXAgent
from stencils.lab09_stencil.example_solution import ExampleAdXAgent

NUM_AGENTS = 2

def main():
    game = AdxTwoDayGame(num_agents=NUM_AGENTS)
    obs = game.reset(seed=42)

    agents = [MyAdXAgent(), ExampleAdXAgent()]
    # Assign campaigns to agents for day 1
    for i, agent in enumerate(agents):
        agent.campaign_day1 = obs[i]["campaign_day1"]
        agent.campaign_day2 = None

    # Collect bid bundles for day 1
    actions_day1 = {}
    for i, agent in enumerate(agents):
        actions_day1[i] = agent.get_bid_bundle(day=1)

    # After day 1, assign day 2 campaigns
    for i, agent in enumerate(agents):
        agent.campaign_day2 = game.agent_campaigns[i][1]

    # Collect bid bundles for day 2
    actions_day2 = {}
    for i, agent in enumerate(agents):
        actions_day2[i] = agent.get_bid_bundle(day=2)

    # Run the game
    _, rewards, _, info = game.step(actions_day1, actions_day2)
    for i, agent in enumerate(agents):
        print(f"Agent {i} ({agent.__class__.__name__}): Reward = {rewards[i]:.2f}, Info = {info[i]}")

if __name__ == "__main__":
    main() 