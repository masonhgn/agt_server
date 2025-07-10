#!/usr/bin/env python3
"""
comprehensive test suite for the agt server system.

this test file consolidates all server functionality testing including:
- server startup and configuration
- client connections and disconnections
- game mechanics and restrictions
- agent interactions
- basic game types (rps, bos, chicken, etc.)
- error handling and edge cases

this does not test specific lab implementations - those are handled separately.
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
import json
import random
from pathlib import Path
from typing import Dict, List, Optional

# add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

# import client classes
try:
    from client import AGTAgent, AGTClient
except ImportError:
    # fallback for when running from different directory
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from server.client import AGTAgent, AGTClient

# import server class
try:
    from server import AGTServer
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from server.server import AGTServer


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


class SimpleTestAgent(AGTAgent):
    """simple test agent that always returns the same action."""
    
    def __init__(self, name: str, action: int):
        super().__init__(name)
        self.action = action
    
    def get_action(self, observation):
        return self.action


class RandomTestAgent(AGTAgent):
    """random test agent for testing game mechanics."""
    
    def __init__(self, name: str, num_actions: int = 3):
        super().__init__(name)
        self.num_actions = num_actions
    
    def get_action(self, observation):
        return random.randint(0, self.num_actions - 1)


class TestServerConfiguration:
    """test server configuration and startup."""
    
    def test_server_configuration(self):
        """test server configuration loading and validation."""
        print("testing server configuration...")
        
        # test 1: no restrictions (all games allowed)
        config = {
            "server_name": "test server",
            "max_players": 10,
            "timeout": 30,
            "save_results": True
        }
        server = AGTServer(config, "localhost", 8080)
        assert server.allowed_games is None, "should allow all games when no restrictions"
        assert len(server.game_configs) >= 6, f"should have at least 6 games, got {len(server.game_configs)}"
        
        # test 2: single game restriction
        config["allowed_games"] = ["rps"]
        server = AGTServer(config, "localhost", 8080)
        assert server.allowed_games == ["rps"], "should restrict to rps only"
        assert "rps" in server.game_configs, "should have rps available"
        
        # test 3: multiple game restriction
        config["allowed_games"] = ["rps", "bos", "chicken"]
        server = AGTServer(config, "localhost", 8080)
        assert server.allowed_games == ["rps", "bos", "chicken"], "should restrict to specified games"
        for game in ["rps", "bos", "chicken"]:
            assert game in server.game_configs, f"should have {game} available"
        
        # test 4: invalid game in restriction
        config["allowed_games"] = ["rps", "invalid_game", "bos"]
        server = AGTServer(config, "localhost", 8080)
        assert "rps" in server.game_configs, "should ignore invalid games"
        assert "bos" in server.game_configs, "should ignore invalid games"
        assert "invalid_game" not in server.game_configs, "should not have invalid game"
        
        print("server configuration tests passed")


class TestClientConnection:
    """test client connection functionality."""
    
    @pytest.mark.asyncio
    async def test_client_connection(self):
        """test basic client connection and disconnection."""
        print("testing client connection...")
        
        # get free port
        port = get_free_port()
        host = "localhost"
        
        # start server
        server_cmd = [
            "python3", "server/server.py",
            "--config", "../server/configs/lab01_rps.json",
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
            if not wait_for_server(host, port, timeout=10):
                raise Exception("server failed to start")
            
            # create client
            agent = SimpleTestAgent("test_agent", 0)
            client = AGTClient(agent, host, port)
            
            # test connection
            await client.connect()
            assert client.connected, "client should be connected"
            
            # test disconnection
            await client.disconnect()
            assert not client.connected, "client should be disconnected"
            
            print("client connection tests passed")
            
        finally:
            # clean up server
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()


class TestGameMechanics:
    """test basic game mechanics."""
    
    def test_rps_game_mechanics(self):
        """test rps game mechanics."""
        print("testing rps game mechanics...")
        
        # import rps game
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))
        from game.RPSGame import RPSGame
        
        game = RPSGame()
        
        # test rock vs paper
        obs, rewards, done, info = game.step({0: 0, 1: 1})
        assert rewards[0] == -1, "rock should lose to paper"
        assert rewards[1] == 1, "paper should beat rock"
        
        # test rock vs scissors
        obs, rewards, done, info = game.step({0: 0, 1: 2})
        assert rewards[0] == 1, "rock should beat scissors"
        assert rewards[1] == -1, "scissors should lose to rock"
        
        # test paper vs scissors
        obs, rewards, done, info = game.step({0: 1, 1: 2})
        assert rewards[0] == -1, "paper should lose to scissors"
        assert rewards[1] == 1, "scissors should beat paper"
        
        # test ties
        obs, rewards, done, info = game.step({0: 0, 1: 0})
        assert rewards[0] == 0, "rock vs rock should be a tie"
        assert rewards[1] == 0, "rock vs rock should be a tie"
        
        print("rps game mechanics tests passed")


class TestAgentInterface:
    """test agent interface compliance."""
    
    def test_agent_interface(self):
        """test that agents implement required interface."""
        print("testing agent interface...")
        
        # test simple agent
        agent = SimpleTestAgent("test", 0)
        assert hasattr(agent, 'get_action'), "agent should have get_action method"
        assert hasattr(agent, 'update'), "agent should have update method"
        assert hasattr(agent, 'reset'), "agent should have reset method"
        
        # test random agent
        random_agent = RandomTestAgent("random", 3)
        assert hasattr(random_agent, 'get_action'), "agent should have get_action method"
        assert hasattr(random_agent, 'update'), "agent should have update method"
        assert hasattr(random_agent, 'reset'), "agent should have reset method"
        
        # test action generation
        for _ in range(10):
            action = agent.get_action({})
            random_action = random_agent.get_action({})
            
            assert action == 0, "simple agent should always return 0"
            assert random_action in [0, 1, 2], "random agent should return valid action"
        
        print("agent interface tests passed")


class TestMultiAgentGame:
    """test multi-agent game scenarios."""
    
    @pytest.mark.asyncio
    async def test_two_agents_rps(self):
        """test two agents playing rps."""
        print("testing two agents rps game...")
        
        # get free port
        port = get_free_port()
        host = "localhost"
        
        # start server
        server_cmd = [
            "python3", "server/server.py",
            "--config", "../server/configs/lab01_rps.json",
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
            if not wait_for_server(host, port, timeout=10):
                raise Exception("server failed to start")
            
            # create agents
            agent1 = SimpleTestAgent("agent1", 0)  # always rock
            agent2 = SimpleTestAgent("agent2", 1)  # always paper
            
            # create clients
            client1 = AGTClient(agent1, host, port)
            client2 = AGTClient(agent2, host, port)
            
            # connect agents
            await client1.connect()
            await client2.connect()
            
            if not client1.connected or not client2.connected:
                raise Exception("failed to connect agents")
            
            # join game
            success1 = await client1.join_game("rps")
            success2 = await client2.join_game("rps")
            
            if not success1 or not success2:
                raise Exception("failed to join game")
            
            # run game
            try:
                await asyncio.wait_for(
                    asyncio.gather(client1.run(), client2.run()),
                    timeout=30
                )
            except asyncio.TimeoutError:
                print("game timed out (expected for simple agents)")
            
            # check results
            print(f"agent1 total reward: {agent1.total_reward}")
            print(f"agent2 total reward: {agent2.total_reward}")
            
            # clean up
            await client1.disconnect()
            await client2.disconnect()
            
            print("two agents rps test passed")
            
        finally:
            # clean up server
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()


class TestErrorHandling:
    """test error handling scenarios."""
    
    @pytest.mark.asyncio
    async def test_invalid_game_type(self):
        """test handling of invalid game type."""
        print("testing invalid game type handling...")
        
        # get free port
        port = get_free_port()
        host = "localhost"
        
        # start server
        server_cmd = [
            "python3", "server/server.py",
            "--config", "../server/configs/lab01_rps.json",
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
            if not wait_for_server(host, port, timeout=10):
                raise Exception("server failed to start")
            
            # create client
            agent = SimpleTestAgent("test_agent", 0)
            client = AGTClient(agent, host, port)
            
            # connect
            await client.connect()
            
            # try to join invalid game
            success = await client.join_game("invalid_game")
            assert not success, "should fail to join invalid game"
            
            # clean up
            await client.disconnect()
            
            print("invalid game type handling test passed")
            
        finally:
            # clean up server
            server_proc.terminate()
            try:
                server_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_proc.kill()


class TestServerStartup:
    """test server startup scenarios."""
    
    def test_server_startup_with_config(self):
        """test server startup with configuration file."""
        print("testing server startup with config...")
        
        # test with valid config
        config_file = "../server/configs/lab01_rps.json"
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            server = AGTServer(config, "localhost", 8080)
            assert server.allowed_games == ["rps"], "should load rps restriction from file"
            assert "rps" in server.game_configs, "should have rps available from file"
            
            print("server startup with config test passed")
        else:
            print("skipping config file test - file not found")


def run_all_tests():
    """run all comprehensive tests."""
    print("running comprehensive server test suite...")
    print("=" * 60)
    
    # create test instances
    config_test = TestServerConfiguration()
    connection_test = TestClientConnection()
    mechanics_test = TestGameMechanics()
    agent_test = TestAgentInterface()
    multi_agent_test = TestMultiAgentGame()
    error_test = TestErrorHandling()
    startup_test = TestServerStartup()
    
    # run tests
    tests = [
        ("server configuration", config_test.test_server_configuration),
        ("game mechanics", mechanics_test.test_rps_game_mechanics),
        ("agent interface", agent_test.test_agent_interface),
        ("server startup", startup_test.test_server_startup_with_config),
    ]
    
    # async tests need to be run differently
    async_tests = [
        ("client connection", connection_test.test_client_connection),
        ("two agents rps", multi_agent_test.test_two_agents_rps),
        ("error handling", error_test.test_invalid_game_type),
    ]
    
    # run sync tests
    for test_name, test_func in tests:
        try:
            print(f"\nrunning {test_name}...")
            test_func()
            print(f"{test_name} passed")
        except Exception as e:
            print(f"{test_name} failed: {e}")
    
    # run async tests
    async def run_async_tests():
        for test_name, test_func in async_tests:
            try:
                print(f"\nrunning {test_name}...")
                await test_func()
                print(f"{test_name} passed")
            except Exception as e:
                print(f"{test_name} failed: {e}")
    
    # run async tests
    try:
        asyncio.run(run_async_tests())
    except Exception as e:
        print(f"async tests failed: {e}")
    
    print("\n" + "=" * 60)
    print("comprehensive server test suite completed!")


if __name__ == "__main__":
    run_all_tests() 