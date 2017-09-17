#!/usr/bin/env python
#START STUDENT CODE44
from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import csv
from collections import defaultdict
import operator
def read_csvLine(line):
    # Given a comma delimited string, return fields
    for row in csv.reader([line]):
        return row

class MRMostVisitor(MRJob):

#    OUTPUT_PROTOCOL = JSONValueProtocol
    SORT_VALUES = True
    mydict = {}
    def __init__(self, *args, **kwargs):
        super(MRMostVisitor, self).__init__(*args, **kwargs)
      
   
    

   
    def mapper_get_pages(self, _, line):
        # yield each word in the line
        fields = read_csvLine(line)
        #using hint:the maximum visits by any visitor to any given webpage is 1.
        yield fields[1],{fields[4]:1}

    def combiner_count_pages(self, page, visits):
        # sum the words we've seen so far
        
        visitsdict =defaultdict(int)
        for visit in visits: 
            for custID in visit.keys():
                
                visitsdict[custID] += visit[custID]
        yield page,visitsdict
    def reducer_init_function(self):
        with open('attributes.csv', 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                #populating this dictionary to get the url link in future
                #not memory efficient but works as master data is limited.
                self.mydict[row[0]] = row[2]
    
    def reducer_find_top_pages(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        #word_count_pairs = sorted(word_count_pairs,reverse=True)
        count =0
        word_count_pairs = sorted(word_count_pairs)
        for pagedetails in word_count_pairs:
               print pagedetails
                
            
    def reducer_count_pages(self, page, visits):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        visitsdict =defaultdict(int)
        for visit in visits: 
            for custID in visit.keys():
                
                visitsdict[custID] += visit[custID]
        #find max by value
        custID = max(visitsdict.iteritems(), key=operator.itemgetter(1))[0]
        yield None,(page+","+self.mydict[page]+","+custID+","+str(visitsdict[custID]))
       

   


    def steps(self):  #pipeline of Map-Reduce jobs
        
        return [
            MRStep( 
                    
                    mapper=self.mapper_get_pages,       # STEP 1: word count step
                    combiner=self.combiner_count_pages,
                    reducer_init =self.reducer_init_function,
                    reducer=self.reducer_count_pages),
            MRStep(reducer=self.reducer_find_top_pages)
            
        ]

if __name__ == '__main__':
    MRMostVisitor.run()

#END STUDENT CODE44