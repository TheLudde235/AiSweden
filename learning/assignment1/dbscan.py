from functions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import random
import math
import time

#TODO: Write your full name.
name = 'Ludvig'
#ENDTODO

# TODO: Selest one of the two problems by commenting the rest of the lines using # before each line
#_, problem, database = uploadDataBase1() # Function that upload the database 1
_, problem, database = uploadDataBase2() # Function that upload the database 2
# ENDTODO

# Important parameters used in DBSCAN
# TODO: Change these parameters so Genetic algorithms works better.
R = 10 # Radius to check neighbouring points. Positive number.
minPoints = 20 # Minimum number of points within the radius to be consider a cluster. Positive integer.
# ENDTODO

DBSCAN_checkErrorsInParameters(R, minPoints) # Function that will double-check if your parameters are in the correct range.
nonVisited, visited, actualCluster, visitedColor, action, nextToVisit = DBSCAN_initialize(database) # Function that will initialize the algorithm
DBSCAN_visualize(nonVisited, visited, visitedColor, [], [], R, name) # Function to visualize the data and how the algorithm works
iteration= 0;
while True: # Main loop of the program that will run forever
    # If there are not next to visit datapoints, one is randomly selected.
    if nextToVisit == []:
        index = random.randint(0, len(nonVisited)-1)
        nextToVisit.append(index)
        action = False

    neighbours = DBSCAN_checkNeighbours(nonVisited, nextToVisit, R) # Function that will find the neighbours of the recently visited datapoints

    nextToVisit, visited, nonVisited, visitedColor, aura, auraColor, actualCluster, action = DBSCAN_updateVisited(nextToVisit, visited, nonVisited, neighbours, action, actualCluster, visitedColor, minPoints) # Function that will update the visited nodes
    iteration+=1;
    print("Iteration",iteration)
    DBSCAN_visualize(nonVisited, visited, visitedColor, aura, auraColor, R, name) # Function to visualize the data and how the algorithm works

    if len(nonVisited) == 0: # If all the datapoints have been visited
        break # If the condition in the line above, break will force the while loop to stop

DBSCAN_saveResults(nonVisited, visited, visitedColor, name, problem) # Function that save the results of the algorithm
