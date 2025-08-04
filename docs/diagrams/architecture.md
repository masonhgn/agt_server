# System Architecture

## High-Level Architecture

The AGT Server follows a layered architecture pattern with clear separation of concerns.

```mermaid
graph TB
    subgraph "Client Layer"
        C1[Student Client 1]
        C2[Student Client 2]
        C3[Student Client N]
    end
    
    subgraph "Server Layer"
        S[AGTServer]
        E[Engine]
    end
    
    subgraph "Game Layer"
        G1[RPS Game]
        G2[BOS Game]
        G3[Chicken Game]
        G4[Lemonade Game]
        G5[Auction Game]
    end
    
    subgraph "Agent Layer"
        A1[Q-Learning Agent]
        A2[Fictitious Play Agent]
        A3[Random Agent]
        A4[Custom Agent]
    end
    
    C1 --> S
    C2 --> S
    C3 --> S
    S --> E
    E --> G1
    E --> G2
    E --> G3
    E --> G4
    E --> G5
    G1 --> A1
    G2 --> A2
    G3 --> A3
    G4 --> A4
```

## Server Components

The main server is composed of several key components:

```mermaid
graph LR
    subgraph "AGTServer"
        S1[Connection Manager]
        S2[Game Manager]
        S3[Player Manager]
        S4[Results Manager]
    end
    
    subgraph "Engine"
        E1[Game Coordinator]
        E2[Action Collector]
        E3[Reward Distributor]
    end
    
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S2 --> E1
    E1 --> E2
    E2 --> E3
```

## Data Flow

How data flows through the system:

```mermaid
graph TD
    A[Client Request] --> B[Server Validation]
    B --> C[Game Engine]
    C --> D[Agent Processing]
    D --> E[Game Logic]
    E --> F[Result Calculation]
    F --> G[Response to Client]
```

## Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| AGTServer | Client connection management, game session coordination |
| Engine | Game execution, action collection, reward distribution |
| BaseGame | Game state management, rule enforcement |
| BaseAgent | Action selection, learning, state tracking |
| Stage | Multi-phase game management | 