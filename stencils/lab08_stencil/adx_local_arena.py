#!/usr/bin/env python3
"""
AdX Local Arena for running tournaments between AdX agents.
This handles multi-player AdX games and bridges the gap between AdX agents and the Engine class.
"""

import time
import random
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from pathlib import Path

from core.engine import Engine, MoveTimeout
from core.game.AdxOneDayGame import AdxOneDayGame


class AdXAgentAdapter:
    """Adapter to make AdX agents compatible with the Engine class."""
    
    def __init__(self, adx_agent):
        self.adx_agent = adx_agent
        self.name = adx_agent.name
        self.campaign = None
        
        # Initialize required attributes for Engine compatibility
        self.action_history = []
        self.reward_history = []
        self.observation_history = []
        self.opp_action_history = []
        self.opp_reward_history = []
        self.game_round = 0
    
    def reset(self):
        """Reset the agent for a new game."""
        # Clear Engine-required attributes
        self.action_history = []
        self.reward_history = []
        self.observation_history = []
        self.opp_action_history = []
        self.opp_reward_history = []
        self.game_round = 0
        
        # Call original agent's reset if it exists
        if hasattr(self.adx_agent, 'reset'):
            self.adx_agent.reset()
    
    def setup(self):
        """Initialize the agent for a new game."""
        if hasattr(self.adx_agent, 'setup'):
            self.adx_agent.setup()
    
    def get_action(self, observation):
        """Bridge method: convert observation to campaign and call get_bid_bundle."""
        # Extract campaign from observation
        if 'campaign' in observation:
            self.adx_agent.campaign = observation['campaign']
        
        # Call the AdX agent's get_bid_bundle method
        return self.adx_agent.get_bid_bundle()
    
    def update(self, reward=None, info=None):
        """Update method for Engine compatibility."""
        if reward is not None:
            self.reward_history.append(reward)


