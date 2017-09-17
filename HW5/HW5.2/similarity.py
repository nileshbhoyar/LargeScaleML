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
from mrjob.protocol import RawValueProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONProtocol

class MRsimilarity(MRJob):
    INPUT_PROTOCOL = JSONProtocol
 
    SORT_VALUES = True
    def makeKeyn(self,key, num_reducers):
        byteof = lambda char: int(format(ord(char), 'b'), 2)
        current_hash = 0
        for c in key:
            current_hash = (current_hash * 31 + byteof(c))
        return current_hash % num_reducers
    

#START SUDENT CODE531_SIMILARITY
    def mapper_jaccard(self, word, rate_stripe):
        #get all words and lengths
#We will emit stripes for each word vector here.  These stripes will
#be used in combiner to find the common length i.e. words occuring together
        nonzero_keys = [key for key, value in rate_stripe.iteritems() if value != 0]

       

        sorted_keys = sorted(nonzero_keys)
        mydict = {}
        for key,value in rate_stripe.iteritems():
            mydict[key] = str(value)
        #yield None,mydict
        # N * N  complexity matrix calculation
        #We are going over each record to find out the common occureances
        for i in range(0, len(sorted_keys)):
            
            left_label = sorted_keys[i]

            stripe = {}

            for j in range(i + 1, len(sorted_keys)):
                right_label = sorted_keys[j]
                rkey = right_label+'-'+mydict[right_label]
                stripe[rkey] = 1
            nkey =  left_label+'-'+mydict[left_label]
            if len(stripe) > 0:
                yield self.makeKeyn(left_label,10),(nkey,stripe)

     

        for key in sorted_keys:
            break
            yield '*',{key:1}
            #{u'DocC': 1}
        #yield '*', { key: 1 for key in sorted_keys }
    def combiner_jaccard(self, left_label, partial_stripes):
         #yield left_label,partial_stripes
        for key in partial_stripes:
            #mydict[key] = str(value)
            
           
            yield key[0],[self.combine_stripes(key[1])]
        #yield left_label, self.combine_stripes(partial_stripes)

#find out the jaccard values.
    def reducer_jaccard(self, left_labeltotal, partial_stripes):
        self.increment_counter('reducers_custom', 'counter_name', 1)
    
        
        total_stripe = self.combine_stripess(partial_stripes)
#         yield left_labeltotal , total_stripe
#         return
        #this stores the total length of each word Vector
        if left_labeltotal == '*':
            self.total_counts = total_stripe
            return
        
        for right_label, intersection_size in total_stripe.iteritems():
            left_label,left_total = left_labeltotal.split('-')
            right_label,right_total = right_label.split('-')
            coordinate = (left_label, right_label)
            #union_size = self.total_counts[left_label] + self.total_counts[right_label]

            union_size = float(left_total) + float(right_total)
            jaccard_distance = float(intersection_size)/float(union_size - intersection_size) #jaccard
            dice_coef = (float(intersection_size) * 2 )/float(union_size ) #dice Coefficient
            #final = {}
            #final['jaccard'] = jaccard_distance
            #final['dice'] = dice_coef
            #final['average'] = (float(jaccard_distance) + float(dice_coef)) /2
            #if (final['jaccard'] == final['dice'] ) and final['dice'] == 1:
            #    continue
            #else:
            yield  coordinate, ( jaccard_distance,dice_coef,(float(jaccard_distance) + float(dice_coef)) /2)
           

#in-memory combiner
    def combine_stripes(self, stripes):
        combined_stripe = {}
        
        #for stripe in stripes:
        for key, value in stripes.iteritems():
                if key in combined_stripe:
                    combined_stripe[key] += value
                else:
                    combined_stripe[key] = value

        return combined_stripe

    def combine_stripess(self, stripes_all):
        combined_stripe = {}
        
        for stripe in stripes_all:
            for stripes in stripe:
                for key, value in stripes.iteritems():
                    if key in combined_stripe:
                        combined_stripe[key] += value
                    else:
                        combined_stripe[key] = value

        return combined_stripe
    def steps(self):
        JOBCONF_STEP1 = {
            'stream.num.map.output.key.fields':3,
            'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapred.lib.KeyFieldBasedComparator',
            #'stream.map.output.field.separator':"\t",
            'mapreduce.partition.keypartitioner.options':'-k1,1',
            #'mapreduce.partition.keycomparator.options':'-k3,-3nr',
            'mapred.reduce.tasks': 10,
            'partitioner':'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner',
            'mapreduce.job.maps':20,
        
            }
        distance_step = MRStep(
                mapper = self.mapper_jaccard,
                combiner = self.combiner_jaccard,
                reducer = self.reducer_jaccard,
          
                jobconf= JOBCONF_STEP1
                 )
             
        return [distance_step]
#END SUDENT CODE531_SIMILARITY
  
if __name__ == '__main__':
    MRsimilarity.run()