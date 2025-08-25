import os
import json
import importlib.util
import random
import sys
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.game.LemonadeGame import LemonadeGame
from core.engine import Engine
from server.adapters import create_adapter

class AgentSubmission:
    """Simple container for a submitted agent"""
    def __init__(self, student_id: str, file_path: str, agent_name: str):
        self.student_id = student_id
        self.file_path = file_path
        self.agent_name = agent_name
        self.submitted_at = datetime.now()
        self.agent = None  # Will be loaded agent instance

class LemonadeCompetition:
    """Main class to handle the entire lemonade competition"""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = agents_dir
        self.submissions: Dict[str, AgentSubmission] = {}
        self.results = {}
        self.game_log = []  # Store detailed game logs
        self.game_counter = 0  # Track game numbers
        os.makedirs(agents_dir, exist_ok=True)
    
    def scan_for_agents(self) -> List[AgentSubmission]:
        """Scan the agents directory for new agent files"""
        new_submissions = []
        
        for filename in os.listdir(self.agents_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                file_path = os.path.join(self.agents_dir, filename)
                
                # Extract student_id and agent_name from filename
                # Expected format: student_id_agent_name.py
                name_parts = filename[:-3].split('_', 1)  # Remove .py and split on first _
                if len(name_parts) >= 2:
                    student_id = name_parts[0]
                    agent_name = name_parts[1]
                else:
                    # Fallback: use filename as agent_name, student_id as "unknown"
                    student_id = "unknown"
                    agent_name = filename[:-3]
                
                # Check if this is a new submission
                if student_id not in self.submissions:
                    submission = AgentSubmission(student_id, file_path, agent_name)
                    self.submissions[student_id] = submission
                    new_submissions.append(submission)
                    print(f"Found new agent: {agent_name} from {student_id}")
        
        return new_submissions
    
    def load_all_agents(self) -> List[AgentSubmission]:
        """Load all agents from the agents directory and return valid ones"""
        # First scan for any new agents
        self.scan_for_agents()
        
        valid_submissions = []
        
        for student_id, submission in self.submissions.items():
            try:
                # Load agent from file
                agent = self._load_agent_from_file(submission.file_path, submission.agent_name)
                if agent:
                    submission.agent = agent
                    valid_submissions.append(submission)
                    print(f"Loaded agent: {submission.agent_name} from {student_id}")
                else:
                    print(f"Failed to load agent from {student_id}")
            except Exception as e:
                print(f"Error loading agent from {student_id}: {e}")
        
        return valid_submissions
    
    def _load_agent_from_file(self, file_path: str, agent_name: str):
        """Load agent from Python file"""
        try:
            # Import the file
            spec = importlib.util.spec_from_file_location("agent_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for agent_submission
            if hasattr(module, 'agent_submission'):
                agent = module.agent_submission
                # Create adapter for lemonade game
                return create_adapter(agent, "lemonade")
            else:
                print(f"No agent_submission found in {file_path}")
                return None
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def run_tournament(self, num_competitions: int = 10, rounds_per_comp: int = 100) -> Dict[str, Any]:
        """Run tournament and return results"""
        valid_submissions = self.load_all_agents()
        
        if len(valid_submissions) < 3:
            print("Need at least 3 agents to run tournament")
            return {}
        
        # Track scores
        scores = {sub.agent_name: 0.0 for sub in valid_submissions}
        games_played = {sub.agent_name: 0 for sub in valid_submissions}
        
        print(f"Running tournament with {len(valid_submissions)} agents")
        
        for comp_num in range(num_competitions):
            print(f"Competition {comp_num + 1}/{num_competitions}")
            
            # Randomly select 3 agents for this competition
            selected_agents = random.sample(valid_submissions, 3)
            
            # Run the competition
            comp_results = self._run_single_competition(selected_agents, rounds_per_comp)
            
            # Update scores
            for i, submission in enumerate(selected_agents):
                scores[submission.agent_name] += comp_results[i]
                games_played[submission.agent_name] += 1
        
        # Calculate averages
        final_scores = {}
        for name in scores:
            if games_played[name] > 0:
                final_scores[name] = scores[name] / games_played[name]
        
        # Create rankings
        rankings = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results for leaderboard
        results = {
            "timestamp": datetime.now().isoformat(),
            "rankings": [{"name": name, "score": score} for name, score in rankings],
            "scores": final_scores,
            "metadata": {
                "total_agents": len(valid_submissions),
                "competitions_run": num_competitions,
                "rounds_per_competition": rounds_per_comp
            }
        }
        
        self.results = results
        return results
    
    def _run_single_competition(self, submissions: List[AgentSubmission], rounds: int) -> List[float]:
        """Run one competition between 3 agents"""
        agents = [sub.agent for sub in submissions]
        agent_names = [sub.agent_name for sub in submissions]
        
        # Increment game counter
        self.game_counter += 1
        
        # Create game
        game = LemonadeGame(rounds=rounds)
        
        # Track detailed game information
        game_info = {
            "game_number": self.game_counter,
            "agents": agent_names,
            "rounds": rounds,
            "agent_actions": {name: defaultdict(int) for name in agent_names},
            "agent_utilities": {name: 0.0 for name in agent_names}
        }
        
        # Run the game with custom logging
        final_rewards = self._run_game_with_logging(game, agents, agent_names, game_info)
        
        # Add final statistics to game info
        for i, name in enumerate(agent_names):
            game_info["agent_utilities"][name] = final_rewards[i]
        
        # Add game info to log
        self.game_log.append(game_info)
        
        # Print game summary
        self._print_game_summary(game_info)
        
        return final_rewards
    
    def _run_game_with_logging(self, game: LemonadeGame, agents: List, agent_names: List[str], game_info: Dict) -> List[float]:
        """Run a game while logging detailed information"""
        # Reset the game
        obs = game.reset()
        
        # Reset all agents and call setup
        for agent in agents:
            agent.reset()
            agent.setup()
        
        # Run the game
        for round_num in range(game.rounds):
            # Get actions from all agents
            actions = {}
            for i, agent in enumerate(agents):
                agent_obs = obs.get(i, {})
                action = self._get_agent_action(agent, agent_obs)
                actions[i] = action
                agent.action_history.append(action)
                
                # Log the action
                game_info["agent_actions"][agent_names[i]][action] += 1
            
            # Step the game
            obs, rewards, done, info = game.step(actions)
            
            # Update agents with results
            for i, agent in enumerate(agents):
                reward = rewards.get(i, 0)
                agent_info = info.get(i, {})
                agent.update(reward, agent_info)
            
            # Check if game is done
            if done:
                break
        
        return [rewards.get(i, 0) for i in range(len(agents))]
    
    def _get_agent_action(self, agent, obs):
        """Get action from agent using the appropriate method"""
        # Check if this is a Lab 1 agent by looking for the specific method implementations
        if hasattr(agent, 'predict') and hasattr(agent, 'optimize') and hasattr(agent, 'calc_move_probs'):
            # This is a Lab 1 agent - use the new architecture
            if hasattr(agent, '_is_fictitious_play') and agent._is_fictitious_play:
                # Fictitious Play agent: call predict() then optimize()
                dist = agent.predict()
                action = agent.optimize(dist)
            elif hasattr(agent, '_is_exponential_weights') and agent._is_exponential_weights:
                # Exponential Weights agent: call calc_move_probs() then sample
                move_probs = agent.calc_move_probs()
                action = random.choices(agent.actions, weights=move_probs, k=1)[0]
            else:
                # Default: use get_action() for backward compatibility
                action = agent.get_action(obs)
        else:
            # Regular agent: use get_action()
            action = agent.get_action(obs)
        
        return action
    
    def _print_game_summary(self, game_info: Dict):
        """Print a summary of the game results"""
        print(f"Game {game_info['game_number']}:")
        print(f"I am currently playing against {' and '.join(game_info['agents'])}")
        
        for agent_name in game_info['agents']:
            actions = game_info['agent_actions'][agent_name]
            total_utility = game_info['agent_utilities'][agent_name]
            avg_utility = total_utility / game_info['rounds'] if game_info['rounds'] > 0 else 0
            
            # Format location choices
            location_str = ", ".join([f"Location {loc} {count} times" for loc, count in sorted(actions.items())])
            
            print(f"{agent_name}: set up their Lemonade Stand at {location_str}.")
            print(f"{agent_name}: got a total utility of {total_utility:.0f} and a average utility of {avg_utility:.2f}")
    
    def save_results(self, filename: str = None):
        """Save results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/lemonade_results_{timestamp}.json"
        
        os.makedirs("results", exist_ok=True)
        
        # Include game logs in results
        results_with_logs = {
            **self.results,
            "game_logs": self.game_log
        }
        
        with open(filename, 'w') as f:
            json.dump(results_with_logs, f, indent=2)
        
        print(f"Results saved to {filename}")
    
    def save_game_log(self, filename: str = None):
        """Save just the game log to a separate file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/lemonade_game_log_{timestamp}.txt"
        
        os.makedirs("results", exist_ok=True)
        
        with open(filename, 'w') as f:
            for game_info in self.game_log:
                f.write(f"Game {game_info['game_number']}:\n")
                f.write(f"I am currently playing against {' and '.join(game_info['agents'])}\n")
                
                for agent_name in game_info['agents']:
                    actions = game_info['agent_actions'][agent_name]
                    total_utility = game_info['agent_utilities'][agent_name]
                    avg_utility = total_utility / game_info['rounds'] if game_info['rounds'] > 0 else 0
                    
                    # Format location choices
                    location_str = ", ".join([f"Location {loc} {count} times" for loc, count in sorted(actions.items())])
                    
                    f.write(f"{agent_name}: set up their Lemonade Stand at {location_str}.\n")
                    f.write(f"{agent_name}: got a total utility of {total_utility:.0f} and a average utility of {avg_utility:.2f}\n")
                
                f.write("\n")
        
        print(f"Game log saved to {filename}")
