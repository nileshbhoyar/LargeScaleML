#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import collections
import re
import json
import math
import numpy as np
import itertools
import mrjob
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol

class MRsimilarity(MRJob):
    INPUT_PROTOCOL = JSONProtocol
    SORT_VALUES = True

#START SUDENT CODE531_SIMILARITY
    def mapper_jaccard(self, word, rate_stripe):
        #get all words and lengths
#We will emit stripes for each word vector here.  These stripes will
#be used in combiner to find the common length i.e. words occuring together
        nonzero_keys = [key for key, value in rate_stripe.iteritems() if value != 0]

    

        sorted_keys = sorted(nonzero_keys)
        # N * N  complexity matrix calculation
        #We are going over each record to find out the common occureances
        for i in range(0, len(sorted_keys)):
            left_label = sorted_keys[i]

            stripe = {}

            for j in range(i + 1, len(sorted_keys)):
                right_label = sorted_keys[j]
                stripe[right_label] = 1

            yield left_label, stripe

     

        for key in sorted_keys:
            yield '*',{key:1}
            #{u'DocC': 1}
        #yield '*', { key: 1 for key in sorted_keys }
    def combiner_jaccard(self, left_label, partial_stripes):
        yield left_label, self.combine_stripes(partial_stripes)

#find out the jaccard values.
    def reducer_jaccard(self, left_label, partial_stripes):
        total_stripe = self.combine_stripes(partial_stripes)
        #this stores the total length of each word Vector
        if left_label == '*':
            self.total_counts = total_stripe
            return

        for right_label, intersection_size in total_stripe.iteritems():
            coordinate = (left_label, right_label)
            union_size = self.total_counts[left_label] + self.total_counts[right_label]

            
            jaccard_distance = float(intersection_size)/float(union_size - intersection_size) #jaccard
            dice_coef = (float(intersection_size) * 2 )/float(union_size ) #dice Coefficient
            final = {}
            final['jaccard'] = jaccard_distance
            final['dice'] = dice_coef
            yield coordinate, final

#in-memory combiner
    def combine_stripes(self, stripes):
        combined_stripe = {}

        for stripe in stripes:
            for key, value in stripe.iteritems():
                if key in combined_stripe:
                    combined_stripe[key] += value
                else:
                    combined_stripe[key] = value

        return combined_stripe

   
    def steps(self):
         distance_step = MRStep(
                mapper = self.mapper_jaccard,
                combiner = self.combiner_jaccard,
                reducer = self.reducer_jaccard,
                jobconf = {
                    'mapreduce.job.reduces': 1
                    
                })
         return [distance_step]
#END SUDENT CODE531_SIMILARITY
  
if __name__ == '__main__':
    MRsimilarity.run()