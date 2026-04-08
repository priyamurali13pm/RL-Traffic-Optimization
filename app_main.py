import numpy as np
import random
import matplotlib.pyplot as plt
import time
from q_learning import QLearningAgent


def display_traffic(traffic, action):
    print("\n--- Traffic State ---")
    
    for i in range(len(traffic)):
        cars = "🚗" * traffic[i]
        marker = " ← GREEN" if i == action else ""
        print(f"Lane {i}: {cars}{marker}")

NUM_LANES = 4
MAX_CARS = 10

def get_state(traffic):
    return tuple(traffic)

def step(traffic, action):
    # cars pass in selected lane
    cars_passed = min(traffic[action], 1)
    traffic[action] -= cars_passed

    # new cars arrive randomly
    for i in range(NUM_LANES):
        traffic[i] += random.randint(2, 4)


    # reward = less total traffic is better
    traffic = [max(0, t) for t in traffic]
    traffic = [min(t, 20) for t in traffic]

    reward = -(sum(traffic) - (max(traffic)) * 3)
    reward += -1
    
    return traffic, reward

# Initialize
agent = QLearningAgent(state_size=NUM_LANES, action_size=NUM_LANES)


# Training
EPISODES = 1500
episode_rewards = []

for ep in range(EPISODES):
    traffic = [random.randint(0, MAX_CARS) for _ in range(NUM_LANES)]
    
    total_reward = 0   # 👈 ADD THIS
    
    for step_num in range(50):
        state = get_state(traffic)
        
        action = agent.choose_action(state)
        
        next_traffic, reward = step(traffic.copy(), action)
        next_state = get_state(next_traffic)
        
        agent.learn(state, action, reward, next_state)
        
        traffic = next_traffic
        total_reward += reward   # 👈 ADD THIS
    
    episode_rewards.append(total_reward)  # 👈 ADD THIS
    
    agent.decay_epsilon()

print("Training complete!")
print("State:", state, "Action:", action, "Reward:", reward)
agent.epsilon = 0
print("Sample Q-values:", list(agent.q_table.items())[:3])
print("First 5 episode rewards:", episode_rewards[:5])

# Evaluation
def run_random():
    traffic = [random.randint(0, MAX_CARS) for _ in range(NUM_LANES)]
    total = 0
    
    for _ in range(50):
        action = random.randint(0, NUM_LANES - 1)
        traffic, reward = step(traffic, action)
        total += reward
    
    return total

def run_qlearning():
    traffic = [random.randint(0, MAX_CARS) for _ in range(NUM_LANES)]
    total = 0
    
    for _ in range(20):   # smaller steps for display
        state = get_state(traffic)

        if state not in agent.q_table:
            action = random.randint(0, NUM_LANES - 1)
        else:
            action = np.argmax(agent.q_table[state])

        display_traffic(traffic, action)   # 👈 ADD HERE
        time.sleep(0.5)
        
        traffic, reward = step(traffic, action)
        total += reward

    return total

random_scores = [run_random() for _ in range(10)]
q_scores = [run_qlearning() for _ in range(10)]

print("\n--- Comparison ---")
print("Random Avg:", np.mean(random_scores))
print("Q-learning Avg:", np.mean(q_scores))

improvement = np.mean(q_scores) - np.mean(random_scores)
print("Improvement:", improvement)

score = (np.mean(q_scores) - np.mean(random_scores)) / abs(np.mean(random_scores))
score = max(0, min(score, 1))  # keep between 0 and 1

print("Score (0-1):", score)

smoothed = np.convolve(episode_rewards, np.ones(50)/50, mode='valid')


plt.figure()
plt.plot(smoothed)
plt.xlabel("Episodes")
plt.ylabel("Total Reward")
plt.title("Smoothed Learning Curve")
plt.savefig("smoothed_plot.png")
print("Graph saved as training_plot.png")
plt.show()