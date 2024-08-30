import numpy as np
import math
import random
import sys
import matplotlib.pyplot as plt

# Class: This class is used to save the coordinates information for all points in the map
# Variables:
#   x: X coordinate of a point
#   y: Y coordinate of a point
class point(object):
    x = 0
    y = 0

    # Function: This function will create a coordinate Variable
    # Inputs:
    #   self: All functions that belongs to a class will have self as the first input.
    #   inputX: the X coordinate of a point
    #   inputY: the Y coordinate of a point
    def __init__(self, inputX, inputY):
        self.x = inputX
        self.y = inputY

# Function: This function will read the information about the uploadDataBase
# Inputs:
#   filename: The name of the file
# Outputs:
#   database: The database with all the coordinates for all the places in the map.
#   numCoordinates: Number of places in the map
def uploadDataBase(filename):
    f = open(filename, "r")
    f.readline()
    f.readline()
    f.readline()
    numPoints = f.readline()
    numPoints = numPoints[-3:-1]
    numPoints = int(numPoints)
    f.readline()
    f.readline()

    database = []
    for i in range(0,numPoints):
        line = f.readline()
        line = line.split()
        p = point(float(line[1]), float(line[2]))
        database.append(p)

    f.close()

    return database, numPoints

# Function: This function will check if the parameters are in the correct ranges. IF not, it will terminate the program
# Inputs:
#   maxGeneration: Maximum number of iterations for Genetic Algorithm.
#   populationSize: How many individuals we have at the same time.
#   numNewOffspring: How many new individuals we are creating each generations.
#   mutationProbability: The probability of performing mutation.
#   numberMutations: If mutation occur, the number of mutations applied.
def checkErrorsInParameters(maxGeneration, populationSize, numNewOffspring, mutationProbability, numberMutations, tournamentSize):
    error = 0
    numFitnessCalls = maxGeneration * numNewOffspring + populationSize
    if numFitnessCalls > 10000:
        print('You are calculating the fitness ',str(numFitnessCalls),' times. The maximum is 10.000.')
        error = 1
    if maxGeneration < 10:
        print('You set \'maxGeneration\' to ',str(maxGeneration),'. The minimum is 10.')
        error = 1
    if populationSize <5:
        print('You set \'populationSize\' to ', str(populationSize),'. The minimum is 5.')
        error = 1
    if numNewOffspring < 1:
        print('You set \'numNewOffspring\' to ', str(numNewOffspring),'. The minimum is 1.')
        error = 1
    if numberMutations < 1:
        print('You set \'numberMutations\' to ', str(numberMutations),'. The minimum is 1.')
        error = 1
    if mutationProbability > 1 or mutationProbability < 0:
        print('You set \'mutationProbability\' to ', str(mutationProbability),'. The correct range is [0, 1].')
        error = 1
    if tournamentSize < 2 or tournamentSize > populationSize:
        print('You set \'tournamentSize\' to ', str(tournamentSize),'. The correct range is [2',str(populationSize),'].')
        error = 1
    if error == 1:
        sys.exit()


# Function: This function will create a complete new population.
# Inputs:
#   populationSize: number of individuals that will be created. Each individual will have a length of (numCoordinates + 1)
#   numPoints: number of places in the map.
# Outputs:
#   population: A new population with populationSize individuals
def newPopulation(populationSize, numPoints):
    population = []
    for i in range(0,populationSize):
        individual = np.arange(1, numPoints, 1)
        np.random.shuffle(individual)
        individual = np.insert(individual,0,0)
        individual = np.append(individual,0)
        population.append(individual)

    return population

# Function: This function will calculate the fitness of all the individuals in individuals
# Inputs:
#   individuals: The paths on which the fitness will be calculated
#   database: The coorddinates information
# Outputs:
#   populationFitness: The fitness of all paths in individuals
def calculateFitness(individuals, database):
    populationSize = len(individuals)
    pathLength = len(individuals[0])
    populationFitness = []
    for i in range(0,populationSize):
        distance = 0
        for j in range(0, pathLength-1):
            pointA = database[individuals[i][j]]
            pointB = database[individuals[i][j+1]]
            distance = distance + math.sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

        populationFitness.append(distance)
    return populationFitness

