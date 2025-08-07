# Test Diagram

This is a simple test to verify Graphviz rendering works.

## Simple Test Diagram

.. graphviz::

   digraph Test {
     A [label="Start"];
     B [label="Process"];
     C [label="End"];
     
     A -> B;
     B -> C;
   }

## System Overview (Simple)

.. graphviz::

   digraph System {
     rankdir=TB;
     
     Client [label="Client"];
     Server [label="Server"];
     Game [label="Game"];
     
     Client -> Server;
     Server -> Game;
   } 