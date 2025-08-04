# Game System

## Game Hierarchy

All games inherit from the BaseGame abstract class:

```mermaid
graph TD
    BG[BaseGame] --> RPS[RPSGame]
    BG --> BOS[BOSGame]
    BG --> BOSII[BOSIIGame]
    BG --> CHK[ChickenGame]
    BG --> LEM[LemonadeGame]
    BG --> AUC[AuctionGame]
    BG --> ADX1[AdxOneDayGame]
    BG --> ADX2[AdxTwoDayGame]
    
    subgraph "Game Interface"
        GI1[reset()]
        GI2[step()]
        GI3[players_to_move()]
    end
    
    BG -.-> GI1
    BG -.-> GI2
    BG -.-> GI3
```

## Matrix Games (Lab01)

Simple two-player matrix games with payoff matrices:

```mermaid
graph LR
    subgraph "Rock Paper Scissors"
        RPS1[Rock] --> RPS2[Paper]
        RPS2 --> RPS3[Scissors]
        RPS3 --> RPS1
    end
    
    subgraph "Battle of the Sexes"
        BOS1[Action A] --> BOS2[Action B]
    end
    
    subgraph "Chicken Game"
        CHK1[Swerve] --> CHK2[Straight]
    end
```

## Spatial Games (Lab04)

Location-based games with spatial competition:

```mermaid
graph TD
    subgraph "Lemonade Stand"
        L1[Location 1] --> L2[Location 2]
        L2 --> L3[Location 3]
        L3 --> L4[Location 4]
        L4 --> L1
    end
    
    subgraph "Customer Flow"
        C1[Customer 1] --> C2[Customer 2]
        C2 --> C3[Customer 3]
    end
```

## Auction Games (Lab06)

Bidding and auction mechanisms:

```mermaid
graph TD
    subgraph "Auction Process"
        A1[Present Items] --> A2[Collect Bids]
        A2 --> A3[Process Algorithm]
        A3 --> A4[Determine Winners]
        A4 --> A5[Calculate Payments]
    end
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