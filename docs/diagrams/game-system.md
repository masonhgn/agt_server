# Game System

## Game Hierarchy

All games inherit from the BaseGame abstract class:

```
BaseGame (Abstract)
├── RPSGame
├── BOSGame
├── BOSIIGame
├── ChickenGame
├── LemonadeGame
├── AuctionGame
├── AdxOneDayGame
└── AdxTwoDayGame

Interface Methods:
├── reset()
├── step()
└── players_to_move()
```

## Matrix Games (Lab01)

Simple two-player matrix games with payoff matrices:

### Rock Paper Scissors
```
Rock → Paper → Scissors → Rock
```

### Battle of the Sexes
```
Action A → Action B
```

### Chicken Game
```
Swerve → Straight
```

## Spatial Games (Lab04)

Location-based games with spatial competition:

### Lemonade Stand
```
Location 1 → Location 2 → Location 3 → Location 4 → Location 1
```

### Customer Flow
```
Customer 1 → Customer 2 → Customer 3
```

## Auction Games (Lab06)

Bidding and auction mechanisms:

### Auction Process
```
Present Items → Collect Bids → Process Algorithm → Determine Winners → Calculate Payments
```

## Game Characteristics

| Game Type | Players | Actions | Learning Focus |
|-----------|---------|---------|----------------|
| RPS | 2 | Rock, Paper, Scissors | Basic game theory |
| BOS | 2 | A, B | Coordination games |
| Chicken | 2 | Swerve, Straight | Conflict resolution |
| Lemonade | N | Location choice | Spatial competition |
| Auction | N | Bid amounts | Auction theory |
| AdX | N | Campaign bids | Ad exchange dynamics | 