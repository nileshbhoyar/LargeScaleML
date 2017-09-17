#!/usr/bin/env python
from numpy import random

import re,sys




scriptName,part = sys.argv


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

###################################################################################
## Geneate random initial centroids around the global aggregate
###################################################################################
def startCentroidsBC(k):
    counter = 0
    for line in open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines():
        if counter == 2:        
            data = re.split(",",line)
            globalAggregate = [float(data[i+3])/float(data[2]) for i in range(1000)]
        counter += 1
    ## perturb the global aggregate for the four initializations    
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
###################################################################################

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

## the totals for each user type
numType = [752,91,54,103]
numType = [float(numType[i]) for i in range(4)]

with open("centroids.txt", 'w+') as f:
    for centroid in centroids:
        centroid = [str(coord) for coord in centroid]
        f.writelines(",".join(centroid) + "\n")