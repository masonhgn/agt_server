# Lab 06: Auctions

This lab introduces auction theory through competitive bidding mechanisms.

## Game Overview

**Type:** Auction-based games
**Players:** 2+ players
**Rounds:** Multiple rounds with bidding phases
**Stages:** Multi-stage with bidding and allocation phases

## Games

### Auction Game
- **Actions:** Bid amounts for items
- **State Space:** Current bids, valuations, and auction history
- **Key Concept:** Optimal bidding strategies and auction design

## State Space

### Observations
```python
observation = {
    "current_round": 3,         # Current auction round
    "my_valuation": 50,         # My value for the item
    "current_bids": [30, 45],   # All current bids
    "auction_history": [...],   # Previous auction results
    "items_remaining": 5        # Items left to auction
}
```

### Actions
```python
action = 25  # Bid amount (integer)
action = 0   # No bid
```

### Rewards
Auction outcome payoffs:
```python
# Second-price auction example
if my_bid == max_bid:  # I win
    second_highest = sorted(bids)[-2]
    reward = my_valuation - second_highest
else:  # I don't win
    reward = 0
```

## Game Structure

### Stage Type
- **Multi-stage** with bidding and allocation phases
- **Auction dynamics** - competitive bidding environment
- **Valuation-based** - different players have different values

### Learning Opportunities
- **Optimal bidding** - bid optimally given valuations
- **Auction design** - understand different auction formats
- **Strategic behavior** - avoid overbidding and underbidding

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.AuctionGame import AuctionGame
from core.agents.lab06.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(AuctionGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Bidding Analysis
```python
def analyze_bidding(self):
    if hasattr(self, 'bid_history'):
        avg_bid = sum(self.bid_history) / len(self.bid_history)
        print(f"Average bid: {avg_bid}")
        print(f"Bid range: {min(self.bid_history)} - {max(self.bid_history)}")
```

## Next Steps

1. **Implement an auction agent** using the common patterns
2. **Study auction theory** to understand optimal strategies
3. **Test different bidding approaches** against various opponents
4. **Compete against other students**

Focus on understanding auction mechanisms and optimal bidding strategies! 