import random
import numpy as np
from core.agents.common.base_agent import BaseAgent

class UniformPolicy:
    """Uniform random policy for exploration."""
    def __init__(self, num_actions: int):
        self.num_actions = num_actions
    def get_move(self, state):
        """Return a random action."""
        return random.randint(0, self.num_actions - 1)

class QLearningAgent(BaseAgent):
    """
    Base Q-Learning agent that can be extended for specific games.
    Implements the core Q-learning algorithm:
    Q(s, a) = Q(s, a) + alpha[r + gamma max_{a'} Q(s', a') - Q(s, a)]
    """
    def __init__(self, name: str, num_states: int, num_actions: int, 
                 learning_rate: float = 0.1, discount_factor: float = 0.9, 
                 exploration_rate: float = 0.1, training_mode: bool = True,
                 save_path: str | None = None):
        super().__init__(name)
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.training_mode = training_mode
        self.save_path = save_path
        # Current state and action
        self.current_state = 0
        self.current_action = None
        self.next_state = None
        # Initialize Q-table
        self.q_table = self._initialize_q_table()
        # Training policy for exploration
        self.training_policy = UniformPolicy(num_actions)
        # Choose initial action
        self.current_action = self._choose_action(self.current_state)
    def _initialize_q_table(self):
        """Initialize Q-table with random values."""
        loaded_table = self._load_q_table()
        if loaded_table is not None:
            return loaded_table
        else:
            # Initialize with random values between -1 and 1
            return np.random.uniform(-1, 1, (self.num_states, self.num_actions))
    def _load_q_table(self):
        """Load Q-table from file if it exists."""
        try:
            if self.save_path:
                return np.load(self.save_path)
        except FileNotFoundError:
            pass
        return None
    def _save_q_table(self):
        """Save Q-table to file."""
        if self.save_path and self.q_table is not None:
            np.save(self.save_path, self.q_table)
    def _choose_action(self, state):
        """Choose action using epsilon-greedy policy."""
        if self.training_mode and random.random() < self.exploration_rate:
            # Exploration: choose random action
            return self.training_policy.get_move(state)
        else:
            # Exploitation: choose best action
            return np.argmax(self.q_table[state])
    def determine_state(self):
        """
        Determine the current state based on game history.
        This should be implemented by subclasses.
        """
        raise NotImplementedError
    def get_action(self, obs):
        """Return the current action."""
        action = self.current_action
        self.action_history.append(action)
        return action
    def update(self, reward: float, info=None):
        """Update Q-table using Q-learning update rule."""
        self.reward_history.append(reward)
        # Determine next state
        self.next_state = self.determine_state()
        # Q-learning update rule
        # Q(s, a) = Q(s, a) + alpha[r + gamma max_{a'} Q(s', a') - Q(s, a)]
        if self.q_table is not None and self.current_action is not None:
            current_q = self.q_table[self.current_state, self.current_action]
            max_next_q = np.max(self.q_table[self.next_state])
            new_q = current_q + self.learning_rate * (
                reward + self.discount_factor * max_next_q - current_q
            )
            self.q_table[self.current_state, self.current_action] = new_q
        # Update state and choose next action
        self.current_state = self.next_state
        self.current_action = self._choose_action(self.current_state)
        # Save Q-table if needed
        if self.save_path:
            self._save_q_table()
    def set_training_mode(self, training_mode: bool):
        """Set whether the agent is in training mode."""
        self.training_mode = training_mode
    def get_q_table(self):
        """Get the current Q-table."""
        return self.q_table.copy()
    def set_q_table(self, q_table):
        """Set the Q-table (useful for loading pre-trained models)."""
        if q_table is not None:
            self.q_table = q_table.copy() 