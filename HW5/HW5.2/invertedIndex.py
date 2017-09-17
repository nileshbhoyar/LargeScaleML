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
class MRinvertedIndex(MRJob):
    INPUT_PROTOCOL = JSONProtocol
    SORT_VALUES = True
#START SUDENT CODE531_INV_INDEX
    def mapper_normalize_transpose(self, word, rate_stripe):



        # Divide each value in the vector by the magnitude to normalize.
        length = len(rate_stripe)
        for key, value in rate_stripe.iteritems():
            #normalized_value = value / magnitude
            yield key, { word: length}
    def combiner_normalize_transpose(self, word, transpose_stripes):
        yield word, self.combine_stripes(transpose_stripes)
    def reducer_normalize_transpose(self, word, transpose_stripes):
        yield word, self.combine_stripes(transpose_stripes)
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

        transpose_step = MRStep(
            mapper = self.mapper_normalize_transpose,
            combiner = self.combiner_normalize_transpose,
            reducer = self.reducer_normalize_transpose,
            jobconf = {
                    'mapreduce.job.reduces': 10
                })
        return [transpose_step]

#END SUDENT CODE531_INV_INDEX
        
if __name__ == '__main__':
    MRinvertedIndex.run() 