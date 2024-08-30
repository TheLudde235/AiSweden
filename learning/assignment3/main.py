from functions import *
# We import all the required libraries
# For examination
# TODO: Write your full name.
name = 'Ludvig'
# ENDTODO

# Parameters to visualize
# TODO: Chage this paramters if you do not want the visualization
showBestSolution = 1
showPopulationDistribution = 0
# ENDTODO
bestFitness = 99999999

# We upload the database
filename = "berlin52.tsp"  # Name of the file that we will read with the dataset
database, numPoints = uploadDataBase(filename)  # Function that reads the database and will give how many coordinates we have


# Important parameters used in GA.
# TODO: Change these parameters so Genetic algorithms works better. You cannot have more than 10.000 fitness calculation (maxGeneration * numNewOffspring + populationSize)

maxGeneration = 500 # Maximum number of iterations for Genetic Algorithm. It should be at least 10.
populationSize = 1200  # How many individuals we have at the same time. It should be at least 5.
numNewOffspring = math.floor((10_000 - populationSize) / maxGeneration) # How many new individuals we are creating each generations. It should be at least 1.
populationSize = 10_000 - maxGeneration * numNewOffspring
mutationProbability = 1 # The probability of performing mutation. value in [0, 1]
numberMutations = 1  # If mutation occur, the number of mutations applied. It should be at least 1.
tournamentSize = 400 # The size of the tournament. This is only used in parent selection method 3. Recommended value in [1, 10]
print(maxGeneration, populationSize, numNewOffspring)
# ENDTODO

checkErrorsInParameters(maxGeneration, populationSize, numNewOffspring, mutationProbability, numberMutations, tournamentSize) # Function that will double-check if your parameters are in the correct range.

population = newPopulation(populationSize, numPoints) # The new population is initialized
populationFitness = calculateFitness(population, database) # Function that calculates the fitness of the individuals. Fitness in this case is the total distance of the path given by each individual.

for g in range(0,maxGeneration):  # Main loop for the program that runs from 1 to the maximum of iterations that we set in maxGeneration
    offsprings = []  # List where the new individuals will be saved
    for o in range(0,numNewOffspring):    # Loop to create new individuals as indicated in numNewOffspring

        # TODO: Select one parent selection method by commenting the rest of the lines using # before each line.
        # parents = parentSelection1(population, populationFitness) # Function that will select two parents that will be used to create the new offspring. Read more in the lab description.
        # parents = parentSelection2(population, populationFitness) # Function that will select two parents that will be used to create the new offspring. Read more in the lab description.
        parents = parentSelection3(population, populationFitness, tournamentSize) # Function that will select two parents that will be used to create the new offspring. Read more in the lab description.
        # parents = parentSelection4(population) # Function that will select two parents that will be used to create the new offspring. Read more in the lab description.
        # ENDTODO

        newOffspring = crossover(parents) # Function that will create a new offspring. Read more in the lab description

        # TODO: Select one mutation method by commenting the rest of the lines using # before each line
        # newOffspring = mutation1(newOffspring, mutationProbability, numberMutations) # Function that will perform changes on the new Offspring. Read more in the lab description.
        newOffspring = mutation2(newOffspring, mutationProbability, numberMutations) # Function that will perform changes on the new Offspring. Read more in the lab description.
        #ENDTODO

        offsprings.append(newOffspring)  # We add the new offspring to the list of oggsprings

    offspringsFitness = calculateFitness(offsprings, database)  # Function that calculates the fitness of the individuals. Fitness in this case is the total distance of the path given by each individual.
    population, populationFitness = updatePopulation(population, populationFitness, offsprings, offspringsFitness) # Function that merges the offsprings into the population, if they are better than some parents
    bestFitness = visulation(population, populationFitness, database, g, maxGeneration, showBestSolution, showPopulationDistribution, bestFitness, name) # Function that helps with the visualization of the solutions
