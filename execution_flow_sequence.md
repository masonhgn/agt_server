# AGT System Execution Flow

## Detailed Sequence Diagram

This diagram shows the actual execution flow of the AGT system, from server startup through game execution to result collection.

```mermaid
sequenceDiagram
    participant S as AGTServer
    participant E as Engine
    participant G as Game
    participant A as Agent
    participant C as Client
    participant R as Results
    
    Note over S,R: Server Startup Phase
    S->>S: Initialize with config
    S->>S: Load game configurations
    S->>S: Setup logging and results dir
    S->>S: Start listening on port
    
    Note over S,R: Client Connection Phase
    C->>S: Connect to server
    S->>S: Create PlayerConnection
    S->>C: Send connection confirmation
    
    Note over S,R: Game Setup Phase
    C->>S: Join game request
    S->>S: Match players for game
    S->>E: Create Engine with game type
    E->>G: Initialize game instance
    G->>G: Reset game state
    G->>E: Return initial observations
    E->>S: Game ready for players
    
    Note over S,R: Game Execution Loop
    loop For each round
        S->>C: Send observation to client
        C->>A: Get action from agent
        A->>A: Process observation
        A->>C: Return action
        C->>S: Send action to server
        
        S->>E: Collect all player actions
        E->>G: Step game with actions
        G->>G: Process game logic
        G->>E: Return new state, rewards, done
        E->>S: Update game state
        
        S->>C: Send results to clients
        C->>A: Update agent with reward
        A->>A: Learn from experience
        
        alt Game not finished
            S->>C: Continue to next round
        else Game finished
            S->>R: Save game results
            S->>C: Send final results
        end
    end
    
    Note over S,R: Tournament Management
    S->>S: Check if tournament complete
    S->>R: Aggregate tournament results
    S->>C: Send tournament rankings
```

## Game-Specific Execution Flows

### Rock Paper Scissors (RPS) Flow

```mermaid
graph TD
    A[Game Start] --> B[Initialize 2 players]
    B --> C[Reset game state]
    C --> D[Send initial observation]
    D --> E[Player 1 chooses action]
    D --> F[Player 2 chooses action]
    E --> G[Collect actions]
    F --> G
    G --> H[Determine winner]
    H --> I[Calculate rewards]
    I --> J[Update agents]
    J --> K{More rounds?}
    K -->|Yes| D
    K -->|No| L[End game]
```

### Auction Game Flow

```mermaid
graph TD
    A[Auction Start] --> B[Initialize bidders]
    B --> C[Present items/bundles]
    C --> D[Collect bids]
    D --> E[Process auction algorithm]
    E --> F[Determine winners]
    F --> G[Calculate payments]
    G --> H[Update agent utilities]
    H --> I{More rounds?}
    I -->|Yes| C
    I -->|No| J[End auction]
```

### Lemonade Stand Flow

```mermaid
graph TD
    A[Lemonade Start] --> B[Initialize players]
    B --> C[Set up locations]
    C --> D[Players choose locations]
    D --> E[Calculate distances]
    E --> F[Determine customer flow]
    F --> G[Calculate profits]
    G --> H[Update agent strategies]
    H --> I{More rounds?}
    I -->|Yes| C
    I -->|No| J[End game]
```

## Agent Learning Patterns

### Q-Learning Agent (Lab03)

```mermaid
graph TD
    A[Agent receives observation] --> B[Convert to state]
    B --> C[Select action using ε-greedy]
    C --> D[Execute action]
    D --> E[Receive reward]
    E --> F[Update Q-table]
    F --> G[Store experience]
    G --> H[Next observation]
    H --> A
```

### Fictitious Play Agent (Lab01)

```mermaid
graph TD
    A[Agent receives observation] --> B[Update opponent model]
    B --> C[Calculate best response]
    C --> D[Select action]
    D --> E[Receive opponent action]
    E --> F[Update belief distribution]
    F --> G[Next round]
    G --> A
```

## Server Communication Protocol

### Message Flow

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

### Message Types

1. **Join Game**: `{"type": "join_game", "game_type": "rps"}`
2. **Get Action**: `{"type": "get_action", "observation": {...}}`
3. **Action**: `{"type": "action", "action": "rock"}`
4. **Results**: `{"type": "results", "reward": 1.0, "done": false}`
5. **Ready Next**: `{"type": "ready_next_round"}`

## Error Handling Flow

```mermaid
graph TD
    A[Error Occurs] --> B{Error Type?}
    B -->|Timeout| C[Use default action]
    B -->|Invalid Action| D[Reject action]
    B -->|Connection Lost| E[Disconnect player]
    B -->|Game Error| F[End game early]
    
    C --> G[Continue game]
    D --> H[Request new action]
    E --> I[Notify other players]
    F --> J[Save partial results]
    
    G --> K[Log error]
    H --> K
    I --> K
    J --> K
```

## Performance Monitoring

### Metrics Collection

```mermaid
graph TD
    A[Game Execution] --> B[Collect Metrics]
    B --> C[Response Times]
    B --> D[Action Frequencies]
    B --> E[Reward Distributions]
    B --> F[Error Rates]
    
    C --> G[Performance Analysis]
    D --> G
    E --> G
    F --> G
    
    G --> H[Generate Reports]
    H --> I[Save to Results]
```

This execution flow shows how the AGT system maintains a robust, scalable architecture while providing a smooth educational experience for students implementing game theory algorithms. 