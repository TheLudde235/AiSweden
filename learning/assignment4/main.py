# Begin your code here
from functions import *
import gym
import time


#TODO: Write your full name.
name = 'Your Name'
#ENDTODO

# Parameters that will create the state space. Use positive numbers, where value > 0 and < 10.
# TODO: Set the state action_space
numCartPositionBins = 10
numCartVelocityBins = 10
numAngleBins = 10
numAnglesVelocityBins = 10
#ENDTODO

# Parameters used in Q-Learning
# TODO: Set the parameters of Q-Learning
alpha = 1 # Learning rate. Value in range [0, 1].
gamma = 0.1 # Discount factor. Value in range [0, 1].
epsilon = 0.1 # Exploration probability. Value in range [0, 1].
#ENDTODO

# Parameters if we want visualization
# TODO: change this if you want visualization or not
visualization = False # True we will see the inverted pendulum. False we will not see it
speed = 1 # 1 is full speed of the visualization. With a 0, each frame will appear each 1 sec
# ENDTODO

if visualization:
    env = gym.make('CartPole-v1', render_mode="human") # We initialize the environment
else:
    env = gym.make('CartPole-v1', render_mode="rgb_array") # We initialize the environment

checkErrorsInParameters(numCartPositionBins, numCartVelocityBins, numAngleBins, numAnglesVelocityBins, alpha, gamma, epsilon) # We check the aprameters
agent = QLearningAgent(range(env.action_space.n), epsilon, gamma, alpha) # The agent is initialized

results = [] # We use this variable to save the results
for i in range(100): # This for loop is to run Q-learning 100 times
    observation = env.reset() # We obtain the information from the environment
    # observation = observation[0] # Remove this line - it was causing the issue

    for t in range(200): # The maximum timesteps tha the agent can reach
        if visualization: # if we want to visualize the cart and the pole
            env.render()
            time.sleep(1-speed) # We use this to reduce the speed.

        stateID = createState(observation, numCartPositionBins, numCartVelocityBins, numAngleBins, numAnglesVelocityBins) # We create the state depending on the observation from the environment and the number of bins that we defined

        action = agent.getAction(stateID) # We obtain which action to take

        # observation, reward, done, info = env.step(action) # Old code
        observation, reward, done, info = env.step(action)  # We apply the action

        if done: # If the action cause the pole to reach more than 15 degrees, that means that we faile
            reward = -100 # We give a really bad reward if we fail

        newStateID = createState(observation, numCartPositionBins, numCartVelocityBins, numAngleBins, numAnglesVelocityBins) # We create the new state after taking the action.

        agent.updateTable(stateID, action, newStateID, reward) # We update the Q table with the new observations and actions that we took

        if done or t == 199: # If we are done because we reached the maximum timesteps or the pole fall, we stop the loop.
            print('Episode ', str(i),' finished after ', str(t+1),' timesteps')
            results.append(t+1)
            break

saveAndPrintResults(results, name) # We save the results into a file.

env.close() # We close the environment.
