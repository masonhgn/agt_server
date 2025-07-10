#!/usr/bin/env python3
"""
integration test for all labs.

this test loops through all labs, starts a server for each lab,
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

# add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from server.client import AGTAgent, AGTClient
except ImportError:
    # fallback for when running from different directory
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from server.client import AGTAgent, AGTClient


# configuration for each lab
LAB_CONFIG = {
    "lab01": {
        "config": "../server/configs/lab01_rps.json",
        "agents": 2,
        "solution_path": "stencils/examples/lab01_example.py",
        "agent_class": "ExampleFictitiousPlayAgent",
        "game_type": "rps",
        "timeout": 30
    },
    "lab02": {
        "config": "../server/configs/lab02_bos.json", 
        "agents": 2,
        "solution_path": "stencils/examples/lab02_example.py",
        "agent_class": "CompromiseAgent",
        "game_type": "bos",
        "timeout": 30
    },
    "lab03": {
        "config": "../server/configs/lab03_chicken.json",
        "agents": 2,
        "solution_path": "stencils/examples/lab03_example.py",
        "agent_class": "ContinueAgent",
        "game_type": "chicken",
        "timeout": 30
    },
    "lab04": {
        "config": "../server/configs/lab04_lemonade.json",
        "agents": 3,
        "solution_path": "stencils/examples/lab04_example.py",
        "agent_class": "AlwaysStayAgent",
        "game_type": "lemonade",
        "timeout": 30
    },
    "lab06": {
        "config": "../server/configs/lab06_auction.json",
        "agents": 4,
        "solution_path": "stencils/examples/lab06_example.py",
        "agent_class": "ExampleMarginalValueAgent",
        "game_type": "auction",
        "timeout": 60
    },
    "lab07": {
        "config": "../server/configs/lab07_auction.json",
        "agents": 4,
        "solution_path": "stencils/examples/lab07_example.py",
        "agent_class": "ExampleSCPPAgent",
        "game_type": "auction",
        "timeout": 45
    },
    "lab09": {
        "config": "../server/configs/lab09_adx.json",
        "agents": 2,
        "solution_path": "stencils/examples/lab09_example.py",
        "agent_class": "ExampleAdXAgent",
        "game_type": "adx_twoday",
        "timeout": 30
    }
}


def get_free_port() -> int:
    """get a free port for the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def wait_for_server(host: str, port: int, timeout: int = 10) -> bool:
    """wait for server to be ready."""
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
    """test agent that uses an example solution."""
    
    def __init__(self, name: str, solution_path: str, agent_class: str):
        super().__init__(name)
        self.solution_path = solution_path
        self.agent_class = agent_class
        self.agent = None
        self._load_agent()
    
    def _load_agent(self):
        """load the example solution agent."""
        try:
            import os
            print(f"[DEBUG] Current working directory: {os.getcwd()}")
            # Use absolute path for the solution file
            abs_solution_path = os.path.abspath(self.solution_path)
            print(f"[DEBUG] Loading agent from: {abs_solution_path}")
            # add the project root to the path for core imports
            project_root = os.path.join(os.path.dirname(__file__), '..')
            sys.path.insert(0, project_root)
            # import the solution module using importlib
            import importlib.util
            module_name = os.path.basename(abs_solution_path).replace('.py', '')
            spec = importlib.util.spec_from_file_location(module_name, abs_solution_path)
            if spec is None:
                raise ImportError(f"Could not create spec for {abs_solution_path}")
            solution_module = importlib.util.module_from_spec(spec)
            if spec.loader is None:
                raise ImportError(f"Could not load module {abs_solution_path}")
            spec.loader.exec_module(solution_module)
            # get the agent class
            agent_class = getattr(solution_module, self.agent_class)
            # create an instance
            self.agent = agent_class(self.name)
        except Exception as e:
            print(f"failed to load agent from {self.solution_path}: {e}")
            raise
    
    def get_action(self, observation):
        """get action from the loaded agent."""
        if self.agent:
            # Handle ADX agents that use get_bid_bundle instead of get_action
            if hasattr(self.agent, 'get_bid_bundle'):
                day = observation.get("day", 1)
                # Set campaign attributes for ADX agents
                if hasattr(self.agent, 'campaign_day1') and 'campaign_day1' in observation:
                    campaign_dict = observation['campaign_day1']
                    # Convert dict back to Campaign object
                    from core.game.campaign import Campaign
                    from core.game.market_segment import MarketSegment
                    campaign_day1 = Campaign(
                        id=campaign_dict['id'],
                        market_segment=MarketSegment(campaign_dict['market_segment']),
                        reach=campaign_dict['reach'],
                        budget=campaign_dict['budget']
                    )
                    self.agent.campaign_day1 = campaign_day1
                if hasattr(self.agent, 'campaign_day2') and 'campaign_day2' in observation:
                    campaign_dict = observation['campaign_day2']
                    # Convert dict back to Campaign object
                    from core.game.campaign import Campaign
                    from core.game.market_segment import MarketSegment
                    campaign_day2 = Campaign(
                        id=campaign_dict['id'],
                        market_segment=MarketSegment(campaign_dict['market_segment']),
                        reach=campaign_dict['reach'],
                        budget=campaign_dict['budget']
                    )
                    self.agent.campaign_day2 = campaign_day2
                bid_bundle = self.agent.get_bid_bundle(day)
                # Convert TwoDayBidBundle to dictionary for JSON serialization
                if hasattr(bid_bundle, 'to_dict'):
                    result = bid_bundle.to_dict()
                    print(f"DEBUG: Converting TwoDayBidBundle to dict: {result}")
                    return result
                else:
                    print(f"DEBUG: TwoDayBidBundle has no to_dict method, returning as-is")
                    return bid_bundle
            else:
                return self.agent.get_action(observation)
        return 0  # default action
    
    def update(self, reward: float, info=None):
        """update the loaded agent."""
        super().update(reward, info or {})
        if self.agent and hasattr(self.agent, 'update'):
            self.agent.update(reward, info or {})


