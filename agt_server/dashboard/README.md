# AGT Server Dashboard

A Flask-based web dashboard for **monitoring and controlling** the AGT tournament server in real-time.

## Features

- **🚀 Complete Server Control**: Start, stop, and configure the AGT server directly from the dashboard
- **⚙️ Configuration Management**: Set game type, port, rounds, and players per game
- **📺 Live Console Output**: Real-time server console output with timestamps
- **📊 Real-time monitoring** of server status and player connections
- **🔄 Auto-refresh** every second (can be disabled)
- **🎮 Game-specific views** showing tournament status and connected players
- **👥 Player tracking** with connection times
- **🏆 Live leaderboard** with real-time updates
- **🎯 Tournament controls** (start, restart)
- **💻 Clean, modern interface** that works on desktop and mobile

## Architecture

This dashboard is now a **complete control center** that:

- **Spawns and manages** the AGT server process
- **Captures console output** in real-time
- **Provides configuration interface** for server settings
- **Monitors server health** and player activity
- **Controls tournament execution**

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Start the Dashboard

```bash
# Basic usage (will control server on localhost:8080)
python app.py

# Custom configuration
AGT_SERVER_HOST=192.168.1.100 AGT_SERVER_PORT=8080 DASHBOARD_PORT=8081 python app.py
```

### Environment Variables

- `AGT_SERVER_HOST`: AGT server hostname (default: localhost)
- `AGT_SERVER_PORT`: AGT server port (default: 8080)
- `DASHBOARD_PORT`: Dashboard port (default: 8081)

### Access Dashboard

Once running, open your web browser and go to:

```
http://localhost:8081
```

## Dashboard Features

### Server Management
- **Start Server**: Launch AGT server with current configuration
- **Stop Server**: Gracefully shutdown the server
- **Configuration**: Set game type, port, rounds, and players per game
- **Live Console**: Real-time server output with timestamps

### Server Status
- Server uptime and health
- Total connected players
- Active games count
- Process status monitoring

### Game Configuration
Configure server settings:
- **Game Type**: RPS, BOS, Chicken, Lemonade, Auction, ADX
- **Server Port**: Custom port for the AGT server
- **Rounds per Tournament**: Number of rounds to play
- **Players per Game**: How many players in each game

### Live Console Output
- **Real-time server logs** with timestamps
- **Process monitoring** and error detection
- **Clear console** functionality
- **Auto-scrolling** to latest output

### Tournament Controls
- **Start Tournament**: Begin tournaments for all available games
- **Restart Tournament**: Reset all player stats and restart

### Live Leaderboard
- Real-time rankings based on total reward
- Player statistics (games played, average reward)
- Updates live as games are played

### Real-time Updates
- Dashboard automatically refreshes every second
- Toggle auto-refresh on/off with the checkbox
- Manual refresh button available

## API Endpoints

The dashboard provides these endpoints:

- `GET /api/status` - Get server status and player data
- `POST /api/start_server` - Start AGT server with configuration
- `POST /api/stop_server` - Stop the AGT server
- `POST /api/update_config` - Update server configuration
- `POST /api/start_tournament` - Start tournaments
- `POST /api/restart_tournament` - Restart tournaments
- `GET /api/console` - Server-Sent Events stream for console output
- `POST /api/clear_console` - Clear console output

## Workflow

### Typical Usage

1. **Start Dashboard**: `python app.py`
2. **Configure Server**: Set game type, port, etc.
3. **Start Server**: Click "Start Server" button
4. **Monitor Console**: Watch real-time server output
5. **Wait for Players**: Monitor player connections
6. **Start Tournament**: Click "Start Tournament" when ready
7. **Monitor Results**: Watch live leaderboard updates
8. **Stop Server**: Click "Stop Server" when done

### Server Control

The dashboard now **completely manages** the AGT server:

- **Process Management**: Spawns and monitors the server process
- **Output Capture**: Captures all console output in real-time
- **Graceful Shutdown**: Properly terminates the server process
- **Configuration**: Passes all settings to the server
- **Health Monitoring**: Detects if server crashes or stops

## Troubleshooting

### Server Won't Start
1. Check console output for error messages
2. Verify Python path and dependencies
3. Ensure port is not already in use
4. Check file permissions

### Console Not Updating
1. Refresh the dashboard page
2. Check browser console for JavaScript errors
3. Verify EventSource support in browser

### Connection Issues
- Check firewall settings
- Ensure both services are running on expected ports
- Verify network connectivity

## Development

### Adding New Features
1. Update the Flask routes in `app.py`
2. Modify the HTML template in `templates/dashboard.html`
3. Add any new CSS styles to the `<style>` section
4. Update JavaScript functions as needed

### Process Management
The dashboard uses `subprocess.Popen` to manage the AGT server:
- Captures stdout/stderr for console output
- Monitors process health
- Handles graceful shutdown
- Restarts on failure (if implemented)

### Deployment
For production deployment, consider using:
- **Gunicorn** as the WSGI server
- **Nginx** as a reverse proxy
- **Docker** for containerization
- **Systemd** for process management

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8081 app:app
```

## Security Considerations

- **Process Isolation**: Server runs as separate process
- **Port Configuration**: Can bind to specific interfaces
- **Graceful Shutdown**: Proper cleanup on stop
- **Error Handling**: Comprehensive error reporting
