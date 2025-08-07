# Core Concepts

This section explains the fundamental concepts that underlie the AGT lab system, helping you understand the "why" behind the "how."

## What is Algorithmic Game Theory?

Algorithmic Game Theory (AGT) combines:
- **Game Theory**: The study of strategic interactions between rational agents
- **Computer Science**: Algorithms and computational methods
- **Economics**: Market mechanisms and resource allocation

The AGT system provides a hands-on way to learn these concepts through programming and experimentation.

## Key Game Theory Concepts

### 1. Strategic Interactions

In game theory, players make decisions that affect each other's outcomes. The AGT system models these interactions through:

- **Simultaneous Games**: Players choose actions at the same time (like Rock Paper Scissors)
- **Sequential Games**: Players take turns (like chess)
- **Repeated Games**: The same game is played multiple times

### 2. Nash Equilibrium

A Nash equilibrium occurs when no player can improve their outcome by changing their strategy, given what other players are doing.

**Example**: In Rock Paper Scissors, playing each action with 1/3 probability is a Nash equilibrium because no player can do better by changing their strategy.

### 3. Best Response

A best response is the optimal action given what you believe other players will do.

**Example**: If you think your opponent will play Rock 70% of the time, your best response is to play Paper.

## Learning Paradigms

### 1. Reinforcement Learning

Agents learn by trying actions and observing rewards:

```
Action → Environment → Reward → Update Strategy
```

**Key Concepts:**
- **Exploration vs Exploitation**: Balance trying new things with using what works
- **Value Functions**: Estimate the long-term value of actions
- **Policy**: The strategy for choosing actions

### 2. Fictitious Play

Agents learn by observing opponent behavior and playing best responses:

```
Observe Opponent → Update Beliefs → Play Best Response
```

**Key Concepts:**
- **Belief Updating**: Track opponent's action frequencies
- **Best Response**: Choose action that maximizes expected payoff
- **Convergence**: Strategies may converge to Nash equilibrium

### 3. Multi-Agent Learning

Multiple agents learning simultaneously creates complex dynamics:

- **Emergent Behavior**: Collective behavior that emerges from individual strategies
- **Coordination**: Agents learning to work together
- **Competition**: Agents learning to outperform each other

## System Architecture Concepts

### 1. Modular Design

The AGT system is built with modularity in mind:

```
Games ← Engine → Agents
  ↓       ↓        ↓
Stages ← Server → Results
```

**Benefits:**
- **Extensibility**: Easy to add new games and agents
- **Maintainability**: Changes in one component don't affect others
- **Testability**: Each component can be tested independently

### 2. Distributed Architecture

The system supports distributed execution:

```
Student Machine → Network → Server → Game Engine
     ↓              ↓         ↓         ↓
   Agent ← Results ← Server ← Engine ← Game
```

**Benefits:**
- **Scalability**: Multiple students can compete simultaneously
- **Reliability**: Server handles coordination and state management
- **Accessibility**: Students can connect from anywhere

### 3. Real-Time Interaction

The system provides real-time game interactions:

- **Low Latency**: Quick response times for interactive learning
- **State Synchronization**: All players see the same game state
- **Immediate Feedback**: Instant rewards and observations

## Educational Design Principles

### 1. Progressive Complexity

Labs build from simple to complex concepts:

1. **Lab 01**: Basic game theory (matrix games)
2. **Lab 02**: State-based strategies (finite state machines)
3. **Lab 03**: Learning algorithms (Q-learning)
4. **Lab 04**: Spatial competition (location games)
5. **Lab 06**: Mechanism design (auctions)

### 2. Hands-On Learning

Students learn by doing:

- **Implementation**: Write actual algorithms
- **Experimentation**: Test different strategies
- **Competition**: Compete against other students
- **Analysis**: Analyze results and improve

### 3. Immediate Feedback

The system provides instant feedback:

- **Real-time Results**: See how your agent performs immediately
- **Comparative Analysis**: Compare against other strategies
- **Iterative Improvement**: Make changes and test again

## Computational Concepts

### 1. State Representation

Games are represented as states that agents can observe:

```python
# Matrix game state (simple)
state = {}  # Often empty for simple games

# Spatial game state (complex)
state = {
    "locations": [0, 1, 2, 3],
    "opponent_positions": [1, 3],
    "customer_distribution": {...}
}
```

### 2. Action Spaces

Different games have different action spaces:

```python
# Discrete actions (matrix games)
actions = [0, 1, 2]  # Rock, Paper, Scissors

# Continuous actions (auctions)
actions = [5.2, 8.7]  # Bid amounts
```

### 3. Reward Functions

Rewards guide learning:

```python
# Zero-sum game (matrix games)
reward_player_1 = -reward_player_2

# General-sum game (spatial games)
reward_player_1 = f(location_1, location_2, customers)
reward_player_2 = g(location_1, location_2, customers)
```

## Research Applications

The AGT system enables research in:

### 1. Multi-Agent Systems

- **Coordination**: How agents learn to work together
- **Competition**: How agents learn to outperform others
- **Emergence**: How complex behavior emerges from simple rules

### 2. Mechanism Design

- **Auction Design**: Creating fair and efficient auction mechanisms
- **Market Design**: Designing markets that work well
- **Resource Allocation**: Allocating resources efficiently

### 3. Machine Learning

- **Multi-Agent Reinforcement Learning**: Learning in competitive environments
- **Adversarial Learning**: Learning against adaptive opponents
- **Federated Learning**: Learning across distributed agents

## Practical Applications

The concepts learned in AGT labs apply to:

### 1. Economics

- **Market Design**: Designing markets for goods and services
- **Auction Theory**: Understanding bidding strategies
- **Game Theory**: Analyzing strategic interactions

### 2. Computer Science

- **Distributed Systems**: Coordinating multiple agents
- **Artificial Intelligence**: Creating intelligent agents
- **Algorithm Design**: Designing efficient algorithms

### 3. Social Sciences

- **Behavioral Economics**: Understanding human decision-making
- **Political Science**: Analyzing voting systems
- **Sociology**: Understanding group dynamics

## Next Steps

Understanding these core concepts will help you:

1. **Design Better Agents**: Use game theory principles to create effective strategies
2. **Analyze Results**: Understand why certain strategies work better than others
3. **Extend the System**: Add new games and learning algorithms
4. **Apply Knowledge**: Use these concepts in real-world applications

The AGT system provides a unique opportunity to learn these concepts through hands-on experimentation and competition. 