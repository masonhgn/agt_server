#!/usr/bin/env python3



"""
engine for running games between agents.

this module provides the main engine for running games between multiple agents.
"""

import time
import threading
from typing import Any, Callable, Dict, Hashable, List, Tuple
import random
import asyncio
from core.game import ObsDict, ActionDict, RewardDict, BaseGame
from core.agents.common.base_agent import BaseAgent


PlayerId = Hashable


class MoveTimeout(Exception):
    """Raised when an agent fails to return an action in time."""


class Engine:
    """main engine for running games between agents."""
    
    def __init__(self, game: BaseGame, agents: List[BaseAgent], rounds: int = 100, game_title: str = None):
        """
        initialize the engine.
        
        args:
            game: the game to run
            agents: list of agents to play the game
            rounds: number of rounds to run
        """
        self.game_title = game_title
        self.game = game
        self.agents = agents
        self.rounds = rounds
        self.cumulative_reward = [0] * len(agents)
        
    # async def _get_agent_action(self, agent: BaseAgent, obs: Dict[str, Any]) -> Any:
    #     if hasattr(agent, 'get_action') and asyncio.iscoroutinefunction(agent.get_action):
    #         return await agent.get_action(obs)
    #     else:
    #         return agent.get_action(obs) 


    def _get_agent_action(self, agent: BaseAgent, obs: Dict[str, Any]) -> Any:
        #use some kind of mapping to map the game type to the appropriate action function


        #game_types = ['rps', 'bos', 'bosii', 'chicken', 'pd', 'lemonade', 'auction', 'adx_twoday', 'adx_oneday']

        # game_action_functions = {
        #     "rps": "get_action",
        #     "bos": "get_action",
        #     "bosii": "get_action",
        #     "chicken": "get_action",
        #     "pd": "get_action",
        #     "lemonade": "get_action",
        #     "auction": "get_action",
        #     "adx_oneday": "get_bid_bundle",
        #     "adx_twoday": "get_bid_bundle",
        # }


        
        #func_name = game_action_functions[self.game_title]
        # func = getattr(agent, func_name)
        # return func(obs)

        return agent.get_action(obs)



        
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
        for i, agent in enumerate(self.agents):
            agent.reset()
            # For auction agents, set up with goods (no valuation function needed)
            if hasattr(agent, 'setup') and hasattr(agent, 'goods'):
                agent.setup(self.game.goods, self.game.kth_price)
            else:
                # For all other agents, call setup without parameters
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
                        try:
                            # Get player name by index for auction games
                            if hasattr(self.game, 'get_player_name'):
                                player_name = self.game.get_player_name(i)
                            else:
                                # Fallback for non-auction games
                                player_name = f"player_{i}"
                            
                            valuations = self.game.current_valuations[player_name]
                            agent.set_valuations(valuations)
                        except (IndexError, KeyError) as e:
                            # Log error but continue - agent might not need valuations
                            print(f"Warning: Could not set valuations for agent {i}: {e}")
                            pass
            
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
                # Add player_id to agent_info for BOSII agents
                agent_info['player_id'] = i
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
                    try:
                        # Get player name by index for auction games
                        if hasattr(self.game, 'get_player_name'):
                            player_name = self.game.get_player_name(i)
                        else:
                            # Fallback for non-auction games
                            player_name = f"player_{i}"
                        
                        valuations = self.game.current_valuations[player_name]
                        agent.set_valuations(valuations)
                    except (IndexError, KeyError) as e:
                        # Log error but continue - agent might not need valuations
                        print(f"Warning: Could not set valuations for agent {i}: {e}")
                        pass
        
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
    
    # =============================================================================
    # ASYNC VERSIONS FOR SERVER USE
    # =============================================================================
    
    async def _get_agent_action_async(self, agent, obs: Dict[str, Any]) -> Any:
        """
        Async version of _get_agent_action for server use.
        Assumes agent is a PlayerConnection object with writer/reader.
        """
        # For server use, agent is a PlayerConnection object
        if hasattr(agent, 'writer') and hasattr(agent, 'reader'):
            # This is a PlayerConnection - send request and wait for response
            import json
            import time
            
            # Clear any pending action
            agent.pending_action = None
            
            # Send request to client
            message = {
                "message": "request_action",
                "observation": obs
            }
            message_str = json.dumps(message) + "\n"
            agent.writer.write(message_str.encode())
            await agent.writer.drain()
            
            # Wait for response with timeout
            timeout = 5.0
            start_time = time.time()
            while agent.pending_action is None and (time.time() - start_time) < timeout:
                await asyncio.sleep(0.1)
            
            if agent.pending_action is not None:
                action = agent.pending_action
                agent.pending_action = None
                return action
            else:
                # Timeout - use default action
                return self._get_default_action()
        else:
            # This is a regular BaseAgent - use synchronous method
            return self._get_agent_action(agent, obs)
    
    def _get_default_action(self):
        """Get default action for timeout cases."""
        # Simple default actions based on game type
        if hasattr(self.game, 'get_default_action'):
            return self.game.get_default_action()
        else:
            return 0  # Default to first action
    
    async def run_async(self, num_rounds: int = None) -> List[float]:
        """
        Async version of run method for server use.
        
        Args:
            num_rounds: number of rounds to run (defaults to self.rounds)
            
        Returns:
            list of final rewards for each agent
        """
        if num_rounds is None:
            num_rounds = self.rounds
            
        # reset the game
        obs = self.game.reset()
        
        # reset all agents and call setup
        for i, agent in enumerate(self.agents):
            # For PlayerConnection objects (server use), send setup message
            if hasattr(agent, 'writer') and hasattr(agent, 'reader'):
                # This is a PlayerConnection - send setup message
                await self._send_agent_setup(agent)
            else:
                # This is a regular BaseAgent - call methods directly
                if hasattr(agent, 'reset'):
                    agent.reset()
                # For auction agents, set up with goods (no valuation function needed)
                if hasattr(agent, 'setup') and hasattr(agent, 'goods'):
                    agent.setup(self.game.goods, self.game.kth_price)
                else:
                    # For all other agents, call setup without parameters
                    if hasattr(agent, 'setup'):
                        agent.setup()
        
        # run the game
        for round_num in range(num_rounds):
            # For auction games, generate valuations BEFORE getting actions
            if hasattr(self.game, 'generate_valuations_for_round'):
                self.game.generate_valuations_for_round()
            
            # For auction games, set valuations on agents before getting actions
            if hasattr(self.game, 'current_valuations') and hasattr(self.game, 'players'):
                for i, agent in enumerate(self.agents):
                    # For PlayerConnection objects (server use), send valuations message
                    if hasattr(agent, 'writer') and hasattr(agent, 'reader'):
                        # This is a PlayerConnection - send valuations message
                        if i < len(self.game.players):
                            try:
                                # Get player name by index for auction games
                                if hasattr(self.game, 'get_player_name'):
                                    player_name = self.game.get_player_name(i)
                                else:
                                    # Fallback for non-auction games
                                    player_name = f"player_{i}"
                                
                                valuations = self.game.current_valuations[player_name]
                                await self._send_agent_valuations(agent, valuations)
                            except (IndexError, KeyError) as e:
                                # Log error but continue - agent might not need valuations
                                print(f"Warning: Could not set valuations for agent {i}: {e}")
                                pass
                    else:
                        # This is a regular BaseAgent - call method directly
                        if hasattr(agent, 'set_valuations') and i < len(self.game.players):
                            try:
                                # Get player name by index for auction games
                                if hasattr(self.game, 'get_player_name'):
                                    player_name = self.game.get_player_name(i)
                                else:
                                    # Fallback for non-auction games
                                    player_name = f"player_{i}"
                                
                                valuations = self.game.current_valuations[player_name]
                                agent.set_valuations(valuations)
                            except (IndexError, KeyError) as e:
                                # Log error but continue - agent might not need valuations
                                print(f"Warning: Could not set valuations for agent {i}: {e}")
                                pass
            
            # get actions from all agents (async for server connections)
            actions = {}
            for i, agent in enumerate(self.agents):
                # get agent-specific observation
                agent_obs = obs.get(i, {})
                action = await self._get_agent_action_async(agent, agent_obs)
                actions[i] = action
                if hasattr(agent, 'action_history'):
                    agent.action_history.append(action)
            
            # Convert dictionary actions back to objects if needed (for ADX games)
            converted_actions = {}
            for agent_id, action in actions.items():
                if isinstance(action, dict) and 'campaign_id' in action and 'bid_entries' in action:
                    # This is a serialized OneDayBidBundle - convert it back
                    from core.game.AdxOneDayGame import OneDayBidBundle
                    converted_actions[agent_id] = OneDayBidBundle.from_dict(action)
                else:
                    # This is already an object or a different type of action
                    converted_actions[agent_id] = action
            
            # step the game
            obs, rewards, done, info = self.game.step(converted_actions)
            
            # update agents with results and track opponent actions
            for i, agent in enumerate(self.agents):
                reward = rewards.get(i, 0)
                agent_info = info.get(i, {})
                # Add player_id to agent_info for BOSII agents
                agent_info['player_id'] = i
                
                # For server connections, send update message
                if hasattr(agent, 'writer'):
                    await self._send_agent_update(agent, obs.get(i, {}), actions.get(i, {}), reward, done, agent_info)
                else:
                    # For regular agents, call update method
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
    
    async def _send_agent_setup(self, agent):
        """Send setup message to connected player."""
        import json
        
        message = {
            "message": "agent_setup",
            "game_type": self.game_title
        }
        
        try:
            message_str = json.dumps(message) + "\n"
            agent.writer.write(message_str.encode())
            await agent.writer.drain()
        except Exception as e:
            print(f"Error sending setup to {agent.name}: {e}")
    
    async def _send_agent_valuations(self, agent, valuations):
        """Send valuations message to connected player."""
        import json
        
        message = {
            "message": "agent_valuations",
            "valuations": valuations
        }
        
        try:
            message_str = json.dumps(message) + "\n"
            agent.writer.write(message_str.encode())
            await agent.writer.drain()
        except Exception as e:
            print(f"Error sending valuations to {agent.name}: {e}")
    
    async def _send_agent_update(self, agent, obs: Dict[str, Any], action: Any, reward: float, done: bool, info: Dict[str, Any]):
        """Send update message to connected player."""
        import json
        
        message = {
            "message": "agent_update",
            "observation": obs,
            "action": action,
            "reward": reward,
            "done": done,
            "info": info
        }
        
        try:
            message_str = json.dumps(message) + "\n"
            agent.writer.write(message_str.encode())
            await agent.writer.drain()
        except Exception as e:
            print(f"Error sending update to {agent.name}: {e}")
    
    async def run_single_round_async(self) -> Tuple[List[float], Dict[str, Any]]:
        """
        Async version of run_single_round for server use.
        
        Returns:
            tuple of (rewards, info)
        """
        # get current observation
        obs = self.game.get_observation()
        
        # For auction games, set valuations on agents before getting actions
        if hasattr(self.game, 'current_valuations') and hasattr(self.game, 'players'):
            for i, agent in enumerate(self.agents):
                # For PlayerConnection objects (server use), send valuations message
                if hasattr(agent, 'writer') and hasattr(agent, 'reader'):
                    # This is a PlayerConnection - send valuations message
                    if i < len(self.game.players):
                        try:
                            # Get player name by index for auction games
                            if hasattr(self.game, 'get_player_name'):
                                player_name = self.game.get_player_name(i)
                            else:
                                # Fallback for non-auction games
                                player_name = f"player_{i}"
                            
                            valuations = self.game.current_valuations[player_name]
                            await self._send_agent_valuations(agent, valuations)
                        except (IndexError, KeyError) as e:
                            # Log error but continue - agent might not need valuations
                            print(f"Warning: Could not set valuations for agent {i}: {e}")
                            pass
                else:
                    # This is a regular BaseAgent - call method directly
                    if hasattr(agent, 'set_valuations') and i < len(self.game.players):
                        try:
                            # Get player name by index for auction games
                            if hasattr(self.game, 'get_player_name'):
                                player_name = self.game.get_player_name(i)
                            else:
                                # Fallback for non-auction games
                                player_name = f"player_{i}"
                            
                            valuations = self.game.current_valuations[player_name]
                            agent.set_valuations(valuations)
                        except (IndexError, KeyError) as e:
                            # Log error but continue - agent might not need valuations
                            print(f"Warning: Could not set valuations for agent {i}: {e}")
                            pass
        
        # get actions from all agents (async for server connections)
        actions = {}
        for i, agent in enumerate(self.agents):
            agent_obs = obs.get(i, {})
            action = await self._get_agent_action_async(agent, agent_obs)
            actions[i] = action
            if hasattr(agent, 'action_history'):
                agent.action_history.append(action)
        
        # step the game
        obs, rewards, done, info = self.game.step(actions)
        
        # update agents with results and track opponent actions
        for i, agent in enumerate(self.agents):
            reward = rewards.get(i, 0)
            agent_info = info.get(i, {})
            
            # For server connections, send update message
            if hasattr(agent, 'writer'):
                await self._send_agent_update(agent, obs.get(i, {}), actions.get(i, {}), reward, done, agent_info)
            else:
                # For regular agents, call update method
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