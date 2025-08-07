# Monitoring System

This guide covers monitoring the AGT server system for performance, health, and troubleshooting.

## System Monitoring Overview

Effective monitoring ensures the AGT server runs smoothly and helps identify issues before they affect student competitions. This guide covers both basic monitoring and advanced analytics.

## Basic Monitoring

### Server Status

Check if the server is running:
```bash
# Check process
ps aux | grep server.py

# Check port usage
netstat -an | grep :8080

# Check server logs
tail -f server.log
```

### Resource Usage

Monitor system resources:
```bash
# CPU and memory usage
htop

# Disk space
df -h

# Network connections
netstat -an | grep :8080 | wc -l
```

### Connection Monitoring

Track client connections:
```bash
# Active connections
netstat -an | grep :8080

# Connection rate
watch -n 1 "netstat -an | grep :8080 | wc -l"

# Connection details
ss -tuln | grep :8080
```

## Advanced Monitoring

### Performance Metrics

Monitor key performance indicators:
```bash
# Response time
python tools/performance_monitor.py --response-time

# Throughput
python tools/performance_monitor.py --throughput

# Error rate
python tools/performance_monitor.py --error-rate
```

### Game Statistics

Track game execution:
```bash
# Games per minute
python tools/game_stats.py --rate

# Average game duration
python tools/game_stats.py --duration

# Success rate
python tools/game_stats.py --success-rate
```

### Player Activity

Monitor student participation:
```bash
# Active players
python tools/player_monitor.py --active

# Player statistics
python tools/player_monitor.py --stats

# Connection history
python tools/player_monitor.py --history
```

## Log Analysis

### Server Logs

Analyze server logs for issues:
```bash
# Error patterns
grep "ERROR" server.log | tail -20

# Warning patterns
grep "WARNING" server.log | tail -20

# Performance issues
grep "slow" server.log | tail -10
```

### Game Logs

Analyze game execution:
```bash
# Failed games
grep "Game failed" game.log | tail -10

# Timeout issues
grep "timeout" game.log | tail -10

# Performance bottlenecks
grep "slow" game.log | tail -10
```

### Custom Log Analysis

Create custom log analysis scripts:
```python
import re
from collections import Counter

def analyze_logs(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Extract error patterns
    errors = [line for line in lines if 'ERROR' in line]
    error_types = Counter([re.search(r'ERROR: (.+)', line).group(1) 
                          for line in errors if re.search(r'ERROR: (.+)', line)])
    
    print("Error Types:")
    for error_type, count in error_types.most_common():
        print(f"  {error_type}: {count}")
```

## Alerting

### Basic Alerts

Set up basic monitoring alerts:
```bash
# Server down alert
python tools/alert_monitor.py --server-down

# High CPU usage
python tools/alert_monitor.py --high-cpu --threshold 80

# High memory usage
python tools/alert_monitor.py --high-memory --threshold 85
```

### Custom Alerts

Create custom alert conditions:
```python
# Custom alert script
import psutil
import smtplib
from email.mime.text import MIMEText

def check_system_health():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    
    if cpu_percent > 90 or memory_percent > 90:
        send_alert(f"High resource usage: CPU {cpu_percent}%, Memory {memory_percent}%")

def send_alert(message):
    # Send email alert
    msg = MIMEText(message)
    msg['Subject'] = 'AGT Server Alert'
    msg['From'] = 'admin@example.com'
    msg['To'] = 'admin@example.com'
    
    # Send email (configure SMTP settings)
    # s.send_message(msg)
```

## Dashboard

### Real-time Dashboard

Create a monitoring dashboard:
```python
# Simple dashboard
import time
import psutil
import requests

def dashboard():
    while True:
        # System metrics
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        
        # Server metrics
        try:
            response = requests.get('http://localhost:8080/health', timeout=5)
            server_status = "OK" if response.status_code == 200 else "ERROR"
        except:
            server_status = "DOWN"
        
        # Display metrics
        print(f"\n=== AGT Server Dashboard ===")
        print(f"CPU: {cpu}% | Memory: {memory}% | Server: {server_status}")
        print(f"Time: {time.strftime('%H:%M:%S')}")
        
        time.sleep(30)
```

### Web Dashboard

Create a web-based dashboard:
```python
# Flask-based dashboard
from flask import Flask, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                         cpu=psutil.cpu_percent(),
                         memory=psutil.virtual_memory().percent,
                         connections=len(psutil.net_connections()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Troubleshooting

### Performance Issues

Identify and resolve performance problems:
```bash
# Check for bottlenecks
python tools/performance_analyzer.py --bottlenecks

# Memory leaks
python tools/memory_analyzer.py --leaks

# CPU profiling
python tools/cpu_profiler.py --profile
```

### Network Issues

Diagnose network problems:
```bash
# Connection drops
python tools/network_monitor.py --drops

# Latency issues
python tools/network_monitor.py --latency

# Bandwidth usage
python tools/network_monitor.py --bandwidth
```

### Application Issues

Debug application problems:
```bash
# Game execution errors
python tools/game_debugger.py --errors

# Agent communication issues
python tools/agent_monitor.py --communication

# Server state analysis
python tools/server_analyzer.py --state
```

## Automated Monitoring

### Cron Jobs

Set up automated monitoring:
```bash
# Add to crontab
# Check server every 5 minutes
*/5 * * * * python /path/to/agt_server_new/tools/health_check.py

# Daily system report
0 9 * * * python /path/to/agt_server_new/tools/daily_report.py

# Weekly performance analysis
0 10 * * 1 python /path/to/agt_server_new/tools/weekly_analysis.py
```

### Monitoring Scripts

Create monitoring scripts:
```python
# Health check script
import requests
import sys

def health_check():
    try:
        response = requests.get('http://localhost:8080/health', timeout=5)
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
    if not health_check():
        sys.exit(1)
```

## Best Practices

### Monitoring Strategy
1. **Monitor key metrics** (CPU, memory, connections)
2. **Set up alerts** for critical issues
3. **Log everything** for troubleshooting
4. **Regular health checks** to catch issues early

### Performance Optimization
1. **Identify bottlenecks** through monitoring
2. **Optimize resource usage** based on metrics
3. **Scale appropriately** based on load
4. **Plan for growth** using historical data

### Incident Response
1. **Document procedures** for common issues
2. **Set up escalation** for critical problems
3. **Test recovery procedures** regularly
4. **Learn from incidents** to improve monitoring

## Next Steps

1. **Set up basic monitoring** for your server
2. **Configure alerts** for critical issues
3. **Create dashboards** for easy monitoring
4. **Establish procedures** for incident response
5. **Regularly review** and improve monitoring

Effective monitoring ensures reliable server operation! 