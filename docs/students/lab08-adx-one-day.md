# Lab 08: AdX One Day

This lab introduces real-time bidding in advertising exchanges with one-day campaigns.

## Game Overview

**Type:** Real-time bidding advertising game
**Players:** 10 players
**Rounds:** Single day with multiple user arrivals
**Stages:** Single stage with real-time auction simulation

## Games

### AdX One Day Game
- **Actions:** Bid bundles for market segments
- **State Space:** Campaign information and user arrivals
- **Key Concept:** Real-time bidding and campaign optimization

## State Space

### Observations
```python
observation = {
    "campaign": {
        "id": 1,
        "market_segment": "MALE_YOUNG_HIGH_INCOME",
        "reach": 500,
        "budget": 500.0
    },
    "day": 1,
    "total_users": 10000
}
```

### Actions
```python
action = {
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
Campaign performance payoffs:
```python
# Profit calculation based on reach fulfillment
reach_fulfilled = min(total_impressions, campaign.reach)
profit = (reach_fulfilled / campaign.reach) * campaign.budget - total_spent
reward = profit
```

## Game Structure

### Stage Type
- **Single day** simulation with multiple user arrivals
- **Real-time auctions** - second-price auctions for each impression
- **Campaign constraints** - budget and reach targets

### Learning Opportunities
- **Bid optimization** - set optimal bids for different segments
- **Budget allocation** - distribute budget across market segments
- **Reach targeting** - maximize reach within budget constraints

## Testing

### Local Testing
```python
from core.engine import Engine
from core.game.AdxOneDayGame import AdxOneDayGame
from core.agents.lab08.random_agent import RandomAgent

my_agent = MyAgent("MyAgent")
opponents = [RandomAgent(f"Random{i}") for i in range(9)]

engine = Engine(AdxOneDayGame(num_agents=10), [my_agent] + opponents, rounds=1)
results = engine.run()

print(f"My score: {results[0]}")
print(f"Average opponent score: {sum(results[1:]) / len(results[1:])}")
```

### Campaign Analysis
```python
def analyze_campaign_performance(self):
    if hasattr(self, 'campaign_history'):
        for campaign in self.campaign_history:
            reach_rate = campaign['impressions'] / campaign['reach']
            budget_utilization = campaign['spent'] / campaign['budget']
            print(f"Campaign {campaign['id']}:")
            print(f"  Reach rate: {reach_rate:.2%}")
            print(f"  Budget utilization: {budget_utilization:.2%}")
```

## Next Steps

1. **Implement an AdX agent** using the common patterns
2. **Study real-time bidding** to understand optimal strategies
3. **Test different bidding approaches** against various opponents
4. **Compete against other students**

Focus on understanding real-time bidding and campaign optimization! 