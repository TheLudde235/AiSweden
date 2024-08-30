from functions import *
#TODO: Write your full name.
name = 'Ludvig'
#ENDTODO

# TODO: Selest one of the two problems by commenting the rest of the lines using # before each line
df, problem, _ = uploadDataBase1() #  Function that upload the database 1
# df, problem, _ = uploadDataBase2() #  Function that upload the database 2
# ENDTODO

# Calculates the manhattan distance between the two datapoints i and j
def distance(df, i, j): # i and j being the indexes of the datapoints in the "df" list
    x_diff = abs(df['x'][i] - df['x'][j])
    y_diff = abs(df['y'][i] - df['y'][j])
    return x_diff + y_diff


# Calculates the mean distance between i and the other datapoint in the same cluster as i
def mean_distances(df, i): # i being hte index of the datapoint in the "df" list
    sum = 0
    points_in_cluster = 0

    closest = df['closest']

    for j in range(len(closest)):
        if j == i:
            continue
        if closest[i] != closest[j]:
            continue

        sum += distance(df, i, j)
        points_in_cluster += 1

    return sum/points_in_cluster

def get_neighboring_cluster(df, k, i):
    sumArr = []
    obj = 0
    closest = df['closest']
    count = 0
    if k == 1:
        return 0
    for Cj in range(1, k + 1):
        # Skips the cluster that i is in
        if closest[i] == Cj:
            continue

        sum = 0
        count = 0

        for p in range(len(closest)):
            if closest[p] == Cj:
                sum += distance(df, i, p)
                count += 1

        sumArr.append({"sum": sum, "count": count})

    koth_sum = math.inf
    koth_count = -1

    for obj in sumArr:
        if obj['sum'] < koth_sum and obj['sum'] != 0:
            koth_sum = obj['sum']
            koth_count = obj['count']
            if koth_count == 0:
                print(koth_sum)
    return koth_sum / koth_count

def s(df, k, i):
    a = mean_distances(df, i)
    b = get_neighboring_cluster(df, k, i)

    if a < b:
        return 1-(a/b)
    if a == b:
        return 0.0

    return (b/a)-1


# Important parameter used in K-means
# TODO: Define the number of clusterings.
# The number should be possitive and less than 8. Integer.
#ENDTODO
def run(df, k):
    K_means_checkErrorsInParameters(k) # Function that will double-check if your parameters are in the correct range.

    df, centroids = K_means_initialize(df, k) # Function that will initialize the algorithm

    K_means_visualize(df, centroids, name) # Function to visualize the data and how the algorithm works

    df = K_means_assignment(df, centroids) # Function that assigns each data point to a centroid

    K_means_visualize(df, centroids, name) # Function to visualize the data and how the algorithm works

    while True: # Main loop of the program that will run forever
        closest_centroids = df['closest'].copy(deep=True) # Save a copy of the current position of the centroids

        centroids = K_means_update(df, centroids)  # Function that update the centroids position

        df = K_means_assignment(df, centroids)  # Function that assigns each data point to a centroid

        if closest_centroids.equals(df['closest']): # If the centroids did not change
            length = len(df['closest'])
            sum = 0
            for p in range(length):
                sum += s(df, k, p)

            K_means_saveResults(df, centroids, name, problem) # Function that save the results of the algorithm
            return sum / length

        K_means_visualize(df, centroids, name) # Function to visualize the data and how the algorithm works



for k in range (2, 8):
    print(k, run(df, k))
