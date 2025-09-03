#!/usr/bin/env python3
"""
Test script to verify AGT Server package installation

Run this script to test if the package was installed correctly
and all imports work as expected.
"""

import sys
import importlib

def test_import(module_name, description):
    """Test if a module can be imported."""
    try:
        module = importlib.import_module(module_name)
        print(f"✓ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {description}: {module_name} - {e}")
        return False

def test_class_import(module_name, class_name, description):
    """Test if a specific class can be imported from a module."""
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, class_name):
            print(f"✓ {description}: {class_name} from {module_name}")
            return True
        else:
            print(f"✗ {description}: {class_name} not found in {module_name}")
            return False
    except ImportError as e:
        print(f"✗ {description}: {module_name} - {e}")
        return False

def main():
    """Run all package tests."""
    print("AGT Server Package Test")
    print("=" * 30)
    
    tests_passed = 0
    total_tests = 0
    
    # Test basic package import
    total_tests += 1
    if test_import("agt_server", "Main package"):
        tests_passed += 1
    
    # Test main server class
    total_tests += 1
    if test_class_import("agt_server", "AGTServer", "Main server class"):
        tests_passed += 1
    
    # Test game engine
    total_tests += 1
    if test_class_import("agt_server", "GameEngine", "Game engine"):
        tests_passed += 1
    
    # Test individual game classes
    game_classes = [
        ("RPSGame", "Rock Paper Scissors game"),
        ("BOSGame", "Battle of the Sexes game"),
        ("ChickenGame", "Chicken game"),
        ("PDGame", "Prisoner's Dilemma game"),
        ("LemonadeGame", "Lemonade Stand game"),
        ("AuctionGame", "Auction game")
    ]
    
    for class_name, description in game_classes:
        total_tests += 1
        if test_class_import("agt_server", class_name, description):
            tests_passed += 1
    
    # Test CLI module
    total_tests += 1
    if test_import("agt_server.cli", "CLI module"):
        tests_passed += 1
    
    # Test server module
    total_tests += 1
    if test_import("agt_server.server.server", "Server module"):
        tests_passed += 1
    
    # Test dashboard module
    total_tests += 1
    if test_import("agt_server.dashboard.app", "Dashboard module"):
        tests_passed += 1
    
    # Test core modules
    total_tests += 1
    if test_import("agt_server.core.engine", "Core engine"):
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 30)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Package is working correctly.")
        print("\nYou can now use:")
        print("  agt-server --help")
        print("  agt-dashboard --help")
        print("  python -m agt_server.cli both")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
        print("You may need to reinstall the package or check dependencies.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
