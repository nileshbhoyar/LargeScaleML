#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import re
import numpy as np
import mrjob
from mrjob.protocol import RawProtocol
from mrjob.job import MRJob
from mrjob.step import MRStep

import time
import logging

class mostLeastDenseWords(MRJob):
    
    # START STUDENT CODE 5.4.1.C
    def mapper1(self, _, line):
        line = line.strip()
        tabs = line.split('\t')
        words = tabs[0].split(' ')
        for word1 in words:
            yield ''.join(words),word1
                    
    def reducer1(self, key , values):
        word2list={}
        for value in values:
            if value not in word2list:
                word2list[value]=1
            else:
                word2list[value]+=1
        yield key,word2list
            
    def mapper2(self, key , values):
        for v in values:
            yield v,(values[v],1)
                    
    def combiner2(self, key , values):
        tf=0
        idf=0
        for pair in values:
            tf+=pair[0]
            idf+=pair[1]
        yield key,(tf,idf)
        
    def reducer2(self, key , values):
        tf=0
        idf=0
        for pair in values:
            tf+=pair[0]
            idf+=pair[1]
        yield key,(tf/idf)

    def steps(self):
        JOBCONF_STEP1 = {
            'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapred.lib.KeyFieldBasedComparator',
            'mapreduce.partition.keypartitioner.options':'-nrk2',
            'mapreduce.partition.keycomparator.options':'-nrk2',
            'mapred.map.tasks': 190,
            'mapred.reduce.tasks': 30,
            'mapreduce.reduce.cpu.vcores':4,
            'partitioner':'org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner'
        }
        return [MRStep(jobconf=JOBCONF_STEP1,mapper=self.mapper1,reducer=self.reducer1
                      ),
                MRStep(mapper=self.mapper2,combiner=self.combiner2,reducer=self.reducer2,jobconf={
                    'mapred.map.tasks': 190,
                    'mapreduce.reduce.cpu.vcores':8
                        }
                      )
               ]
    # END STUDENT CODE 5.4.1.C
        
if __name__ == '__main__':
    start_time = time.time()
    mostLeastDenseWords.run()
    elapsed_time = time.time() - start_time
    a = 'time elapsed:', str(elapsed_time)
    logging.warning(a)