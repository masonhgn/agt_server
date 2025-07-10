#!/usr/bin/env python3
"""
Integration test for all labs.

This test loops through all labs, starts a server for each lab,
connects the appropriate number of example solution agents,
and verifies that the games complete successfully.
"""

import pytest
import subprocess
import time
import socket
import asyncio
import sys
import os
import signal
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

try:
    from client import AGTAgent, AGTClient
except ImportError:
    # Fallback for when running from different directory
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from server.client import AGTAgent, AGTClient


# Configuration for each lab
LAB_CONFIG = {
    "lab01": {
        "config": "server/configs/lab01_rps.json",
        "agents": 2,
        "solution_path": "stencils/solutions/lab01/example_solution.py",
        "agent_class": "ExampleFictitiousPlayAgent",
        "game_type": "rps",
        "timeout": 30
    },
    "lab02": {
        "config": "server/configs/lab02_bos.json", 
        "agents": 2,
        "solution_path": "stencils/solutions/lab02/example_solution.py",
        "agent_class": "CompromiseAgent",
        "game_type": "bos",
        "timeout": 30
    },
    "lab03": {
        "config": "server/configs/lab03_chicken.json",
        "agents": 2,
        "solution_path": "stencils/solutions/lab03/example_solution.py",
        "agent_class": "ContinueAgent",
        "game_type": "chicken",
        "timeout": 30
    },
    "lab04": {
        "config": "server/configs/lab04_lemonade.json",
        "agents": 3,
        "solution_path": "stencils/solutions/lab04/example_solution.py",
        "agent_class": "AlwaysStayAgent",
        "game_type": "lemonade",
        "timeout": 30
    },
    "lab06": {
        "config": "server/configs/lab06_auction.json",
        "agents": 4,
        "solution_path": "stencils/solutions/lab06/example_solutions.py",
        "agent_class": "ExampleMarginalValueAgent",
        "game_type": "auction",
        "timeout": 60
    },
    "lab07": {
        "config": "server/configs/lab07_auction.json",
        "agents": 4,
        "solution_path": "stencils/solutions/lab07/example_solutions.py",
        "agent_class": "ExampleSCPPAgent",
        "game_type": "auction",
        "timeout": 45
    },
    "lab09": {
        "config": "server/configs/lab09_adx.json",
        "agents": 2,
        "solution_path": "stencils/solutions/lab09/example_solution.py",
        "agent_class": "ExampleAdXAgent",
        "game_type": "adx_twoday",
        "timeout": 30
    }
}


def get_free_port() -> int:
    """Get a free port for the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def wait_for_server(host: str, port: int, timeout: int = 10) -> bool:
    """Wait for server to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    return True
        except:
            pass
        time.sleep(0.1)
    return False


class TestAgent(AGTAgent):
    """Test agent that uses an example solution."""
    
    def __init__(self, name: str, solution_path: str, agent_class: str):
        super().__init__(name)
        self.solution_path = solution_path
        self.agent_class = agent_class
        self.agent = None
        self._load_agent()
    
    def _load_agent(self):
        """Load the example solution agent."""
        try:
            # Add the solution directory to the path
            solution_dir = os.path.dirname(self.solution_path)
            sys.path.insert(0, solution_dir)
            
            # Add the project root to the path for core imports
            project_root = os.path.join(os.path.dirname(__file__), '..')
            sys.path.insert(0, project_root)
            
            # Import the solution module
            module_name = os.path.basename(self.solution_path).replace('.py', '')
            solution_module = __import__(module_name)
            
            # Get the agent class
            agent_class = getattr(solution_module, self.agent_class)
            
            # Create an instance
            self.agent = agent_class(self.name)
            
        except Exception as e:
            print(f"Failed to load agent from {self.solution_path}: {e}")
            raise
    
    def get_action(self, observation):
        """Get action from the loaded agent."""
        if self.agent:
            return self.agent.get_action(observation)
        return 0  # Default action
    
    def update(self, reward: float, info=None):
        """Update the loaded agent."""
        super().update(reward, info or {})
        if self.agent and hasattr(self.agent, 'update'):
            self.agent.update(reward, info or {})


