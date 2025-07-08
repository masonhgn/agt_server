# CS1440/2440 Lab 4: Lemonade Stand

## Introduction
Welcome to Lab 4! In this lab, you'll be competing in the Lemonade Stand Game, a 3-player strategic game where you'll set up your lemonade stand at different positions on a circular board. You'll develop agents using both traditional game theory techniques and reinforcement learning methods learned in the previous labs.

## Game Rules

### Lemonade Stand Game
The Lemonade Stand Game is a 3-player simultaneous-move game where each player chooses a position from 0 to 11 on a circular board (think of it as a clock face).

**Payoff Structure:**
- **All three players choose the same position**: Each player gets 8 points
- **Two players choose the same position**: The two players each get 6 points, the third player gets 12 points
- **All players choose different positions**: The player in the "middle" gets the most points

**Middle Player Calculation:**
When all three players choose different positions, the payoffs are calculated as follows:
1. Sort the three positions in ascending order: [a, b, c]
2. The player at position `a` gets: (b - a) + (12 + a - c)
3. The player at position `b` gets: (b - a) + (c - b)
4. The player at position `c` gets: (c - b) + (12 + a - c)

### Example Scenarios
- Players choose [5, 5, 5]: All get 8 points
- Players choose [3, 3, 7]: Players at 3 get 6 points each, player at 7 gets 12 points
- Players choose [2, 5, 8]: Player at 2 gets 7 points, player at 5 gets 6 points, player at 8 gets 11 points

## Assignment Overview

You have two main tasks:

### Task 1: Non-Reinforcement Learning Agent
Implement a strategic agent that doesn't use reinforcement learning. You can use techniques like:
- Fictitious Play
- Best Response
- Pattern recognition
- Game theory analysis

### Task 2: Reinforcement Learning Agent
Implement a Q-Learning agent that learns optimal strategies through experience. You'll need to:
- Design a state representation
- Implement Q-Learning updates
- Handle exploration vs exploitation

## Files to Complete

### 1. `my_lemonade_agent.py`
This file contains the stencil for your non-RL agent. You need to:
- Complete the `get_action()` method
- Optionally modify the `setup()` and `update()` methods
- Give your agent a name

### 2. `my_rl_lemonade_agent.py`
This file contains the stencil for your RL agent. You need to:
- Complete the `determine_state()` method
- Set appropriate hyperparameters
- Give your agent a name

### 3. `q_learning.py`
This file contains a Q-Learning implementation that you can use or modify.

## Agent Interface

Your agents have access to the following methods:

### History Methods
- `self.get_action_history()` - Your action history
- `self.get_util_history()` - Your utility history
- `self.get_opp1_action_history()` - First opponent's action history
- `self.get_opp2_action_history()` - Second opponent's action history
- `self.get_opp1_util_history()` - First opponent's utility history
- `self.get_opp2_util_history()` - Second opponent's utility history

### Last Round Methods
- `self.get_last_action()` - Your last action
- `self.get_last_util()` - Your last utility
- `self.get_opp1_last_action()` - First opponent's last action
- `self.get_opp2_last_action()` - Second opponent's last action
- `self.get_opp1_last_util()` - First opponent's last utility
- `self.get_opp2_last_util()` - Second opponent's last utility

### Utility Calculation
- `self.calculate_utils(a1, a2, a3)` - Calculate utilities for three actions

## Testing Your Agents

### Local Testing
Run your agents locally to test against provided opponents:
```bash
python my_lemonade_agent.py
python my_rl_lemonade_agent.py
```

### Training the RL Agent
The RL agent will automatically train for 100,000 rounds before testing. You can modify the training parameters in the main section.

## Evaluation

Your agents will be evaluated on:
1. **Performance**: Average utility against various opponent types
2. **Strategy**: Quality of decision-making and adaptation
3. **Code Quality**: Clean, well-documented implementation

## Tips for Success

1. **Understand the Game**: The key insight is that being in the middle of your opponents is often optimal
2. **State Design**: For RL, consider what information is most relevant for decision-making
3. **Exploration**: Balance exploration and exploitation in your RL agent
4. **Pattern Recognition**: Look for patterns in opponent behavior
5. **Testing**: Test against different types of opponents to ensure robustness

## Submission

Submit both completed agent files:
- `my_lemonade_agent.py`
- `my_rl_lemonade_agent.py`

Make sure your agents have proper names and are ready for competition!

Good luck, and may the best lemonade stand win! 