#!/usr/bin/env python3
"""
Game framework for Lab 3.
"""

import sys
import os

# Add the core directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.engine import Engine
from core.game.ChickenGame import ChickenGame


class GameFramework:
    """Game framework for running simulations."""
    
    def __init__(self, game_type: str = "chicken", rounds: int = 100):
        """
        Initialize game framework.
        
        Args:
            game_type: Type of game to play
            rounds: Number of rounds
        """
        self.game_type = game_type
        self.rounds = rounds
        
        if game_type == "chicken":
            self.game = ChickenGame(rounds=rounds)
        else:
            raise ValueError(f"Unknown game type: {game_type}")
    
    def run_simulation(self, agents):
        """
        Run a simulation with the given agents.
        
        Args:
            agents: List of agents to play
            
        Returns:
            Final rewards for each agent
        """
        engine = Engine(self.game, agents, rounds=self.rounds)
        return engine.run()
    
    def run_training(self, agents, training_rounds: int = 20000):
        """
        Run training simulation.
        
        Args:
            agents: List of agents to train
            training_rounds: Number of training rounds
            
        Returns:
            Training results
        """
        training_game = ChickenGame(rounds=training_rounds)
        engine = Engine(training_game, agents, rounds=training_rounds)
        return engine.run()
    
    def run_testing(self, agents, testing_rounds: int = 300):
        """
        Run testing simulation.
        
        Args:
            agents: List of agents to test
            testing_rounds: Number of testing rounds
            
        Returns:
            Testing results
        """
        testing_game = ChickenGame(rounds=testing_rounds)
        engine = Engine(testing_game, agents, rounds=testing_rounds)
        return engine.run()
