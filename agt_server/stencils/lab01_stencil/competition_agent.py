#!/usr/bin/env python3
"""
Competition Agent for Lab 1 - Chicken Game
This is the agent you will submit for the class competition.
"""

import sys
import os
import asyncio
import argparse
import random

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.chicken_agent import ChickenAgent
from server.connect_stencil import connect_agent_to_server


class CompetitionAgent(ChickenAgent):
    """Your competition agent for the Chicken game."""
    
    def __init__(self, name: str = "CompetitionAgent"):
        super().__init__(name)
        # TODO: Initialize any variables you need for your strategy
        self.SWERVE, self.CONTINUE = 0, 1
    
    def setup(self):
        """
        Initializes the agent for each new game they play.
        Called at the beginning of each new game.
        """
        # TODO: Initialize your agent for a new game
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
        raise NotImplementedError
    
    def update(self, obs=None, actions=None, reward=None, done=None, info=None):
        """
        Updates your agent with the current history, namely your opponent's choice 
        and your agent's utility in the last game.
        
        Args:
            obs: Current observation from the game
            actions: Actions taken by all players
            reward: Your agent's utility in the last game
            done: Whether the game is finished
            info: Additional information (may contain opponent's action)
        """
        # TODO: Add any additional state updates your strategy needs
        if reward is not None:
            self.reward_history.append(reward)
        
        # You can access your action history with self.action_history
        # You can access your reward history with self.reward_history


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = False  # Set to True to connect to server, False for local testing
    name = ...  # TODO: Please give your agent a name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    game = "chicken"  # Game type (hardcoded for this agent)
    
    if server:
        async def main():
            agent = CompetitionAgent(name)
            await connect_agent_to_server(agent, game, name, host, port, verbose)

        asyncio.run(main())
    else:
        # Test your agent locally
        print("Testing Chicken Competition Agent locally...")
        print("=" * 50)

        from core.engine import Engine
        from core.game.ChickenGame import ChickenGame
        from core.agents.lab03.random_chicken_agent import RandomChickenAgent

        agent = CompetitionAgent("CompetitionAgent")
        opponent = RandomChickenAgent("RandomAgent")

        agents = [agent, opponent]
        game_instance = ChickenGame(rounds=1000)
        engine = Engine(game_instance, agents, rounds=1000)
        final_rewards = engine.run()

        for i, a in enumerate(agents):
            print(f"{a.name}: {final_rewards[i]:.2f}")

        print("\nLocal test completed!")

# Export for server testing
agent_submission = CompetitionAgent("CompetitionAgent")
