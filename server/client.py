#!/usr/bin/env python3
"""
agt client library

this library allows students to connect their completed stencils to the agt server
for competitions and testing.
"""

import asyncio
import json
import socket
import time
import argparse
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class AGTAgent(ABC):
    """base class for agt agents that can connect to the server."""
    
    def __init__(self, name: str):
        self.name = name
        self.device_id = f"{name}_{int(time.time())}"
        self.game_type: Optional[str] = None
        self.current_round = 0
        self.total_reward = 0
        self.game_history = []
    
    @abstractmethod
    def get_action(self, observation: Dict[str, Any]) -> Any:
        """
        get the agent's action based on the current observation.
        
        args:
            observation: game state information
            
        returns:
            the action to take
        """
        pass
    
    def reset(self):
        """reset the agent for a new game."""
        self.current_round = 0
        self.total_reward = 0
        self.game_history = []
    
    def update(self, reward: float, info: Dict[str, Any]):
        """update the agent with reward and info from the last action."""
        self.total_reward += reward
        self.current_round += 1
        self.game_history.append({
            "round": self.current_round,
            "reward": reward,
            "info": info
        })


class AGTClient:
    """client for connecting to the agt server."""
    
    def __init__(self, agent: AGTAgent, host: str = "localhost", port: int = 8080):
        self.agent = agent
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.connected = False
    
    async def connect(self):
        """connect to the agt server."""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.connected = True
            print(f"connected to agt server at {self.host}:{self.port}")
            
            # handle initial handshake
            await self.handle_connection()
            
        except Exception as e:
            print(f"failed to connect to server: {e}")
            self.connected = False
    
    async def handle_connection(self):
        """handle the initial connection handshake."""
        print("debug: starting connection handshake...")

        # wait for request_device_id
        msg = await self.receive_message()
        print(f"debug: received (expect request_device_id): {msg}")
        if not msg or msg.get("message") != "request_device_id":
            print("failed: expected request_device_id")
            self.connected = False
            return

        # send device id
        print("debug: sending device id...")
        await self.send_message({
            "message": "provide_device_id",
            "device_id": self.agent.device_id
        })

        # wait for request_name
        msg = await self.receive_message()
        print(f"debug: received (expect request_name): {msg}")
        if not msg or msg.get("message") != "request_name":
            print("failed: expected request_name")
            self.connected = False
            return

        # send name
        print("debug: sending name...")
        await self.send_message({
            "message": "provide_name",
            "name": self.agent.name
        })

        # wait for connection_established
        message = await self.receive_message()
        print(f"debug: received (expect connection_established): {message}")
        if message and message.get("message") == "connection_established":
            print(f"connection established as {message.get('name')}")
            assigned_name = message.get("name")
            if assigned_name:
                self.agent.name = assigned_name
            print(f"available games: {message.get('available_games', [])}")
            # send ready message to let server know we're ready
            print("debug: sending ready message...")
            await self.send_message({
                "message": "ready"
            })
            print("debug: connection handshake complete")
        else:
            print("failed to establish connection")
            print(f"debug: expected 'connection_established' but got: {message}")
            self.connected = False
    
    async def join_game(self, game_type: str):
        """join a specific game."""
        if not self.connected:
            print("not connected to server")
            return False
        
        await self.send_message({
            "message": "join_game",
            "game_type": game_type
        })
        
        message = await self.receive_message()
        if message and message.get("message") == "joined_game":
            print(f"joined {game_type} game")
            self.agent.game_type = game_type
            return True
        else:
            print(f"failed to join {game_type} game")
            return False
    
    async def run(self):
        """main client loop."""
        if not self.connected:
            print("not connected to server")
            return
        
        try:
            while True:
                message = await self.receive_message()
                if not message:
                    break
                
                await self.handle_message(message)
                
        except Exception as e:
            print(f"error in client loop: {e}")
        finally:
            await self.disconnect()
    
    async def handle_message(self, message: Dict[str, Any]):
        """handle messages from the server."""
        msg_type = message.get("message")
        
        if msg_type == "game_start":
            print(f"game starting: {message.get('game_type')}")
            self.agent.reset()
            
        elif msg_type == "request_action":
            observation = message.get("observation", {})
            round_num = message.get("round", 0)
            
            # get action from agent
            action = self.agent.get_action(observation)
            
            # send action to server
            await self.send_message({
                "message": "provide_action",
                "action": action
            })
            
            print(f"round {round_num}: sent action {action}")
            
        elif msg_type == "round_result":
            reward = message.get("reward", 0)
            info = message.get("info", {})
            
            # update agent
            self.agent.update(reward, info)
            
            # send ready for next round
            await self.send_message({
                "message": "ready_next_round"
            })
            
            print(f"round result: reward={reward}")
            
        elif msg_type == "game_end":
            results = message.get("results", {})
            print(f"game ended. final results: {results}")
            
        elif msg_type == "error":
            error = message.get("error", "unknown error")
            print(f"server error: {error}")
    
    async def send_message(self, message: Dict[str, Any]):
        """send a message to the server."""
        if self.writer:
            data = json.dumps(message).encode()
            self.writer.write(data)
            await self.writer.drain()
    
    async def receive_message(self) -> Optional[Dict[str, Any]]:
        """receive a message from the server."""
        if self.reader:
            try:
                data = await self.reader.read(1024)
                if data:
                    return json.loads(data.decode())
            except Exception as e:
                print(f"error receiving message: {e}")
        return None
    
    async def disconnect(self):
        """disconnect from the server."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
        self.connected = False
        print("disconnected from server")


# example usage and command line interface
async def main():
    """example usage of the agt client."""
    parser = argparse.ArgumentParser(description='agt client')
    parser.add_argument('--name', type=str, required=True, help='agent name')
    parser.add_argument('--game', type=str, required=True, 
                       choices=['rps', 'bos', 'bosii', 'chicken', 'lemonade', 'auction'],
                       help='game type to join')
    parser.add_argument('--host', type=str, default='localhost', help='server host')
    parser.add_argument('--port', type=int, default=8080, help='server port')
    parser.add_argument('--agent-file', type=str, help='path to agent implementation file')
    
    args = parser.parse_args()
    
    # create a simple random agent as default
    class RandomAgent(AGTAgent):
        def get_action(self, observation):
            import random
            if self.game_type == "auction":
                return {"A": random.randint(0, 10), "B": random.randint(0, 10),
                       "C": random.randint(0, 10), "D": random.randint(0, 10)}
            else:
                return random.randint(0, 2)
    
    agent = RandomAgent(args.name)
    
    # import agent from file if provided
    if args.agent_file:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_module", args.agent_file)
            if spec is not None:
                agent_module = importlib.util.module_from_spec(spec)
                if spec.loader is not None:
                    spec.loader.exec_module(agent_module)
                    
                    # look for agent_submission
                    if hasattr(agent_module, 'agent_submission'):
                        agent = agent_module.agent_submission
        except Exception as e:
            print(f"warning: could not load agent from {args.agent_file}: {e}")
            print("using default random agent instead.")
    
    # create client and connect
    client = AGTClient(agent, args.host, args.port)
    await client.connect()
    
    if client.connected:
        # join game and run
        if await client.join_game(args.game):
            await client.run()
        else:
            print(f"failed to join {args.game} game")
    else:
        print("failed to connect to server")


if __name__ == "__main__":
    asyncio.run(main()) 