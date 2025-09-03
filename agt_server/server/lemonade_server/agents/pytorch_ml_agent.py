import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from core.agents.common.base_agent import BaseAgent

class LemonadeMLAgent(BaseAgent):
    """PyTorch-based machine learning agent for the Lemonade Stand game"""
    
    def __init__(self, name: str = "PyTorchML"):
        super().__init__(name)
        self.positions = list(range(12))  # 12 possible positions (0-11)
        
        # Neural network parameters
        self.input_size = 36  # 12 positions * 3 players (including self)
        self.hidden_size = 64
        self.output_size = 12  # 12 possible actions
        
        # Create neural network
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = self._create_network().to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        
        # Experience replay buffer
        self.memory = deque(maxlen=1000)
        self.batch_size = 32
        
        # Exploration parameters
        self.epsilon = 0.1  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        # Game state tracking
        self.last_state = None
        self.last_action = None
        self.opponent_history = deque(maxlen=10)  # Track last 10 opponent moves
        
    def _create_network(self):
        """Create the neural network architecture"""
        return nn.Sequential(
            nn.Linear(self.input_size, self.hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(self.hidden_size, self.hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(self.hidden_size, self.output_size),
            nn.Softmax(dim=1)
        )
    
    def _encode_state(self, opponent_positions=None):
        """Encode the current game state as a feature vector"""
        # Create a feature vector representing the game state
        state = np.zeros(self.input_size)
        
        # Encode opponent positions (if available)
        if opponent_positions and len(opponent_positions) >= 2:
            opp1_pos = opponent_positions[0] if len(opponent_positions) > 0 else 0
            opp2_pos = opponent_positions[1] if len(opponent_positions) > 1 else 0
            
            # One-hot encode opponent positions (positions 0-11)
            if 0 <= opp1_pos < 12:
                state[opp1_pos] = 1.0
            if 0 <= opp2_pos < 12:
                state[opp2_pos + 12] = 1.0
        
        # Encode our last action (if available)
        if self.action_history:
            last_action = self.action_history[-1]
            if 0 <= last_action < 12:
                state[last_action + 24] = 1.0
        
        # Add some opponent pattern information
        if len(self.opponent_history) >= 2:
            # Add frequency of recent opponent moves
            for pos in range(12):
                freq = sum(1 for move in self.opponent_history if move == pos) / len(self.opponent_history)
                state[pos + 24] = freq
        
        return torch.FloatTensor(state).unsqueeze(0).to(self.device)
    
    def _get_q_values(self, state):
        """Get Q-values for all actions given a state"""
        with torch.no_grad():
            q_values = self.network(state)
        return q_values.squeeze(0)
    
    def _choose_action(self, q_values, training=True):
        """Choose action based on Q-values and exploration"""
        if training and random.random() < self.epsilon:
            # Exploration: choose random action
            return random.choice(self.positions)
        else:
            # Exploitation: choose best action
            return q_values.argmax().item()
    
    def _calculate_reward(self, my_action, opponent_positions, my_utility):
        """Calculate a shaped reward based on game outcome"""
        if not opponent_positions or len(opponent_positions) < 2:
            return my_utility
        
        # Calculate distances to opponents
        opp1_pos = opponent_positions[0]
        opp2_pos = opponent_positions[1]
        
        # Circular distance calculation
        def circular_distance(pos1, pos2):
            direct = abs(pos1 - pos2)
            return min(direct, 12 - direct)
        
        dist_to_opp1 = circular_distance(my_action, opp1_pos)
        dist_to_opp2 = circular_distance(my_action, opp2_pos)
        
        # Reward shaping: prefer positions that are not too close to opponents
        # but also not too far (to avoid being isolated)
        min_dist = min(dist_to_opp1, dist_to_opp2)
        max_dist = max(dist_to_opp1, dist_to_opp2)
        
        # Bonus for being at optimal distance (not too close, not too far)
        distance_bonus = 0
        if 2 <= min_dist <= 4:  # Good distance from closest opponent
            distance_bonus = 1.0
        elif min_dist <= 1:  # Too close
            distance_bonus = -1.0
        
        return my_utility + distance_bonus
    
    def _train_network(self):
        """Train the network on a batch of experiences"""
        if len(self.memory) < self.batch_size:
            return
        
        # Sample batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states = torch.cat([exp['state'] for exp in batch])
        actions = torch.LongTensor([exp['action'] for exp in batch])
        rewards = torch.FloatTensor([exp['reward'] for exp in batch])
        next_states = torch.cat([exp['next_state'] for exp in batch])
        
        # Current Q-values
        current_q_values = self.network(states)
        current_q = current_q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Next Q-values (for target calculation)
        with torch.no_grad():
            next_q_values = self.network(next_states)
            next_q = next_q_values.max(1)[0]
        
        # Target Q-values
        target_q = rewards + 0.95 * next_q  # Discount factor of 0.95
        
        # Compute loss and update
        loss = self.criterion(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def get_action(self, opponent_positions=None):
        """Choose the next action using the neural network"""
        # Encode current state
        state = self._encode_state(opponent_positions)
        
        # Get Q-values for all actions
        q_values = self._get_q_values(state)
        
        # Choose action
        action = self._choose_action(q_values, training=True)
        
        # Store for training
        self.last_state = state
        self.last_action = action
        
        return action
    
    def update(self, reward: float, info=None):
        """Update the agent with the reward and train the network"""
        super().update(reward, info)
        
        # Extract opponent positions from info if available
        opponent_positions = None
        if info and 'actions' in info:
            actions = info['actions']
            if len(actions) >= 3:
                # Get opponent positions (assuming we're player 0)
                opponent_positions = [actions[1], actions[2]]
                
                # Update opponent history
                for pos in opponent_positions:
                    self.opponent_history.append(pos)
        
        # Cclculate shaped reward
        shaped_reward = self._calculate_reward(
            self.last_action, 
            opponent_positions, 
            reward
        )
        
        # Store experience in memory
        if self.last_state is not None and self.last_action is not None:
            next_state = self._encode_state(opponent_positions)
            self.memory.append({
                'state': self.last_state,
                'action': self.last_action,
                'reward': shaped_reward,
                'next_state': next_state
            })
        
        # Train the network
        self._train_network()
    
    def setup(self):
        """Initialize for a new game"""
        super().setup()
        # Reset opponent history for new game
        self.opponent_history.clear()
    
    def reset(self):
        """Reset the agent for a new game"""
        super().reset()
        self.opponent_history.clear()
        self.last_state = None
        self.last_action = None

# Export for the competition
agent_submission = LemonadeMLAgent("PyTorchML")
