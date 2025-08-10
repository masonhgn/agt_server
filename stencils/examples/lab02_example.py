#!/usr/bin/env python3
"""
Example solution for Lab 2 - Battle of the Sexes
This shows what a completed implementation looks like.
"""

import sys
import os
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent

import random
import numpy as np

class CompromiseAgent(object):
    def __init__(self, name="CompromiseAgent"):
        self.name = name
    
    def get_action(self, state):
        # Compromise by choosing a middle action
        return 1  # Middle action in BOS game
    
    def update(self, reward, info=None):
        pass

class StubbornAgent:
    def __init__(self):
        self.name = "StubbornAgent"
    
    def get_action(self, state):
        # Always choose the same action
        return 0  # Stubborn choice
    
    def update(self, reward, info=None):
        pass


class ExampleBOSFiniteStateAgent:
    """Example implementation of a finite state machine for BOS."""
    
    def __init__(self, name: str = "ExampleBOSFSM"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0
    
    def get_action(self, obs):
        """Return action based on current state."""
        if self.curr_state == 0:
            return self.STUBBORN  # Start with Stubborn
        elif self.curr_state in [1, 3]:
            return self.COMPROMISE  # Compromise for 2 rounds
        else:
            return self.STUBBORN  # Otherwise be Stubborn
    
    def update(self, reward, info=None):
        """Update state based on opponent's last action."""
        self.reward_history.append(reward)
        
        if len(self.action_history) == 0:
            return
        
        my_last_action = self.action_history[-1]
        opp_last_action = self.get_opponent_last_action()
        
        if opp_last_action is None:
            return
        
        # State transition logic
        if self.curr_state == 0:
            if opp_last_action == self.STUBBORN:
                self.curr_state = 1  # Opponent was stubborn, compromise for 2 rounds
        elif self.curr_state == 1:
            self.curr_state = 2  # Second compromise round
        elif self.curr_state == 2:
            if opp_last_action == self.STUBBORN:
                self.curr_state = 3  # Opponent was stubborn again, compromise for 2 more rounds
            else:
                self.curr_state = 0  # Opponent compromised, return to initial state
        elif self.curr_state == 3:
            self.curr_state = 4  # Second compromise round
        elif self.curr_state == 4:
            self.curr_state = 4  # Stay in punishment state
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Infer opponent's action from reward and my action
        if my_last_action == self.COMPROMISE:
            if my_last_reward == 0:
                return self.COMPROMISE  # Both compromised
            elif my_last_reward == 3:
                return self.STUBBORN     # I compromised, they were stubborn
        elif my_last_action == self.STUBBORN:
            if my_last_reward == 7:
                return self.COMPROMISE   # I was stubborn, they compromised
            elif my_last_reward == 0:
                return self.STUBBORN     # Both were stubborn
        
        return None  # Can't determine


class ExampleBOSIIAgent(BaseAgent):
    """Example implementation for BOSII with incomplete information."""
    
    def __init__(self, name: str = "ExampleBOSII"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.GOOD_MOOD, self.BAD_MOOD = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0
        self.is_row = True  # Assume row player for this example
        self.current_mood = None
        self.mood_history = []
    
    def get_action(self, obs):
        """Return action based on current state and mood information."""
        if self.is_row_player():
            # Row player strategy: be stubborn initially, then adapt
            if self.curr_state == 0:
                return self.STUBBORN
            else:
                return self.COMPROMISE
        else:
            # Column player strategy: consider mood
            if self.get_mood() == self.GOOD_MOOD:
                return self.COMPROMISE
            else:
                return self.STUBBORN
    
    def update(self, reward, info=None):
        """Update state and mood information."""
        self.reward_history.append(reward)
        
        # Update mood information (in a real implementation, this would come from the game)
        if not self.is_row_player():
            # Simulate mood updates for column player
            import random
            self.current_mood = random.choice([self.GOOD_MOOD, self.BAD_MOOD])
            self.mood_history.append(self.current_mood)
        
        # Simple state transition
        if len(self.action_history) > 0:
            my_last_action = self.action_history[-1]
            opp_last_action = self.get_opponent_last_action()
            
            if opp_last_action == self.STUBBORN:
                self.curr_state = min(self.curr_state + 1, 2)
            else:
                self.curr_state = max(self.curr_state - 1, 0)
    
    def is_row_player(self):
        return self.is_row
    
    def get_mood(self):
        return self.current_mood
    
    def get_last_mood(self):
        return self.mood_history[-1] if self.mood_history else None
    
    def get_mood_history(self):
        return self.mood_history.copy()
    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # Simplified inference for BOSII
        if my_last_action == self.COMPROMISE:
            if my_last_reward == 0:
                return self.COMPROMISE
            elif my_last_reward == 3:
                return self.STUBBORN
        elif my_last_action == self.STUBBORN:
            if my_last_reward == 7:
                return self.COMPROMISE
            elif my_last_reward == 0:
                return self.STUBBORN
        
        return None


if __name__ == "__main__":
    print("Example Solutions for Lab 2")
    print("=" * 40)
    
    # Test BOS Finite State Machine
    print("\nTesting BOS Finite State Machine vs Random:")
    game = BOSGame(rounds=100)
    agents = [
        ExampleBOSFiniteStateAgent("ExampleBOSFSM"),
        RandomBOSAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics for BOS
    bos_agent = agents[0]
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in bos_agent.action_history:
        action_counts[action] += 1
    
    print(f"\n{bos_agent.name} statistics:")
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(bos_agent.reward_history)}")
    print(f"Average reward: {sum(bos_agent.reward_history) / len(bos_agent.reward_history):.3f}")
    print(f"Final state: {bos_agent.curr_state}")
    
    # Test BOSII
    print("\nTesting BOSII vs Random:")
    game = BOSIIGame(rounds=100)
    agents = [
        ExampleBOSIIAgent("ExampleBOSII"),
        RandomBOSAgent("Random")
    ]
    
    engine = Engine(game, agents, rounds=100)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics for BOSII
    bosii_agent = agents[0]
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in bosii_agent.action_history:
        action_counts[action] += 1
    
    print(f"\n{bosii_agent.name} statistics:")
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Total reward: {sum(bosii_agent.reward_history)}")
    print(f"Average reward: {sum(bosii_agent.reward_history) / len(bosii_agent.reward_history):.3f}")
    print(f"Final state: {bosii_agent.curr_state}")
    print(f"Is row player: {bosii_agent.is_row_player()}")
    if bosii_agent.mood_history:
        print(f"Mood history: {bosii_agent.mood_history}")
    
    print("\nExample solutions completed!")
    print("Use these as reference for implementing your own agents.") 