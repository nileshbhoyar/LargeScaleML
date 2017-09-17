#!/usr/bin/env python
#START STUDENT CODE43

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import csv

def read_csvLine(line):
    # Given a comma delimited string, return fields
    for row in csv.reader([line]):
        return row

class MRMostVisitor(MRJob):

#    OUTPUT_PROTOCOL = JSONValueProtocol
    SORT_VALUES = True
    
    def __init__(self, *args, **kwargs):
        super(MRMostVisitor, self).__init__(*args, **kwargs)
        self.N = 5
       
        
    def mapper_init_pages(self):
        self.N = 5 #to check why this assignment not working.
    def mapper_get_pages(self, _, line):
        # yield each word in the line
        fields = read_csvLine(line)
        yield (fields[1],fields[4]) ,1

    def combiner_count_pages(self, page, counts):
        # sum the words we've seen so far
        yield (page, sum(counts))

    def reducer_count_pages(self, page, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        yield None, (sum(counts), page)

    # discard the key; it is just None
    def reducer_find_top_pages(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        word_count_pairs = sorted(word_count_pairs,reverse=True)
        for i in range(self.N):#as only top 5 pages requested
            yield word_count_pairs[i]

    def steps(self):  #pipeline of Map-Reduce jobs
        return [
            MRStep( mapper_init = self.mapper_init_pages,
                    mapper=self.mapper_get_pages,       # STEP 1: word count step
                    combiner=self.combiner_count_pages,
                    reducer=self.reducer_count_pages),
            MRStep(reducer=self.reducer_find_top_pages) # Step 2: most frequent word
        ]

if __name__ == '__main__':
    MRMostVisits.run()