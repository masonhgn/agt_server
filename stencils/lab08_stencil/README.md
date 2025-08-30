# Lab 8: TAC AdX Game (One-Day Variant)

This lab implements an agent for the Trading Agent Competition (TAC) Ad Exchange game in a simplified one-day format.

## Overview

In this lab, you will build an agent that plays the role of an ad network competing to fulfill advertising campaigns. Your agent will:

1. Be assigned a campaign with a target market segment, reach goal, and budget
2. Submit bids for different market segments before the day starts
3. Compete in second-price auctions for user impressions
4. Earn profit based on campaign fulfillment and spending

## Game Mechanics

### Campaign Assignment
- Each agent is randomly assigned a campaign at the start
- Campaigns target market segments with at least 2 demographic attributes
- Examples: `Female_Old`, `Male_Young_HighIncome`, `Young_LowIncome`

### Market Segments
There are 26 possible market segments combining:
- Gender: `Male`, `Female`
- Age: `Young`, `Old` 
- Income: `LowIncome`, `HighIncome`

### Bidding Strategy
Your agent must submit a `OneDayBidBundle` containing:
- Campaign ID
- Day spending limit
- List of `SimpleBidEntry` objects with:
  - Market segment to bid on
  - Bid amount
  - Spending limit for that segment

### Auction Process
- 10,000 users arrive throughout the day
- Each user triggers a second-price auction
- Highest bidder wins and pays the second-highest bid
- Spending limits are enforced per segment and per day

### Scoring
Profit = (reach_fulfilled / campaign.reach) × campaign.budget - total_spent

## Files

### Core Implementation
- `my_adx_agent.py` - **TODO**: Implement your bidding strategy

### Reference
- `solutions/basic_bidding_agent.py` - Basic bidding strategy example
- `solutions/aggressive_bidding_agent.py` - Aggressive bidding strategy example
- `writeup.txt` - Detailed lab description
- `Lab_8_Writeup (1).pdf` - Original lab writeup

## Implementation Guide

### 1. Understand Your Campaign
Your agent receives a campaign with:
```python
self.campaign.id          # Campaign identifier
self.campaign.market_segment  # Target demographic (e.g., Female_Old)
self.campaign.reach       # Number of impressions needed
self.campaign.budget      # Total budget available
```

### 2. Implement get_bid_bundle()
This method should:
1. Identify which market segments match your campaign
2. Set appropriate bids and spending limits
3. Return a `OneDayBidBundle`

### 3. Helper Functions
Use these functions to work with market segments:
```python
# Get all possible market segments
for segment in MarketSegment.all_segments():
    # Check if segment matches your campaign
    if MarketSegment.is_subset(self.campaign.market_segment, segment):
        # Create bid entry for this segment
        pass
```

### 4. Example Strategies
The solution files demonstrate different approaches:

**Basic Bidding Agent:**
- Bids $1.0 on all matching segments
- Uses full budget as spending limits
- Simple but effective strategy

**Aggressive Bidding Agent:**
- Bids $2.0 on matching segments
- Allocates budget evenly across segments
- Uses 80% of budget as day limit for safety margin

## Testing

### Local Testing
You can test your agent locally by running your implementation:

```bash
# Test locally
python my_adx_agent.py
```

The local test will:
- Run your agent against the example solutions and random agents
- Play 10 games with 10 agents each (multi-player AdX games)
- Show detailed results and rankings for each game
- Calculate final tournament statistics including:
  - Average reward per game
  - Total reward across all games
  - Win rate (percentage of games with positive profit)
  - Maximum and minimum rewards
- Save results to CSV files in the `results/` directory

You can also test your agent programmatically:
```python
from core.engine import Engine
from core.game.AdxOneDayGame import AdxOneDayGame
from my_adx_agent import MyOneDayAgent

# Create your agent
agent = MyOneDayAgent()

# Test against other agents
engine = Engine(AdxOneDayGame(num_agents=10), [agent] + opponents, rounds=1)
```

### Server Testing
Connect to the lab server using the provided client library.

## Key Concepts

### Market Segment Matching
- Campaign segments can be general (e.g., `Female`)
- User segments can be specific (e.g., `Female_Old_HighIncome`)
- Use `MarketSegment.is_subset()` to check if a user segment matches your campaign

### Budget Management
- Set day_limit to control total spending
- Set spending_limit per segment to control segment-specific spending
- Balance between winning auctions and staying within budget

### Bidding Strategy
- Consider user frequencies in different segments
- Account for competition from other agents
- Optimize for reach fulfillment vs. cost

## Competition

The lab includes a competition where your agent competes against others in multiple simulations. The agent with the highest average profit wins.
