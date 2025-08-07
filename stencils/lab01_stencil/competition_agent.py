import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from core.agents.common.base_agent import BaseAgent
from core.engine import Engine
from core.game.RPSGame import RPSGame
from core.agents.lab01.random_agent import RandomAgent


class CompetitionAgent(BaseAgent):
    def __init__(self, name: str = "Competition"):
        super().__init__(name)
        self.ROCK, self.PAPER, self.SCISSORS = 0, 1, 2
        self.actions = [self.ROCK, self.PAPER, self.SCISSORS]
    
    def get_action(self, obs):
        """
        TODO: Implement your competition strategy here!
        
        This is where you'll put your best agent implementation.
        You can use any combination of:
        - Fictitious Play
        - Exponential Weights  
        - Pattern recognition
        - Counter-strategies
        - Or any other approach you think will work well
        
        Return one of: self.ROCK (0), self.PAPER (1), or self.SCISSORS (2)
        """
        # TODO: Fill out your competition strategy
        raise NotImplementedError
    
    def update(self, reward: float):
        """Update internal state with the reward received."""
        self.reward_history.append(reward)
        # TODO: Add any additional state updates your strategy needs


if __name__ == "__main__":
    # TODO: Please edit these variables
    agent_name = "YourName_Competition"  # TODO: Give your agent a name
    
    # Create agents
    agent = CompetitionAgent(agent_name)
    opponent = RandomAgent("Random")
    
    # Create game and run
    game = RPSGame(rounds=1000)
    agents = [agent, opponent]
    
    engine = Engine(game, agents, rounds=1000)
    final_rewards = engine.run()
    
    print(f"Final rewards: {final_rewards}")
    print(f"Cumulative rewards: {engine.cumulative_reward}")
    
    # Print statistics
    print(f"\n{agent.name} statistics:")
    action_counts = [0, 0, 0]  # Rock, Paper, Scissors
    for action in agent.action_history:
        action_counts[action] += 1
    print(f"Rock: {action_counts[0]}, Paper: {action_counts[1]}, Scissors: {action_counts[2]}")
    print(f"Total reward: {sum(agent.reward_history)}")
    print(f"Average reward: {sum(agent.reward_history) / len(agent.reward_history) if agent.reward_history else 0:.3f}")

# Export for server testing
agent_submission = CompetitionAgent("TestCompetition") 