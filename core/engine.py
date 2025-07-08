#!/usr/bin/env python3
"""
engine for running games between agents.

this module provides the main engine for running games between multiple agents.
"""

import time
import threading
from typing import Any, Callable, Dict, Hashable, List, Tuple

from core.game import ObsDict, ActionDict, RewardDict, BaseGame
from core.agents.common.base_agent import BaseAgent


PlayerId = Hashable


class MoveTimeout(Exception):
    """Raised when an agent fails to return an action in time."""


class Engine:
    """main engine for running games between agents."""
    
    def __init__(self, game: BaseGame, agents: List[BaseAgent], rounds: int = 100):
        """
        initialize the engine.
        
        args:
            game: the game to run
            agents: list of agents to play the game
            rounds: number of rounds to run
        """
        self.game = game
        self.agents = agents
        self.rounds = rounds
        self.cumulative_reward = [0] * len(agents)
        
    def run(self, num_rounds: int = None) -> List[float]:
        """
        run the game for the specified number of rounds.
        
        args:
            num_rounds: number of rounds to run (defaults to self.rounds)
            
        returns:
            list of final rewards for each agent
        """
        if num_rounds is None:
            num_rounds = self.rounds
            
        # reset the game
        obs = self.game.reset()
        
        # reset all agents
        for agent in self.agents:
            agent.reset()
        
        # run the game
        for round_num in range(num_rounds):
            # get actions from all agents
            actions = {}
            for i, agent in enumerate(self.agents):
                # get agent-specific observation
                agent_obs = obs.get(i, {})
                action = agent.get_action(agent_obs)
                actions[i] = action
            
            # step the game
            obs, rewards, done, info = self.game.step(actions)
            
            # update agents with results
            for i, agent in enumerate(self.agents):
                reward = rewards.get(i, 0)
                agent_info = info.get(i, {})
                agent.update(reward, agent_info)
                self.cumulative_reward[i] += reward
            
            # check if game is done
            if done:
                break
        
        return self.cumulative_reward.copy()
    
    def run_single_round(self) -> Tuple[List[float], Dict[str, Any]]:
        """
        run a single round of the game.
        
        returns:
            tuple of (rewards, info)
        """
        # get current observation
        obs = self.game.get_observation()
        
        # get actions from all agents
        actions = {}
        for i, agent in enumerate(self.agents):
            agent_obs = obs.get(i, {})
            action = agent.get_action(agent_obs)
            actions[i] = action
        
        # step the game
        obs, rewards, done, info = self.game.step(actions)
        
        # update agents with results
        for i, agent in enumerate(self.agents):
            reward = rewards.get(i, 0)
            agent_info = info.get(i, {})
            agent.update(reward, agent_info)
            self.cumulative_reward[i] += reward
        
        return rewards, info
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        get statistics about the current game state.
        
        returns:
            dictionary containing game statistics
        """
        stats = {
            "cumulative_rewards": self.cumulative_reward.copy(),
            "agent_names": [agent.name for agent in self.agents],
            "game_state": self.game.get_game_state()
        }
        
        # add agent-specific statistics
        for i, agent in enumerate(self.agents):
            if hasattr(agent, 'get_statistics'):
                stats[f"agent_{i}_stats"] = agent.get_statistics()
        
        return stats
