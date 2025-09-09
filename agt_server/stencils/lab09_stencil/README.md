# Lab 9: TAC AdX Game (Two-Day Variant)

This lab implements a two-day advertising exchange game where agents compete in AdX auctions over two consecutive days. The budget for the second day's campaign depends on the quality score achieved on the first day.

## Game Overview

- **Type**: Multi-day real-time bidding advertising game
- **Players**: 2+ players  
- **Rounds**: Two days with strategic bidding decisions
- **Key Concept**: Multi-day strategic bidding and campaign planning

## Quality Score

The quality score determines the budget multiplier for day 2. It's calculated using the formula:

```
QC(x) = (2/a) * (arctan(a * (x/R - b)) - arctan(-b)) + 1
```

Where:
- a = 4.08577
- b = 3.08577  
- x = impressions achieved
- R = campaign reach

The quality score ranges from approximately 0.89 to 1.38:
- 0.89: Very low quality (0 impressions)
- 0.90: Very good quality (reached campaign goal)
- 1.38: Perfect quality (exceeded campaign goal significantly)

## File Structure

### `my_adx_agent.py`
Main agent file containing the `MyTwoDaysTwoCampaignsAgent` class. This is where you implement your bidding strategy.

### `solutions/example_solution.py`
Example implementation showing a basic bidding strategy.

## Agent API

### Required Methods

#### `get_bid_bundle(day: int) -> TwoDayBidBundle`
Returns a bid bundle for the specified day (1 or 2). This is the main method you need to implement.

#### `get_first_campaign() -> Campaign`
Returns the campaign assigned for day 1.

#### `get_second_campaign() -> Campaign`  
Returns the campaign assigned for day 2.

### Optional Helper Methods

#### `calculate_quality_score(impressions_achieved: int, campaign_reach: int) -> float`
Calculates the quality score using the formula from the writeup.

## TwoDayBidBundle Structure

```python
TwoDayBidBundle(
    day=1,                    # Day number (1 or 2)
    campaign_id=123,          # Campaign ID
    day_limit=500.0,          # Total spending limit for the day
    bid_entries=[...]         # List of SimpleBidEntry objects
)
```

## SimpleBidEntry Structure

```python
SimpleBidEntry(
    market_segment=MarketSegment.MALE_YOUNG,  # Target market segment
    bid=1.5,                                  # Bid amount (CPM)
    spending_limit=100.0                      # Max spending in this segment
)
```

## Market Segments

There are 26 possible market segments combining:
- Gender: MALE, FEMALE
- Age: YOUNG, OLD  
- Income: LOW_INCOME, HIGH_INCOME

Examples: `MALE_YOUNG_HIGH_INCOME`, `FEMALE_OLD_LOW_INCOME`

## Strategic Considerations

1. **Day 1 Trade-off**: Balance profit vs quality score
   - High bids → Lower profit but higher quality score
   - Low bids → Higher profit but lower quality score

2. **Day 2 Planning**: Quality score affects budget
   - High quality score → Larger day 2 budget
   - Low quality score → Smaller day 2 budget

3. **Market Segment Matching**: Use `MarketSegment.is_subset()` to find matching segments

## Testing

Run your agent against the example solution to test your implementation:

```python
from core.engine import Engine
from core.game.AdxTwoDayGame import AdxTwoDayGame
from my_adx_agent import MyTwoDaysTwoCampaignsAgent
from solutions.example_solution import ExampleTwoDaysTwoCampaignsAgent

my_agent = MyTwoDaysTwoCampaignsAgent()
opponent = ExampleTwoDaysTwoCampaignsAgent()

engine = Engine(AdxTwoDayGame(num_players=2), [my_agent, opponent], rounds=2)
results = engine.run()
```

## Competition

Your agent will compete against 9 other agents in 100 simulations of the two-day game. The competition runs every hour after the due date.
