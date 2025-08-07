# Agent System

## Agent Hierarchy

All agents inherit from the BaseAgent abstract class:

.. graphviz::

   digraph AgentHierarchy {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     BA [label="BaseAgent", fillcolor=lightcoral];
     QA [label="QLearningAgent"];
     FA [label="FictitiousPlayAgent"];
     RA [label="RandomAgent"];
     SA [label="StubbornAgent"];
     CA [label="CompromiseAgent"];
     
     subgraph cluster_interface {
       label="Agent Interface";
       style=filled;
       color=lightgrey;
       AI1 [label="get_action()"];
       AI2 [label="update()"];
       AI3 [label="reset()"];
     }
     
     BA -> QA;
     BA -> FA;
     BA -> RA;
     BA -> SA;
     BA -> CA;
     
     BA -> AI1 [style=dashed];
     BA -> AI2 [style=dashed];
     BA -> AI3 [style=dashed];
   }

## Learning Strategies

### Q-Learning (Lab03)

Reinforcement learning approach for repeated games:

.. graphviz::

   digraph QLearningCycle {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_qlearning {
       label="Q-Learning Cycle";
       style=filled;
       color=lightgrey;
       Q1 [label="Observe State"];
       Q2 [label="Select Action"];
       Q3 [label="Execute Action"];
       Q4 [label="Receive Reward"];
       Q5 [label="Update Q-Table"];
     }
     
     Q1 -> Q2;
     Q2 -> Q3;
     Q3 -> Q4;
     Q4 -> Q5;
     Q5 -> Q1;
   }

### Fictitious Play (Lab01)

Belief-based learning approach:

.. graphviz::

   digraph FictitiousPlayCycle {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_fictitious {
       label="Fictitious Play Cycle";
       style=filled;
       color=lightgreen;
       F1 [label="Observe Opponent"];
       F2 [label="Update Beliefs"];
       F3 [label="Calculate Best Response"];
       F4 [label="Select Action"];
     }
     
     F1 -> F2;
     F2 -> F3;
     F3 -> F4;
     F4 -> F1;
   }

## Lab-Specific Agents

### Lab01: Basic Game Theory

.. graphviz::

   digraph Lab01Agents {
     rankdir=LR;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_lab01 {
       label="Lab01 Agents";
       style=filled;
       color=lightgrey;
       L1A1 [label="Rock Agent"];
       L1A2 [label="Paper Agent"];
       L1A3 [label="Scissors Agent"];
       L1A4 [label="Random Agent"];
       L1A5 [label="Stubborn Agent"];
     }
   }

### Lab02: Finite State Machines

.. graphviz::

   digraph BOSFiniteState {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_fsm {
       label="BOS Finite State";
       style=filled;
       color=lightgrey;
       FS1 [label="State A"];
       FS2 [label="State B"];
       FS3 [label="State C"];
     }
     
     FS1 -> FS2;
     FS2 -> FS3;
     FS3 -> FS1;
   }

### Lab03: Q-Learning

.. graphviz::

   digraph ChickenQLearning {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_chicken_q {
       label="Chicken Q-Learning";
       style=filled;
       color=lightgrey;
       CQ1 [label="State: Last Actions"];
       CQ2 [label="Q-Table Lookup"];
       CQ3 [label="Epsilon-Greedy Selection"];
       CQ4 [label="Action Execution"];
     }
     
     CQ1 -> CQ2;
     CQ2 -> CQ3;
     CQ3 -> CQ4;
     CQ4 -> CQ1;
   }

### Lab04: Reinforcement Learning

.. graphviz::

   digraph LemonadeRL {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_lemonade_rl {
       label="Lemonade RL";
       style=filled;
       color=lightgreen;
       LR1 [label="Location State"];
       LR2 [label="Policy Network"];
       LR3 [label="Location Selection"];
       LR4 [label="Profit Calculation"];
     }
     
     LR1 -> LR2;
     LR2 -> LR3;
     LR3 -> LR4;
     LR4 -> LR1;
   }

### Lab06: Auction Bidding

.. graphviz::

   digraph AuctionAgent {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_auction_agent {
       label="Auction Agent";
       style=filled;
       color=lightyellow;
       AA1 [label="Item Valuation"];
       AA2 [label="Marginal Value"];
       AA3 [label="Bid Calculation"];
       AA4 [label="Bid Submission"];
     }
     
     AA1 -> AA2;
     AA2 -> AA3;
     AA3 -> AA4;
     AA4 -> AA1;
   }

## Agent Characteristics

| Agent Type | Learning Method | Best For | Complexity |
|------------|-----------------|----------|------------|
| Random | None | Baseline | Low |
| Stubborn | None | Fixed strategy | Low |
| Fictitious Play | Belief updating | Matrix games | Medium |
| Q-Learning | Reinforcement | Repeated games | High |
| Custom | Various | Specific scenarios | Variable | 