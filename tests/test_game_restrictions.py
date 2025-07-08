#!/usr/bin/env python3
"""
test script to verify game restrictions work correctly.
"""

import json
import os

from server.server import AGTServer

def test_game_restrictions():
    """test that game restrictions work correctly."""
    
    print("testing game restrictions...")
    
    # test 1: no restrictions (all games allowed)
    print("\n1. testing no restrictions:")
    config = {
        "server_name": "test server",
        "max_players": 10,
        "timeout": 30,
        "save_results": True
    }
    server = AGTServer(config, "localhost", 8080)
    print(f"   allowed games: {server.allowed_games}")
    print(f"   available games: {list(server.game_configs.keys())}")
    assert server.allowed_games is None, "should allow all games when no restrictions"
    assert len(server.game_configs) == 6, f"should have 6 games, got {len(server.game_configs)}"
    
    # test 2: single game restriction
    print("\n2. testing single game restriction:")
    config["allowed_games"] = ["rps"]
    server = AGTServer(config, "localhost", 8080)
    print(f"   allowed games: {server.allowed_games}")
    print(f"   available games: {list(server.game_configs.keys())}")
    assert server.allowed_games == ["rps"], "should restrict to rps only"
    assert list(server.game_configs.keys()) == ["rps"], "should only have rps available"
    
    # test 3: multiple game restriction
    print("\n3. testing multiple game restriction:")
    config["allowed_games"] = ["rps", "bos", "chicken"]
    server = AGTServer(config, "localhost", 8080)
    print(f"   allowed games: {server.allowed_games}")
    print(f"   available games: {list(server.game_configs.keys())}")
    assert server.allowed_games == ["rps", "bos", "chicken"], "should restrict to specified games"
    assert set(server.game_configs.keys()) == {"rps", "bos", "chicken"}, "should only have specified games available"
    
    # test 4: invalid game in restriction
    print("\n4. testing invalid game in restriction:")
    config["allowed_games"] = ["rps", "invalid_game", "bos"]
    server = AGTServer(config, "localhost", 8080)
    print(f"   allowed games: {server.allowed_games}")
    print(f"   available games: {list(server.game_configs.keys())}")
    assert set(server.game_configs.keys()) == {"rps", "bos"}, "should ignore invalid games"
    
    # test 5: configuration file loading
    print("\n5. testing configuration file loading:")
    config_file = "configs/lab01_rps.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            file_config = json.load(f)
        server = AGTServer(file_config, "localhost", 8080)
        print(f"   allowed games: {server.allowed_games}")
        print(f"   available games: {list(server.game_configs.keys())}")
        assert server.allowed_games == ["rps"], "should load rps restriction from file"
        assert list(server.game_configs.keys()) == ["rps"], "should only have rps available from file"
    else:
        print(f"   skipping file test - {config_file} not found")
    
    print("\nPASS: all tests passed!")

if __name__ == "__main__":
    test_game_restrictions() 