async def run_agent_client(agent: TestAgent, host: str, port: int, game_type: str, timeout: int):
    """run an agent client and return the results."""
    client = AGTClient(agent, host, port)
    
    try:
        # connect to server
        await client.connect()
        if not client.connected:
            return False, "failed to connect"
        
        # join game
        success = await client.join_game(game_type)
        if not success:
            return False, "failed to join game"
        
        # run the game
        await asyncio.wait_for(client.run(), timeout=timeout)
        
        print(f"run_agent_client for {agent.name} completed and returning success")
        return True, "success"
        
    except asyncio.TimeoutError:
        print(f"run_agent_client for {agent.name} timed out")
        return False, "timeout"
    except Exception as e:
        print(f"run_agent_client for {agent.name} error: {e}")
        return False, f"error: {e}"
    finally:
        await client.disconnect()
        print(f"run_agent_client for {agent.name} finished (finally block)")


@pytest.mark.parametrize("lab_name", LAB_CONFIG.keys())
def test_lab_integration(lab_name):
    """test integration for a specific lab."""
    config = LAB_CONFIG[lab_name]
    
    print(f"\n{'='*60}")
    print(f"testing {lab_name.upper()}")
    print(f"{'='*60}")
    
    # get a free port
    port = get_free_port()
    host = "localhost"
    
    # start server
    print(f"starting server on port {port}...")
    server_cmd = [
        "python3", "server/server.py",
        "--config", config["config"],
        "--port", str(port)
    ]
    
    server_proc = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.join(os.path.dirname(__file__), '..')
    )
    
    try:
        # wait for server to be ready
        print("waiting for server to be ready...")
        if not wait_for_server(host, port, timeout=10):
            raise Exception("server failed to start")
        
        print(f"server ready on {host}:{port}")
        
        # create agents
        agents = []
        for i in range(config["agents"]):
            agent_name = f"{lab_name}_agent_{i}"
            agent = TestAgent(
                agent_name,
                config["solution_path"],
                config["agent_class"]
            )
            agents.append(agent)
        
        print(f"created {len(agents)} agents")
        
        # run agents
        print("starting agents...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # run all agents concurrently
            tasks = []
            for agent in agents:
                task = run_agent_client(
                    agent, host, port, config["game_type"], config["timeout"]
                )
                tasks.append(task)
            
            # wait for all agents to complete
            results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            
            # check results
            success_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"agent {i}: failed - {result}")
                elif isinstance(result, tuple) and len(result) == 2:
                    success, message = result
                    if success:
                        success_count += 1
                        print(f"agent {i}: success")
                    else:
                        print(f"agent {i}: failed - {message}")
                else:
                    print(f"agent {i}: unknown result - {result}")
            
            # verify results
            assert success_count >= config["agents"] * 0.8, f"only {success_count}/{config['agents']} agents succeeded"
            
            # check that agents received some rewards (but allow 0 for well-matched agents)
            total_rewards = sum(agent.total_reward for agent in agents)
            # for rps, 0 rewards are valid if agents are well-matched (ties)
            if lab_name == "lab01":
                print(f"lab 01 total rewards: {total_rewards} (0 is valid for well-matched rps agents)")
            else:
                assert total_rewards != 0, "no rewards received"
            
            print(f"{lab_name.upper()} test passed")
            print(f"   agents: {success_count}/{config['agents']} succeeded")
            print(f"   total rewards: {total_rewards}")
            
        finally:
            loop.close()
    
    finally:
        # clean up server
        print("cleaning up server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_proc.kill()
        
        # check server output for errors
        stdout, stderr = server_proc.communicate()
        if stderr:
            print(f"server stderr: {stderr.decode()}")


def run_all_lab_tests():
    """run all lab integration tests."""
    print("running lab integration tests...")
    print("=" * 60)
    
    results = {}
    for lab_name in LAB_CONFIG.keys():
        try:
            test_lab_integration(lab_name)
            results[lab_name] = "passed"
            print(f"{lab_name.upper()} passed")
        except Exception as e:
            results[lab_name] = f"failed: {e}"
            print(f"{lab_name.upper()} failed: {e}")
    
    # print summary
    print("\n" + "=" * 60)
    print("lab integration test summary:")
    for lab_name, result in results.items():
        status = "passed" if result == "passed" else "failed"
        print(f"  {lab_name.upper()}: {status}")
    
    passed_count = sum(1 for result in results.values() if result == "passed")
    total_count = len(results)
    
    print(f"\ntotal: {passed_count}/{total_count} labs passed")
    
    if passed_count == total_count:
        print("all lab integration tests completed successfully!")
    else:
        print("some lab integration tests failed")
    
    return passed_count == total_count


if __name__ == "__main__":
    run_all_lab_tests() 