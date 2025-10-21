#!/usr/bin/env python3
"""
NetworkAgent - Server-side agent that represents remote clients in LocalArena/Engine.

This class implements the BaseAgent interface and handles async communication
with remote clients, allowing the server to use LocalArena/Engine directly.
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional
from core.agents.common.base_agent import BaseAgent


class NetworkAgent(BaseAgent):
    """
    Server-side agent that represents a remote client in LocalArena/Engine.
    
    This agent implements the BaseAgent interface and handles async communication
    with remote clients via PlayerConnection objects.
    """
    
    def __init__(self, name: str, player_connection):
        """
        Initialize NetworkAgent.
        
        Args:
            name: Agent name
            player_connection: PlayerConnection object for network communication
        """
        super().__init__(name)
        self.player_connection = player_connection
        self.pending_action = None
        self.action_timeout = 30.0  # 30 second timeout for actions
        
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """
        Get action from remote client (synchronous interface for BaseAgent).
        
        This method sends a message synchronously and waits for the response.
        
        Args:
            observation: Game observation to send to client
            
        Returns:
            Action from the remote client
        """
        # Clear any pending action
        self.player_connection.pending_action = None
        
        # Send observation to client synchronously
        self._send_observation_sync(observation)
        
        # Wait synchronously for response (blocking wait)
        start_time = time.time()
        while self.player_connection.pending_action is None:
            if time.time() - start_time > self.action_timeout:
                raise TimeoutError(f"Client {self.name} did not respond within {self.action_timeout} seconds")
            time.sleep(0.01)  # Blocking sleep
        
        # Get and clear the action
        action = self.player_connection.pending_action
        self.player_connection.pending_action = None
        
        # If this is a serialized OneDayBidBundle, reconstruct it
        if isinstance(action, dict) and "campaign_id" in action and "bid_entries" in action:
            from core.game.AdxOneDayGame import OneDayBidBundle
            from core.game.bid_entry import SimpleBidEntry
            from core.game.market_segment import MarketSegment
            
            # Reconstruct bid entries
            bid_entries = []
            for entry_dict in action["bid_entries"]:
                bid_entries.append(SimpleBidEntry(
                    market_segment=MarketSegment(entry_dict["market_segment"]),
                    bid=entry_dict["bid"],
                    spending_limit=entry_dict["spending_limit"]
                ))
            
            # Reconstruct OneDayBidBundle
            action = OneDayBidBundle(
                campaign_id=action["campaign_id"],
                day_limit=action["day_limit"],
                bid_entries=bid_entries
            )
        
        return action
    
    def _send_observation_sync(self, observation: Dict[str, Any]):
        """Send observation to the remote client synchronously."""
        # Convert observation to simple JSON-serializable format
        serializable_obs = self._simplify_observation(observation)
        
        message = {
            "message": "request_action",
            "observation": serializable_obs
        }
        
        # Send message synchronously
        try:
            message_str = json.dumps(message) + "\n"
            self.player_connection.writer.write(message_str.encode())
            # Note: We can't use await writer.drain() in sync context
            # The message will be sent when the event loop processes it
        except Exception as e:
            raise ConnectionError(f"Failed to send message to {self.name}: {e}")
    
    def _simplify_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Convert observation to simple JSON-serializable format."""
        simplified = {}
        
        for key, value in observation.items():
            if key == "campaign":
                # Convert Campaign object to simple dict
                simplified[key] = {
                    "id": value.id,
                    "market_segment": value.market_segment.value,  # Just the string value
                    "reach": value.reach,
                    "budget": value.budget,
                    "start_day": value.start_day,
                    "end_day": value.end_day
                }
            elif isinstance(value, (str, int, float, bool, type(None))):
                # Basic types are already serializable
                simplified[key] = value
            elif isinstance(value, list):
                # Handle lists of basic types
                simplified[key] = [item for item in value if isinstance(item, (str, int, float, bool, type(None)))]
            else:
                # For anything else, convert to string
                simplified[key] = str(value)
        
        return simplified
    
    async def _send_observation(self, observation: Dict[str, Any]):
        """Send observation to the remote client."""
        message = {
            "message": "request_action",
            "observation": observation
        }
        
        # Send message to client
        await self._send_message(message)
    
    async def _send_message(self, message: Dict[str, Any]):
        """Send a message to the remote client."""
        try:
            message_str = json.dumps(message) + "\n"
            self.player_connection.writer.write(message_str.encode())
            await self.player_connection.writer.drain()
        except Exception as e:
            raise ConnectionError(f"Failed to send message to {self.name}: {e}")
    
    def reset(self):
        """Reset the agent for a new game."""
        super().reset()
        self.pending_action = None
    
    def update(self, reward: float, info: Dict[str, Any]):
        """Update the agent with reward and info from the last action."""
        super().update(reward, info)
        # Could send update to client if needed, but not required for basic functionality
    
    def is_connected(self) -> bool:
        """Check if the remote client is still connected."""
        return (self.player_connection.writer is not None and 
                not self.player_connection.writer.is_closing())
    
    def disconnect(self):
        """Disconnect from the remote client."""
        if self.player_connection.writer:
            self.player_connection.writer.close()
