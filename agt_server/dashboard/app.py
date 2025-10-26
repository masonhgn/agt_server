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
import json
import signal
import psutil
import json
from datetime import datetime
from binary_encoding import decode_message

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
console_history = []  # Persistent console history
server_config = {
    'game_type': 'rps',
    'num_players': 2,
    'port': AGT_SERVER_PORT,
    'host': '0.0.0.0',
}

# Track server state from console output (single-game format)
server_state = {
    'total_players': 0,
    'leaderboard': [],
    'current_game': None,  # Game type as string
    'players': [],  # List of connected players
    'tournament_started': False,
    'current_round': 0,
    'total_rounds': 0
}

def log_console(message):
    """Add message to console output queue with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted_message = f"[{timestamp}] {message}"
    console_output.put(formatted_message)
    console_history.append(formatted_message)  # Add to persistent history


def parse_console_line(line):
    """Parse clean console output to update server state."""
    global server_state
    log_console(f"Parsing console line: {line}")
    # Print ALL console output to dashboard console unconditionally
    if line.strip():  # Only log non-empty lines
        log_console(line)
    
    # Parse binary encoded messages
    if line.startswith("encoded:"):
        message_type, data = decode_message(line)
        
        log_console(f"Decoded - message_type: {message_type}, data: {data}, data type: {type(data)}")
        
        if message_type is None or data is None:
            log_console(f"Failed to decode message: {line}")
            return
        
        if message_type == 'PLAYER_CONNECT':
            try:
                player_name = data['player_name']
                address = data['address']
                
                # Add player if not already present
                if not any(p['name'] == player_name for p in server_state['players']):
                    server_state['players'].append({
                        'name': player_name,
                        'connected_time': datetime.now().strftime('%H:%M:%S')
                    })
                    server_state['total_players'] = len(server_state['players'])
                    log_console(f"Added player {player_name}. Total players: {server_state['total_players']}")
                else:
                    log_console(f"Player {player_name} already exists")
            except Exception as e:
                log_console(f"Error in PLAYER_CONNECT handling: {e}")
                log_console(f"data type: {type(data)}, data: {data}")
                log_console(f"server_state type: {type(server_state)}, server_state: {server_state}")
            








            
        elif message_type == 'PLAYER_DISCONNECT':
            try:
                player_name = data['player_name']
                remaining_count = data['remaining_count']
                
                # Remove player from players list
                server_state['players'] = [
                    p for p in server_state['players'] 
                    if p['name'] != player_name
                ]
                server_state['total_players'] = len(server_state['players'])
                log_console(f"❌ Removed player {player_name}. Remaining: {remaining_count}")
            except Exception as e:
                log_console(f"Error in PLAYER_DISCONNECT handling: {e}")
                log_console(f"data type: {type(data)}, data: {data}")
            
        elif message_type == 'TOURNAMENT_START':
            try:
                game_type = data['game_type']
                player_count = data['player_count']
                
                server_state['tournament_started'] = True
                log_console(f"🏁 Tournament started: {game_type} with {player_count} players")
            except Exception as e:
                log_console(f"Error in TOURNAMENT_START handling: {e}")
                log_console(f"data type: {type(data)}, data: {data}")

            
        elif message_type == 'TOURNAMENT_END':
            try:
                game_type = data['game_type']
                
                server_state['tournament_started'] = False
                server_state['tournament_completed'] = True
                log_console(f"🏁 Tournament ended: {game_type}")
            except Exception as e:
                log_console(f"Error in TOURNAMENT_END handling: {e}")
                log_console(f"data type: {type(data)}, data: {data}")
        
        elif message_type == 'RESULTS_SAVED':
            try:
                filename = data['filename']
                log_console(f"💾 Results saved: {filename}")
            except Exception as e:
                log_console(f"Error in RESULTS_SAVED handling: {e}")
                log_console(f"data type: {type(data)}, data: {data}")
        
        else:
            log_console(f"🔍 Unknown message type: {message_type}")
def start_agt_server(config):
    """Start the AGT server with given configuration."""
    global agt_process, server_state
    
    if agt_process and agt_process.poll() is None:
        log_console("Server is already running")
        return False
    
    # Reset server state for new server (single-game format)
    server_state = {
        'total_players': 0,
        'leaderboard': [],
        'current_game': config['game_type'],
        'players': [],
        'tournament_started': False,
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
                        # Log console output to dashboard console
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
                'tournament_completed': False,
                'leaderboard': [],
                'current_game': None,
                'players': [],
                'tournament_started': False,
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
                'tournament_completed': False,
                'leaderboard': [],
                'current_game': None,
                'players': [],
                'tournament_started': False,
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
        
        # Debug logging
        print(datetime.now().strftime('%H:%M:%S'))
        log_console(f"aPI STATUS CALL: server_running={server_running}, total_players={server_state['total_players']}")
        #log_console(f"SERVER STATE: {server_state}")
        
        # Return status based on parsed console output (single-game format)
        status_data = {
            "server_status": "Running" if server_running else "Stopped",
            "total_players": server_state['total_players'],
            "players": server_state['players'],  # List of connected players
            "leaderboard": server_state['leaderboard'],
            "current_game": server_state['current_game'],  # Game type as string
            "tournament_started": server_state.get('tournament_started', False),
            "config": server_config,
            "current_round": server_state.get('current_round', 0),
            "total_rounds": server_state.get('total_rounds', 0)
        }
        
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
            'tournament_completed': False,
            'leaderboard': [],
            'current_game': server_state['current_game'],  # Keep current game type
            'players': server_state['players'],  # Keep current players
            'tournament_started': False,
            'current_round': 0,
            'total_rounds': 0
        }
        
        log_console("Tournament state reset for restart")
        return jsonify({"success": True, "message": "Tournament state reset"})
    except Exception as e:
        log_console(f"Error restarting tournament: {e}")
        return jsonify({"success": False, "error": f"Failed to restart: {str(e)}"})

@app.route('/api/config')
def get_config():
    """Get current server configuration."""
    return jsonify(server_config)

@app.route('/api/console')
def get_console():
    """Get console output as Server-Sent Events."""
    def generate():
        # First, send all historical messages
        if console_history:
            data = json.dumps({"messages": console_history, "historical": True})
            yield f"data: {data}\n\n"
        
        while True:
            try:
                # Get all available console messages
                messages = []
                while not console_output.empty():
                    messages.append(console_output.get_nowait())
                
                if messages:
                    data = json.dumps({"messages": messages, "historical": False})
                    yield f"data: {data}\n\n"
                
                time.sleep(0.5)  # Check every 500ms
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/clear_console', methods=['POST'])
def clear_console():
    """Clear console output."""
    global console_output, console_history
    console_output = queue.Queue()
    console_history = []  # Clear persistent history too
    return jsonify({"success": True})

if __name__ == '__main__':
    print(f"AGT Dashboard starting on port {DASHBOARD_PORT}")
    print(f"Will control AGT server at {AGT_SERVER_HOST}:{AGT_SERVER_PORT}")
    print(f"Dashboard URL: http://localhost:{DASHBOARD_PORT}")
    app.run(host='0.0.0.0', port=DASHBOARD_PORT, debug=False)
