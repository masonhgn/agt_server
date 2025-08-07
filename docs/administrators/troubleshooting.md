# Troubleshooting

This guide covers common issues and their solutions for AGT server administrators.

## Quick Diagnosis

### Server Status Check
```bash
# Check if server is running
ps aux | grep server.py

# Check port availability
netstat -an | grep :8080

# Check server logs
tail -f server.log
```

### Basic Health Check
```bash
# Test server connectivity
telnet localhost 8080

# Check Python environment
python --version
pip list | grep -E "(numpy|pandas|asyncio)"

# Check file permissions
ls -la server/
```

## Common Issues

### Server Won't Start

#### Port Already in Use
```bash
# Find process using port
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use different port
python server/server.py --port 8081
```

#### Python Environment Issues
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python
```

#### Missing Dependencies
```bash
# Install missing packages
pip install numpy pandas asyncio

# Check for conflicts
pip check

# Update pip
pip install --upgrade pip
```

### Clients Can't Connect

#### Network Issues
```bash
# Check firewall
sudo ufw status

# Allow port
sudo ufw allow 8080

# Test network connectivity
ping <client_ip>
```

#### Server Configuration
```bash
# Check server host binding
python server/server.py --host 0.0.0.0

# Check server logs for connection errors
grep "connection" server.log
```

#### Client Issues
```bash
# Test client connection
python -c "
import socket
s = socket.socket()
s.connect(('localhost', 8080))
print('Connection successful')
s.close()
"
```

### Games Not Running

#### Game Configuration Issues
```bash
# Test individual games
python -c "from core.game.RPSGame import RPSGame; print('RPS OK')"
python -c "from core.game.BOSGame import BOSGame; print('BOS OK')"

# Check game configurations
python tools/validate_games.py
```

#### Agent Issues
```bash
# Test agent loading
python -c "from core.agents.lab01.random_agent import RandomAgent; print('Agent OK')"

# Check agent implementations
python tools/validate_agents.py
```

#### Engine Issues
```bash
# Test engine functionality
python -c "from core.engine import Engine; print('Engine OK')"

# Run test game
python tests/test_engine.py
```

### Performance Problems

#### High CPU Usage
```bash
# Check CPU usage
top -p $(pgrep -f server.py)

# Identify bottlenecks
python tools/performance_analyzer.py --cpu

# Restart with limits
python server/server.py --max-games 10
```

#### High Memory Usage
```bash
# Check memory usage
free -h

# Find memory leaks
python tools/memory_analyzer.py

# Restart server
pkill -f server.py
python server/server.py
```

#### Slow Response Times
```bash
# Check network latency
ping localhost

# Monitor response times
python tools/response_monitor.py

# Optimize server settings
python server/server.py --timeout 30
```

## Debug Mode

### Enable Debug Logging
```bash
# Start with debug mode
python server/server.py --debug --log-level DEBUG

# Verbose output
python server/server.py --verbose
```

### Debug Configuration
```json
{
    "debug": {
        "log_level": "DEBUG",
        "verbose": true,
        "trace_games": true,
        "trace_agents": true
    }
}
```

### Debug Tools
```bash
# Interactive debugger
python -m pdb server/server.py

# Memory profiling
python -m memory_profiler server/server.py

# CPU profiling
python -m cProfile server/server.py
```

## Error Analysis

### Common Error Messages

#### Connection Errors
```
ERROR: Connection refused
SOLUTION: Check if server is running and port is available

ERROR: Timeout on connection
SOLUTION: Check network connectivity and server load

ERROR: Invalid message format
SOLUTION: Check client implementation and message structure
```

#### Game Errors
```
ERROR: Invalid action
SOLUTION: Check agent implementation and action format

ERROR: Game state invalid
SOLUTION: Check game implementation and state management

ERROR: Agent timeout
SOLUTION: Check agent performance and increase timeout
```

#### System Errors
```
ERROR: Out of memory
SOLUTION: Restart server, reduce concurrent games

ERROR: File not found
SOLUTION: Check file paths and permissions

ERROR: Permission denied
SOLUTION: Check file permissions and user access
```

### Log Analysis
```bash
# Extract error patterns
grep "ERROR" server.log | cut -d' ' -f4- | sort | uniq -c

# Find recent errors
grep "ERROR" server.log | tail -20

# Analyze error frequency
python tools/error_analyzer.py --frequency
```

## Recovery Procedures

### Server Recovery
```bash
# Stop server gracefully
pkill -TERM -f server.py

# Force stop if needed
pkill -KILL -f server.py

# Restart server
python server/server.py --config server_config.json
```

### Data Recovery
```bash
# Backup current results
cp -r results/ results_backup_$(date +%Y%m%d_%H%M%S)/

# Restore from backup
cp -r results_backup_20240101_120000/* results/

# Verify data integrity
python tools/verify_results.py
```

### Configuration Recovery
```bash
# Backup configuration
cp server_config.json server_config_backup.json

# Restore configuration
cp server_config_backup.json server_config.json

# Validate configuration
python tools/validate_config.py
```

## Prevention

### Regular Maintenance
```bash
# Daily health check
python tools/daily_health_check.py

# Weekly cleanup
python tools/cleanup_old_logs.py

# Monthly backup
python tools/backup_system.py
```

### Monitoring Setup
```bash
# Set up monitoring
python tools/setup_monitoring.py

# Configure alerts
python tools/setup_alerts.py

# Create dashboards
python tools/setup_dashboard.py
```

### Documentation
```bash
# Document procedures
python tools/generate_procedures.py

# Update troubleshooting guide
python tools/update_troubleshooting.py

# Create runbooks
python tools/create_runbooks.py
```

## Emergency Procedures

### Critical Issues

#### Server Down
1. **Check process**: `ps aux | grep server.py`
2. **Check logs**: `tail -f server.log`
3. **Restart server**: `python server/server.py`
4. **Notify users**: Send status update

#### Data Loss
1. **Stop server**: `pkill -f server.py`
2. **Backup current state**: `cp -r results/ backup/`
3. **Restore from backup**: `cp -r backup/* results/`
4. **Verify data**: `python tools/verify_results.py`
5. **Restart server**: `python server/server.py`

#### Security Breach
1. **Stop server**: `pkill -f server.py`
2. **Check logs**: `grep "unauthorized" server.log`
3. **Update firewall**: `sudo ufw deny 8080`
4. **Investigate**: Check for suspicious activity
5. **Secure system**: Update passwords and keys

### Communication Plan
1. **Immediate**: Notify key stakeholders
2. **Status updates**: Regular progress reports
3. **Resolution**: Document solution and lessons learned
4. **Prevention**: Update procedures to prevent recurrence

## Best Practices

### Proactive Maintenance
1. **Regular backups** of configurations and data
2. **Monitor system resources** continuously
3. **Test recovery procedures** regularly
4. **Document all changes** and procedures

### Incident Response
1. **Assess impact** quickly and accurately
2. **Communicate clearly** with stakeholders
3. **Follow procedures** but adapt as needed
4. **Learn from incidents** to improve systems

### Continuous Improvement
1. **Review incidents** regularly
2. **Update procedures** based on lessons learned
3. **Train team members** on troubleshooting
4. **Automate routine tasks** where possible

## Next Steps

1. **Set up monitoring** and alerting systems
2. **Create runbooks** for common issues
3. **Train team members** on troubleshooting procedures
4. **Establish escalation** procedures for complex issues
5. **Regularly review** and update troubleshooting procedures

Effective troubleshooting ensures reliable system operation! 