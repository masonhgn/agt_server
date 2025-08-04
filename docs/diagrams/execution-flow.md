# Execution Flow

## Game Session Sequence

The typical flow of a game session:

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant E as Engine
    participant G as Game
    participant A as Agent
    
    C->>S: Connect
    S->>C: Confirm connection
    C->>S: Join game
    S->>E: Create game
    E->>G: Initialize
    G->>E: Initial state
    E->>C: Game ready
    
    loop Game rounds
        E->>C: Send observation
        C->>A: Get action
        A->>C: Return action
        C->>E: Send action
        E->>G: Step game
        G->>E: New state
        E->>C: Send results
    end
    
    E->>S: Game complete
    S->>C: Final results
```

## Tournament Management

How tournaments are managed:

```mermaid
graph TD
    T1[Start Tournament] --> T2[Match Players]
    T2 --> T3[Run Games]
    T3 --> T4[Collect Results]
    T4 --> T5{More Matches?}
    T5 -->|Yes| T2
    T5 -->|No| T6[Calculate Rankings]
    T6 --> T7[Save Results]
```

## Game Round Flow

Detailed flow of a single game round:

```mermaid
graph TD
    R1[Round Start] --> R2[Send Observations]
    R2 --> R3[Collect Actions]
    R3 --> R4[Process Game Logic]
    R4 --> R5[Calculate Rewards]
    R5 --> R6[Update Agents]
    R6 --> R7{Game Done?}
    R7 -->|No| R1
    R7 -->|Yes| R8[End Game]
```

## Error Handling

How the system handles various error conditions:

```mermaid
graph TD
    E1[Error Occurs] --> E2{Error Type?}
    E2 -->|Timeout| E3[Use Default Action]
    E2 -->|Invalid Action| E4[Reject Action]
    E2 -->|Connection Lost| E5[Disconnect Player]
    E2 -->|Game Error| E6[End Game Early]
    
    E3 --> E7[Continue Game]
    E4 --> E8[Request New Action]
    E5 --> E9[Notify Other Players]
    E6 --> E10[Save Partial Results]
    
    E7 --> E11[Log Error]
    E8 --> E11
    E9 --> E11
    E10 --> E11
```

## Performance Monitoring

Metrics collection during execution:

```mermaid
graph TD
    P1[Game Execution] --> P2[Collect Metrics]
    P2 --> P3[Response Times]
    P2 --> P4[Action Frequencies]
    P2 --> P5[Reward Distributions]
    P2 --> P6[Error Rates]
    
    P3 --> P7[Performance Analysis]
    P4 --> P7
    P5 --> P7
    P6 --> P7
    
    P7 --> P8[Generate Reports]
    P8 --> P9[Save to Results]
```

## Communication Protocol

Message flow between client and server:

```mermaid
graph LR
    A[Client] -->|Join Game| B[Server]
    B -->|Game Ready| A
    A -->|Get Action| B
    B -->|Observation| A
    A -->|Action| B
    B -->|Results| A
    A -->|Ready Next| B
    B -->|Next Round| A
```

## Message Types

| Message Type | Direction | Purpose |
|--------------|-----------|---------|
| Join Game | Client → Server | Request to join a game |
| Game Ready | Server → Client | Confirm game is ready |
| Get Action | Server → Client | Request action from agent |
| Action | Client → Server | Send chosen action |
| Results | Server → Client | Send game results |
| Ready Next | Client → Server | Ready for next round | 