import sys
import os
import asyncio
# Add the core directory to the path (same approach as server.py)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.agents.common.bosii_agent import BOSIIAgent
from core.engine import Engine
from core.game.BOSIIGame import BOSIIGame
from core.agents.lab02.random_bos_agent import RandomBOSAgent


class BOSIICompetitionAgent(BOSIIAgent):
    """Competition agent for Battle of the Sexes with Incomplete Information."""
    
    def __init__(self, name: str = "BOSIIComp"):
        super().__init__(name)
        self.curr_state = 0
        self.opponent_pattern = []  # Track opponent's recent actions
        self.cooperation_count = 0  # Count cooperative moves
        self.defection_count = 0    # Count defections
    
    def get_action(self, obs=None, opponent_last_move=None, player_type=None, mood=None):
        """
        Return either self.STUBBORN or self.COMPROMISE based on the current state.
        Consider whether you're the row or column player and the mood information.
        """
        # Call parent to handle both interfaces
        super().get_action(obs, opponent_last_move, player_type, mood)
        
        # Adaptive strategy for BOSII:
        # - Start with COMPROMISE to establish cooperation
        # - Adapt based on opponent's behavior and mood (if column player)
        # - Use tit-for-tat with forgiveness
        
        if self.is_row_player():
            # Row player strategy
            if self.curr_state == 0:
                # Initial state: try to cooperate
                return self.COMPROMISE
            elif self.curr_state == 1:
                # Cooperative state: mostly cooperate
                return self.COMPROMISE
            elif self.curr_state == 2:
                # Tit-for-tat state: mirror opponent's last move
                if len(self.opponent_pattern) > 0:
                    return self.opponent_pattern[-1]
                else:
                    return self.COMPROMISE
            elif self.curr_state == 3:
                # Defensive state: be stubborn
                return self.STUBBORN
            else:
                return self.COMPROMISE  # Default fallback
        else:
            # Column player strategy - consider mood
            if self.get_mood() == self.GOOD_MOOD:
                # Good mood: more cooperative
                if self.curr_state == 0:
                    return self.COMPROMISE
                elif self.curr_state == 1:
                    return self.COMPROMISE
                elif self.curr_state == 2:
                    if len(self.opponent_pattern) > 0:
                        return self.opponent_pattern[-1]
                    else:
                        return self.COMPROMISE
                else:
                    return self.COMPROMISE
            else:
                # Bad mood: more aggressive
                if self.curr_state == 0:
                    return self.STUBBORN
                elif self.curr_state == 1:
                    return self.STUBBORN
                elif self.curr_state == 2: 
                    if len(self.opponent_pattern) > 0:
                        return self.opponent_pattern[-1]
                    else:
                        return self.STUBBORN
                else:
                    return self.STUBBORN
    
    def update(self, observation: dict = None, action: dict = None, reward: float = None, done: bool = None, info: dict = None):
        """
        Update the current state based on the game history.
        This should update self.curr_state based on your FSM transition rules.
        """
        # Call parent update method
        super().update(observation, action, reward, done, info)
        
        # Get opponent's last action
        opponent_action = self.get_opponent_last_action()
        
        if opponent_action is not None:
            # Update opponent pattern
            self.opponent_pattern.append(opponent_action)
            if len(self.opponent_pattern) > 5:
                self.opponent_pattern.pop(0)  # Keep only last 5 moves
            
            # Update cooperation/defection counts
            if opponent_action == self.COMPROMISE:
                self.cooperation_count += 1
            else:
                self.defection_count += 1
            
            # State transition logic
            if self.curr_state == 0:  # Initial state
                if opponent_action == self.COMPROMISE:
                    # Opponent cooperated, stay cooperative
                    self.curr_state = 1
                else:
                    # Opponent defected, switch to tit-for-tat
                    self.curr_state = 2
            
            elif self.curr_state == 1:  # Cooperative state
                if opponent_action == self.STUBBORN:
                    # Opponent defected, switch to tit-for-tat
                    self.curr_state = 2
            
            elif self.curr_state == 2:  # Tit-for-tat state
                # Analyze recent pattern
                if len(self.opponent_pattern) >= 3:
                    recent_defections = sum(1 for a in self.opponent_pattern[-3:] if a == self.STUBBORN)
                    if recent_defections >= 2:
                        # Too many recent defections, go defensive
                        self.curr_state = 3
                    elif recent_defections == 0:
                        # All cooperation recently, go back to cooperative
                        self.curr_state = 1
            
            elif self.curr_state == 3:  # Defensive state
                # Check if opponent has been cooperative recently
                if len(self.opponent_pattern) >= 2:
                    recent_cooperations = sum(1 for a in self.opponent_pattern[-2:] if a == self.COMPROMISE)
                    if recent_cooperations >= 2:
                        # Opponent cooperating, try tit-for-tat
                        self.curr_state = 2
    

    
    def get_opponent_last_action(self):
        """Helper method to get opponent's last action (inferred from reward)."""
        if len(self.action_history) == 0:
            return None
        
        my_last_action = self.action_history[-1]
        my_last_reward = self.reward_history[-1]
        
        # This is a simplified inference - in BOSII it's more complex
        # due to mood-dependent payoffs
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
    

    
    def setup(self):
        """Setup the agent for a new game."""
        super().setup()
        # We'll determine player type from the info in update method
        # The engine assigns player IDs based on agent position in the list


