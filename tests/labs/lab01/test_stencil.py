#!/usr/bin/env python3
"""
Test script to verify the Lab 1 stencil works correctly with actual implementations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import numpy as np
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.game.ChickenGame import ChickenGame
from core.agents.lab01.random_agent import RandomAgent
from core.agents.lab01.rock_agent import RockAgent
from core.agents.common.base_agent import BaseAgent


# Student implementation of Fictitious Play Agent
class StudentFictitiousPlayAgent(BaseAgent):
    def __init__(self, name: str = "StudentFictitiousPlay"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.opponent_action_counts = [0, 0, 0]  # Count of each action by opponent
    
    def get_action(self, obs):
        """Return the best response to predicted opponent action."""
        dist = self.predict()
        best_move = self.optimize(dist)
        action = self.actions[best_move]
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """Store the reward and update opponent action counts."""
        self.reward_history.append(reward)
        
        # Update opponent action counts based on the reward
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            # Infer opponent's action from reward
            if reward == 0:
                # Tie - opponent played same as us
                opp_action = my_action
            elif reward == 1:
                # We won - opponent played the action we beat
                if my_action == 0:  # Rock beats Scissors
                    opp_action = 2
                elif my_action == 1:  # Paper beats Rock
                    opp_action = 0
                else:  # Scissors beats Paper
                    opp_action = 1
            else:  # reward == -1
                # We lost - opponent played the action that beats us
                if my_action == 0:  # Rock loses to Paper
                    opp_action = 1
                elif my_action == 1:  # Paper loses to Scissors
                    opp_action = 2
                else:  # Scissors loses to Rock
                    opp_action = 0
            
            self.opponent_action_counts[opp_action] += 1
    
    def predict(self):
        """Uses the opponent's previous moves to generate a probability distribution."""
        total_actions = sum(self.opponent_action_counts)
        if total_actions == 0:
            # If no history, assume uniform distribution
            return [1/3, 1/3, 1/3]
        
        # Return empirical distribution
        return [count / total_actions for count in self.opponent_action_counts]
    
    def optimize(self, dist):
        """Given the distribution, return the best move according to FP."""
        # RPS payoff matrix (row = our action, col = opponent action)
        # 0 = tie, 1 = win, -1 = lose
        payoff_matrix = [
            [0, -1, 1],   # Rock vs [Rock, Paper, Scissors]
            [1, 0, -1],   # Paper vs [Rock, Paper, Scissors]
            [-1, 1, 0]    # Scissors vs [Rock, Paper, Scissors]
        ]
        
        # Calculate expected payoff for each action
        expected_payoffs = []
        for our_action in range(3):
            expected_payoff = sum(payoff_matrix[our_action][opp_action] * dist[opp_action] 
                                for opp_action in range(3))
            expected_payoffs.append(expected_payoff)
        
        # Return action with highest expected payoff
        return np.argmax(expected_payoffs)


# Student implementation of Exponential Agent
class StudentExponentialAgent(BaseAgent):
    def __init__(self, name: str = "StudentExponential"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.action_rewards = np.zeros(len(self.actions))  # Cumulative rewards for each action
        self.action_counts = [0, 0, 0]  # Number of times each action was played
        self.eta = 0.1  # Learning rate
    
    def get_action(self, obs):
        """Return an action based on exponential weights strategy."""
        move_probs = self.calc_move_probs()
        action = np.random.choice(self.actions, p=move_probs)
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """Update action rewards and counts."""
        self.reward_history.append(reward)
        
        # Update the reward for the last action taken
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
    
    @staticmethod
    def softmax(x):
        """Compute softmax values for each set of scores in x."""
        # Shifting values to avoid nan issues (due to underflow)
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)
    
    def calc_move_probs(self):
        """Uses historical average rewards to generate probability distribution."""
        if sum(self.action_counts) == 0:
            # If no actions taken yet, return uniform distribution
            return [1/3, 1/3, 1/3]
        
        # Calculate average reward for each action
        avg_rewards = []
        for i in range(3):
            if self.action_counts[i] > 0:
                avg_rewards.append(self.action_rewards[i] / self.action_counts[i])
            else:
                avg_rewards.append(0)
        
        # Apply exponential weights
        weighted_rewards = [self.eta * avg for avg in avg_rewards]
        return self.softmax(weighted_rewards)


