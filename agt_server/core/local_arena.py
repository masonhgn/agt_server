from __future__ import annotations

import time
import threading
from typing import Dict, List, Any, Optional
from itertools import combinations
import numpy as np
import pandas as pd
from pathlib import Path
import inspect
import random

from core.engine import Engine, MoveTimeout
from core.game.base_game import BaseGame
from core.agents.common.base_agent import BaseAgent
from core.utils import debug_print


class LocalArena:
    """
    local arena for running tournaments between agents.
    
    this handles:
    - running games between all pairs of agents
    - collecting and aggregating results
    - generating reports and statistics
    """
    
    def __init__(
        self,
        game_class: type[BaseGame],
        agents: List[BaseAgent],
        num_agents_per_game: int,
        num_rounds: int,
        timeout: float = 1.0,
        save_results: bool = True,
        results_path: Optional[str] = None,
        verbose: bool = True
    ):
        self.game_class = game_class
        self.agents = agents
        self.num_agents_per_game = num_agents_per_game
        self.num_rounds = num_rounds
        self.timeout = timeout
        self.save_results = save_results
        self.results_path = results_path or "results"
        self.verbose = verbose
        
        # results tracking
        self.game_results: Dict[str, Dict[str, float]] = {}
        self.agent_stats: Dict[str, Dict[str, Any]] = {}
        
        # create results directory
        if self.save_results:
            Path(self.results_path).mkdir(exist_ok=True)
    





    def run_tournament(self) -> pd.DataFrame:
        """run a full tournament of num_rounds rounds between num_agents_per_game agents"""

        debug_print(f"starting tournament with {len(self.agents)} agents")
        debug_print(f"games: {self.num_rounds} rounds each")
        debug_print(f"timeout: {self.timeout}s per move")
        debug_print("=" * 50)





        # initialize results
        agent_names = [agent.name for agent in self.agents]
        self.game_results = {name: {other: 0.0 for other in agent_names} for name in agent_names}
        self.agent_stats = {name: {} for name in agent_names}
        

        game_num = 1

        #we'll create num_pairings pairings of num_agents_per_game agents each
        num_groupings = 10

        for grouping in range(num_groupings):
            #we'll create a pairing of num_agents_per_game agents each
            grouping = random.sample(self.agents, min(self.num_agents_per_game, len(self.agents)))

            if self.verbose:
                debug_print(f"grouping: {grouping}")
            for g in grouping: g.reset() #initialize
            
            #we'll run a game between the pairing
            game = self.game_class()  # type: ignore

            try:
                engine = Engine(game, grouping, rounds=self.num_rounds)
                final_rewards = engine.run()


                for agent_idx, agent in enumerate(grouping):
                    # Use index-based access for final_rewards
                    agent_score = final_rewards[agent_idx]
                    
                    # Record against all other agents in the grouping
                    for opponent_idx, opponent in enumerate(grouping):
                        if agent_idx != opponent_idx:
                            self.game_results[agent.name][opponent.name] = agent_score

            except MoveTimeout as e:
                if self.verbose:
                    debug_print(f"  error: {e}")
                # record timeout as large negative score
                for agent in grouping:
                    self.game_results[agent.name][agent.name] = -10e9
            
            game_num += 1
        
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
        """calculate statistics for each agent."""
        agent_names = list(self.game_results.keys())
        
        for name in agent_names:
            # calculate total score and average score
            scores = [self.game_results[name][opponent] for opponent in agent_names if opponent != name]
            total_score = sum(scores)
            avg_score = total_score / len(scores) if scores else 0
            
            # calculate wins, losses, ties
            wins = sum(1 for score in scores if score > 0)
            losses = sum(1 for score in scores if score < 0)
            ties = sum(1 for score in scores if score == 0)
            
            self.agent_stats[name] = {
                'total_score': total_score,
                'average_score': avg_score,
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'win_rate': wins / len(scores) if scores else 0
            }
    
    def _generate_results_dataframe(self) -> pd.DataFrame:
        """generate a pandas dataframe with all results."""
        # create the pairwise results matrix
        agent_names = list(self.game_results.keys())
        results_matrix = []
        
        for name in agent_names:
            row = [name]
            for opponent in agent_names:
                if name == opponent:
                    row.append(0.0)  # self-play is 0
                else:
                    row.append(self.game_results[name][opponent])
            results_matrix.append(row)
        
        # create dataframe
        df = pd.DataFrame(results_matrix, columns=['agent'] + agent_names)  # type: ignore
        
        # add statistics columns
        df['total score'] = [self.agent_stats[name]['total_score'] for name in agent_names]
        df['average score'] = [self.agent_stats[name]['average_score'] for name in agent_names]
        df['wins'] = [self.agent_stats[name]['wins'] for name in agent_names]
        df['losses'] = [self.agent_stats[name]['losses'] for name in agent_names]
        df['ties'] = [self.agent_stats[name]['ties'] for name in agent_names]
        df['win rate'] = [self.agent_stats[name]['win_rate'] for name in agent_names]
        
        return df
    
    def _save_results(self, results_df: pd.DataFrame):
        """save results to files."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # save main results
        results_file = Path(self.results_path) / f"tournament_results_{timestamp}.csv"
        results_df.to_csv(results_file, index=False)
        
        # save detailed game results
        game_results_file = Path(self.results_path) / f"game_results_{timestamp}.csv"
        game_df = pd.DataFrame(self.game_results)
        game_df.to_csv(game_results_file)
        
        if self.verbose:
            debug_print(f"results saved to {self.results_path}/")
    
    def _print_summary(self, results_df: pd.DataFrame):
        """print a summary of the tournament results."""
        print("\n" + "=" * 50)
        print("tournament summary")
        print("=" * 50)
        
        # sort by total score
        sorted_df = results_df.sort_values('total score', ascending=False)
        
        print("\nfinal rankings:")
        for i, (_, row) in enumerate(sorted_df.iterrows(), 1):
            print(f"{i:2d}. {row['agent']:20s} | score: {row['total score']:6.1f} | "
                  f"avg: {row['average score']:5.1f} | "
                  f"w/l/t: {row['wins']}/{row['losses']}/{row['ties']} | "
                  f"win rate: {row['win rate']:.1%}")
        
        print("\n" + "=" * 50) 