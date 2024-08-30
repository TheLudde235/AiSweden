import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import random
import math
import sys
from operator import itemgetter

colmap = {0: 'k', 1: 'red', 2: 'green', 3: 'blue', 4: 'yellow', 5: 'orange', 6: 'magenta', 7: 'turquoise', 8:'darkred', 9:'darkgreen', 10:'darkblue', 11:'gold', 12:'darkorange', 13: 'darkmagenta', 14:'darkturquoise'}

# Function: Upload the first database: Mouse problem
# Outputs:
#   df: database
#   problemName: The name of the problemName
#   examples: All data points
def uploadDataBase1():
    np.random.seed(1000)

    listx = list(np.random.normal(0.5, 0.06, 1000)*80)
    aux = list(np.random.normal(0.3, 0.04, 200)*80)
    listx = listx+aux
    aux = list(np.random.normal(0.7, 0.04, 200)*80)
    listx = listx+aux

    listy = list(np.random.normal(0.4, 0.06, 1000)*80)
    aux = list(np.random.normal(0.75, 0.04, 200)*80)
    listy = listy+aux
    aux = list(np.random.normal(0.75, 0.04, 200)*80)
    listy = listy+aux

    df = pd.DataFrame({
        'x': listx,
        'y': listy
    })

    examples = []
    for i in range(len(listx)):
        examples.append([listx[i], listy[i]])

    np.random.seed()
    problemName = 'Problem 1'
    return df, problemName, examples

# Function: Upload the first database: Face problem
# Outputs:
#   df: database
#   problemName: The name of the problemName
#   examples: All data points
def uploadDataBase2():
    center = [40, 40]
    radius = 30
    listx = []
    listy = []
    for x in range(center[0]-radius, center[0]+radius+1):
        for _ in range(0,10):
            listx.append(x + random.gauss(0, 1))
            listx.append(x + random.gauss(0, 1))
            yvalue = math.sqrt((radius**2 - (x-center[0])**2)) + center[1]
            listy.append(yvalue + random.gauss(0, 1))
            oppositeyvalue = center[1] - (yvalue - center[1])
            listy.append(oppositeyvalue + random.gauss(0, 1))

    aux = list(np.random.normal(0.35, 0.03, 100)*80)
    listx = listx+aux
    aux = list(np.random.normal(0.65, 0.03, 100)*80)
    listx = listx+aux
    aux = list(np.random.normal(0.5, 0.05, 100)*80)
    listx = listx+aux

    aux = list(np.random.normal(0.6, 0.03, 100)*80)
    listy = listy+aux
    aux = list(np.random.normal(0.6, 0.03, 100)*80)
    listy = listy+aux
    aux = list(np.random.normal(0.4, 0.02, 100)*80)
    listy = listy+aux

    df = pd.DataFrame({
        'x': listx,
        'y': listy
    })

    examples = []
    for i in range(len(listx)):
        examples.append([listx[i], listy[i]])
    problemName = 'Problem 2'
    return df, problemName, examples

# Function: This function will check if the parameters are in the correct ranges. IF not, it will terminate the program
# Inputs:
#   k: Number of clusters
def K_means_checkErrorsInParameters(k):
    error = 0
    if k < 1 or k > 7:
        print('You set \'k\' to ', str(k),'. The correct range is an integer in {1, 7}.')
        error = 1
    if not (k == int(k)):
        print('You set \'k\' to ', str(k),'. The value is not an integer.')
        error = 1
    if error == 1:
        sys.exit()

# Function: This function will assign each datapoint to the closer controid
# Inputs:
#   df: database
#   centroids: All different centroids
# Outputs:
#   df: database with the new cluster assignment.
def K_means_assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    df['color'] = df['closest'].map(lambda x: colmap[x])
    return df

# Function: The centroids position will be updated
# Inputs:
#   df: Database
#   centroids: All the centroids
# Outputs:
#   centroids: The new position of the centroids
def K_means_update(df, centroids):
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return centroids

# Function: This function will initialize all the centroids and sets all the datapoints without an assigned centroid.
# Inputs:
#   df: database
#   k: Number of centroids
# Outputs:
#   df: The database
#   centroids: Position of all centroids
def K_means_initialize(df, k):
    df['color'] = ['k'] * len(df['x'])

    centroids = {
        i+1: [np.random.randint(0, 80), np.random.randint(0, 80)]
        for i in range(k)
    }

    return df, centroids

