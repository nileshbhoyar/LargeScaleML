#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

import re

import mrjob
from mrjob.protocol import RawProtocol

#from mrjob.protocol import  RawValueProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep

from collections import defaultdict

class mostFrequentWords(MRJob):
    INPUT_PROTOCOL = RawProtocol
    
   
    
    # START STUDENT CODE 5.4.1.B
    INPUT_PROTOCOL = RawProtocol
    MRJob.SORT_VALUES = True
    
    def mapper(self, key, value):
        words = re.findall("\w+", key.lower())
        #words =word_tokenize(key.lower())

        for word in words:
            yield word,1

  
    def combiner(self, word, counts):
      
         yield word, sum(counts)   

    def reducer(self, word, counts):

         yield word, sum(counts)
    def steps(self):
        return [
            MRStep( 
                    mapper=self.mapper,
                    combiner=self.combiner,
                    reducer=self.reducer,
                    jobconf = {
                    'mapreduce.job.reduces': 40,
                    'mapreduce.reduce.cpu.vcores':8
                    }
                  ),]
  
        
        
if __name__ == '__main__':
    mostFrequentWords.run()