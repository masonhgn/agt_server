# Agent System

## Agent Hierarchy

All agents inherit from the BaseAgent abstract class:

```mermaid
graph TD
    BA[BaseAgent] --> QA[QLearningAgent]
    BA --> FA[FictitiousPlayAgent]
    BA --> RA[RandomAgent]
    BA --> SA[StubbornAgent]
    BA --> CA[CompromiseAgent]
    
    subgraph "Agent Interface"
        AI1[get_action()]
        AI2[update()]
        AI3[reset()]
    end
    
    BA -.-> AI1
    BA -.-> AI2
    BA -.-> AI3
```

## Learning Strategies

### Q-Learning (Lab03)

Reinforcement learning approach for repeated games:

```mermaid
graph TD
    subgraph "Q-Learning Cycle"
        Q1[Observe State] --> Q2[Select Action]
        Q2 --> Q3[Execute Action]
        Q3 --> Q4[Receive Reward]
        Q4 --> Q5[Update Q-Table]
        Q5 --> Q1
    end
```

### Fictitious Play (Lab01)

Belief-based learning approach:

```mermaid
graph TD
    subgraph "Fictitious Play Cycle"
        F1[Observe Opponent] --> F2[Update Beliefs]
        F2 --> F3[Calculate Best Response]
        F3 --> F4[Select Action]
        F4 --> F1
    end
```

## Lab-Specific Agents

### Lab01: Basic Game Theory

```mermaid
graph LR
    subgraph "Lab01 Agents"
        L1A1[Rock Agent]
        L1A2[Paper Agent]
        L1A3[Scissors Agent]
        L1A4[Random Agent]
        L1A5[Stubborn Agent]
    end
```

### Lab02: Finite State Machines

```mermaid
graph TD
    subgraph "BOS Finite State"
        FS1[State A] --> FS2[State B]
        FS2 --> FS3[State C]
        FS3 --> FS1
    end
```

### Lab03: Q-Learning

```mermaid
graph TD
    subgraph "Chicken Q-Learning"
        CQ1[State: Last Actions] --> CQ2[Q-Table Lookup]
        CQ2 --> CQ3[Epsilon-Greedy Selection]
        CQ3 --> CQ4[Action Execution]
        CQ4 --> CQ1
    end
```

### Lab04: Reinforcement Learning

```mermaid
graph TD
    subgraph "Lemonade RL"
        LR1[Location State] --> LR2[Policy Network]
        LR2 --> LR3[Location Selection]
        LR3 --> LR4[Profit Calculation]
        LR4 --> LR1
    end
```

### Lab06: Auction Bidding

```mermaid
graph TD
    subgraph "Auction Agent"
        AA1[Item Valuation] --> AA2[Marginal Value]
        AA2 --> AA3[Bid Calculation]
        AA3 --> AA4[Bid Submission]
        AA4 --> AA1
    end
```

## Agent Characteristics

| Agent Type | Learning Method | Best For | Complexity |
|------------|-----------------|----------|------------|
| Random | None | Baseline | Low |
| Stubborn | None | Fixed strategy | Low |
| Fictitious Play | Belief updating | Matrix games | Medium |
| Q-Learning | Reinforcement | Repeated games | High |
| Custom | Various | Specific scenarios | Variable | 