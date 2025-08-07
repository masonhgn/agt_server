# Server Setup for Administrators

This guide is for TAs, instructors, and system administrators who need to set up and manage the AGT server for lab competitions.

## System Overview

The AGT server is a distributed system that:
- **Hosts game competitions** between student agents
- **Manages client connections** from student machines
- **Coordinates tournaments** and tracks results
- **Provides real-time monitoring** of system status

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended) or macOS
- **Python**: 3.8+ with pip
- **Memory**: 4GB+ RAM (8GB+ for large tournaments)
- **Network**: Stable internet connection for client connections
- **Storage**: 10GB+ free space for logs and results

### Software Dependencies
```bash
# Core Python packages
pip install asyncio pandas numpy

# Optional: For enhanced monitoring
pip install psutil matplotlib seaborn
```

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd agt_server_new
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Test the server starts correctly
python server/server.py --help
```

## Configuration

### Server Configuration File

Create a configuration file `server_config.json`:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "max_connections": 100,
    "timeout": 30
  },
  "games": {
    "allowed_games": ["rps", "bos", "chicken", "lemonade", "auction"],
    "default_rounds": 100,
    "tournament_mode": true
  },
  "logging": {
    "level": "INFO",
    "file": "server.log",
    "max_size": "10MB",
    "backup_count": 5
  },
  "results": {
    "save_path": "./results",
    "format": "csv",
    "auto_backup": true
  }
}
```

### Environment Variables

Set these environment variables for production:

```bash
export AGT_SERVER_HOST="0.0.0.0"
export AGT_SERVER_PORT="8080"
export AGT_LOG_LEVEL="INFO"
export AGT_RESULTS_DIR="./results"
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

### Production Start (with logging)
```bash
nohup python server/server.py --config server_config.json > server.log 2>&1 &
```

### Using Systemd (Linux)

Create `/etc/systemd/system/agt-server.service`:

```ini
[Unit]
Description=AGT Game Theory Server
After=network.target

[Service]
Type=simple
User=agt-user
WorkingDirectory=/path/to/agt_server_new
ExecStart=/usr/bin/python3 server/server.py --config server_config.json
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable agt-server
sudo systemctl start agt-server
sudo systemctl status agt-server
```

## Monitoring the Server

### 1. Check Server Status

```bash
# Check if server is running
ps aux | grep server.py

# Check server logs
tail -f server.log

# Check system resources
htop
```

### 2. Monitor Connections

The server provides real-time connection information:

```bash
# View active connections
netstat -an | grep :8080

# Monitor connection rate
watch -n 1 "netstat -an | grep :8080 | wc -l"
```

### 3. Check Game Status

```bash
# View current games
grep "Game started" server.log | tail -10

# View completed games
grep "Game completed" server.log | tail -10
```

## Managing Tournaments

### Starting a Tournament

```bash
# Start tournament mode
python server/server.py --tournament --config tournament_config.json
```

### Tournament Configuration

Create `tournament_config.json`:

```json
{
  "tournament": {
    "name": "Lab01_Competition",
    "game_type": "rps",
    "rounds_per_game": 100,
    "max_players": 20,
    "auto_start": true,
    "timeout": 300
  },
  "brackets": {
    "type": "round_robin",
    "seeding": "random"
  },
  "results": {
    "save_path": "./tournament_results",
    "leaderboard": true,
    "detailed_stats": true
  }
}
```

### Monitoring Tournament Progress

```bash
# Check tournament status
tail -f tournament.log

# View leaderboard
cat tournament_results/leaderboard.csv

# Check player statistics
python -c "
import pandas as pd
df = pd.read_csv('tournament_results/player_stats.csv')
print(df.sort_values('total_score', ascending=False).head(10))
"
```

## Troubleshooting

### Common Issues

#### 1. Server Won't Start

**Problem**: Port already in use
```bash
# Check what's using the port
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use a different port
python server/server.py --port 8081
```

#### 2. Clients Can't Connect

**Problem**: Firewall blocking connections
```bash
# Check firewall status
sudo ufw status

