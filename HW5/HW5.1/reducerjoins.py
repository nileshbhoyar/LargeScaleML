import sys, os, re
from mrjob.job import MRJob
from mrjob.step import MRStep


class MRJoin(MRJob):

  # Performs secondary sort
  #    OUTPUT_PROTOCOL = JSONValueProtocol
  SORT_VALUES = True
   
    #def __init__(self, *args, **kwargs):
    #    super(MRjoins, self).__init__(*args, **kwargs)
  def configure_options(self):
        super(MRJoin, self).configure_options()
        self.add_passthrough_option('--join-type', type = 'string', default = 'left')      


  def mapper(self, _, line):
    splits = line.rstrip("\n").split("|")

    if len(splits) == 2: # country data
      symbol = 'A' # make country sort before transaction data
      country2digit = splits[1]
      yield country2digit, [symbol, splits]
    else: # person data
      symbol = 'B'
      country2digit = splits[2]
      yield country2digit, [symbol, splits]

  def reducer_inner(self, key, values):
    countries = {}
    for value in values:
      if value[0] == 'A':
        countries[value[1][1]] = value[1][0]
      if value[0] == 'B':
        if  key in countries:
           yield key, countries[key] + value[1][0] + value[1][1] + value[1][2]

  def reducer_left(self, key, values):
    countries = {} # should come first, as they are sorted on artificia key 'A'
    for value in values:
      if value[0] == 'A':
        countries[value[1][1]] = value[1][0]
      if value[0] == 'B':
        if  key in countries:
           yield key, countries[key] + value[1][0] + value[1][1] + value[1][2]
        else:
            yield key,"None"+ value[1][0] + value[1][1] + value[1][2]
           
  def reducer_init(self):
     self.countries = {}  #this is used in final method to do filtering on right join
     self.passed_countries = set()
  def reducer_right(self, key, values):
   
    for value in values:
      if value[0] == 'A':
        self.countries[value[1][1]] = value[1][0]
      if value[0] == 'B':
        if  key in self.countries:
           yield key, self.countries[key] + value[1][0] + value[1][1] + value[1][2]
           self.passed_countries.add(key)
  def reducer_right_final(self):
    for element in self.countries:
            if element not in self.passed_countries:
                yield element,self.countries[element]+"None" + "None"
     
           #yield key, ["None"] + value[1][0] + value[1][1] + value[1][2]      

  def steps(self):  #pipeline of Map-Reduce jobs
     
        if self.options.join_type == 'left':
             step = MRStep( 
                    mapper=self.mapper,       # STEP 1: word count step
                    reducer=self.reducer_left 
                    )
        elif self.options.join_type == 'inner':
             step = MRStep(  mapper=self.mapper,       # STEP 1: word count step
                    reducer=self.reducer_inner
                    )
        else:
             step =  MRStep( 
                     mapper=self.mapper,       # STEP 1: word count step
                    reducer=self.reducer_right,
                    reducer_final = self.reducer_right_final,
                    reducer_init = self.reducer_init,
                  jobconf = {
                    'mapreduce.job.reduces': 1
                }
                    )
        return [step]
if __name__ == '__main__':
  MRJoin.run()