#!/usr/bin/env python3
"""
engine for running games between agents.

this module provides the main engine for running games between multiple agents.
"""

import time
import threading
from typing import Any, Callable, Dict, Hashable, List, Tuple
import random

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
        
    def _get_agent_action(self, agent: BaseAgent, obs: Dict[str, Any]) -> Any:
        """
        Get action from agent using the appropriate method based on agent type.
        For Lab 1 agents, this calls predict()/optimize() or calc_move_probs() directly.
        For other agents, this calls get_action().
        """
        # Check if this is a Lab 1 agent by looking for the specific method implementations
        if hasattr(agent, 'predict') and hasattr(agent, 'optimize') and hasattr(agent, 'calc_move_probs'):
            # This is a Lab 1 agent - use the new architecture
            if hasattr(agent, '_is_fictitious_play') and agent._is_fictitious_play:
                # Fictitious Play agent: call predict() then optimize()
                dist = agent.predict()
                action = agent.optimize(dist)
            elif hasattr(agent, '_is_exponential_weights') and agent._is_exponential_weights:
                # Exponential Weights agent: call calc_move_probs() then sample
                move_probs = agent.calc_move_probs()
                action = random.choices(agent.actions, weights=move_probs, k=1)[0]
            else:
                # Default: use get_action() for backward compatibility
                action = agent.get_action(obs)
        else:
            # Regular agent: use get_action()
            action = agent.get_action(obs)
        
        return action
        
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
        
        # reset all agents and call setup
        for agent in self.agents:
            agent.reset()
            # For auction agents, set up with goods (no valuation function needed)
            if hasattr(agent, 'setup') and hasattr(agent, 'goods'):
                agent.setup(self.game.goods, self.game.kth_price)
            else:
                agent.setup()
        
        # run the game
        for round_num in range(num_rounds):
            # For auction games, generate valuations BEFORE getting actions
            if hasattr(self.game, 'generate_valuations_for_round'):
                self.game.generate_valuations_for_round()
            
            # For auction games, set valuations on agents before getting actions
            if hasattr(self.game, 'current_valuations') and hasattr(self.game, 'players'):
                for i, agent in enumerate(self.agents):
                    if hasattr(agent, 'set_valuations') and i < len(self.game.players):
                        player_name = self.game.players[i]
                        valuations = self.game.current_valuations[player_name]
                        agent.set_valuations(valuations)
            
            # get actions from all agents
            actions = {}
            for i, agent in enumerate(self.agents):
                # get agent-specific observation
                agent_obs = obs.get(i, {})
                action = self._get_agent_action(agent, agent_obs)
                actions[i] = action
                if hasattr(agent, 'action_history'):
                    agent.action_history.append(action)
            
            # step the game
            obs, rewards, done, info = self.game.step(actions)
            
            # update agents with results and track opponent actions
            for i, agent in enumerate(self.agents):
                reward = rewards.get(i, 0)
                agent_info = info.get(i, {})
                agent.update(obs.get(i, {}), actions.get(i, {}), reward, done, agent_info)
                self.cumulative_reward[i] += reward
                
                # Track opponent actions for 2-player games
                if len(self.agents) == 2:
                    opponent_idx = 1 - i  # Other player
                    opponent_action = actions.get(opponent_idx)
                    opponent_reward = rewards.get(opponent_idx, 0)
                    if opponent_action is not None and hasattr(agent, 'add_opponent_action'):
                        agent.add_opponent_action(opponent_action)
                        agent.add_opponent_reward(opponent_reward)
            
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
        
        # For auction games, set valuations on agents before getting actions
        if hasattr(self.game, 'current_valuations') and hasattr(self.game, 'players'):
            for i, agent in enumerate(self.agents):
                if hasattr(agent, 'set_valuations') and i < len(self.game.players):
                    player_name = self.game.players[i]
                    valuations = self.game.current_valuations[player_name]
                    agent.set_valuations(valuations)
        
        # get actions from all agents
        actions = {}
        for i, agent in enumerate(self.agents):
            agent_obs = obs.get(i, {})
            action = self._get_agent_action(agent, agent_obs)
            actions[i] = action
            if hasattr(agent, 'action_history'):
                agent.action_history.append(action)
        
        # step the game
        obs, rewards, done, info = self.game.step(actions)
        
        # update agents with results and track opponent actions
        for i, agent in enumerate(self.agents):
            reward = rewards.get(i, 0)
            agent_info = info.get(i, {})
            agent.update(obs.get(i, {}), actions.get(i, {}), reward, done, agent_info)
            self.cumulative_reward[i] += reward
            
            # Track opponent actions for 2-player games
            if len(self.agents) == 2:
                opponent_idx = 1 - i  # Other player
                opponent_action = actions.get(opponent_idx)
                opponent_reward = rewards.get(opponent_idx, 0)
                if opponent_action is not None and hasattr(agent, 'add_opponent_action'):
                    agent.add_opponent_action(opponent_action)
                    agent.add_opponent_reward(opponent_reward)
        
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
