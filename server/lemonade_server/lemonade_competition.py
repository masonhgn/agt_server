import os
import json
import importlib.util
import random
import sys
from datetime import datetime
from typing import Dict, List, Any

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
        
        # Create game
        game = LemonadeGame(rounds=rounds)
        
        # Run the game
        engine = Engine(game, agents)
        final_rewards = engine.run()
        
        return final_rewards
    
    def save_results(self, filename: str = None):
        """Save results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/lemonade_results_{timestamp}.json"
        
        os.makedirs("results", exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Results saved to {filename}")