async def run_agent_client(agent: TestAgent, host: str, port: int, game_type: str, timeout: int):
    """Run an agent client and return the results."""
    client = AGTClient(agent, host, port)
    
    try:
        # Connect to server
        await client.connect()
        if not client.connected:
            return False, "Failed to connect"
        
        # Join game
        success = await client.join_game(game_type)
        if not success:
            return False, "Failed to join game"
        
        # Run the game
        await asyncio.wait_for(client.run(), timeout=timeout)
        
        print(f"run_agent_client for {agent.name} completed and returning Success")
        return True, "Success"
        
    except asyncio.TimeoutError:
        print(f"run_agent_client for {agent.name} timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"run_agent_client for {agent.name} error: {e}")
        return False, f"Error: {e}"
    finally:
        await client.disconnect()
        print(f"run_agent_client for {agent.name} finished (finally block)")


@pytest.mark.parametrize("lab_name", LAB_CONFIG.keys())
def test_lab_integration(lab_name):
    """Test integration for a specific lab."""
    config = LAB_CONFIG[lab_name]
    
    print(f"\n{'='*60}")
    print(f"Testing {lab_name.upper()}")
    print(f"{'='*60}")
    
    # Get a free port
    port = get_free_port()
    host = "localhost"
    
    # Start server
    print(f"Starting server on port {port}...")
    server_cmd = [
        "python3", "server/server.py",
        "--config", config["config"],
        "--port", str(port)
    ]
    
    server_proc = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    try:
        # Wait for server to be ready
        print("Waiting for server to be ready...")
        if not wait_for_server(host, port, timeout=10):
            raise Exception("Server failed to start")
        
        print(f"Server ready on {host}:{port}")
        
        # Create agents
        agents = []
        for i in range(config["agents"]):
            agent_name = f"{lab_name}_agent_{i}"
            agent = TestAgent(
                agent_name,
                config["solution_path"],
                config["agent_class"]
            )
            agents.append(agent)
        
        print(f"Created {len(agents)} agents")
        
        # Run agents
        print("Starting agents...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Run all agents concurrently
            tasks = []
            for agent in agents:
                task = run_agent_client(
                    agent, host, port, config["game_type"], config["timeout"]
                )
                tasks.append(task)
            
            # Wait for all agents to complete
            results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            
            # Check results
            success_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Agent {i}: FAILED - {result}")
                elif isinstance(result, tuple) and len(result) == 2:
                    success, message = result
                    if success:
                        success_count += 1
                        print(f"Agent {i}: SUCCESS")
                    else:
                        print(f"Agent {i}: FAILED - {message}")
                else:
                    print(f"Agent {i}: UNKNOWN RESULT - {result}")
            
            # Verify results
            assert success_count >= config["agents"] * 0.8, f"Only {success_count}/{config['agents']} agents succeeded"
            
            # Check that agents received some rewards (but allow 0 for well-matched agents)
            total_rewards = sum(agent.total_reward for agent in agents)
            # For RPS, 0 rewards are valid if agents are well-matched (ties)
            if lab_name == "lab01":
                print(f"Lab 01 total rewards: {total_rewards} (0 is valid for well-matched RPS agents)")
            else:
                assert total_rewards != 0, "No rewards received"
            
            print(f"✅ {lab_name.upper()} TEST PASSED")
            print(f"   Agents: {success_count}/{config['agents']} succeeded")
            print(f"   Total rewards: {total_rewards}")
            
        finally:
            loop.close()
    
    finally:
        # Clean up server
        print("Cleaning up server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
        
        # Check server output for errors
        stdout, stderr = server_proc.communicate()
        if stderr:
            print(f"Server stderr: {stderr.decode()}")


if __name__ == "__main__":
    # Run all tests
    print("Running lab integration tests...")
    
    for lab_name in LAB_CONFIG.keys():
        try:
            test_lab_integration(lab_name)
            print(f"✅ {lab_name.upper()} PASSED")
        except Exception as e:
            print(f"❌ {lab_name.upper()} FAILED: {e}")
    
    print("\n🎉 All lab integration tests completed!") 