class AdXLocalArena:
    """
    Local arena for running AdX tournaments between agents.
    
    This handles:
    - running multi-player AdX games
    - collecting and aggregating results
    - generating reports and statistics
    - bridging AdX agents with the Engine class
    """
    
    def __init__(
        self,
        agents: List[Any],  # List of AdX agents (will be wrapped with adapters)
        num_agents_per_game: int = 10,
        num_games: int = 100,
        timeout: float = 1.0,
        save_results: bool = True,
        results_path: Optional[str] = None,
        verbose: bool = True
    ):
        self.agents = [AdXAgentAdapter(agent) for agent in agents]
        self.num_agents_per_game = num_agents_per_game
        self.num_games = num_games
        self.timeout = timeout
        self.save_results = save_results
        self.results_path = results_path or "results"
        self.verbose = verbose
        
        # results tracking
        self.game_results: Dict[str, List[float]] = {}
        self.agent_stats: Dict[str, Dict[str, Any]] = {}
        
        # create results directory
        if self.save_results:
            Path(self.results_path).mkdir(exist_ok=True)
    
    def run_tournament(self) -> pd.DataFrame:
        """Run a full tournament with multi-player AdX games."""
        if self.verbose:
            print(f"Starting AdX tournament with {len(self.agents)} agents")
            print(f"Games: {self.num_games} games with {self.num_agents_per_game} agents each")
            print(f"Timeout: {self.timeout}s per move")
            print("=" * 50)
        
        # initialize results
        agent_names = [agent.name for agent in self.agents]
        self.game_results = {name: [] for name in agent_names}
        self.agent_stats = {name: {} for name in agent_names}
        
        # run games
        for game_num in range(self.num_games):
            if self.verbose:
                print(f"Game {game_num + 1}/{self.num_games}")
            
            # select random subset of agents for this game
            game_agents = random.sample(self.agents, min(self.num_agents_per_game, len(self.agents)))
            
            # reset agents for new game
            for agent in game_agents:
                agent.reset()
            
            # create game instance
            game = AdxOneDayGame(num_agents=len(game_agents))
            
            # run the game
            try:
                engine = Engine(game, game_agents, rounds=1)
                final_rewards = engine.run()
                
                # record results
                for i, agent in enumerate(game_agents):
                    self.game_results[agent.name].append(final_rewards[i])
                
                if self.verbose:
                    # Show top 3 performers in this game
                    game_results = [(agent.name, final_rewards[i]) for i, agent in enumerate(game_agents)]
                    game_results.sort(key=lambda x: x[1], reverse=True)
                    print(f"  Top 3: {game_results[0][0]} ({game_results[0][1]:.2f}), "
                          f"{game_results[1][0]} ({game_results[1][1]:.2f}), "
                          f"{game_results[2][0]} ({game_results[2][1]:.2f})")
                    
            except MoveTimeout as e:
                if self.verbose:
                    print(f"  Error: {e}")
                # record timeout as large negative score
                for agent in game_agents:
                    self.game_results[agent.name].append(-1000)
        
        # calculate final statistics
        self._calculate_statistics()
        
        # generate and save results
        results_df = self._generate_results_dataframe()
        
        if self.save_results:
            self._save_results(results_df)
        
        if self.verbose:
            self._print_summary(results_df)
        
        return results_df
    
    def _calculate_statistics(self):
        """Calculate statistics for each agent."""
        for name, rewards in self.game_results.items():
            if rewards:
                total_reward = sum(rewards)
                avg_reward = total_reward / len(rewards)
                max_reward = max(rewards)
                min_reward = min(rewards)
                wins = sum(1 for r in rewards if r > 0)
                win_rate = wins / len(rewards)
                
                self.agent_stats[name] = {
                    'total_reward': total_reward,
                    'average_reward': avg_reward,
                    'max_reward': max_reward,
                    'min_reward': min_reward,
                    'wins': wins,
                    'games_played': len(rewards),
                    'win_rate': win_rate
                }
            else:
                self.agent_stats[name] = {
                    'total_reward': 0,
                    'average_reward': 0,
                    'max_reward': 0,
                    'min_reward': 0,
                    'wins': 0,
                    'games_played': 0,
                    'win_rate': 0
                }
    
    def _generate_results_dataframe(self) -> pd.DataFrame:
        """Generate a pandas dataframe with all results."""
        agent_names = list(self.game_results.keys())
        results_data = []
        
        for name in agent_names:
            stats = self.agent_stats[name]
            results_data.append({
                'agent': name,
                'total_reward': stats['total_reward'],
                'average_reward': stats['average_reward'],
                'max_reward': stats['max_reward'],
                'min_reward': stats['min_reward'],
                'wins': stats['wins'],
                'games_played': stats['games_played'],
                'win_rate': stats['win_rate']
            })
        
        return pd.DataFrame(results_data)
    
    def _save_results(self, results_df: pd.DataFrame):
        """Save results to files."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # save main results
        results_file = Path(self.results_path) / f"adx_tournament_results_{timestamp}.csv"
        results_df.to_csv(results_file, index=False)
        
        if self.verbose:
            print(f"Results saved to {self.results_path}/")
    
    def _print_summary(self, results_df: pd.DataFrame):
        """Print a summary of the tournament results."""
        print("\n" + "=" * 50)
        print("AdX Tournament Summary")
        print("=" * 50)
        
        # sort by average reward
        sorted_df = results_df.sort_values('average_reward', ascending=False)
        
        print("\nFinal Rankings:")
        for i, (_, row) in enumerate(sorted_df.iterrows(), 1):
            print(f"{i:2d}. {row['agent']:20s} | "
                  f"avg: {row['average_reward']:6.2f} | "
                  f"total: {row['total_reward']:8.2f} | "
                  f"wins: {row['wins']:3d}/{row['games_played']:3d} | "
                  f"win rate: {row['win_rate']:.1%}")
        
        print("\n" + "=" * 50)