# Agent name for submission
name = "BOSIICompetitionAgent"


################### SUBMISSION #####################
agent_submission = BOSIICompetitionAgent(name)
####################################################


if __name__ == "__main__":
    # Configuration variables - modify these as needed
    server = True  # Set to True to connect to server, False for local testing
    name = "hey"  # Agent name
    host = "localhost"  # Server host
    port = 8080  # Server port
    verbose = False  # Enable verbose debug output
    
    if server:
        # Connect to server
        print(f"Starting {name} for bosii game...")
        print(f"Connecting to server at {host}:{port}")
        
        # Add server directory to path for imports
        server_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'server')
        sys.path.insert(0, server_dir)
        
        from client import AGTClient
        from adapters import create_adapter
        
        async def main():
            # Create agent
            agent = BOSIICompetitionAgent(name)
            
            # Create adapter for server communication
            server_agent = create_adapter(agent, "bosii")
            
            # Create client and connect
            client = AGTClient(server_agent, host, port, verbose=verbose)
            await client.connect()
            
            if client.connected:
                print("Connected to server!")
                print("Joining bosii game...")
                
                if await client.join_game("bosii"):
                    print("Joined game successfully!")
                    print("Waiting for tournament to start...")
                    await client.run()
                else:
                    print("Failed to join game")
            else:
                print("Failed to connect to server")
        
        # Run the async main function
        asyncio.run(main())
        
    else:
        # Test your agent locally
        print("Testing BOSII Competition Agent locally...")
        print("=" * 50)
        
        # Import opponent agents for testing
        try:
            from simple_bosii_agent import SimpleBOSIIAgent
        except ImportError:
            print("Note: Simple BOSII agent not found, using random agents instead")
            from core.agents.lab02.random_bos_agent import RandomBOSAgent
            SimpleBOSIIAgent = RandomBOSAgent
        
        # Create agents for testing
        agent = BOSIICompetitionAgent("CompetitionAgent")
        opponent1 = SimpleBOSIIAgent("SimpleBOSIIAgent")
        
        # Create game and run
        game = BOSIIGame(rounds=100)
        agents = [agent, opponent1]
        
        engine = Engine(game, agents, rounds=100)
        final_rewards = engine.run()
        
        print(f"Final rewards: {final_rewards}")
        print(f"Cumulative rewards: {engine.cumulative_reward}")
        
        # Print statistics
        print(f"\n{agent.name} statistics:")
        action_counts = [0, 0]  # Compromise, Stubborn
        for action in agent.action_history:
            action_counts[action] += 1
        
        print(f"Compromise: {action_counts[0]}, Stubborn: {action_counts[1]}")
        print(f"Total reward: {sum(agent.reward_history)}")
        print(f"Average reward: {sum(agent.reward_history) / len(agent.reward_history) if agent.reward_history else 0:.3f}")
        print(f"Final state: {agent.curr_state}")
        print(f"Is row player: {agent.is_row_player()}")
        if agent.mood_history:
            print(f"Mood history: {agent.mood_history}")
        print(f"Cooperation count: {agent.cooperation_count}")
        print(f"Defection count: {agent.defection_count}")
        
        print("\nLocal test completed!") 