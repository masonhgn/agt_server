# Agent System

## Agent Hierarchy

All agents inherit from the BaseAgent abstract class:

```
BaseAgent (Abstract)
├── QLearningAgent
├── FictitiousPlayAgent
├── RandomAgent
├── StubbornAgent
└── CompromiseAgent

Interface Methods:
├── get_action()
├── update()
└── reset()
```

## Learning Strategies

### Q-Learning (Lab03)

Reinforcement learning approach for repeated games:

```
Observe State → Select Action → Execute Action → Receive Reward → Update Q-Table → (loop)
```

### Fictitious Play (Lab01)

Belief-based learning approach:

```
Observe Opponent → Update Beliefs → Calculate Best Response → Select Action → (loop)
```

## Lab-Specific Agents

### Lab01: Basic Game Theory

```
Lab01 Agents:
├── Rock Agent
├── Paper Agent
├── Scissors Agent
├── Random Agent
└── Stubborn Agent
```

### Lab02: Finite State Machines

```
BOS Finite State:
State A → State B → State C → State A
```

### Lab03: Q-Learning

```
Chicken Q-Learning:
State: Last Actions → Q-Table Lookup → Epsilon-Greedy Selection → Action Execution → (loop)
```

### Lab04: Reinforcement Learning

```
Lemonade RL:
Location State → Policy Network → Location Selection → Profit Calculation → (loop)
```

### Lab06: Auction Bidding

```
Auction Agent:
Item Valuation → Marginal Value → Bid Calculation → Bid Submission → (loop)
```

## Agent Characteristics

| Agent Type | Learning Method | Best For | Complexity |
|------------|-----------------|----------|------------|
| Random | None | Baseline | Low |
| Stubborn | None | Fixed strategy | Low |
| Fictitious Play | Belief updating | Matrix games | Medium |
| Q-Learning | Reinforcement | Repeated games | High |
| Custom | Various | Specific scenarios | Variable | 