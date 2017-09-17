#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

import mrjob
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep

class distribution(MRJob):
    counter=0
    # START STUDENT CODE 5.4.1.D
    def mapper(self, _, line):
        line = line.strip()
        tabs = line.split('\t')
        words = tabs[0]
        yield len(words),1
    def combiner(self,key,value):
        yield key,sum(value)
    def reducer(self, key , value):
        yield key,sum(value)

    def steps(self):
        return [MRStep(mapper=self.mapper,combiner=self.combiner,reducer=self.reducer,jobconf={
            'mapred.map.tasks': 190,
		    'mapreduce.reduce.cpu.vcores':8
        })]
    # END STUDENT CODE 5.4.1.D
    
if __name__ == '__main__':
    distribution.run()