# Function: This function will visualize how K-means evolve through the iterations showing all the datapoints and their respective centroids.
# Inputs:
#   df: Database with all datapoints
#   centroids: Position of all centroids
#   name: Your name
def K_means_visualize(df, centroids, name):
    fig = plt.figure(num = 1, figsize = (5,5))
    plt.clf()
    plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5)
    for i in centroids.keys():
        plt.scatter(*centroids[i], color=colmap[i+7], edgecolor='k')
    plt.xlim(0, 80)
    plt.ylim(0, 80)
    plt.title(name + '\'s solution')
    plt.ylabel('y coordinate')
    plt.xlabel('x coordinate')
    plt.pause(0.3)
    plt.draw()

# Function: This function will save the final results in an image.
# Inputs:
#   df: Database with all datapoints
#   centroids: Position of all centroids
#   name: Your name
#   problem: Which problem was solved
def K_means_saveResults(df, centroids, name, problem):
    fig = plt.figure(num = 1, figsize = (5,5))
    plt.clf()
    plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5)
    for i in centroids.keys():
        plt.scatter(*centroids[i], color=colmap[i+7], edgecolor='k')
    plt.xlim(0, 80)
    plt.ylim(0, 80)
    plt.title(name + '\'s solution')
    plt.ylabel('y coordinate')
    plt.xlabel('x coordinate')
    plt.pause(0.2)
    plt.draw()
    fig.savefig(name + '\'s K-means ' + problem + ' solution.png')

# Function: This function will check if the parameters are in the correct ranges. IF not, it will terminate the program
# Inputs:
#   R: Radius of the circunference in order to check for neighbours
#   minPoints: Minimum number of points within the radius to be consider a cluster
def DBSCAN_checkErrorsInParameters(R, minPoints):
    error = 0
    if R <= 0:
        print('You set \'R\' to ', str(R),'. R > 0')
        error = 1
    if minPoints <= 0:
        print('You set \'minPoints\' to ', str(minPoints),'. minPoints > 0')
        error = 1
    if not (minPoints == int(minPoints)):
        print('You set \'minPoints\' to ', str(minPoints),'. The value is not an integer.')
        error = 1
    if error == 1:
        sys.exit()

# Function: This funciton will initialize the algorithm
# Inputs:
#   database: Database with all datapoints
# Outputs:
#   nonVisited: Datapoints that were not visited by the algorithm
#   visited: Datapoints that were visited by the algorithm
#   actualCluster: Index of the actual cluster
#   color: Indicate the cluster of each visited point
#   action: Variable that indicates if a neighbour was included into a cluster
#   nextToVisit: List containing the points that are going to be checked.
def DBSCAN_initialize(database):
    nonVisited  = list(database)
    visited = []
    actualCluster = 0
    color = []
    action = False
    nextToVisit = []
    return nonVisited, visited, actualCluster, color, action, nextToVisit

# Function: This function will find the neighbour points that can be found in nextToVisit and they are not visited.
# Inputs:
#   nonVisited: Datapoints that were not visited by the algorithm
#   nextToVisit: List containing the points that are going to be checked.
#   R: Radius of the circunference in order to check for neighbours
# Outputs:
#   indexes: The indexes of the neighbours of the points in nextToVisit
def DBSCAN_checkNeighbours(nonVisited, nextToVisit, R):
    indexes = []
    for i in range(len(nextToVisit)):
        for j in range(len(nonVisited)):
            if nextToVisit[i] != j:
                dist = np.sqrt((nonVisited[nextToVisit[i]][0]-nonVisited[j][0])**2 + (nonVisited[nextToVisit[i]][1]-nonVisited[j][1])**2)
                if dist < R and (not (j in indexes)) and (not(j in nextToVisit)):
                    a_bolean = (not (j in indexes))
                    indexes.append(j)
    return indexes

# Function: This function will update the list of visited node
# Inputs:
#   nextToVisit: The datapoints that were evaluated but not added to the visited list
#   visited: List with the visited datapoints
#   nonVisited: List with the non visited datapoints
#   neighbours: list with the neighbours of the points in nextToVisit
#   action: Variable that indicates if a neighbour was included into a cluster
#   actualCluster: Index of the actual cluster
#   visitedColor: Indicates to which cluster belong every of the visited points
#   minPoints: Minimum number of points within the radius to be consider a cluster
# Outputs:
#   nextToVisit: The points that will be visited in the next iteration
#   visited: The updated list of the visited points
#   nonVisited: The updated list of the non visited points
#   visitedColor: Indicates to which cluster belong every of the visited points
#   aura: Position of the neighbours that are being visited. Just used for visualization purposes
#   auraColor: Cluster of the neighbours. Just used for visualization purposes
#   actualCluster: Index of the actual cluster
#   action: Variable that indicates if a neighbour was included into a cluster
def DBSCAN_updateVisited(nextToVisit, visited, nonVisited, neighbours, action, actualCluster, visitedColor, minPoints):
    nextToVisit.sort()
    neighbours.sort()
    aura = []
    auraColor = []
    if (action == False and len(neighbours)>=minPoints) or action == True:
        if action == False:
            action = True
            actualCluster += 1
        decreaseValue = 0

        for i in range(len(nonVisited)):
            if i in nextToVisit:
                visited.append(nonVisited[i])
                aura.append(visited[-1])
                visitedColor.append(actualCluster)
                auraColor.append(actualCluster)
                decreaseValue += 1

            if i in neighbours:
                neighbours[neighbours.index(i)] -= decreaseValue

        for i in range(len(nextToVisit)):
            del nonVisited[nextToVisit[i]]
            for j in range(len(nextToVisit)):
                nextToVisit[j] -= 1

    else:
        for i in range(len(nextToVisit)):
            visited.append(nonVisited[nextToVisit[i]])
            del nonVisited[nextToVisit[i]]
            visitedColor.append(0)
        action = False
    nextToVisit = list(neighbours)
    return nextToVisit, visited, nonVisited, visitedColor, aura, auraColor, actualCluster, action

