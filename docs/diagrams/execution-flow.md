# Execution Flow

## Game Session Sequence

The typical flow of a game session:

.. graphviz::

   digraph GameSession {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     C [label="Client"];
     S [label="Server"];
     E [label="Engine"];
     G [label="Game"];
     A [label="Agent"];
     
     C -> S [label="Connect"];
     S -> C [label="Confirm connection"];
     C -> S [label="Join game"];
     S -> E [label="Create game"];
     E -> G [label="Initialize"];
     G -> E [label="Initial state"];
     E -> C [label="Game ready"];
     
     subgraph cluster_loop {
       label="Game rounds";
       style=filled;
       color=lightgrey;
       E -> C [label="Send observation"];
       C -> A [label="Get action"];
       A -> C [label="Return action"];
       C -> E [label="Send action"];
       E -> G [label="Step game"];
       G -> E [label="New state"];
       E -> C [label="Send results"];
     }
     
     E -> S [label="Game complete"];
     S -> C [label="Final results"];
   }

## Tournament Management

How tournaments are managed:

.. graphviz::

   digraph TournamentFlow {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     T1 [label="Start Tournament"];
     T2 [label="Match Players"];
     T3 [label="Run Games"];
     T4 [label="Collect Results"];
     T5 [label="More Matches?", shape=diamond];
     T6 [label="Calculate Rankings"];
     T7 [label="Save Results"];
     
     T1 -> T2;
     T2 -> T3;
     T3 -> T4;
     T4 -> T5;
     T5 -> T2 [label="Yes"];
     T5 -> T6 [label="No"];
     T6 -> T7;
   }

## Game Round Flow

Detailed flow of a single game round:

.. graphviz::

   digraph GameRound {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     R1 [label="Round Start"];
     R2 [label="Send Observations"];
     R3 [label="Collect Actions"];
     R4 [label="Process Game Logic"];
     R5 [label="Calculate Rewards"];
     R6 [label="Update Agents"];
     R7 [label="Game Done?", shape=diamond];
     R8 [label="End Game"];
     
     R1 -> R2;
     R2 -> R3;
     R3 -> R4;
     R4 -> R5;
     R5 -> R6;
     R6 -> R7;
     R7 -> R1 [label="No"];
     R7 -> R8 [label="Yes"];
   }

## Error Handling

How the system handles various error conditions:

.. graphviz::

   digraph ErrorHandling {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     E1 [label="Error Occurs"];
     E2 [label="Error Type?", shape=diamond];
     E3 [label="Use Default Action"];
     E4 [label="Reject Action"];
     E5 [label="Disconnect Player"];
     E6 [label="End Game Early"];
     E7 [label="Continue Game"];
     E8 [label="Request New Action"];
     E9 [label="Notify Other Players"];
     E10 [label="Save Partial Results"];
     E11 [label="Log Error"];
     
     E1 -> E2;
     E2 -> E3 [label="Timeout"];
     E2 -> E4 [label="Invalid Action"];
     E2 -> E5 [label="Connection Lost"];
     E2 -> E6 [label="Game Error"];
     E3 -> E7;
     E4 -> E8;
     E5 -> E9;
     E6 -> E10;
     E7 -> E11;
     E8 -> E11;
     E9 -> E11;
     E10 -> E11;
   }

## Performance Monitoring

Metrics collection during execution:

.. graphviz::

   digraph PerformanceMonitoring {
     rankdir=TB;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     P1 [label="Game Execution"];
     P2 [label="Collect Metrics"];
     P3 [label="Response Times"];
     P4 [label="Action Frequencies"];
     P5 [label="Reward Distributions"];
     P6 [label="Error Rates"];
     P7 [label="Performance Analysis"];
     P8 [label="Generate Reports"];
     P9 [label="Save to Results"];
     
     P1 -> P2;
     P2 -> P3;
     P2 -> P4;
     P2 -> P5;
     P2 -> P6;
     P3 -> P7;
     P4 -> P7;
     P5 -> P7;
     P6 -> P7;
     P7 -> P8;
     P8 -> P9;
   }

## Communication Protocol

Message flow between client and server:

.. graphviz::

   digraph CommunicationProtocol {
     rankdir=LR;
     node [shape=box, style=filled, fillcolor=lightblue];
     
     A [label="Client"];
     B [label="Server"];
     
     A -> B [label="Join Game"];
     B -> A [label="Game Ready"];
     A -> B [label="Get Action"];
     B -> A [label="Observation"];
     A -> B [label="Action"];
     B -> A [label="Results"];
     A -> B [label="Ready Next"];
     B -> A [label="Next Round"];
   }

## Message Types

| Message Type | Direction | Purpose |
|--------------|-----------|---------|
| Join Game | Client → Server | Request to join a game |
| Game Ready | Server → Client | Confirm game is ready |
| Get Action | Server → Client | Request action from agent |
| Action | Client → Server | Send chosen action |
| Results | Server → Client | Send game results |
| Ready Next | Client → Server | Ready for next round | 