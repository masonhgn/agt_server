# agt server configuration

this directory contains configuration files for running lab-specific agt servers.

## lab-specific configurations

each lab has its own configuration file that restricts the server to only allow the relevant game(s):

- `lab01_rps.json` - lab 1: rock paper scissors only
- `lab02_bos.json` - lab 2: battle of the sexes (bos and bosii) only
- `lab03_chicken.json` - lab 3: chicken game only
- `lab04_lemonade.json` - lab 4: lemonade stand only
- `lab06_auction.json` - lab 6: simultaneous auction only
- `lab07_auction.json` - lab 7: advanced auction only
- `lab08_adx.json` - lab 8: ad exchange (one day) only
- `lab09_adx.json` - lab 9: ad exchange (two day) only

## usage

### using configuration files

```bash
# run lab 1 server (rps only)
python server.py --config configs/lab01_rps.json

# run lab 2 server (bos and bosii only)
python server.py --config configs/lab02_bos.json

# run lab 3 server (chicken only)
python server.py --config configs/lab03_chicken.json

# run lab 4 server (lemonade only)
python server.py --config configs/lab04_lemonade.json

# run lab 6 server (auction only)
python server.py --config configs/lab06_auction.json

# run lab 7 server (advanced auction only)
python server.py --config configs/lab07_auction.json

# run lab 8 server (ad exchange one day only)
python server.py --config configs/lab08_adx.json

# run lab 9 server (ad exchange two day only)
python server.py --config configs/lab09_adx.json
```

### using command line arguments

you can also restrict games directly via command line:

```bash
# restrict to a single game
python server.py --game rps

# restrict to multiple games
python server.py --games rps bos chicken

# run all games (default)
python server.py
```

## configuration options

each configuration file can include:

- `server_name`: display name for the server
- `max_players`: maximum number of concurrent players
- `timeout`: connection timeout in seconds
- `save_results`: whether to save game results to files
- `allowed_games`: list of game types to allow (if not specified, all games are allowed)

## benefits

1. **lab isolation**: students can only join games relevant to their current lab
2. **reduced confusion**: no accidental joins to wrong game types
3. **better organization**: clear separation between different lab competitions
4. **security**: prevents cross-lab interference

## example output

when running a restricted server:

```
server restricted to game: rps
2024-01-15 10:30:00,000 - info - agt server started on 0.0.0.0:8080
2024-01-15 10:30:00,000 - info - game restrictions: only rps allowed
2024-01-15 10:30:00,000 - info - available games:
2024-01-15 10:30:00,000 - info -   rps: rock paper scissors (2 players)
``` 