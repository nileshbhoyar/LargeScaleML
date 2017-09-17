#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import re
import mrjob
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
        
  
               
    
        
    def mapper(self, _, recs):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
        fields = recs.split("\t")
        
        products = fields[0].lower().replace('\n','').split()
        for i, term in enumerate(products):
                # Create a new stripe for each term
                stripe = {}

                for j, token in enumerate(products):
                    # Don't count the term's co-occurrence with itself
                    if i != j:
                        x = stripe.get(token,None)
                        if x == None:
                            stripe[token] = int( fields[1])
                        else:
                            stripe[token] += int(fields[1])

                # Emit the term and the stripe
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
                    mapper=self.mapper,       # STEP 1: word count step
                    combiner = self.combiner,
                    reducer=self.reducer
                    )
        return [step]
            


  #END SUDENT CODE531_STRIPES
  
if __name__ == '__main__':
  MRbuildStripes.run()