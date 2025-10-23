#!/usr/bin/env python3
"""
Simple network adapter for connecting network clients to LocalArena.

This is a minimal adapter that implements BaseAgent interface for network clients.
Much simpler than the previous NetworkAgent approach.
"""

import json
import time
from typing import Dict, Any
from core.agents.common.base_agent import BaseAgent


class NetworkAdapter(BaseAgent):
    """
    - this servers as the interface between the server's game instance and a connected client.
    - when the server's game instance needs to get an action from the agent, it calls the get_action method in this class.
    """
    
    def __init__(self, name: str, writer, reader):
        super().__init__(name)
        self.writer = writer
        self.reader = reader
        self.action_timeout = 30.0
    
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """Simple synchronous get_action with blocking I/O."""
        try:
            # Send message
            message = {"message": "request_action", "observation": observation}
            message_str = json.dumps(message) + "\n"
            self.writer.write(message_str.encode())
            self.writer.flush()  # Blocking flush
            
            # Wait for response with timeout
            start_time = time.time()
            while time.time() - start_time < self.action_timeout:
                try:
                    # Simple blocking read
                    data = self.reader.read(1024)
                    if data:
                        response = json.loads(data.decode().strip())
                        if response.get("message") == "action":
                            return response.get("action")
                except:
                    time.sleep(0.01)
                    continue
                    
            raise TimeoutError(f"Client {self.name} timeout")
            
        except Exception as e:
            raise ConnectionError(f"Failed to communicate with {self.name}: {e}")

    
    # def _simplify_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
    #     """Convert observation to simple JSON-serializable format."""
    #     simplified = {}
        
    #     for key, value in observation.items():
    #         if key == "campaign":
    #             # Convert Campaign object to simple dict
    #             simplified[key] = {
    #                 "id": value.id,
    #                 "market_segment": value.market_segment.value,  # Just the string value
    #                 "reach": value.reach,
    #                 "budget": value.budget,
    #                 "start_day": value.start_day,
    #                 "end_day": value.end_day
    #             }
    #         elif isinstance(value, (str, int, float, bool, type(None))):
    #             # Basic types are already serializable
    #             simplified[key] = value
    #         elif isinstance(value, list):
    #             # Handle lists of basic types
    #             simplified[key] = [item for item in value if isinstance(item, (str, int, float, bool, type(None)))]
    #         else:
    #             # For anything else, convert to string
    #             simplified[key] = str(value)
        
    #     return simplified
    










    # def _reconstruct_bid_bundle(self, action_dict: Dict[str, Any]):
    #     """Reconstruct OneDayBidBundle from serialized dictionary."""
    #     from core.game.AdxOneDayGame import OneDayBidBundle
    #     from core.game.bid_entry import SimpleBidEntry
    #     from core.game.market_segment import MarketSegment
        
    #     # Reconstruct bid entries
    #     bid_entries = []
    #     for entry_dict in action_dict["bid_entries"]:
    #         bid_entries.append(SimpleBidEntry(
    #             market_segment=MarketSegment(entry_dict["market_segment"]),
    #             bid=entry_dict["bid"],
    #             spending_limit=entry_dict["spending_limit"]
    #         ))
        
    #     # Reconstruct OneDayBidBundle
    #     return OneDayBidBundle(
    #         campaign_id=action_dict["campaign_id"],
    #         day_limit=action_dict["day_limit"],
    #         bid_entries=bid_entries
    #     )
