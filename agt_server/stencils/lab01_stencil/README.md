# Lab 1: Repeated Games of Complete Information

This lab implements two different agent strategies for playing three different two-player games: the Prisoners' Dilemma, Rock-Paper-Scissors, and Chicken. The two agent strategies are Fictitious Play and Exponential Weights.

## Setup

1. Create a python virtual environment and activate it. Be sure to use python 3.10 or higher.
2. Run `pip install --upgrade agt server`

## Files

- `fictitious_play_stencil.py` - Implement Fictitious Play strategy
- `exponential_stencil.py` - Implement Exponential Weights strategy  
- `competition_agent.py` - Implement your competition agent for Chicken
- `example_agent.py` - Example solutions demonstrating the new architecture

## Architecture

**NEW ARCHITECTURE**: The server now calls methods directly as described in the writeup:

- **Fictitious Play agents**: The server calls `predict()` to get opponent's predicted distribution, then `optimize(dist)` to get the best response
- **Exponential Weights agents**: The server calls `calc_move_probs()` to get move probabilities, then samples from the distribution

This matches the writeup exactly: "For the former, the agt server calls the agent's predict() method, so that it can build its probability distribution, and then optimize() to solicit its next move. For the latter, the agt server calls calc_move_probs(), and then samples from this distribution to arrive at the agent's next move."

## Implementation Details

### Fictitious Play (`fictitious_play_stencil.py`)

You need to implement two methods:

1. **`predict()`**: Use the opponent's previous moves to generate a probability distribution over the opponent's next move
   - Use `self.get_opp_action_history()` to access opponent's action history
   - Return a list of 3 probabilities [p_rock, p_paper, p_scissors]

2. **`optimize(dist)`**: Use the probability distribution over the opponent's moves, along with knowledge of the payoff matrix, to calculate the best move
   - Use `self.calculate_utils(a1, a2)` to get utilities for action combinations
   - Return the best action (0=Rock, 1=Paper, 2=Scissors)

### Exponential Weights (`exponential_stencil.py`)

You need to implement one method:

1. **`calc_move_probs()`**: Use your historical average payoffs to generate a probability distribution over your next move using the Exponential Weights strategy
   - Use `self.action_rewards` and `self.action_counts` to compute averages
   - Use `self.softmax()` to convert averages to probabilities
   - Return a list of 3 probabilities [p_rock, p_paper, p_scissors]

### Competition Agent (`competition_agent.py`)

You need to implement three methods:

1. **`setup()`**: Initialize the agent for each new game
2. **`get_action()`**: Returns your agent's next action for Chicken (0=Swerve, 1=Continue)
3. **`update()`**: Updates your agent with the current history

## Available Methods

All agents have access to these helper methods:

- `self.calculate_utils(a1, a2)` - Returns [u1, u2] for actions a1 and a2
- `self.get_opp_action_history()` - Get opponent's complete action history
- `self.get_opp_last_action()` - Get opponent's last action
- `self.get_opp_last_util()` - Get opponent's last utility
- `self.get_last_action()` - Get your last action
- `self.get_last_util()` - Get your last utility
- `self.get_util_history()` - Get your complete utility history
- `self.get_action_history()` - Get your complete action history
- `self.get_reward_history()` - Get your complete reward history

## Testing

Run the stencils locally to test your implementations:

```bash
python fictitious_play_stencil.py
python exponential_stencil.py
python competition_agent.py
```

## Expected Performance

- **Fictitious Play**: Should earn payoffs of about 500–600 against TA bots over 1000 rounds
- **Exponential Weights**: Should earn payoffs of about 150-200 more than TA bots over 1000 rounds

## Games

### Rock-Paper-Scissors Payoff Matrix
```
R\C  R  P  S
R    0 -1  1
P    1  0 -1
S   -1  1  0
```

### Chicken Payoff Matrix
```
S\C  S  C
S    0 -1
C    1 -5
```
Where S = Swerve, C = Continue

## Notes

- The `get_action()` method is provided for backward compatibility but is not used in the new architecture
- The server automatically tracks opponent actions and rewards
- All agents inherit from `RPSAgent` or `ChickenAgent` which provide game-specific logic
- The new architecture ensures exact compatibility with the lab writeup 