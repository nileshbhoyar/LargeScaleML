#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

import re

import mrjob
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys
class longest5gram(MRJob):
    
    # START STUDENT CODE 5.4.1.A
    

    def mapper(self, _,recs):
        fields = recs.split("\t")
        ngram_length = len(fields[0])
        yield None, (ngram_length, fields[0])

   
    def combiner(self, _, pairs):
        yield None, self.get_longest_ngram(pairs)

   
    def reducer(self, _, pairs):
        ngram_length, ngram = self.get_longest_ngram(pairs)
        yield None,(ngram_length, ngram)
    def reducer_second(self, _,pairs):
        ngram_length, ngram = self.get_longest_ngram(pairs)
        yield ngram_length, ngram
        #yield None,pairs
    
    def get_longest_ngram(self, pairs):
        longest_ngram = None
        longest_ngram_length = 0

        for ngram_length, ngram in pairs:
            if ngram_length > longest_ngram_length:
                longest_ngram = ngram
                longest_ngram_length = ngram_length
            elif ngram_length == longest_ngram_length and ngram < longest_ngram:
                longest_ngram = ngram

        return longest_ngram_length, longest_ngram
    def steps(self):  #pipeline of Map-Reduce jobs
     
        return [
            MRStep( 
                    mapper=self.mapper,       
                    combiner=self.combiner,
                    reducer=self.reducer,
                    jobconf = {
                    'mapreduce.job.reduces': 5,
                    'mapreduce.reduce.cpu.vcores':8
                }
                
            ),
            MRStep(reducer=self.reducer_second,
                  jobconf = {
                    'mapreduce.job.reduces': 1,
                    'mapreduce.reduce.cpu.vcores':8
                }
                  ) # Step 2: most frequent word
        ]


    # END STUDENT CODE 5.4.1.A
    
if __name__ == '__main__' and sys.argv[0].find('ipykernel') == -1:
    longest5gram().run()