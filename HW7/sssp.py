#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

# START STUDENT CODE 7.0
# (ADD CELLS AS NEEDED)


from __future__ import division 
import re
import random
import sys
import mrjob
from mrjob.job import MRJob 
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

class MRSSSP(MRJob):
   
    def mapper(self, _, line):
         fields = line.strip().split('\t')
         name = str(eval(fields[0]))
         value = eval(fields[1])
         neighbors = value[0]
         distance = int(value[1])
         status = value[2]
         path= []
         if len(value) > 3:
             path = value[3]


         if status == 'Q':
                     
            self.increment_counter('group', 'QQ_counter', 1)
            yield name, [neighbors, distance, 'V', path]
            if neighbors:
                for node in neighbors:
                    temp_path = list(path)
                    temp_path.append(node)
                  
                    yield str(node), [None, distance + int(neighbors[node]) , 'Q',temp_path]
         else:
            yield name, [neighbors, distance, status,path]
    
    def reducer(self, key, values):
        neighbors = {}
        distance = sys.maxint
        status = None
        path = []

      
        for val in values:

            #if already visited nothing to do than pass through
            if val[2] == 'V':
                neighbors = val[0]
                distance = val[1]
                status = val[2]
                path = val[3]
                break

#for frontiers we just need to find all neighbours and update the distance from mapper entry
            elif val[0]:
                neighbors = val[0]
                if status != 'Q':
                    status = val[2]

            else:
                status = val[2]
                path = val[3]
  
            # Update minimum distance if necessary
            distance = min(distance, val[1])

        yield key, [neighbors, distance, status,path]
        
    def steps(self): 
       
        return [MRStep( 
                        mapper=self.mapper,
                        reducer=self.reducer,
                        jobconf = {
                        'mapred.map.tasks': 100,
                        'mapred.reduce.tasks':20,
                        'mapreduce.reduce.cpu.vcores':4,
                        })
               ]
   
if __name__ == '__main__' and sys.argv[0].find('ipykernel') == -1:
    MRSSSP.run()
# END STUDENT CODE 7.0