# Function: This function will select two parents. The first parent will be the best in the population. The second parent will be the second best in the population
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populattionFitness: It indicates how good each individual in the population is
# Outputs:
#   parents: Two individuals that are selected to be used in crossover.
def parentSelection1(population, populationFitness):
    auxList = populationFitness.copy()
    auxList.sort()
    indexFirstParent = populationFitness.index(auxList[0])
    indexSecondParent = populationFitness.index(auxList[1])
    parents = []
    parents.append(population[indexFirstParent].copy())
    parents.append(population[indexSecondParent].copy())
    return parents

# Function: This function will select two parents. The first parent will be the best in the population. The second parent is randomly selected
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populattionFitness: It indicates how good each individual in the population is
# Outputs:
#   parents: Two individuals that are selected to be used in crossover.
def parentSelection2(population, populationFitness):
    auxList = populationFitness.copy()
    auxList.sort()
    indexFirstParent = populationFitness.index(auxList[0])
    indexSecondParent = indexFirstParent
    while indexFirstParent == indexSecondParent:
        indexSecondParent = random.randint(0,len(population)-1)
    parents = []
    parents.append(population[indexFirstParent].copy())
    parents.append(population[indexSecondParent].copy())
    return parents

# Function: This function will select two parents. The first parent will be the best in the population. The second parent is randomly selected
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populattionFitness: It indicates how good each individual in the population is
#   tournamentSize: How many individuals will be randomly picked to participate in the tournament
# Outputs:
#   parents: Two individuals that are selected to be used in crossover.
def parentSelection3(population, populationFitness, tournamentSize):
    parents = []
    for i in range(0,2):
        indexesTournament = random.sample(range(0,len(population)-1), tournamentSize)
        tournament = []
        tournamentFitness = []
        for j in range(0, len(indexesTournament)):
            tournament.append(population[indexesTournament[j]].copy())
            tournamentFitness.append(populationFitness[indexesTournament[j]])
        auxList = tournamentFitness.copy()
        auxList.sort()
        if i == 0:
            indexFirstParent = populationFitness.index(auxList[0])
            parents.append(population[indexFirstParent].copy())
        if i == 1:
            indexSecondParent = populationFitness.index(auxList[0])
            if indexFirstParent == indexSecondParent:
                indexSecondParent = populationFitness.index(auxList[1])
            parents.append(population[indexSecondParent].copy())
    return parents

# Function: This function will select two parents. Both parents are randomly selected
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populattionFitness: It indicates how good each individual in the population is
# Outputs:
#   parents: Two individuals that are selected to be used in crossover.
def parentSelection4(population):

    indexes = random.sample(range(0,len(population)-1), 2)
    parents = []
    parents.append(population[indexes[0]].copy())
    parents.append(population[indexes[1]].copy())
    return parents

# Function: This function will create a new offspring.
# Inputs:
#   parents: The parents that will be used to create a new poffspring
# Outputs:
#   offspring: The new offspring
def crossover(parents):
    idx1 = random.randint(2, len(parents[0])-7)
    idx2 = random.randint(idx1+2, len(parents[0])-3)
    offspring = parents[0].copy()
    offspring[idx1:idx2] = 0
    i = 0
    while idx1 < idx2:
        if not (parents[1][i] in offspring):
            offspring[idx1] = parents[1][i]
            idx1 = idx1 + 1
        i = i + 1
    return offspring

# Function: This function will mutate an offspring.
# Inputs:
#   individual: A path (a solution to the problem)
#   mutationProbability: The probability to apply mutation
#   numberMutations: The number of mutations if mutation is applied
# Outputs:
#   individual: The mutated offspring
def mutation1(individual, mutationProbability, numberMutations):
    if random.random() < mutationProbability:
        for i in range(0,numberMutations):
            idx1 = random.randint(1, len(individual)-2)
            idx2 = idx1
            while idx1 == idx2:
                idx2 = random.randint(1, len(individual)-2)
            aux = individual[idx1]
            individual[idx1] = individual[idx2]
            individual[idx2] = aux
    return individual

