#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import re
import mrjob
import csv
import json
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep
from itertools import  combinations
class MRbuildStripes(MRJob):
  
  #START SUDENT CODE531_STRIPES
    SORT_VALUES = True
   
    #def __init__(self, *args, **kwargs):
    #    super(MRjoins, self).__init__(*args, **kwargs)
        
  
    def mapper_init(self):
        self.basis = set()
        self.vocabulary = set()

        with open('features.txt', 'r') as basis_file:
            self.features = set([row[0] for row in csv.reader(basis_file, delimiter = '\t')])

        with open('vocabulary.txt', 'r') as vocabulary_file:
            self.vocabulary = set([row[0] for row in csv.reader(vocabulary_file, delimiter = '\t')])
           
    
        
    def mapper(self, _, recs):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
        fields = recs.split("\t")
        
        products = fields[0].lower().replace('\n','').split()
        for i, term in enumerate(products):
                # Create a new stripe for each term
                stripe = {}
                # check if term is in vocab
                if term not in self.vocabulary:
                        continue
                for j, token in enumerate(products):
                    
                    if i != j:
                        if token not in self.features:
                            continue
                        x = stripe.get(token,None)
                        
                        if x == None:
                            stripe[token] = int( fields[1])
                        else:
                            stripe[token] += int(fields[1])

                # Emit the term and the stripe
                if len(stripe) > 0:
                    yield term, stripe
    
    def combiner(self, word, stripes):
        yield word, self.combine_stripes(stripes)

    def combine_stripes(self, stripes):
        combined_stripe = {}

        for stripe in stripes:
            for key, value in stripe.iteritems():
                if key in combined_stripe:
                    combined_stripe[key] += int(value)
                else:
                    combined_stripe[key] = int(value)

        return combined_stripe
    def reducer(self,key, records):
        yield key, self.combine_stripes(records)
        
    def steps(self):  #pipeline of Map-Reduce jobs
        step = MRStep( 
                    mapper_init=self.mapper_init,
                    mapper=self.mapper,       
                    combiner = self.combiner,
                    reducer=self.reducer,
                    jobconf={
                          'mapreduce.job.reduces': 20,
                           'mapred.map.tasks': 60,
                    }
                    )
        return [step]
            


  #END SUDENT CODE531_STRIPES
  
if __name__ == '__main__':
  MRbuildStripes.run()