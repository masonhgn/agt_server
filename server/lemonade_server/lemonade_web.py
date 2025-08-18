import os
import sys

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from flask import Flask, request, jsonify, render_template_string
from lemonade_competition import LemonadeCompetition
import requests

app = Flask(__name__)
competition = LemonadeCompetition()

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lemonade Competition</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ccc; }
        .submission { margin: 10px 0; padding: 10px; background: #f9f9f9; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>Lemonade Stand Competition</h1>
    
    <div class="section">
        <h2>Current Agents ({{ submissions|length }})</h2>
        {% if submissions %}
            {% for student_id, submission in submissions.items() %}
                <div class="submission">
                    <strong>{{ submission.agent_name }}</strong> by {{ student_id }}<br>
                    File: {{ submission.file_path.split('/')[-1] }}<br>
                    Submitted: {{ submission.submitted_at.strftime('%Y-%m-%d %H:%M') }}
                </div>
            {% endfor %}
        {% else %}
            <p>No agents found in agents/ directory.</p>
        {% endif %}
    </div>
    
    <div class="section">
        <h2>Actions</h2>
        <p><a href="/scan">Scan for New Agents</a></p>
        <p><a href="/run_tournament">Run Tournament</a></p>
        <p><a href="/results">View Results</a></p>
        <p><a href="/push_to_leaderboard">Push to Leaderboard</a></p>
    </div>
    
    {% if message %}
        <div class="section">
            <p class="{{ message_type }}">{{ message }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, submissions=competition.submissions)

@app.route('/scan')
def scan_agents():
    new_agents = competition.scan_for_agents()
    message = f"Found {len(new_agents)} new agents" if new_agents else "No new agents found"
    return render_template_string(HTML_TEMPLATE, 
                                submissions=competition.submissions,
                                message=message,
                                message_type="success")

@app.route('/run_tournament')
def run_tournament():
    results = competition.run_tournament()
    competition.save_results()
    return jsonify(results)

@app.route('/results')
def get_results():
    return jsonify(competition.results)

@app.route('/push_to_leaderboard')
def push_to_leaderboard():
    if not competition.results:
        return "No results to push. Run tournament first."
    
    from leaderboard_pusher import LeaderboardPusher
    pusher = LeaderboardPusher("http://localhost:8082/api/results")
    
    if pusher.push_results(competition.results):
        return "Results pushed to leaderboard successfully!"
    else:
        return "Failed to push results to leaderboard"

if __name__ == '__main__':
    print("Lemonade Competition Server starting...")
    print("Web interface available at: http://localhost:8083")
    print("Agents directory: agents/")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=8083, debug=True)