# Function: This function will mutate an offspring.
# Inputs:
#   individual: A path (a solution to the problem)
#   mutationProbability: The probability to apply mutation
#   numberMutations: The number of mutations if mutation is applied
# Outputs:
#   individual: The mutated offspring
def mutation2(individual, mutationProbability, numberMutations):
    if random.random() < mutationProbability:
        for i in range(0,numberMutations):
            idx1 = random.randint(1, len(individual)-2)
            idx2 = idx1
            while idx1 == idx2:
                idx2 = random.randint(1, len(individual)-2)
            if idx1 > idx2:
                aux = idx1
                idx1 = idx2
                idx2 = aux
            auxList = individual[idx1:idx2]
            individual[idx1:idx2] = auxList[::-1]
    return individual
# Function: This function will update the population with the new offsprings only if the offsprings are better.
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populationFitness: It indicates how good each individual in the population is
#   offsprings: A set of new individuals that does not belongs to the population. Each individual is a solution to the problem
#   offspringsFitness: It indicates how good each new offspring is
# Outputs:
#   population:
#   populationFitness:
def updatePopulation(population, populationFitness, offsprings, offspringsFitness):
    populationFitnessAux = populationFitness.copy()
    offspringsFitnessAux = offspringsFitness.copy()

    populationFitnessAux.sort()
    offspringsFitnessAux.sort()
    for i in range(1,len(offsprings)+1):
        if offspringsFitnessAux[-i] < populationFitnessAux[-1]:
            idxOffs = offspringsFitness.index(offspringsFitnessAux[-i])
            idxPop = populationFitness.index(populationFitnessAux[-1])
            population[idxPop] = offsprings[idxOffs]
            populationFitness[idxPop] = offspringsFitness[idxOffs]
            populationFitnessAux = populationFitness.copy()
            populationFitnessAux.sort()

    return population, populationFitness

# Function:
# Inputs:
#   population: A set of individuals. Each individual is a solution to the problem
#   populationFitness: it indicates how good each individual in the population is
#   database: The coorddinates information
#   g: Current generation
#   maxGeneration: Maximum number of generations
#   showBestSolution: If 1, this funciton will show a map with all the different paths
#   showPopulationDistribution: If 1, this function will show the distribution of the populationSize
#   bestFitness: The best fitness so far
#   name: Your name
def visulation(population, populationFitness, database, g, maxGeneration, showBestSolution, showPopulationDistribution, bestFitness, name):
    currentBest =  min(populationFitness)
    indexBestSolution = populationFitness.index(currentBest)

    if currentBest < bestFitness  or ((g+1) == maxGeneration):
        # print('New solution found at generation',str(g+1),'/',str(maxGeneration),': ',str(math.trunc(currentBest*100)/100),' meters')
        bestFitness = currentBest
        fig1 = plt.figure(1)

        if (showBestSolution == 1) or ((g+1) == maxGeneration):
            X = []
            Y = []
            for i in range(0,len(database)):
                X.append(database[i].x)
                Y.append(database[i].y)
            bestSolutionX = []
            bestSolutionY = []
            for i in range(0, len(population[indexBestSolution])):
                bestSolutionX.append(database[population[indexBestSolution][i]].x)
                bestSolutionY.append(database[population[indexBestSolution][i]].y)

            plt.clf()
            plt.scatter(X,Y,color = 'k')
            plt.plot(bestSolutionX, bestSolutionY)
            plt.title(name + ' solution (Dist: ' +str(math.trunc(currentBest*100)/100) + ')')
            plt.ylabel('y coordinate')
            plt.xlabel('x coordinate')
            plt.pause(0.1)
            plt.draw()
        if showPopulationDistribution == 1:
            fig2 = plt.figure(2)
            plt.clf()
            X = []
            Y = []
            for i in range(0,len(database)):
                X.append(database[i].x)
                Y.append(database[i].y)
            plt.scatter(X,Y,color = 'b')
            for i in range(0, len(population)):
                solutionX = []
                solutionY = []
                for j in range(0, len(population[i])):
                    solutionX.append(database[population[i][j]].x)
                    solutionY.append(database[population[i][j]].y)
                    plt.plot(solutionX, solutionY, color = 'k', alpha = 0.05)

            plt.title(name + ' population distribution')
            plt.ylabel('y coordinate')
            plt.xlabel('x coordinate')
            plt.pause(0.01)
            plt.draw()

    if (g+1) == maxGeneration:
        print('\nThe distance of the best solution is',str(math.trunc(currentBest*100)/100))
        fig1.savefig(name + ' solution.png')

    return bestFitness
