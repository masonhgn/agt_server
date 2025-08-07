# Lab 07: Advanced Auctions

This lab introduces advanced auction mechanisms and bidding strategies.

## Game Overview

**Type:** Multi-player auction games
**Players:** 2+ players
**Rounds:** Multiple rounds with complex bidding phases
**Stages:** Multi-stage with bidding, allocation, and payment phases

## Games

### Advanced Auction Game
- **Actions:** Complex bid structures with multiple parameters
- **State Space:** Market segments, valuations, and auction history
- **Key Concept:** Advanced bidding strategies and auction design

## State Space

### Observations
```python
observation = {
    "current_round": 3,         # Current auction round
    "market_segments": [...],   # Available market segments
    "my_valuations": {...},     # My valuations for each segment
    "auction_history": [...],   # Previous auction results
    "remaining_budget": 1000,   # My remaining budget
    "opponent_bids": {...}      # Other players' bid information
}
```

### Actions
```python
action = {
    "bid_entries": [
        {
            "market_segment": "MALE_YOUNG_HIGH_INCOME",
            "bid": 2.5,
            "spending_limit": 100
        }
    ],
    "day_limit": 500
}
```

### Rewards
Complex auction payoffs:
```python
# Profit calculation
profit = (impressions_won / target_reach) * campaign_budget - total_spent
reward = profit
```

## Game Structure

### Stage Type
- **Multi-stage** with complex bidding and allocation
- **Market segmentation** - different segments have different values
- **Budget constraints** - limited spending across segments

### Learning Opportunities
- **Optimal bidding** - balance bid amounts and spending limits
- **Market analysis** - understand segment valuations
- **Budget management** - allocate budget across segments efficiently

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.AuctionGame import AuctionGame
from core.agents.lab07.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(AuctionGame(), [my_agent, opponent], rounds=100)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Opponent score: {results[1]}")
```

### Budget Analysis
```python
def analyze_budget_usage(self):
    if hasattr(self, 'spending_history'):
        total_spent = sum(self.spending_history)
        avg_spent = total_spent / len(self.spending_history)
        print(f"Average spending per round: {avg_spent}")
        print(f"Budget utilization: {total_spent / self.initial_budget:.2%}")
```

## Next Steps

1. **Implement an advanced auction agent** using the common patterns
2. **Study auction theory** to understand optimal bidding strategies
3. **Test different bidding approaches** against various opponents
4. **Compete against other students**

Focus on understanding advanced auction mechanisms and optimal bidding strategies! 