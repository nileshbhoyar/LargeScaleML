#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

# START STUDENT CODE 7.1
# (ADD CELLS AS NEEDED)


from __future__ import division 
import re
import random
import sys
import mrjob
from mrjob.job import MRJob 
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

class EDA(MRJob):
    def configure_options(self):
        super(EDA, self).configure_options()
        self.add_passthrough_option('--runtype', default='countnodes')

    def mapper_nodes(self, _, line):
         fields = line.strip().split('\t')
         name = str(eval(fields[0]))
         
         value = eval(fields[1])
         yield name,1
         for node in value:
               yield node,1
                
    def reducer_nodes(self, key, values):
        
         yield key,1
    def mapper_find_sum(self,key,value):
        yield None,1
    def reducer_find_sum(self, key, values):
        yield None, sum(values)
        
    def mapper_links(self, _, line):
         fields = line.strip().split('\t')
         name = str(eval(fields[0]))
         value = eval(fields[1])
        
         degree = len(value)
         yield degree, 1

    def reducer_links(self, degree, frequency):
        yield degree, sum(frequency)
    def mapssum_links(self, _, line):
         fields = line.strip().split('\t')
         name = str(eval(fields[0]))
         value = eval(fields[1])
        
         degree = len(value)
         yield None,degree

    def mapsumreducer_links(self, degree, frequency):
        yield None, sum(frequency)    
    def steps(self): 
       
         if self.options.runtype == 'countnodes':
            return [
                MRStep(mapper=self.mapper_nodes,
                       combiner=self.reducer_nodes,
                       reducer=self.reducer_nodes,
                       jobconf = {
                        'mapred.map.tasks': 500,
                        'mapred.reduce.tasks': 30,
                        'mapreduce.reduce.cpu.vcores':4,
                }
                      ),
                MRStep(mapper=self.mapper_find_sum,
                       reducer=self.reducer_find_sum,
                       jobconf = {
                        'mapred.map.tasks': 50,
                        'mapred.reduce.tasks': 1,
                        'mapreduce.reduce.cpu.vcores':8,
                        }
                      )
                
            ]
         elif self.options.runtype == 'countlinks':
            return [
                MRStep(mapper=self.mapper_links,
                       combiner=self.reducer_links,
                       reducer=self.reducer_links,
                       jobconf = {
                        'mapred.map.tasks': 300,
                        'mapred.reduce.tasks': 1,
                        'mapreduce.reduce.cpu.vcores':8,
                        })
            ]
         elif self.options.runtype == 'sumlinks':
            return [
                MRStep(mapper=self.mapssum_links,
                       combiner=self.mapsumreducer_links,
                       reducer=self.mapsumreducer_links,
                      jobconf = {
                        'mapred.map.tasks': 300,
                        'mapred.reduce.tasks': 1,
                        'mapreduce.reduce.cpu.vcores':8,
                        })
            ]
   
if __name__ == '__main__' and sys.argv[0].find('ipykernel') == -1:
    EDA.run()
# END STUDENT CODE 7.1