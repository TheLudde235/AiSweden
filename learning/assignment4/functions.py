import gym
import random
import math
import numpy
import pandas
import matplotlib.pyplot as plt
import sys

class QLearningAgent:
    # Function: This function will create the agent
    def __init__(self, actions, epsilon, gamma, alpha):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = actions
        self.table = {}

    # Function: It returns the q(state,action) value from the table
    def getQValue(self, state, action):
        if not (state in self.table) or not (action in self.table[state]):
            return 0
        else:
            return self.table[state][action]

    # Function: It returns an action given an state
    def getAction(self, state):
        if len(self.actions) == 0:
            return None
        q = []
        for a in self.actions:
            q.append(self.getQValue(state,a))

        maxQ = max(q)

        # Exploration, we set random q values
        if random.random() < self.epsilon:
            minQ = min(q)
            mag = max(abs(minQ), abs(maxQ))
            q = [q[i] + random.random() * mag - 0.5 *mag for i in range(len(self.actions))]
            maxQ = max(q)

        count = q.count(maxQ)
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)
        return self.actions[i]

    # Function: This function will update the q values from the table.
    def updateTable(self, state, action, nextState, reward):
        if not (state in self.table):
            self.table[state] = {}
        if not (action in self.table[state]):
            self.table[state][action] = reward
        else:
            maxqnew = max([self.getQValue(nextState, a) for a in self.actions])
            diff = reward + self.gamma * maxqnew - self.table[state][action]
            self.table[state][action] = self.table[state][action] + self.alpha * diff

# Function:
# Inputs:
#   numCartPositionBins: Number of bins in which the possibilities of the cart position will be grouped
#   numCartVelocityBins: Number of bins in which the possibilities of the cart velocity will be grouped
#   numAngleBins: Number of bins in which the possibilities of the angle of the pole will be grouped
#   numAnglesVelocityBins: Number of bins in which the possibilities of the pole angle velocity will be grouped
#   alpha: Learning rate
#   gamma: Discount factor
#   epsilon: Exploration probability
def checkErrorsInParameters(numCartPositionBins, numCartVelocityBins, numAngleBins, numAnglesVelocityBins, alpha, gamma, epsilon):
    error = 0
    if numCartPositionBins > 10 or numCartPositionBins < 1 or not (numCartPositionBins == int(numCartPositionBins)):
        print('You set \'numCartPositionBins\' to ',str(numCartPositionBins),'. The correct range is {1,...,10} and only integers.')
        error = 1
    if numCartVelocityBins > 10 or numCartVelocityBins < 1 or not (numCartVelocityBins == int(numCartVelocityBins)):
        print('You set \'numCartVelocityBins\' to ',str(numCartVelocityBins),'. The correct range is {1,...,10} and only integers.')
        error = 1
    if numAngleBins > 10 or numAngleBins < 1 or not (numAngleBins == int(numAngleBins)):
        print('You set \'numAngleBins\' to ',str(numAngleBins),'. The correct range is {1,...,10} and only integers.')
        error = 1
    if numAnglesVelocityBins > 10 or numAnglesVelocityBins < 1 or not (numAnglesVelocityBins == int(numAnglesVelocityBins)):
        print('You set \'numAnglesVelocityBins\' to ',str(numAnglesVelocityBins),'. The correct range is {1,...,10} and only integers.')
        error = 1
    if alpha < 0 or alpha > 1:
        print('You set \'alpha\' to ',str(alpha),'. The correct range is [0, 1].')
        error = 1
    if gamma < 0 or gamma > 1:
        print('You set \'gamma\' to ',str(gamma),'. The correct range is [0, 1].')
        error = 1
    if epsilon < 0 or epsilon > 1:
        print('You set \'epsilon\' to ',str(epsilon),'. The correct range is [0, 1].')
        error = 1
    if error == 1:
        sys.exit()

# Function: This funciton will create the ID of the state based on the input parameters
# Inputs:
#   observation: Information of the environment
#   numCartPositionBins: Number of bins in which the possibilities of the cart position will be grouped
#   numCartVelocityBins: Number of bins in which the possibilities of the cart velocity will be grouped
#   numAngleBins: Number of bins in which the possibilities of the angle of the pole will be grouped
#   numAnglesVelocityBins: Number of bins in which the possibilities of the pole angle velocity will be grouped
# Outputs:
#   stateID: The identifier of the state
def createState(observation, numCartPositionBins, numCartVelocityBins, numAngleBins, numAnglesVelocityBins):
    cart_position_bins = pandas.cut([-2.4, 2.4], bins=numCartPositionBins, retbins=True)[1][1:-1]
    cart_velocity_bins = pandas.cut([-1, 1], bins=numCartVelocityBins, retbins=True)[1][1:-1]
    pole_angle_bins = pandas.cut([-2, 2], bins=numAngleBins, retbins=True)[1][1:-1]
    angle_rate_bins = pandas.cut([-3.5, 3.5], bins=numAnglesVelocityBins, retbins=True)[1][1:-1]

    cpID = numpy.digitize(x=observation[0], bins = cart_position_bins)[0]
    cvID = numpy.digitize(x=observation[1], bins = cart_velocity_bins)[0]
    paID = numpy.digitize(x=[observation[2]], bins = pole_angle_bins)[0]
    arID = numpy.digitize(x=[observation[3]], bins = angle_rate_bins)[0]

    stateID = int(str(cpID) + str(cvID) + str(paID) + str(arID))

    return stateID

# Function: This function will print and save the results
# Inputs:
#   results: The results obtained by the algorithm
#   name: Your name
def saveAndPrintResults(results, name):

    plt.plot(results)
    plt.title(name+'\'s results(Last30_avg: '+str(sum(results[-30:]) / 30)+' steps)')
    plt.ylabel('number of steps')
    plt.xlabel('Iteration number')
    plt.legend(['results'], loc='best')
    plt.savefig(name + '\'s solution.png')

    print('Last 30 average score: ', sum(results[-30:]) / 30 )
    results.sort()
    print('Best 30 average score: ', sum(results[-30:]) / 30 )
    print('Overall average score: ', sum(results) / len(results))
