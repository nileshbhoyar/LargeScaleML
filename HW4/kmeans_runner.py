#!/usr/bin/env python
#START STUDENT CODE45_RUNNER


#!/usr/bin/env python
from numpy import random
from Kmeans import MRKmeans
from itertools import chain
import re,sys
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

def stop_criterion(centroid_points_old, centroid_points_new,T):
    oldvalue = list(chain(*centroid_points_old))
    newvalue = list(chain(*centroid_points_new))
    Diff = [abs(x-y) for x, y in zip(oldvalue, newvalue)]
    Flag = True
    for i in Diff:
        if(i>T):
            Flag = False
            break
    return Flag
##################################################################################
# Use four centroids from the coding
##################################################################################
def partA():
    
    centroids = []
    for i in range(k):
        rndpoints = random.sample(1000)
        total = sum(rndpoints)
        #normalize first
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


def partD():
  
    centroids = []
    counter = 0
    for line in open("topUsers_Apr-Jul_2014_1000-words_summaries.txt").readlines():
        if counter and counter > 1:        
            data = re.split(",",line)
            coords = [float(data[i+3])/float(data[2]) for i in range(1000)]
            centroids.append(coords)
        counter += 1
    return centroids


if part == "A":
    k = 4
    centroids = partA()
if part == "B":
    k = 2
    centroids = startCentroidsBC(k)
if part == "C":
    k = 4
    centroids = startCentroidsBC(k)
if part == "D":
    k = 4
    centroids = partD()



with open("centroids.txt", 'w+') as f:
    for centroid in centroids:
        centroid = [str(coord) for coord in centroid]
        f.writelines(",".join(centroid) + "\n")

iterate = 0
stop = 0

clusters = ["NA" for i in range(k)]
N = ["NA" for i in range(k)]
while(1):
    with mr_job.make_runner() as runner:
        runner.run()
        oldCentroids = centroids[:]
        purities = []
        for line in runner.stream_output():
            key,value =  mr_job.parse_output_line(line)
            clusters[key] = value[0]
            N[key] = value[1]
            centroids[key] = value[2]
            sumCodes = value[3]
            purities.append(float(max(sumCodes))/float(sum(sumCodes)))
        ## update the centroids
        with open("centroids.txt", 'w+') as f:
            for centroid in centroids:
                centroid = [str(coord) for coord in centroid]
                f.writelines(",".join(centroid) + "\n")
        
        print str(iterate+1)+","+",".join(str(purity) for purity in purities)
    iterate += 1    
    if(stop_criterion(oldCentroids,centroids,0.001)):
        break
    


#END STUDENT CODE45_RUNNER