def list2arr(l):
    return np.array(l)



# Function: This function will visualize how DBSCAN evolve through the iterations showing all the datapoints and their respective centroids.
# Inputs:
#   nonVisited: List of nonVisited datapoints
#   visited: List of visited datapoints
#   visitedColor: List that indicates the cluster of which each data point in visited belong
#   aura: Position of the neighbours that are being visited. Just used for visualization purposes
#   auraColor: Cluster of the neighbours. Just used for visualization purposes
#   R: Radius of the circunference in order to check for neighbours
#   name: Your name
def DBSCAN_visualize(nonVisited, visited, visitedColor, aura, auraColor, R, name):
    fig = plt.figure(num = 1, figsize = (5,5))
    plt.clf()
#    for h in range(len(nonVisited)):
    arr = np.array(nonVisited)
    if len(arr)>0:
        plt.scatter(arr[:,0], arr[:,1], color='grey', edgecolor = 'k')
    arr = np.array(visited)
    if len(arr)>0:
        plt.scatter(arr[:,0], arr[:,1], color=itemgetter(*visitedColor)(colmap), edgecolor = 'k')
    arr = np.array(aura)
    if len(arr)>0:
        plt.scatter(arr[:,0], arr[:,1], color=itemgetter(*auraColor)(colmap), alpha=0.25, edgecolor=itemgetter(*auraColor)(colmap), s=(R*(R))**2)
#    for h in range(len(nonVisited)):
#        plt.scatter(nonVisited[h][0], nonVisited[h][1], color='grey', edgecolor = 'k')
#    for h in range(len(visited)):
#        plt.scatter(visited[h][0], visited[h][1], color=colmap[visitedColor[h]], edgecolor = 'k')
#    for h in range(len(aura)):
#        plt.scatter(aura[h][0], aura[h][1], color = colmap[auraColor[h]], alpha=0.25, edgecolor = colmap[auraColor[h]], s=(R*(R))**2)
    plt.xlim(0, 80)
    plt.ylim(0, 80)
    plt.title(name + '\'s solution')
    plt.ylabel('y coordinate')
    plt.xlabel('x coordinate')
    plt.pause(0.01)
    plt.draw()

# Function: This function will save the final results in an image.
# Inputs:
#   nonVisited: List of nonVisited datapoints
#   visited: List of visited datapoints
#   visitedColor: List that indicates the cluster of which each data point in visited belong
#   name: Your name
#   problem: Which problem was solved
def DBSCAN_saveResults(nonVisited, visited, visitedColor, name, problem):
    fig = plt.figure(num = 1, figsize = (5,5))
    plt.clf()
    arr = np.array(nonVisited)
    if len(arr)>0:
        plt.scatter(arr[:,0], arr[:,1], color='grey') #, edgecolor = 'k')
    arr = np.array(visited)
    if len(arr)>0:
        plt.scatter(arr[:,0], arr[:,1], color=itemgetter(*visitedColor)(colmap)) #, edgecolor = 'k')
    # for h in range(len(nonVisited)):
    #     plt.scatter(nonVisited[h][0], nonVisited[h][1], color='grey') #, edgecolor = 'k')
    # for h in range(len(visited)):
    #     plt.scatter(visited[h][0], visited[h][1], color=colmap[visitedColor[h]]) #, edgecolor = 'k')
    plt.xlim(0, 80)
    plt.ylim(0, 80)
    plt.title(name + '\'s solution')
    plt.ylabel('y coordinate')
    plt.xlabel('x coordinate')
    plt.pause(0.01)
    plt.draw()
    fig.savefig(name + '\'s DBSCAN ' + problem + ' solution.png')
