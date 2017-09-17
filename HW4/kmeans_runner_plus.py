#!/usr/bin/env python
#START STUDENT CODE46_RUNNER


#!/usr/bin/env python
from numpy import random
from Kmeansparallel import MRKmeans
import re,sys
import numpy as np
mr_job = MRKmeans(args=["topUsers_Apr-Jul_2014_1000-words.txt","--file","centroids.txt"])

thresh = 0.0001

scriptName,part = sys.argv

## only stop when distance is below thresh for all centroids
def stopSignal(k,thresh,newCentroids,oldCentroids):
    stop = 1
    for i in range(k):
        dist = 0
        for j in range(len(newCentroids[i])): 
            dist += (newCentroids[i][j] - oldCentroids[i][j]) ** 2
        dist = dist ** 0.5
        if (dist > thresh):
            stop  = 0
            break
    return stop

##################################################################################
# Use four centroids from the coding
##################################################################################
def startCentroidsA():
    k = 4
    centroids = []
    for i in range(k):
        rndpoints = random.sample(1000)
        total = sum(rndpoints)
        centroid = [pt/total for pt in rndpoints]
        centroids.append(centroid)
    return centroids
###################################################################################
def startCentroidsBC(k):
    counter = 0
    for line in open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines():
        if counter == 1:        
            data = re.split(",",line)
            globalAggregate = [float(data[i+3])/float(data[2]) for i in range(1000)]
        counter += 1
    #perturb the global aggregate for the four initializations    
    centroids = []
    for i in range(k):
        rndpoints = random.sample(1000)
        peturpoints = [rndpoints[n]/10+globalAggregate[n] for n in range(1000)]
        centroids.append(peturpoints)
        total = 0
        for j in range(len(centroids[i])):
            total += centroids[i][j]
        for j in range(len(centroids[i])):
            centroids[i][j] = centroids[i][j]/total
    return centroids

##################################################################################
# Use four centroids from the coding
##################################################################################
def startCentroidsD():
    k = 4
    centroids = []
    counter = 0
    for line in open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines():
        if counter and counter > 1:        
            data = re.split(",",line)
            coords = [float(data[i+3])/float(data[2]) for i in range(1000)]
            centroids.append(coords)
        counter += 1
    return centroids
###################################################################################

if part == "A":
    k = 4
    centroids = startCentroidsA()
if part == "B":
    k = 2
    centroids = startCentroidsBC(k)
if part == "C":
    k = 4
    centroids = startCentroidsBC(k)
if part == "D":
    k = 4
    centroids = startCentroidsD()



#data = np.loadtxt('topUsers_Apr-Jul_2014_1000-words_summaries.txt',delimiter = ",")

centroids_list = []
counter = 0
for line in open("topUsers_Apr-Jul_2014_1000-words.txt").readlines():
    if counter and counter > 1:        
        data = re.split(",",line)
        coords = [float(data[i+3]) for i in range(1000)]
        centroids_list.append(coords)
    counter += 1
data = np.asarray(centroids_list)        
centroids = data[np.random.choice(range(data.shape[0]),1), :]
data_ex = data[:, np.newaxis, :]

        # run k - 1 passes through the data set to select the initial centroids
while centroids.shape[0] < 4 :
            #print (centroids)
            euclidean_dist = (data_ex - centroids) ** 2
            distance_arr = np.sum(euclidean_dist, axis=2)
            min_location = np.zeros(distance_arr.shape)
            min_location[range(distance_arr.shape[0]), np.argmin(distance_arr, axis=1)] = 1
            # calculate J
            j_val = np.sum(distance_arr[min_location == True])
            # calculate the probability distribution
            prob_dist = np.min(distance_arr, axis=1)/j_val
            # select the next centroid using the probability distribution calculated before
            centroids = np.vstack([centroids, data[np.random.choice(range(data.shape[0]),1, p = prob_dist), :]])
centroid_points = centroids


with open('Centroids.txt', 'w+') as f:
        f.writelines(','.join(str(j) for j in i) + '\n' for i in centroid_points)


iterate = 0
stop = 0

clusters = ["NA" for i in range(k)]
N = ["NA" for i in range(k)]

while(not stop):
    print "iteration"+str(iterate)+":"
    with mr_job.make_runner() as runner:
        runner.run()
        oldCentroids = centroids[:]
        clusterPurities = []
        for line in runner.stream_output():
            key,value =  mr_job.parse_output_line(line)
            clusters[key] = value[0]
            N[key] = value[1]
            centroids[key] = value[2]
            sumCodes = value[3]
            clusterPurities.append(float(max(sumCodes))/float(sum(sumCodes)))
        ## update the centroids
        with open("centroids.txt", 'w+') as f:
            for centroid in centroids:
                centroid = [str(coord) for coord in centroid]
                f.writelines(",".join(centroid) + "\n")
        
        print str(iterate+1)+","+",".join(str(purity) for purity in clusterPurities)
        stop = stopSignal(k,thresh,centroids,oldCentroids)
        if not iterate:
            stop = 0
    iterate += 1


#END STUDENT CODE46_RUNNER