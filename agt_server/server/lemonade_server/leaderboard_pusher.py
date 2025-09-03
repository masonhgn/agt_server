import os
import sys
import requests
import json
from typing import Dict, Any

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class LeaderboardPusher:
    def __init__(self, leaderboard_url: str):
        self.leaderboard_url = leaderboard_url
    
    def push_results(self, results: Dict[str, Any]) -> bool:
        """Push results to leaderboard"""
        try:
            print(f"Pushing results to {self.leaderboard_url}")
            print(f"Results: {json.dumps(results, indent=2)}")
            
            response = requests.post(
                self.leaderboard_url,
                json=results,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"Response status: {response.status_code}")
            if response.text:
                print(f"Response: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error pushing to leaderboard: {e}")
            return False
