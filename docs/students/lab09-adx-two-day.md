# Lab 09: AdX Two Day

This lab introduces multi-day advertising campaigns with strategic bidding across days.

## Game Overview

**Type:** Multi-day real-time bidding advertising game
**Players:** 2+ players
**Rounds:** Two days with strategic bidding decisions
**Stages:** Multi-stage with day 1 and day 2 campaigns

## Games

### AdX Two Day Game
- **Actions:** Bid bundles for each day with strategic planning
- **State Space:** Campaign information for both days
- **Key Concept:** Multi-day strategic bidding and campaign planning

## State Space

### Observations
```python
observation = {
    "day": 1,
    "campaign_day1": {
        "id": 1,
        "market_segment": "MALE_YOUNG_HIGH_INCOME",
        "reach": 500,
        "budget": 500.0
    },
    "campaign_day2": {
        "id": 2,
        "market_segment": "FEMALE_OLD_LOW_INCOME",
        "reach": 300,
        "budget": 300.0
    }
}
```

### Actions
```python
action = {
    "day": 1,
    "campaign_id": 1,
    "day_limit": 500.0,
    "bid_entries": [
        {
            "market_segment": "MALE_YOUNG_HIGH_INCOME",
            "bid": 2.5,
            "spending_limit": 100.0
        }
    ]
}
```

### Rewards
Multi-day campaign performance:
```python
# Day-specific profit calculation
reach_fulfilled = min(day_impressions, campaign.reach)
day_profit = (reach_fulfilled / campaign.reach) * campaign.budget - day_spent
reward = day_profit
```

## Game Structure

### Stage Type
- **Two-day simulation** with strategic bidding decisions
- **Day 1 and Day 2** campaigns with different parameters
- **Strategic planning** - balance performance across days

### Learning Opportunities
- **Multi-day optimization** - plan bidding across both days
- **Strategic allocation** - distribute budget between days
- **Campaign coordination** - optimize overall performance

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.AdxTwoDayGame import AdxTwoDayGame
from core.agents.lab09.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponent = RandomAgent("Random")

engine = Engine(AdxTwoDayGame(num_players=2), [my_agent, opponent], rounds=2)
results = engine.run()

print(f"My total score: {results[0]}")
print(f"Opponent total score: {results[1]}")
```

### Multi-day Analysis
```python
def analyze_multi_day_performance(self):
    if hasattr(self, 'day_performance'):
        for day, performance in self.day_performance.items():
            print(f"Day {day}:")
            print(f"  Impressions: {performance['impressions']}")
            print(f"  Reach rate: {performance['reach_rate']:.2%}")
            print(f"  Profit: {performance['profit']:.2f}")
```

## Next Steps

1. **Implement a multi-day AdX agent** using the common patterns
2. **Study multi-day optimization** to understand strategic planning
3. **Test different bidding approaches** against various opponents
4. **Compete against other students**

Focus on understanding multi-day strategic bidding and campaign coordination! 