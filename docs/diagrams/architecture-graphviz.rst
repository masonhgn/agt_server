# System Architecture (Graphviz)

## High-Level Architecture

The AGT Server follows a layered architecture pattern with clear separation of concerns.

.. graphviz::

   digraph AGTArchitecture {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_client {
       label="Client Layer";
       style=filled;
       color=lightgrey;
       C1 [label="Student Client 1"];
       C2 [label="Student Client 2"];
       C3 [label="Student Client N"];
     }
     
     subgraph cluster_server {
       label="Server Layer";
       style=filled;
       color=lightgreen;
       S [label="AGTServer"];
       E [label="Engine"];
     }
     
     subgraph cluster_game {
       label="Game Layer";
       style=filled;
       color=lightyellow;
       G1 [label="RPS Game"];
       G2 [label="BOS Game"];
       G3 [label="Chicken Game"];
       G4 [label="Lemonade Game"];
       G5 [label="Auction Game"];
     }
     
     subgraph cluster_agent {
       label="Agent Layer";
       style=filled;
       color=lightcoral;
       A1 [label="Q-Learning Agent"];
       A2 [label="Fictitious Play Agent"];
       A3 [label="Random Agent"];
       A4 [label="Custom Agent"];
     }
     
     C1 -> S;
     C2 -> S;
     C3 -> S;
     S -> E;
     E -> G1;
     E -> G2;
     E -> G3;
     E -> G4;
     E -> G5;
     G1 -> A1;
     G2 -> A2;
     G3 -> A3;
     G4 -> A4;
   }

## Server Components

The main server components and their responsibilities:

.. graphviz::

   digraph ServerComponents {
     rankdir=LR;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     subgraph cluster_agtserver {
       label="AGTServer";
       style=filled;
       color=lightgrey;
       S1 [label="Connection Manager"];
       S2 [label="Game Manager"];
       S3 [label="Player Manager"];
       S4 [label="Results Manager"];
     }
     
     subgraph cluster_engine {
       label="Engine";
       style=filled;
       color=lightgreen;
       E1 [label="Game Coordinator"];
       E2 [label="Action Collector"];
       E3 [label="Reward Distributor"];
     }
     
     S1 -> S2;
     S2 -> S3;
     S3 -> S4;
     S2 -> E1;
     E1 -> E2;
     E2 -> E3;
   }

## Data Flow

How data flows through the system:

.. graphviz::

   digraph DataFlow {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     A [label="Client Request"];
     B [label="Server Validation"];
     C [label="Game Engine"];
     D [label="Agent Processing"];
     E [label="Game Logic"];
     F [label="Result Calculation"];
     G [label="Response to Client"];
     
     A -> B;
     B -> C;
     C -> D;
     D -> E;
     E -> F;
     F -> G;
   } 