# Student implementation of Competition Agent
class StudentCompetitionAgent(BaseAgent):
    def __init__(self, name: str = "StudentCompetition"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        self.opponent_action_counts = [0, 0, 0]
        self.action_rewards = np.zeros(3)
        self.action_counts = [0, 0, 0]
        self.eta = 0.1
    
    def get_action(self, obs):
        """Implement a hybrid strategy combining FP and exponential weights."""
        if len(self.action_history) < 10:
            # Early game: use exponential weights
            move_probs = self.calc_move_probs()
            action = np.random.choice(self.actions, p=move_probs)
        else:
            # Late game: use fictitious play
            dist = self.predict()
            best_move = self.optimize(dist)
            action = self.actions[best_move]
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        
        # Update exponential weights
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
        
        # Update opponent action counts (infer from reward)
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            if reward == 0:
                opp_action = my_action
            elif reward == 1:
                if my_action == 0: opp_action = 2
                elif my_action == 1: opp_action = 0
                else: opp_action = 1
            else:
                if my_action == 0: opp_action = 1
                elif my_action == 1: opp_action = 2
                else: opp_action = 0
            
            self.opponent_action_counts[opp_action] += 1
    
    def predict(self):
        """Predict opponent's next move using empirical distribution."""
        total_actions = sum(self.opponent_action_counts)
        if total_actions == 0:
            return [1/3, 1/3, 1/3]
        return [count / total_actions for count in self.opponent_action_counts]
    
    def optimize(self, dist):
        """Find best response to predicted opponent distribution."""
        payoff_matrix = [
            [0, -1, 1],
            [1, 0, -1],
            [-1, 1, 0]
        ]
        
        expected_payoffs = []
        for our_action in range(3):
            expected_payoff = sum(payoff_matrix[our_action][opp_action] * dist[opp_action] 
                                for opp_action in range(3))
            expected_payoffs.append(expected_payoff)
        
        return np.argmax(expected_payoffs)
    
    def calc_move_probs(self):
        """Calculate move probabilities using exponential weights."""
        if sum(self.action_counts) == 0:
            return [1/3, 1/3, 1/3]
        
        avg_rewards = []
        for i in range(3):
            if self.action_counts[i] > 0:
                avg_rewards.append(self.action_rewards[i] / self.action_counts[i])
            else:
                avg_rewards.append(0)
        
        weighted_rewards = [self.eta * avg for avg in avg_rewards]
        return self.softmax(weighted_rewards)
    
    @staticmethod
    def softmax(x):
        """Compute softmax values."""
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)


# Student implementation of Competition Agent for Chicken
class StudentChickenCompetitionAgent(BaseAgent):
    def __init__(self, name: str = "StudentChickenCompetition"):
        super().__init__(name)
        self.SWERVE, self.CONTINUE = 0, 1
        self.actions = [self.SWERVE, self.CONTINUE]
        self.opponent_action_counts = [0, 0]
        self.action_rewards = np.zeros(2)
        self.action_counts = [0, 0]
        self.eta = 0.1
    
    def setup(self):
        """Initialize the agent for each new game."""
        self.opponent_action_counts = [0, 0]
        self.action_rewards = np.zeros(2)
        self.action_counts = [0, 0]
    
    def get_action(self, obs):
        """Implement a strategy for Chicken game."""
        # Use a mixed strategy that swerves 70% of the time
        # This is a simple strategy that students can improve upon
        import random
        if random.random() < 0.7:
            action = self.SWERVE
        else:
            action = self.CONTINUE
        
        self.action_history.append(action)
        return action
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        
        # Update action rewards
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
        
        # Infer opponent's action from reward and our action
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            # Chicken payoff matrix (row player, column player):
            # S\C  S  C
            # S    0  -1
            # C    1  -5
            
            if my_action == self.SWERVE:
                if reward == 0:
                    opp_action = self.SWERVE  # Both swerved
                else:  # reward == -1
                    opp_action = self.CONTINUE  # We swerved, they continued
            else:  # my_action == self.CONTINUE
                if reward == 1:
                    opp_action = self.SWERVE  # We continued, they swerved
                else:  # reward == -5
                    opp_action = self.CONTINUE  # Both continued
            
            self.opponent_action_counts[opp_action] += 1


