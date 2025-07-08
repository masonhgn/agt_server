import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game.AdxOneDayGame import AdxOneDayGame
from lab08_stencil.my_adx_agent import MyAdXAgent
from lab08_stencil.example_solution import ExampleAdXAgent

NUM_AGENTS = 2

def main():
    game = AdxOneDayGame(num_agents=NUM_AGENTS)
    obs = game.reset(seed=42)

    agents = [MyAdXAgent(), ExampleAdXAgent()]
    # Assign campaigns to agents
    for i, agent in enumerate(agents):
        agent.campaign = obs[i]["campaign"]

    # Collect bid bundles
    actions = {}
    for i, agent in enumerate(agents):
        actions[i] = agent.get_bid_bundle()

    # Run the game
    _, rewards, _, info = game.step(actions)
    for i, agent in enumerate(agents):
        print(f"Agent {i} ({agent.__class__.__name__}): Reward = {rewards[i]:.2f}, Info = {info[i]}")

if __name__ == "__main__":
    main() 