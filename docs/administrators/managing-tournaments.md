# Managing Tournaments

This guide covers tournament setup, monitoring, and results management for administrators.

## Tournament Overview

Tournaments in the AGT system allow multiple students to compete against each other in structured competitions. The system supports various tournament formats and provides comprehensive result tracking.

## Tournament Types

### Round Robin
- **Format**: Each player competes against every other player
- **Games**: Multiple games per match for statistical significance
- **Advantage**: Fair comparison of all players
- **Disadvantage**: Scales poorly with many players

### Single Elimination
- **Format**: Players eliminated after losing one match
- **Games**: Best-of-N series per match
- **Advantage**: Fast completion, dramatic structure
- **Disadvantage**: Luck can affect outcomes

### Double Elimination
- **Format**: Players must lose twice to be eliminated
- **Games**: Losers bracket provides second chance
- **Advantage**: Reduces luck factor
- **Disadvantage**: More complex bracket management

## Setting Up Tournaments

### 1. Tournament Configuration

Create `tournament_config.json`:
```json
{
    "tournament": {
        "name": "Lab01_RPS_Competition",
        "type": "round_robin",
        "game_type": "rps",
        "rounds_per_game": 100,
        "games_per_match": 3,
        "timeout": 600,
        "auto_start": true
    },
    "players": {
        "max_players": 20,
        "registration_deadline": "2024-01-15T23:59:59",
        "min_players": 2
    },
    "results": {
        "save_path": "./tournament_results",
        "leaderboard": true,
        "detailed_stats": true,
        "export_format": ["csv", "json"]
    }
}
```

### 2. Start Tournament Server

```bash
# Start with tournament configuration
python server/server.py --tournament --config tournament_config.json

# Start with specific game type
python server/server.py --tournament --game rps --rounds 100
```

### 3. Monitor Registration

```bash
# Check registered players
python tools/tournament_status.py --list-players

# Check tournament progress
python tools/tournament_status.py --progress
```

## Tournament Management

### Player Registration

Students register by connecting to the server:
```bash
# Students connect with their agents
python stencils/lab01_stencil/example_solution.py
```

### Match Scheduling

The system automatically schedules matches:
```bash
# View current matches
python tools/tournament_status.py --matches

# View upcoming matches
python tools/tournament_status.py --upcoming
```

### Progress Monitoring

```bash
# Real-time tournament status
tail -f tournament.log

# Check specific player progress
python tools/player_stats.py --player "StudentName"
```

## Results Management

### Live Results

```bash
# View current leaderboard
python tools/leaderboard.py --live

# Export current results
python tools/export_results.py --format csv --output current_results.csv
```

### Final Results

```bash
# Generate final report
python tools/generate_report.py --tournament "Lab01_RPS_Competition" --output final_report.html

# Export all data
python tools/export_results.py --all --format json --output tournament_data.json
```

### Results Analysis

```python
# Analyze tournament results
import pandas as pd

# Load results
results = pd.read_csv('tournament_results/final_results.csv')

# Top performers
top_players = results.sort_values('total_score', ascending=False).head(10)
print(top_players[['player_name', 'total_score', 'games_played']])

# Performance distribution
print(results['total_score'].describe())
```

## Tournament Troubleshooting

### Common Issues

#### Players Not Connecting
```bash
# Check server status
python tools/server_status.py

# Check network connectivity
telnet localhost 8080

# Restart tournament server
pkill -f "server.py"
python server/server.py --tournament --config tournament_config.json
```

#### Stuck Matches
```bash
# Check for hanging games
python tools/check_games.py --stuck

# Force timeout stuck games
python tools/timeout_games.py --force

# Restart specific match
python tools/restart_match.py --match-id "match_123"
```

#### Results Not Saving
```bash
# Check disk space
df -h

# Check file permissions
ls -la tournament_results/

# Manually save results
python tools/save_results.py --force
```

### Debug Mode

```bash
# Enable debug logging
python server/server.py --tournament --debug --log-level DEBUG

# Verbose tournament output
python server/server.py --tournament --verbose
```

## Advanced Tournament Features

### Custom Brackets

Create custom tournament brackets:
```json
{
    "tournament": {
        "type": "custom",
        "brackets": [
            {
                "round": 1,
                "matches": [
                    {"player1": "Alice", "player2": "Bob"},
                    {"player1": "Charlie", "player2": "David"}
                ]
            }
        ]
    }
}
```

### Seeding Players

Seed players based on previous performance:
```json
{
    "tournament": {
        "seeding": {
            "method": "previous_performance",
            "data_source": "previous_tournaments.csv",
            "weight": 0.7
        }
    }
}
```

### Time Controls

Set time limits for matches:
```json
{
    "tournament": {
        "time_controls": {
            "match_timeout": 300,
            "game_timeout": 60,
            "move_timeout": 10
        }
    }
}
```

## Reporting and Analytics

### Performance Reports

```bash
# Generate comprehensive report
python tools/generate_report.py --comprehensive --output full_report.html

# Player performance analysis
python tools/analyze_performance.py --player "StudentName" --output player_report.pdf
```

### Statistical Analysis

```python
# Advanced analytics
import pandas as pd
import matplotlib.pyplot as plt

# Load tournament data
data = pd.read_csv('tournament_results/detailed_results.csv')

# Win rate analysis
win_rates = data.groupby('player_name')['won'].mean().sort_values(ascending=False)
print("Win Rates:")
print(win_rates)

# Performance over time
plt.figure(figsize=(12, 6))
for player in data['player_name'].unique():
    player_data = data[data['player_name'] == player]
    plt.plot(player_data['game_number'], player_data['cumulative_score'], label=player)
plt.legend()
plt.savefig('performance_over_time.png')
```

## Best Practices

### Tournament Planning
1. **Set clear rules** and communicate them to students
2. **Test the system** with a small group first
3. **Monitor resources** during large tournaments
4. **Backup results** regularly during long tournaments

### Communication
1. **Announce tournament** well in advance
2. **Provide clear instructions** for student connection
3. **Update progress** regularly during tournament
4. **Share results** promptly after completion

### Technical Management
1. **Monitor server resources** during tournaments
2. **Have backup procedures** ready
3. **Test recovery procedures** before major tournaments
4. **Document any issues** for future improvements

## Next Steps

1. **Plan your tournament** structure and rules
2. **Test the system** with a small group
3. **Set up monitoring** and alerting
4. **Prepare communication** materials for students
5. **Execute the tournament** and monitor progress

Tournaments are now ready to run smoothly! 