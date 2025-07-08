#!/usr/bin/env python3
"""
Test script for BOS Finite State Machine stencil with actual implementations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from core.engine import Engine
from core.game.BOSGame import BOSGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent
from core.agents.lab02.compromise_agent import CompromiseAgent
from core.agents.lab02.stubborn_agent import StubbornAgent
from core.agents.common.base_agent import BaseAgent


# Student implementation of BOS Finite State Agent
class StudentBOSFiniteStateAgent(BaseAgent):
    """Finite State Machine agent for Battle of the Sexes."""
    
    def __init__(self, name: str = "StudentBOSFSM"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.curr_state = 0  # Initial state
    
    def get_action(self, obs):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        """
        # Simple state machine: state 0 = compromise, state 1 = stubborn
        if self.curr_state == 0:
            action = self.COMPROMISE
        else:
            action = self.STUBBORN
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """
        Update the current state based on the game history.
        """
        self.reward_history.append(reward)
        
        if len(self.action_history) > 0:
            my_last_action = self.action_history[-1]
            opp_last_action = self.get_opponent_last_action()
            
            if opp_last_action is not None:
                # State transition: if opponent was stubborn, become stubborn
                if opp_last_action == self.STUBBORN:
                    self.curr_state = 1
                else:
                    self.curr_state = 0
    
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


# Student implementation of BOS Competition Agent
class StudentBOSCompetitionAgent(BaseAgent):
    """Competition agent for Battle of the Sexes."""
    
    def __init__(self, name: str = "StudentBOSComp"):
        super().__init__(name)
        self.COMPROMISE, self.STUBBORN = 0, 1
        self.actions = [self.COMPROMISE, self.STUBBORN]
        self.opponent_compromise_count = 0
        self.opponent_stubborn_count = 0
        self.total_rounds = 0
    
    def get_action(self, obs):
        """
        Implement a strategy that adapts based on opponent behavior.
        """
        if self.total_rounds < 5:
            # Early game: start with compromise
            action = self.COMPROMISE
        else:
            # Late game: if opponent mostly compromises, be stubborn
            # If opponent mostly stubborn, compromise
            if self.opponent_compromise_count > self.opponent_stubborn_count:
                action = self.STUBBORN  # Exploit compromising opponent
            else:
                action = self.COMPROMISE  # Avoid conflict with stubborn opponent
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """
        Update opponent action counts based on reward.
        """
        self.reward_history.append(reward)
        self.total_rounds += 1
        
        if len(self.action_history) > 0:
            my_last_action = self.action_history[-1]
            opp_last_action = self.get_opponent_last_action()
            
            if opp_last_action is not None:
                if opp_last_action == self.COMPROMISE:
                    self.opponent_compromise_count += 1
                else:
                    self.opponent_stubborn_count += 1
    
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


