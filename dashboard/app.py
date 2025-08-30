#!/usr/bin/env python3
"""
AGT Server Dashboard - Flask Application

A web-based dashboard for monitoring and controlling the AGT tournament server in real-time.
"""

from flask import Flask, render_template, jsonify, request, Response
import requests
import time
import os
import sys
import subprocess
import threading
import queue
import signal
import psutil
import json
from datetime import datetime

# Add the parent directory to the path to import server modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__)

# Configuration
AGT_SERVER_HOST = os.environ.get('AGT_SERVER_HOST', 'localhost')
AGT_SERVER_PORT = int(os.environ.get('AGT_SERVER_PORT', '8080'))
DASHBOARD_PORT = int(os.environ.get('DASHBOARD_PORT', '8081'))

# Global state
agt_process = None
console_output = queue.Queue()
server_config = {
    'game_type': 'rps',
    'num_rounds': 100,  # Default for RPS
    'num_players': 2,
    'port': AGT_SERVER_PORT,
    'host': '0.0.0.0'
}

# Track server state from console output
server_state = {
    'total_players': 0,
    'active_games': 0,
    'total_tournaments': 0,
    'active_tournaments': 0,
    'tournament_completed': False,
    'leaderboard': [],
    'games': {},
    'uptime': 'N/A',
    'current_round': 0,
    'total_rounds': 0
}

