# System Architecture (PlantUML)

## High-Level Architecture

The AGT Server follows a layered architecture pattern with clear separation of concerns.

.. plantuml::

   @startuml
   !theme plain
   
   package "Client Layer" {
     [Student Client 1]
     [Student Client 2]
     [Student Client N]
   }
   
   package "Server Layer" {
     [AGTServer]
     [Engine]
   }
   
   package "Game Layer" {
     [RPS Game]
     [BOS Game]
     [Chicken Game]
     [Lemonade Game]
     [Auction Game]
   }
   
   package "Agent Layer" {
     [Q-Learning Agent]
     [Fictitious Play Agent]
     [Random Agent]
     [Custom Agent]
   }
   
   [Student Client 1] --> [AGTServer]
   [Student Client 2] --> [AGTServer]
   [Student Client N] --> [AGTServer]
   [AGTServer] --> [Engine]
   [Engine] --> [RPS Game]
   [Engine] --> [BOS Game]
   [Engine] --> [Chicken Game]
   [Engine] --> [Lemonade Game]
   [Engine] --> [Auction Game]
   [RPS Game] --> [Q-Learning Agent]
   [BOS Game] --> [Fictitious Play Agent]
   [Chicken Game] --> [Random Agent]
   [Lemonade Game] --> [Custom Agent]
   
   @enduml

## Server Components

The main server components and their responsibilities:

.. plantuml::

   @startuml
   !theme plain
   
   package "AGTServer" {
     [Connection Manager]
     [Game Manager]
     [Player Manager]
     [Results Manager]
   }
   
   package "Engine" {
     [Game Coordinator]
     [Action Collector]
     [Reward Distributor]
   }
   
   [Connection Manager] --> [Game Manager]
   [Game Manager] --> [Player Manager]
   [Player Manager] --> [Results Manager]
   [Game Manager] --> [Game Coordinator]
   [Game Coordinator] --> [Action Collector]
   [Action Collector] --> [Reward Distributor]
   
   @enduml

## Data Flow

How data flows through the system:

.. plantuml::

   @startuml
   !theme plain
   
   [Client Request] --> [Server Validation]
   [Server Validation] --> [Game Engine]
   [Game Engine] --> [Agent Processing]
   [Agent Processing] --> [Game Logic]
   [Game Logic] --> [Result Calculation]
   [Result Calculation] --> [Response to Client]
   
   @enduml

## Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| AGTServer | Client connection management, game session coordination |
| Engine | Game execution, action collection, reward distribution |
| BaseGame | Game state management, rule enforcement |
| BaseAgent | Action selection, learning, state tracking |
| Stage | Multi-phase game management | 