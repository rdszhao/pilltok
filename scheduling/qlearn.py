import numpy as np

num_medications = 2
times_per_day = 2
num_states = num_medications * times_per_day + 1  # Plus 1 for the state when all meds have been taken

num_actions = 2  # two possible actions: 0 (no reminder sent) or 1 (reminder sent)

# initialize q-table with zeros
q_table = np.zeros((num_states, num_actions))

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.1  # Exploration rate

# Simulation parameters
num_episodes = 1000  # Total number of simulation episodes
max_steps_per_episode = 4  # Maximum steps in an episode, assuming 2 times per day

# Function to choose an action based on the current state
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        # explore
        return np.random.choice([0, 1])
    else:
        # exploit
        return np.argmax(q_table[state])

# Function to update the Q-table
def update_q_table(state, action, reward, next_state):
    old_value = q_table[state, action]
    next_max = np.max(q_table[next_state])
    new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
    q_table[state, action] = new_value

# learning loop
for episode in range(num_episodes):
    state = 0
    done = False
    total_reward = 0

    for step in range(max_steps_per_episode):
        action = choose_action(state)

        # Take the action and observe the new state and reward
        # This is where the app logic would determine the new state and reward
        # For simplicity, we'll assume a random binary reward indicating medication was taken or missed
        reward = np.random.choice([-1, 1])  # This should be based on actual adherence response
        next_state = state + 1 if reward == 1 else state  # Move to the next state only if medication was taken

        # Update Q-Table
        update_q_table(state, action, reward, next_state)

        state = next_state  # Transition to the next state
        total_reward += reward

        if state == num_states - 1:  # All medications taken for the day
            break

    # Optional: Add logic to handle the end of the episode, such as logging

# After training, you can inspect the Q-table to see learned values
print(q_table)