def log_console(message):
    """Add message to console output queue with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    console_output.put(f"[{timestamp}] {message}")

def parse_console_line(line):
    """Parse console output to update server state."""
    global server_state
    # log_console(f"🔍 PARSING LINE: {line}")
    
    # Simple test - log every line that contains "Player"
    # if "Player" in line:
    #     log_console(f"LINE CONTAINS 'Player': {line}")  # Commented out debug output
    
    # Parse player connections
    if "Player" in line and "joined" in line and "game!" in line:
        # log_console(f"FOUND PLAYER JOIN LINE: {line}")  # Commented out debug output
        # log_console(f"MATCHING PATTERN: Found player join line")  # Commented out debug output
        # Example: "Player CompetitionAgent joined rps game! (1 players total)"
        import re
        match = re.search(r'Player ([^ ]+) joined (\w+) game! \((\d+) players total\)', line)
        if match:
            player_name = match.group(1)
            game_type = match.group(2)
            player_count = int(match.group(3))
            
            # log_console(f"PARSED: Player {player_name} joined {game_type} game! ({player_count} players total)")  # Commented out debug output
            
            # Update server state
            if game_type not in server_state['games']:
                # Use appropriate defaults based on game type
                game_defaults = {
                    'rps': {'num_players': 2, 'num_rounds': 100},
                    'bos': {'num_players': 2, 'num_rounds': 100},
                    'bosii': {'num_players': 2, 'num_rounds': 100},
                    'chicken': {'num_players': 2, 'num_rounds': 100},
                    'pd': {'num_players': 2, 'num_rounds': 100},
                    'lemonade': {'num_players': 3, 'num_rounds': 100},
                    'auction': {'num_players': 4, 'num_rounds': 10},
                    'adx_twoday': {'num_players': 2, 'num_rounds': 2},
                    'adx_oneday': {'num_players': 2, 'num_rounds': 1}
                }
                
                defaults = game_defaults.get(game_type, {'num_players': 2, 'num_rounds': 100})
                
                server_state['games'][game_type] = {
                    'name': game_type.upper(),
                    'players': [],
                    'config': defaults,
                    'tournament_started': False
                }
            
            # Add player if not already present
            if not any(p['name'] == player_name for p in server_state['games'][game_type]['players']):
                server_state['games'][game_type]['players'].append({
                    'name': player_name,
                    'connected_time': 'now'
                })
                # log_console(f"ADDED: Player {player_name} to {game_type} game")  # Commented out debug output
            else:
                # log_console(f"SKIPPED: Player {player_name} already in {game_type} game")  # Commented out debug output
                pass
            
            server_state['total_players'] = sum(len(game['players']) for game in server_state['games'].values())
            server_state['active_games'] = len([g for g in server_state['games'].values() if g['players']])
            
            # log_console(f"UPDATED: Total players = {server_state['total_players']}, Active games = {server_state['active_games']}")  # Commented out debug output
        else:
            # log_console(f"PARSE FAILED: Could not parse line: {line}")  # Commented out debug output
            # log_console(f"REGEX TEST: Looking for pattern in: {repr(line)}")  # Commented out debug output
            pass
    
    # Parse player disconnections
    elif "Player" in line and "disconnected from" in line and "players remaining" in line:
        # Example: "Player CompetitionAgent disconnected from rps game! (0 players remaining)"
        import re
        match = re.search(r'Player ([^ ]+) disconnected from (\w+) game! \((\d+) players remaining\)', line)
        if match:
            player_name = match.group(1)
            game_type = match.group(2)
            remaining_count = int(match.group(3))
            
            if game_type in server_state['games']:
                # Remove player
                server_state['games'][game_type]['players'] = [
                    p for p in server_state['games'][game_type]['players'] 
                    if p['name'] != player_name
                ]
                
                server_state['total_players'] = sum(len(game['players']) for game in server_state['games'].values())
                server_state['active_games'] = len([g for g in server_state['games'].values() if g['players']])
    
    # Parse tournament starts
    elif "Starting tournament for" in line and "players!" in line:
        # Example: "Starting tournament for rps with 2 players!"
        import re
        match = re.search(r'Starting tournament for (\w+) with (\d+) players!', line)
        if match:
            game_type = match.group(1)
            player_count = int(match.group(2))
            
            log_console(f"TOURNAMENT STARTED: {game_type} with {player_count} players")
            
            if game_type in server_state['games']:
                server_state['games'][game_type]['tournament_started'] = True
                server_state['active_tournaments'] += 1
                server_state['total_tournaments'] += 1
                # Initialize round counter
                if 'current_round' not in server_state:
                    server_state['current_round'] = 0
    
    # Parse round updates
    elif "TOURNAMENT ROUND" in line:
        # Example: "TOURNAMENT ROUND 1/1000"
        import re
        match = re.search(r'TOURNAMENT ROUND (\d+)/(\d+)', line)
        if match:
            current_round = int(match.group(1))
            total_rounds = int(match.group(2))
            server_state['current_round'] = current_round
            server_state['total_rounds'] = total_rounds
            log_console(f"ROUND UPDATE: {current_round}/{total_rounds}")
    
    # Parse tournament completion
    elif "TOURNAMENT" in line and "ended" in line:
        # Example: "TOURNAMENT rps ended."
        import re
        match = re.search(r'TOURNAMENT (\w+) ended', line)
        if match:
            game_type = match.group(1)
            log_console(f"TOURNAMENT COMPLETED: {game_type}")
            
            if game_type in server_state['games']:
                server_state['games'][game_type]['tournament_started'] = False
                server_state['active_tournaments'] = max(0, server_state['active_tournaments'] - 1)
                server_state['tournament_completed'] = True
                server_state['current_round'] = server_state.get('total_rounds', 0)
    
    # Parse results saved (tournament completion)
    elif "Results saved to" in line:
        log_console("TOURNAMENT RESULTS SAVED")
        server_state['tournament_completed'] = True
        server_state['active_tournaments'] = 0
    
    # Parse final leaderboard
    elif "FINAL LEADERBOARD for" in line:
        # Example: "FINAL LEADERBOARD for rps:"
        import re
        match = re.search(r'FINAL LEADERBOARD for (\w+):', line)
        if match:
            game_type = match.group(1)
            log_console(f"FINAL LEADERBOARD START: {game_type}")
            # The leaderboard entries will follow in subsequent lines
    
    # Parse leaderboard entries
    elif line.strip().startswith("#") and ":" in line and ("Total:" in line or "Games:" in line):
        # Example: "  #1: CompetitionAgent - Total: 45.20, Games: 50, Avg: 0.90"
        import re
        # match = re.search(r'#(\d+): (\w+) - Total: ([\d.]+), Games: (\d+), Avg: ([\d.]+)', line.strip())
        match = re.search(r'#\s*(\d+):\s+(.+?)\s+-\s+Total:\s+([+-]?\d+(?:\.\d+)?),\s+Games:\s+(\d+),\s+Avg:\s+([+-]?\d+(?:\.\d+)?)',
        line.strip())
        if match:
            rank = int(match.group(1))
            player_name = match.group(2)
            total_reward = float(match.group(3))
            games_played = int(match.group(4))
            avg_reward = float(match.group(5))
            
            # Add to leaderboard
            leaderboard_entry = {
                'name': player_name,
                'rank': rank,
                'total_reward': total_reward,
                'games_played': games_played,
                'avg_reward': avg_reward
            }
            
            # Update or add to leaderboard
            existing_index = next((i for i, entry in enumerate(server_state['leaderboard']) 
                                 if entry['name'] == player_name), None)
            if existing_index is not None:
                server_state['leaderboard'][existing_index] = leaderboard_entry
            else:
                server_state['leaderboard'].append(leaderboard_entry)
            
            # Sort leaderboard by total reward (descending)
            server_state['leaderboard'].sort(key=lambda x: x['total_reward'], reverse=True)
            
            log_console(f"LEADERBOARD ENTRY: #{rank} {player_name} - {total_reward:.2f} points")

def start_agt_server(config):
    """Start the AGT server with given configuration."""
    global agt_process, server_state
    
    if agt_process and agt_process.poll() is None:
        log_console("Server is already running")
        return False
    
    # Reset server state for new server
    server_state = {
        'total_players': 0,
        'active_games': 0,
        'total_tournaments': 0,
        'active_tournaments': 0,
        'tournament_completed': False,
        'leaderboard': [],
        'games': {},
        'uptime': 'N/A',
        'current_round': 0,
        'total_rounds': 0
    }
    
    try:
        # Build command
        cmd = [
            sys.executable,  # Use current Python interpreter
            os.path.join(os.path.dirname(__file__), '..', 'server', 'server.py'),
            '--game', config['game_type'],
            '--port', str(config['port']),
            '--host', config['host']
        ]
        
        log_console(f"Starting AGT server with command: {' '.join(cmd)}")
        
        # Start process with output capture
        # log_console(f"Starting subprocess with command: {' '.join(cmd)}")  # Commented out debug output
        agt_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,  # Unbuffered output
            universal_newlines=True
        )
        # log_console(f"Subprocess started with PID: {agt_process.pid}")  # Commented out debug output
        
        # Start output monitoring thread
        def monitor_output():
            # log_console("MONITOR OUTPUT: Starting output monitoring thread")  # Commented out debug output
            line_count = 0
            while agt_process and agt_process.poll() is None:
                try:
                    line = agt_process.stdout.readline()
                    if line:
                        line_text = line.strip()
                        line_count += 1
                        # log_console(f"RAW OUTPUT #{line_count}: {line_text}")  # Commented out debug output
                        # Parse console output to update server state
                        parse_console_line(line_text)
                    else:
                        # No output available, sleep briefly
                        time.sleep(0.1)
                        # Log every 10 seconds to show we're still monitoring
                        if line_count == 0 and int(time.time()) % 10 == 0:
                            log_console(f"Still monitoring... (no output yet, line_count={line_count})")
                except Exception as e:
                    log_console(f"Error reading output: {e}")
                    break
            if agt_process:
                return_code = agt_process.poll()
                log_console(f"Server process exited with code {return_code}")
        
        monitor_thread = threading.Thread(target=monitor_output, daemon=True)
        monitor_thread.start()
        
        # Wait a moment to see if it starts successfully
        time.sleep(2)
        if agt_process.poll() is None:
            log_console("AGT server started successfully")
            return True
        else:
            log_console("Failed to start AGT server")
            return False
            
    except Exception as e:
        log_console(f"Error starting server: {str(e)}")
        return False

def stop_agt_server():
    """Stop the AGT server gracefully."""
    global agt_process, server_state
    
    if not agt_process or agt_process.poll() is not None:
        log_console("Server is not running")
        return False
    
    try:
        log_console("Stopping AGT server...")
        
        # Try graceful shutdown first
        agt_process.terminate()
        
        # Wait for graceful shutdown
        try:
            agt_process.wait(timeout=5)
            log_console("Server stopped gracefully")
            # Reset server state
            server_state = {
                'total_players': 0,
                'active_games': 0,
                'total_tournaments': 0,
                'active_tournaments': 0,
                'tournament_completed': False,
                'leaderboard': [],
                'games': {},
                'uptime': 'N/A',
                'current_round': 0,
                'total_rounds': 0
            }
            return True
        except subprocess.TimeoutExpired:
            # Force kill if graceful shutdown fails
            log_console("Force killing server...")
            agt_process.kill()
            agt_process.wait()
            log_console("Server force killed")
            # Reset server state
            server_state = {
                'total_players': 0,
                'active_games': 0,
                'total_tournaments': 0,
                'active_tournaments': 0,
                'tournament_completed': False,
                'leaderboard': [],
                'games': {},
                'uptime': 'N/A',
                'current_round': 0,
                'total_rounds': 0
            }
            return True
            
    except Exception as e:
        log_console(f"Error stopping server: {str(e)}")
        return False

def get_server_status():
    """Get current server status."""
    global agt_process
    
    if agt_process and agt_process.poll() is None:
        return "Running"
    else:
        return "Stopped"

@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """Get server status and configuration."""
    try:
        # Check if our server is running
        server_running = agt_process and agt_process.poll() is None
        
        # Debug logging (commented out to reduce noise)
        # log_console(f"🔍 API STATUS CALL: server_running={server_running}, total_players={server_state['total_players']}")
        # log_console(f"🔍 SERVER STATE: {server_state}")
        
        # Return status based on parsed console output
        status_data = {
            "server_status": "Running" if server_running else "Stopped",
            "server_controlled": True,
            "uptime": server_state['uptime'],
            "total_players": server_state['total_players'],
            "active_games": server_state['active_games'],
            "total_tournaments": server_state['total_tournaments'],
            "active_tournaments": server_state['active_tournaments'],
            "tournament_completed": server_state['tournament_completed'],
            "leaderboard": server_state['leaderboard'],
            "games": server_state['games'],
            "config": server_config,
            "current_round": server_state.get('current_round', 0),
            "total_rounds": server_state.get('total_rounds', 0)
        }
        
        # log_console(f"📤 SENDING STATUS: {status_data}")
        return jsonify(status_data)
        
    except Exception as e:
        log_console(f"STATUS ERROR: {str(e)}")
        return jsonify({
            "error": f"Dashboard error: {str(e)}",
            "server_status": "Error",
            "server_controlled": True,
            "config": server_config
        })

@app.route('/api/start_server', methods=['POST'])
def start_server():
    """Start the AGT server with configuration."""
    try:
        config = request.json or server_config
        success = start_agt_server(config)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stop_server', methods=['POST'])
def stop_server():
    """Stop the AGT server."""
    try:
        success = stop_agt_server()
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/update_config', methods=['POST'])
def update_config():
    """Update server configuration."""
    global server_config
    try:
        new_config = request.json
        server_config.update(new_config)
        log_console(f"Configuration updated: {new_config}")
        return jsonify({"success": True, "config": server_config})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/start_tournament', methods=['POST'])
def start_tournament():
    """Start tournaments via AGT server."""
    if not (agt_process and agt_process.poll() is None):
        return jsonify({"success": False, "error": "Server is not running"})
    
    try:
        # Send SIGTSTP (Ctrl+Z) to the AGT server process to start tournaments
        agt_process.send_signal(signal.SIGTSTP)
        log_console("Sent SIGTSTP signal to start tournaments")
        return jsonify({"success": True, "message": "Tournament start signal sent"})
    except Exception as e:
        log_console(f"Error sending tournament start signal: {e}")
        return jsonify({"success": False, "error": f"Failed to send signal: {str(e)}"})

@app.route('/api/restart_tournament', methods=['POST'])
def restart_tournament():
    """Restart tournaments via AGT server."""
    if not (agt_process and agt_process.poll() is None):
        return jsonify({"success": False, "error": "Server is not running"})
    
    try:
        # Reset server state for restart
        global server_state
        server_state = {
            'total_players': server_state['total_players'],  # Keep current players
            'active_games': server_state['active_games'],
            'total_tournaments': 0,
            'active_tournaments': 0,
            'tournament_completed': False,
            'leaderboard': [],
            'games': server_state['games'],  # Keep current games
            'current_round': 0,
            'total_rounds': 0
        }
        
        # Reset tournament_started flag for all games
        for game in server_state['games'].values():
            game['tournament_started'] = False
        
        log_console("Tournament state reset for restart")
        return jsonify({"success": True, "message": "Tournament state reset"})
    except Exception as e:
        log_console(f"Error restarting tournament: {e}")
        return jsonify({"success": False, "error": f"Failed to restart: {str(e)}"})

@app.route('/api/console')
def get_console():
    """Get console output as Server-Sent Events."""
    def generate():
        while True:
            try:
                # Get all available console messages
                messages = []
                while not console_output.empty():
                    messages.append(console_output.get_nowait())
                
                if messages:
                    data = json.dumps({"messages": messages})
                    yield f"data: {data}\n\n"
                
                time.sleep(0.5)  # Check every 500ms
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/clear_console', methods=['POST'])
def clear_console():
    """Clear console output."""
    global console_output
    console_output = queue.Queue()
    return jsonify({"success": True})

if __name__ == '__main__':
    print(f"AGT Dashboard starting on port {DASHBOARD_PORT}")
    print(f"Will control AGT server at {AGT_SERVER_HOST}:{AGT_SERVER_PORT}")
    print(f"Dashboard URL: http://localhost:{DASHBOARD_PORT}")
    app.run(host='0.0.0.0', port=DASHBOARD_PORT, debug=False)