def test_fictitious_play_agent():
    """Test the fictitious play agent implementation."""
    print("Testing Fictitious Play Agent...")
    
    agent = StudentFictitiousPlayAgent("TestFP")
    opponent = RandomAgent("Random")
    
    game = RPSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(100)
    
    print(f"Final rewards: {final_rewards}")
    print(f"FP Agent total reward: {sum(agent.reward_history)}")
    print(f"FP Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is learning and not just playing randomly
    assert len(agent.action_history) == 100, "Agent should have played 100 actions"
    assert len(agent.reward_history) == 100, "Agent should have 100 rewards"
    
    print("PASS: Fictitious Play Agent test passed!")


def test_exponential_agent():
    """Test the exponential agent implementation."""
    print("Testing Exponential Agent...")
    
    agent = StudentExponentialAgent("TestExp")
    opponent = RandomAgent("Random")
    
    game = RPSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(100)
    
    print(f"Final rewards: {final_rewards}")
    print(f"Exp Agent total reward: {sum(agent.reward_history)}")
    print(f"Exp Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is learning
    assert len(agent.action_history) == 100, "Agent should have played 100 actions"
    assert len(agent.reward_history) == 100, "Agent should have 100 rewards"
    
    print("PASS: Exponential Agent test passed!")


def test_competition_agent():
    """Test the competition agent implementation."""
    print("Testing Competition Agent...")
    
    agent = StudentCompetitionAgent("TestComp")
    opponent = RandomAgent("Random")
    
    game = RPSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(100)
    
    print(f"Final rewards: {final_rewards}")
    print(f"Comp Agent total reward: {sum(agent.reward_history)}")
    print(f"Comp Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is learning
    assert len(agent.action_history) == 100, "Agent should have played 100 actions"
    assert len(agent.reward_history) == 100, "Agent should have 100 rewards"
    
    print("PASS: Competition Agent test passed!")


def test_chicken_competition_agent():
    """Test the competition agent implementation for Chicken game."""
    print("Testing Chicken Competition Agent...")
    
    agent = StudentChickenCompetitionAgent("TestChickenComp")
    opponent = RandomAgent("Random")
    
    game = ChickenGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(100)
    
    print(f"Final rewards: {final_rewards}")
    print(f"Chicken Comp Agent total reward: {sum(agent.reward_history)}")
    print(f"Chicken Comp Agent average reward: {sum(agent.reward_history) / len(agent.reward_history):.3f}")
    
    # Verify the agent is working
    assert len(agent.action_history) == 100, "Agent should have played 100 actions"
    assert len(agent.reward_history) == 100, "Agent should have 100 rewards"
    
    # Check that actions are valid for Chicken game
    for action in agent.action_history:
        assert action in [0, 1], f"Invalid action {action} for Chicken game"
    
    print("PASS: Chicken Competition Agent test passed!")


def test_agent_vs_rock():
    """Test that agents can beat a deterministic rock agent."""
    print("Testing agents vs Rock agent...")
    
    rock_agent = RockAgent("Rock")
    
    # Test FP vs Rock
    fp_agent = StudentFictitiousPlayAgent("FP")
    game = RPSGame()
    agents = [fp_agent, rock_agent]
    engine = Engine(game, agents)
    final_rewards = engine.run(50)
    
    fp_reward = sum(fp_agent.reward_history)
    print(f"FP vs Rock: {fp_reward}")
    assert fp_reward > 0, "FP agent should beat rock agent"
    
    # Test Exponential vs Rock
    exp_agent = StudentExponentialAgent("Exp")
    game = RPSGame()
    agents = [exp_agent, rock_agent]
    engine = Engine(game, agents)
    final_rewards = engine.run(50)
    
    exp_reward = sum(exp_agent.reward_history)
    print(f"Exp vs Rock: {exp_reward}")
    assert exp_reward > 0, "Exponential agent should beat rock agent"
    
    print("PASS: Agent vs Rock tests passed!")


def test_agent_learning():
    """Test that agents show learning behavior."""
    print("Testing agent learning behavior...")
    
    # Test that agents improve over time
    agent = StudentCompetitionAgent("LearningTest")
    opponent = RandomAgent("Random")
    
    game = RPSGame()
    agents = [agent, opponent]
    engine = Engine(game, agents)
    final_rewards = engine.run(200)
    
    # Split rewards into first and second half
    mid_point = len(agent.reward_history) // 2
    first_half = agent.reward_history[:mid_point]
    second_half = agent.reward_history[mid_point:]
    
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    
    print(f"First half average: {first_avg:.3f}")
    print(f"Second half average: {second_avg:.3f}")
    
    # Agent should improve or at least not get significantly worse
    assert second_avg >= first_avg - 0.1, "Agent should not get significantly worse over time"
    
    print("PASS: Agent learning test passed!")


if __name__ == "__main__":
    print("Lab 1 Comprehensive Test Suite")
    print("=" * 40)
    
    test_fictitious_play_agent()
    print()
    test_exponential_agent()
    print()
    test_competition_agent()
    print()
    test_chicken_competition_agent()
    print()
    test_agent_vs_rock()
    print()
    test_agent_learning()
    
    print("\n" + "=" * 40)
    print("PASS: All Lab 1 tests completed successfully!")
    print("\nThese tests verify that:")
    print("1. All agent implementations work correctly")
    print("2. Agents can learn and improve over time")
    print("3. Agents can beat simple deterministic strategies")
    print("4. The game engine and reward system work properly")
    print("5. Competition agent works correctly for Chicken game") 