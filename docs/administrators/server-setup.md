# Server Setup for Administrators

This guide covers setting up and managing the AGT server for instructors and teaching assistants.

## System Overview

The AGT server is a Python-based game engine that manages student competitions across multiple game theory labs. It handles client connections, game execution, tournament management, and results collection.

## Prerequisites

### System Requirements
- **Python 3.8+** (3.13 recommended)
- **Network access** for student connections
- **Storage space** for results and logs
- **Memory:** 2GB+ RAM for concurrent games

### Dependencies
```bash
pip install -r requirements.txt
```

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd agt_server_new
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Server
Create a configuration file `server_config.json`:
```json
{
    "host": "0.0.0.0",
    "port": 8080,
    "allowed_games": ["rps", "bos", "chicken", "lemonade", "auction"],
    "max_players": 50,
    "game_timeout": 300,
    "results_dir": "results"
}
```

## Starting the Server

### Basic Start
```bash
python server/server.py
```

### With Configuration
```bash
python server/server.py --config server_config.json
```

### Production Deployment
```bash
# Using systemd service
sudo systemctl start agt-server

# Using screen for background
screen -S agt-server python server/server.py
```

## Configuration Options

### Network Settings
- **host**: Server IP (0.0.0.0 for all interfaces)
- **port**: Server port (default: 8080)
- **max_connections**: Maximum concurrent connections

### Game Settings
- **allowed_games**: List of enabled game types
- **game_timeout**: Maximum time per game (seconds)
- **rounds_per_game**: Default rounds per game

### Tournament Settings
- **tournament_mode**: Enable tournament brackets
- **match_timeout**: Time limit per match
- **results_format**: CSV, JSON, or both

## Monitoring

### Log Files
```bash
# View server logs
tail -f logs/server.log

# View error logs
tail -f logs/error.log
```

### Server Status
```bash
# Check if server is running
ps aux | grep server.py

# Check network connections
netstat -an | grep 8080
```

### Performance Monitoring
```bash
# Monitor CPU and memory
htop

# Monitor network traffic
iftop
```

## Managing Tournaments

### Start Tournament
```bash
# Start tournament mode
python server/server.py --tournament

# With specific configuration
python server/server.py --tournament --config tournament_config.json
```

### Tournament Configuration
```json
{
    "tournament": {
        "type": "round_robin",
        "games_per_match": 3,
        "timeout": 600,
        "brackets": true
    }
}
```

### Results Collection
```bash
# Export results
python tools/export_results.py --format csv

# Generate reports
python tools/generate_report.py --output report.html
```

## Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check Python version
python --version

# Check dependencies
pip list | grep -E "(numpy|pandas|asyncio)"

# Check port availability
netstat -an | grep 8080
```

#### Client Connection Issues
```bash
# Check firewall settings
sudo ufw status

# Test network connectivity
telnet localhost 8080
```

#### Game Execution Errors
```bash
# Check game configurations
python -c "from core.game.RPSGame import RPSGame; print('RPS OK')"

# Test individual games
python tests/test_games.py
```

### Debug Mode
```bash
# Enable debug logging
python server/server.py --debug

# Verbose output
python server/server.py --verbose
```

## Security Considerations

### Network Security
- **Firewall**: Configure to allow only necessary ports
- **SSL/TLS**: Consider HTTPS for production
- **Rate limiting**: Prevent abuse

### Access Control
- **Authentication**: Implement if needed
- **IP whitelisting**: Restrict to campus networks
- **Session management**: Track and limit connections

## Backup and Recovery

### Data Backup
```bash
# Backup results
tar -czf results_backup_$(date +%Y%m%d).tar.gz results/

# Backup configurations
cp server_config.json backup/
```

### Recovery Procedures
```bash
# Restore from backup
tar -xzf results_backup_20240101.tar.gz

# Restart with backup config
python server/server.py --config backup/server_config.json
```

## Performance Optimization

### Server Tuning
- **Connection pooling**: Optimize for concurrent clients
- **Memory management**: Monitor and adjust buffer sizes
- **CPU optimization**: Use async/await patterns

### Scaling Considerations
- **Load balancing**: Multiple server instances
- **Database**: Consider persistent storage for large tournaments
- **Caching**: Cache frequently accessed data

## Next Steps

1. **Test the server** with sample clients
2. **Configure monitoring** and alerting
3. **Set up automated backups**
4. **Plan for scaling** as usage grows
5. **Document procedures** for your team

The server is now ready to handle student competitions! 