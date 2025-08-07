# Game System

## Game Hierarchy

All games inherit from the BaseGame abstract class:

.. graphviz::

   digraph GameHierarchy {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     BG [label="BaseGame", fillcolor=lightcoral];
     RPS [label="RPSGame"];
     BOS [label="BOSGame"];
     BOSII [label="BOSIIGame"];
     CHK [label="ChickenGame"];
     LEM [label="LemonadeGame"];
     AUC [label="AuctionGame"];
     ADX1 [label="AdxOneDayGame"];
     ADX2 [label="AdxTwoDayGame"];
     
     subgraph cluster_interface {
       label="Game Interface";
       style=filled;
       color=lightgrey;
       GI1 [label="reset()"];
       GI2 [label="step()"];
       GI3 [label="players_to_move()"];
     }
     
     BG -> RPS;
     BG -> BOS;
     BG -> BOSII;
     BG -> CHK;
     BG -> LEM;
     BG -> AUC;
     BG -> ADX1;
     BG -> ADX2;
     
     BG -> GI1 [style=dashed];
     BG -> GI2 [style=dashed];
     BG -> GI3 [style=dashed];
   }

## Matrix Games (Lab01)

Simple two-player matrix games with payoff matrices:

.. graphviz::

   digraph MatrixGames {
     rankdir=LR;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_rps {
       label="Rock Paper Scissors";
       style=filled;
       color=lightgrey;
       RPS1 [label="Rock"];
       RPS2 [label="Paper"];
       RPS3 [label="Scissors"];
     }
     
     subgraph cluster_bos {
       label="Battle of the Sexes";
       style=filled;
       color=lightgreen;
       BOS1 [label="Action A"];
       BOS2 [label="Action B"];
     }
     
     subgraph cluster_chicken {
       label="Chicken Game";
       style=filled;
       color=lightyellow;
       CHK1 [label="Swerve"];
       CHK2 [label="Straight"];
     }
     
     RPS1 -> RPS2;
     RPS2 -> RPS3;
     RPS3 -> RPS1;
     BOS1 -> BOS2;
     CHK1 -> CHK2;
   }

## Spatial Games (Lab04)

Location-based games with spatial competition:

.. graphviz::

   digraph SpatialGames {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_lemonade {
       label="Lemonade Stand";
       style=filled;
       color=lightgrey;
       L1 [label="Location 1"];
       L2 [label="Location 2"];
       L3 [label="Location 3"];
       L4 [label="Location 4"];
     }
     
     subgraph cluster_customers {
       label="Customer Flow";
       style=filled;
       color=lightgreen;
       C1 [label="Customer 1"];
       C2 [label="Customer 2"];
       C3 [label="Customer 3"];
     }
     
     L1 -> L2;
     L2 -> L3;
     L3 -> L4;
     L4 -> L1;
     C1 -> C2;
     C2 -> C3;
   }

## Auction Games (Lab06)

Bidding and auction mechanisms:

.. graphviz::

   digraph AuctionProcess {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_auction {
       label="Auction Process";
       style=filled;
       color=lightgrey;
       A1 [label="Present Items"];
       A2 [label="Collect Bids"];
       A3 [label="Process Algorithm"];
       A4 [label="Determine Winners"];
       A5 [label="Calculate Payments"];
     }
     
     A1 -> A2;
     A2 -> A3;
     A3 -> A4;
     A4 -> A5;
   }

## Game Characteristics

| Game Type | Players | Actions | Learning Focus |
|-----------|---------|---------|----------------|
| RPS | 2 | Rock, Paper, Scissors | Basic game theory |
| BOS | 2 | A, B | Coordination games |
| Chicken | 2 | Swerve, Straight | Conflict resolution |
| Lemonade | N | Location choice | Spatial competition |
| Auction | N | Bid amounts | Auction theory |
| AdX | N | Campaign bids | Ad exchange dynamics | 