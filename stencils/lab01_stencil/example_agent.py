import numpy as np
import sys
import os

# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.agents.common.base_agent import BaseAgent


class ExampleCompetitionAgent(BaseAgent):
    def __init__(self, name: str = "ExampleCompetition"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
        
        # Fictitious Play components
        self.opponent_action_counts = [0, 0, 0]  # Count of each action by opponent
        
        # Exponential Weights components
        self.action_rewards = np.zeros(len(self.actions))  # Cumulative rewards for each action
        self.action_counts = [0, 0, 0]  # Number of times each action was played
        
        # Strategy mixing parameters
        self.fp_weight = 0.8  # Weight for Fictitious Play
        self.ew_weight = 0.2  # Weight for Exponential Weights
        self.min_rounds_for_mixing = 5  # Start mixing strategies after this many rounds
    
    def get_action(self, obs):
        """
        Implemented competition strategy combining Fictitious Play and Exponential Weights.
        
        This strategy:
        1. Uses Fictitious Play to predict opponent's next move and play best response
        2. Uses Exponential Weights to learn from our own action rewards
        3. Combines both strategies with adaptive weights
        """
        if len(self.action_history) < self.min_rounds_for_mixing:
            # Early game: use mostly Fictitious Play
            action = self._fictitious_play_action()
        else:
            # Later game: mix strategies
            fp_action = self._fictitious_play_action()
            ew_action = self._exponential_weights_action()
            
            # Mix strategies based on weights
            if np.random.random() < self.fp_weight:
                action = fp_action
            else:
                action = ew_action
        
        self.action_history.append(action)
        return action
    
    def _fictitious_play_action(self):
        """Get action using Fictitious Play strategy."""
        dist = self._predict_opponent_distribution()
        best_move = self._optimize_against_distribution(dist)
        return self.actions[best_move]
    
    def _exponential_weights_action(self):
        """Get action using Exponential Weights strategy."""
        move_probs = self._calc_move_probs()
        return np.random.choice(self.actions, p=move_probs)
    
    def _predict_opponent_distribution(self):
        """Predict opponent's next move distribution using Fictitious Play."""
        if sum(self.opponent_action_counts) == 0:
            # No history yet, assume uniform distribution
            return np.array([1/3, 1/3, 1/3])
        
        # Return empirical distribution of opponent's actions
        total = sum(self.opponent_action_counts)
        return np.array(self.opponent_action_counts) / total
    
    def _optimize_against_distribution(self, dist):
        """Find best response to opponent's predicted distribution."""
        expected_payoffs = np.zeros(3)
        
        for my_action in self.actions:
            for opp_action in self.actions:
                # RPS payoff matrix
                if my_action == opp_action:
                    payoff = 0
                elif (my_action == 0 and opp_action == 2) or \
                     (my_action == 1 and opp_action == 0) or \
                     (my_action == 2 and opp_action == 1):
                    payoff = 1  # Win
                else:
                    payoff = -1  # Lose
                
                expected_payoffs[my_action] += dist[opp_action] * payoff
        
        return np.argmax(expected_payoffs)
    
    def _calc_move_probs(self):
        """Calculate move probabilities using Exponential Weights."""
        if sum(self.action_counts) == 0:
            # No history yet, return uniform distribution
            return np.array([1/3, 1/3, 1/3])
        
        # Calculate average rewards for each action
        avg_rewards = np.zeros(3)
        for i in range(3):
            if self.action_counts[i] > 0:
                avg_rewards[i] = self.action_rewards[i] / self.action_counts[i]
            else:
                avg_rewards[i] = 0.0
        
        # Apply softmax to get probabilities
        return self._softmax(avg_rewards)
    
    @staticmethod
    def _softmax(x):
        """Compute softmax values for each set of scores in x."""
        # Shifting values to avoid nan issues (due to underflow)
        shifted_x = x - np.max(x)
        exp_values = np.exp(shifted_x)
        return exp_values / np.sum(exp_values)
    
    def update(self, reward: float, info=None):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        
        # Update Exponential Weights components
        if len(self.action_history) > 0:
            last_action = self.action_history[-1]
            self.action_rewards[last_action] += reward
            self.action_counts[last_action] += 1
        
        # Update Fictitious Play components
        if len(self.action_history) > 0:
            my_action = self.action_history[-1]
            
            # Infer opponent's action from reward and our action
            if reward == 0:
                opp_action = my_action  # Tie
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
        
        # Adapt strategy weights based on performance
        self._adapt_weights()
    
    def _adapt_weights(self):
        """Adapt the mixing weights based on recent performance."""
        if len(self.reward_history) < 10:
            return
        
        # Look at last 10 rounds
        recent_rewards = self.reward_history[-10:]
        avg_recent_reward = np.mean(recent_rewards)
        
        # If doing well, increase Fictitious Play weight
        if avg_recent_reward > 0.05:
            self.fp_weight = min(0.95, self.fp_weight + 0.02)
            self.ew_weight = max(0.05, self.ew_weight - 0.02)
        # If doing poorly, increase Exponential Weights weight
        elif avg_recent_reward < -0.05:
            self.fp_weight = max(0.05, self.fp_weight - 0.02)
            self.ew_weight = min(0.95, self.ew_weight + 0.02)


# Export for server testing
agent_submission = ExampleCompetitionAgent("ExampleCompetition")


# Direct execution support
if __name__ == "__main__":
    import asyncio
    import sys
    import os
    
    # Add server directory to path
    server_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'server')
    sys.path.insert(0, server_dir)
    
    from client import AGTClient
    from adapters import create_adapter
    
    async def main():
        """Run the agent directly by connecting to the server."""
        import argparse
        
        parser = argparse.ArgumentParser(description='Run Example Competition Agent')
        parser.add_argument('--host', type=str, default='localhost', help='Server host')
        parser.add_argument('--port', type=int, default=8080, help='Server port')
        parser.add_argument('--name', type=str, default='ExampleCompetition', help='Agent name')
        parser.add_argument('--game', type=str, default='rps', choices=['rps', 'bos', 'bosii', 'chicken'], help='Game type')
        
        args = parser.parse_args()
        
        # Create adapter for the agent
        agent = create_adapter(agent_submission, args.game)
        agent.name = args.name
        
        print(f"Starting {agent.name} for {args.game} game...")
        print(f"Connecting to server at {args.host}:{args.port}")
        
        # Create client and connect
        client = AGTClient(agent, args.host, args.port)
        await client.connect()
        
        if client.connected:
            print("Connected to server!")
            print(f"Joining {args.game} game...")
            
            if await client.join_game(args.game):
                print("Joined game successfully!")
                print("Waiting for game to start...")
                await client.run()
            else:
                print("Failed to join game")
        else:
            print("Failed to connect to server")
            sys.exit(1)
    
    # Run the async main function
    asyncio.run(main())
