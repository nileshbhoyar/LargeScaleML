#!/usr/bin/env python
#START STUDENT CODE46
from numpy import argmin, array, random
from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import chain
import os
import re

#Calculate find the nearest centroid for data point 
#copied from http://nbviewer.jupyter.org/urls/dl.dropbox.com/s/oppgyfqxphlh69g/MrJobKmeans_Corrected.ipynb
def MinDist(datapoint, centroid_points):
    datapoint = array(datapoint)
    centroid_points = array(centroid_points)
    diff = datapoint - centroid_points 
    diffsq = diff*diff
    # Get the nearest centroid for each instance
    minidx = argmin(list(diffsq.sum(axis = 1)))
    return minidx

#Check whether centroids converge

#copied from http://nbviewer.jupyter.org/urls/dl.dropbox.com/s/oppgyfqxphlh69g/MrJobKmeans_Corrected.ipynb
def stop_criterion(centroid_points_old, centroid_points_new,T):
    oldvalue = list(chain(*centroid_points_old))
    newvalue = list(chain(*centroid_points_new))
    Diff = [abs(x-y) for x, y in zip(oldvalue, newvalue)]
    # if centroids are not changing enough
    Flag = True
    for i in Diff:
        if(i>T):
            Flag = False
            break
    return Flag

class MRKmeans(MRJob):
    centroid_points=[]
    k = 4
    n = 1000   
    def steps(self):
        return [
            MRStep(mapper_init = self.mapper_init, mapper=self.mapper,combiner = self.combiner,reducer=self.reducer)
               ]
    #load centroids info from file
    def mapper_init(self):
         self.centroid_points = [map(float,s.split('\n')[0].split(',')) for s in open("centroids.txt").readlines()]
        
    #load data and output the nearest centroid index and data point 
    def mapper(self, _, line):
        total = 0
        data = re.split(',',line)
        ID = data[0]
        code = int(data[1])
        users = [ID]
        codes = [0,0,0,0] #one hot representations
        codes[code] = 1
        coords = [float(data[i+3])/float(data[2]) for i in range(1000)]
        for coord in coords:
            total += coord

        
        #generate key value pair.  Key --> 0-3 class of user and then value is user/1/cordinates and codes
        yield (int(MinDist(coords,self.centroid_points)),[users,1,coords,codes])
        
    #Combine sum of data points locally
    def combiner(self, idx, inputdata):
        N = 0
        sumCoords = [0*num for num in range(1000)]
        sumCodes = [0,0,0,0]
        users = []
        for line in inputdata:
            users.extend(line[0]) #add user in user list
            N += line[1]
            coords = line[2]
            codes = line[3]
            #sum of all cordinates used in reducer for new center
            sumCoords = [sumCoords[i]+coords[i] for i in range(len(sumCoords))] 
            #sum all codes
            sumCodes = [sumCodes[i]+codes[i] for i in range(len(sumCodes))] 
        yield (idx,[users,N,sumCoords,sumCodes])
        
    #Aggregate sum for each cluster and then calculate the new centroids
    def reducer(self, idx, inputdata): 
        N = 0
        sumCoords = [0*num for num in range(1000)]
        sumCodes = [0,0,0,0]        
        users = []
        
        for line in inputdata:
            users.extend(line[0])
            N += line[1]
            coords = line[2]
            codes = line[3]
            sumCoords = [sumCoords[i]+coords[i] for i in range(len(sumCoords))]
            sumCodes = [sumCodes[i]+codes[i] for i in range(len(sumCodes))]
        centroid = [sumCoords[i]/N for i in range(len(sumCoords))] #calculate the new centroid here.
        #sumcodes are needed to find out purity in runner section
        yield (idx,[users,N,centroid,sumCodes])
      
if __name__ == '__main__':
    MRKmeans.run()


#END STUDENT CODE46