import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.q_table = {}
        
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.8
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)

        if random.uniform(0,1) < self.epsilon:
            return random.randint(0, self.action_size - 1)

        return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.action_size)

        best_next = np.max(self.q_table[next_state])

        # ✅ FIXED LINE
        #self.q_table[state][action] += self.alpha * (
        #    reward + self.gamma * best_next - self.q_table[state][action]
        #)

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

