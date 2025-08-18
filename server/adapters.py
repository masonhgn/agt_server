#!/usr/bin/env python3
"""
adapter classes for converting between stencil interfaces and server format.

this module provides adapters that convert the various stencil agent interfaces
to the unified agt server format, allowing students to use their completed
stencils directly with the server.
"""

import sys
import os
from typing import Dict, Any, List

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Handle import from different working directories
try:
    from client import AGTAgent
except ImportError:
    from server.client import AGTAgent


class RPSAdapter(AGTAgent):
    """adapter for rps agents from lab 1."""
    
    def __init__(self, rps_agent):
        super().__init__(rps_agent.name)
        self.rps_agent = rps_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to rps agent format."""
        # rps agents expect opponent's last move
        opponent_last_move = observation.get("opponent_last_move", None)
        
        # get action from rps agent
        action = self.rps_agent.get_action(opponent_last_move)
        
        # store history
        self.game_history.append({
            "opponent_last_move": opponent_last_move,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the rps agent."""
        super().reset()
        if hasattr(self.rps_agent, 'reset'):
            self.rps_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the rps agent with results."""
        super().update(reward, info)
        if hasattr(self.rps_agent, 'update'):
            self.rps_agent.update(reward, info)


class BOSAdapter(AGTAgent):
    """adapter for bos agents from lab 2."""
    
    def __init__(self, bos_agent):
        super().__init__(bos_agent.name)
        self.bos_agent = bos_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to bos agent format."""
        # bos agents expect opponent's last move
        opponent_last_move = observation.get("opponent_last_move", None)
        
        # get action from bos agent
        action = self.bos_agent.get_action(opponent_last_move)
        
        # store history
        self.game_history.append({
            "opponent_last_move": opponent_last_move,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the bos agent."""
        super().reset()
        if hasattr(self.bos_agent, 'reset'):
            self.bos_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the bos agent with results."""
        super().update(reward, info)
        if hasattr(self.bos_agent, 'update'):
            self.bos_agent.update(reward, info)


class BOSIIAdapter(AGTAgent):
    """adapter for bosii agents from lab 2."""
    
    def __init__(self, bosii_agent):
        super().__init__(bosii_agent.name)
        self.bosii_agent = bosii_agent
        self.game_history = []
        self.player_type = None
        self.mood = None
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to bosii agent format."""
        # bosii agents expect opponent's last move, player type, and mood
        opponent_last_move = observation.get("opponent_last_move", None)
        player_type = observation.get("player_type", self.player_type)
        mood = observation.get("mood", self.mood)
        
        # store player info
        if player_type is not None:
            self.player_type = player_type
        if mood is not None:
            self.mood = mood
        
        # get action from bosii agent
        action = self.bosii_agent.get_action(opponent_last_move, player_type, mood)
        
        # store history
        self.game_history.append({
            "opponent_last_move": opponent_last_move,
            "player_type": player_type,
            "mood": mood,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the bosii agent."""
        super().reset()
        self.player_type = None
        self.mood = None
        if hasattr(self.bosii_agent, 'reset'):
            self.bosii_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the bosii agent with results."""
        super().update(reward, info)
        if hasattr(self.bosii_agent, 'update'):
            self.bosii_agent.update(reward, info)


class ChickenAdapter(AGTAgent):
    """adapter for chicken agents from lab 3."""
    
    def __init__(self, chicken_agent):
        super().__init__(chicken_agent.name)
        self.chicken_agent = chicken_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to chicken agent format."""
        # chicken agents expect opponent's last move
        opponent_last_move = observation.get("opponent_last_move", None)
        
        # get action from chicken agent
        action = self.chicken_agent.get_action(opponent_last_move)
        
        # store history
        self.game_history.append({
            "opponent_last_move": opponent_last_move,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the chicken agent."""
        super().reset()
        if hasattr(self.chicken_agent, 'reset'):
            self.chicken_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the chicken agent with results."""
        super().update(reward, info)
        if hasattr(self.chicken_agent, 'update'):
            self.chicken_agent.update(reward, info)


class PDAdapter(AGTAgent):
    """adapter for pd agents from lab 1."""
    
    def __init__(self, pd_agent):
        super().__init__(pd_agent.name)
        self.pd_agent = pd_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to pd agent format."""
        # pd agents expect opponent's last move
        opponent_last_move = observation.get("opponent_last_move", None)
        
        # get action from pd agent
        action = self.pd_agent.get_action(opponent_last_move)
        
        # store history
        self.game_history.append({
            "opponent_last_move": opponent_last_move,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the pd agent."""
        super().reset()
        if hasattr(self.pd_agent, 'reset'):
            self.pd_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the pd agent with results."""
        super().update(reward, info)
        if hasattr(self.pd_agent, 'update'):
            self.pd_agent.update(reward, info)


class LemonadeAdapter(AGTAgent):
    """adapter for lemonade agents from lab 4."""
    
    def __init__(self, lemonade_agent):
        super().__init__(lemonade_agent.name)
        self.lemonade_agent = lemonade_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> int:
        """convert server observation to lemonade agent format."""
        # lemonade agents expect opponent positions
        opponent_positions = observation.get("opponent_positions", [])
        
        # get action from lemonade agent
        action = self.lemonade_agent.get_action(opponent_positions)
        
        # store history
        self.game_history.append({
            "opponent_positions": opponent_positions,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the lemonade agent."""
        super().reset()
        if hasattr(self.lemonade_agent, 'reset'):
            self.lemonade_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the lemonade agent with results."""
        super().update(reward, info)
        if hasattr(self.lemonade_agent, 'update'):
            self.lemonade_agent.update(reward, info)


class AuctionAdapter(AGTAgent):
    """adapter for auction agents from lab 6."""
    
    def __init__(self, auction_agent):
        super().__init__(auction_agent.name)
        self.auction_agent = auction_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, int]:
        """convert server observation to auction agent format."""
        # auction agents expect valuation functions and goods
        valuation_func = observation.get("valuation_func", None)
        goods = observation.get("goods", set())
        
        # get action from auction agent
        action = self.auction_agent.get_action(valuation_func, goods)
        
        # store history
        self.game_history.append({
            "valuation_func": valuation_func,
            "goods": goods,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the auction agent."""
        super().reset()
        if hasattr(self.auction_agent, 'reset'):
            self.auction_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the auction agent with results."""
        super().update(reward, info)
        if hasattr(self.auction_agent, 'update'):
            self.auction_agent.update(reward, info)


class ADXAdapter(AGTAgent):
    """adapter for adx agents from lab 9."""
    
    def __init__(self, adx_agent):
        super().__init__(adx_agent.name)
        self.adx_agent = adx_agent
        self.game_history = []
    
    def get_action(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """convert server observation to adx agent format."""
        # adx agents expect campaign information
        campaign = observation.get("campaign", None)
        day = observation.get("day", 1)
        
        # get action from adx agent
        if hasattr(self.adx_agent, 'get_bid_bundle'):
            action = self.adx_agent.get_bid_bundle(day)
        else:
            action = self.adx_agent.get_action(observation)
        
        # store history
        self.game_history.append({
            "campaign": campaign,
            "day": day,
            "my_action": action
        })
        
        return action
    
    def reset(self):
        """reset the adx agent."""
        super().reset()
        if hasattr(self.adx_agent, 'reset'):
            self.adx_agent.reset()
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the adx agent with results."""
        super().update(reward, info)
        if hasattr(self.adx_agent, 'update'):
            self.adx_agent.update(reward, info)


# helper function to create adapters
def create_adapter(agent, game_type: str) -> AGTAgent:
    """create an appropriate adapter for the given agent and game type."""
    if game_type == "rps":
        return RPSAdapter(agent)
    elif game_type == "bos":
        return BOSAdapter(agent)
    elif game_type == "bosii":
        return BOSIIAdapter(agent)
    elif game_type == "chicken":
        return ChickenAdapter(agent)
    elif game_type == "pd":
        return PDAdapter(agent)
    elif game_type == "lemonade":
        return LemonadeAdapter(agent)
    elif game_type == "auction":
        return AuctionAdapter(agent)
    elif game_type == "adx_twoday":
        return ADXAdapter(agent)
    else:
        raise ValueError(f"unknown game type: {game_type}")


def load_agent_from_stencil(stencil_path: str, game_type: str) -> AGTAgent:
    """Load an agent from a completed stencil and create an adapter."""
    try:
        # Add the stencil directory to the path
        stencil_dir = os.path.dirname(stencil_path)
        if stencil_dir not in sys.path:
            sys.path.insert(0, stencil_dir)
        
        # Import the stencil module
        module_name = os.path.basename(stencil_path).replace('.py', '')
        spec = __import__(module_name, fromlist=['agent_submission'])
        
        # Get the agent submission
        if hasattr(spec, 'agent_submission'):
            agent = spec.agent_submission
            return create_adapter(agent, game_type)
        else:
            raise ValueError("No agent_submission found in stencil")
            
    except Exception as e:
        raise ValueError(f"Failed to load agent from {stencil_path}: {e}")


# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AGT Agent Adapter')
    parser.add_argument('--stencil', type=str, required=True, help='Path to completed stencil')
    parser.add_argument('--game', type=str, required=True, 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'pd', 'lemonade', 'auction', 'adx_twoday'],
                       help='Game type')
    parser.add_argument('--name', type=str, help='Agent name (optional)')
    
    args = parser.parse_args()
    
    try:
        agent = load_agent_from_stencil(args.stencil, args.game)
        if args.name:
            agent.name = args.name
        
        print(f"Successfully loaded agent: {agent.name}")
        print(f"Game type: {args.game}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 