# Allow the port
sudo ufw allow 8080

# Or disable firewall (development only)
sudo ufw disable
```

#### 3. High Memory Usage

**Problem**: Too many concurrent games
```bash
# Check memory usage
free -h

# Restart server with memory limits
python server/server.py --max-games 10 --max-connections 50
```

#### 4. Slow Performance

**Problem**: System resources exhausted
```bash
# Check CPU and memory
top

# Check disk space
df -h

# Restart with resource limits
python server/server.py --max-games 5 --timeout 60
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
python server/server.py --debug --log-level DEBUG
```

### Health Checks

Create a health check script `health_check.py`:

```python
import requests
import sys

def check_server():
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("Server is healthy")
            return True
        else:
            print(f"Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"Server is not responding: {e}")
        return False

if __name__ == "__main__":
    if not check_server():
        sys.exit(1)
```

## Backup and Recovery

### Automated Backups

Create a backup script `backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/agt_server"
mkdir -p $BACKUP_DIR

# Backup results
tar -czf $BACKUP_DIR/results_$DATE.tar.gz results/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz *.log

# Backup configuration
cp server_config.json $BACKUP_DIR/config_$DATE.json

echo "Backup completed: $DATE"
```

### Recovery Procedures

#### Restore Results
```bash
# Extract backup
tar -xzf results_20240101_120000.tar.gz

# Restore to server
cp -r results/* /path/to/agt_server_new/results/
```

#### Restore Configuration
```bash
# Restore config
cp config_20240101_120000.json server_config.json

# Restart server
sudo systemctl restart agt-server
```

## Security Considerations

### Network Security

1. **Firewall Configuration**
```bash
# Allow only necessary ports
sudo ufw allow 8080/tcp
sudo ufw deny 22/tcp  # If not using SSH
```

2. **Rate Limiting**
```bash
# Install rate limiting
sudo apt install iptables-persistent

# Limit connections per IP
sudo iptables -A INPUT -p tcp --dport 8080 -m limit --limit 10/minute --limit-burst 20 -j ACCEPT
```

### Access Control

1. **User Management**
```bash
# Create dedicated user
sudo useradd -m -s /bin/bash agt-user
sudo usermod -aG sudo agt-user
```

2. **File Permissions**
```bash
# Set proper permissions
sudo chown -R agt-user:agt-user /path/to/agt_server_new
sudo chmod 755 /path/to/agt_server_new
sudo chmod 644 /path/to/agt_server_new/server_config.json
```

## Performance Optimization

### System Tuning

1. **Increase File Descriptors**
```bash
# Edit limits
sudo nano /etc/security/limits.conf

# Add these lines:
agt-user soft nofile 65536
agt-user hard nofile 65536
```

2. **Optimize Network Settings**
```bash
# Edit sysctl
sudo nano /etc/sysctl.conf

# Add these lines:
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
```

### Monitoring Tools

Install monitoring tools:

```bash
# System monitoring
sudo apt install htop iotop nethogs

# Network monitoring
sudo apt install iftop nethogs

# Log monitoring
sudo apt install logwatch
```

## Scaling Considerations

### Load Balancing

For multiple servers, use a load balancer:

```bash
# Install nginx
sudo apt install nginx

# Configure load balancer
sudo nano /etc/nginx/sites-available/agt-load-balancer
```

### Database Integration

For large-scale deployments, consider adding a database:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb agt_server
sudo -u postgres createuser agt_user
```

## Next Steps

1. **Test the setup** with a small group of students
2. **Monitor performance** during the first competition
3. **Gather feedback** from students and TAs
4. **Optimize configuration** based on usage patterns
5. **Plan for scaling** as the system grows

For more detailed information about managing tournaments and monitoring, see the other administrator guides. 