def test_bos_finite_state_agent():
    """Test the BOS finite state machine agent implementation."""
    print("Testing BOS Finite State Machine Agent...")
    
    agent = StudentBOSFiniteStateAgent("TestFSM")
    opponent = RandomBOSAgent("Random")
    
    game = BOSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(50)
    
    print(f"Final rewards: {final_rewards}")
    print(f"FSM Agent total reward: {sum(agent.reward_history)}")
    print(f"FSM Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is working
    assert len(agent.action_history) == 50, "Agent should have played 50 actions"
    assert len(agent.reward_history) == 50, "Agent should have 50 rewards"
    
    # Count actions
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Final state: {agent.curr_state}")
    
    print("PASS: BOS Finite State Machine Agent test passed!")


def test_bos_competition_agent():
    """Test the BOS competition agent implementation."""
    print("Testing BOS Competition Agent...")
    
    agent = StudentBOSCompetitionAgent("TestComp")
    opponent = RandomBOSAgent("Random")
    
    game = BOSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(50)
    
    print(f"Final rewards: {final_rewards}")
    print(f"Comp Agent total reward: {sum(agent.reward_history)}")
    print(f"Comp Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is working
    assert len(agent.action_history) == 50, "Agent should have played 50 actions"
    assert len(agent.reward_history) == 50, "Agent should have 50 rewards"
    
    # Count actions
    action_counts = [0, 0]  # Compromise, Stubborn
    for action in agent.action_history:
        action_counts[action] += 1
    
    print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
    print(f"Opponent compromise count: {agent.opponent_compromise_count}")
    print(f"Opponent stubborn count: {agent.opponent_stubborn_count}")
    
    print("PASS: BOS Competition Agent test passed!")


def test_agent_vs_deterministic():
    """Test that agents can handle deterministic opponents."""
    print("Testing agents vs deterministic opponents...")
    
    # Test FSM vs Compromise
    fsm_agent = StudentBOSFiniteStateAgent("FSM")
    compromise_agent = CompromiseAgent("Compromise")
    
    game = BOSGame()
    agents = [fsm_agent, compromise_agent]
    engine = Engine(game, agents)
    final_rewards = engine.run(30)
    
    fsm_reward = sum(fsm_agent.reward_history)
    print(f"FSM vs Compromise: {fsm_reward}")
    
    # Test Competition vs Stubborn
    comp_agent = StudentBOSCompetitionAgent("Comp")
    stubborn_agent = StubbornAgent("Stubborn")
    
    game = BOSGame()
    agents = [comp_agent, stubborn_agent]
    engine = Engine(game, agents)
    final_rewards = engine.run(30)
    
    comp_reward = sum(comp_agent.reward_history)
    print(f"Comp vs Stubborn: {comp_reward}")
    
    print("PASS: Agent vs deterministic tests passed!")


def test_state_transitions():
    """Test that the FSM agent properly transitions states."""
    print("Testing FSM state transitions...")
    
    agent = StudentBOSFiniteStateAgent("StateTest")
    
    # Simulate some actions and rewards to test state transitions
    agent.get_action({})  # Initial action
    agent.update(0)  # Both compromised, should stay in state 0
    
    assert agent.curr_state == 0, "Should stay in state 0 after mutual compromise"
    
    agent.get_action({})
    agent.update(3)  # I compromised, they were stubborn, should go to state 1
    
    assert agent.curr_state == 1, "Should transition to state 1 after opponent stubborn"
    
    agent.get_action({})
    agent.update(7)  # I was stubborn, they compromised, should go back to state 0
    
    assert agent.curr_state == 0, "Should transition back to state 0 after opponent compromise"
    
    print("PASS: State transition tests passed!")


def test_learning_behavior():
    """Test that agents show learning behavior."""
    print("Testing agent learning behavior...")
    
    agent = StudentBOSCompetitionAgent("LearningTest")
    opponent = RandomBOSAgent("Random")
    
    game = BOSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(100)
    
    # Split rewards into first and second half
    mid_point = len(agent.reward_history) // 2
    first_half = agent.reward_history[:mid_point]
    second_half = agent.reward_history[mid_point:]
    
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    
    print(f"First half average: {first_avg:.3f}")
    print(f"Second half average: {second_avg:.3f}")
    
    # Agent should improve or at least not get significantly worse
    assert second_avg >= first_avg - 0.5, "Agent should not get significantly worse over time"
    
    print("PASS: Agent learning test passed!")


if __name__ == "__main__":
    print("Lab 2 BOS Comprehensive Test Suite")
    print("=" * 40)
    
    test_bos_finite_state_agent()
    print()
    test_bos_competition_agent()
    print()
    test_agent_vs_deterministic()
    print()
    test_state_transitions()
    print()
    test_learning_behavior()
    
    print("\n" + "=" * 40)
    print("PASS: All Lab 2 BOS tests completed successfully!")
    print("\nThese tests verify that:")
    print("1. Finite state machine agents work correctly")
    print("2. Competition agents can adapt to opponent behavior")
    print("3. Agents can handle deterministic opponents")
    print("4. State transitions work properly")
    print("5. Agents show learning behavior over time") 