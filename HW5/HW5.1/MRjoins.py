#!/usr/bin/env python
#START STUDENT CODE43

from mrjob.job import MRJob
from mrjob.step import MRStep
import re




class MRjoins(MRJob):

#    OUTPUT_PROTOCOL = JSONValueProtocol
    SORT_VALUES = True
   
    #def __init__(self, *args, **kwargs):
    #    super(MRjoins, self).__init__(*args, **kwargs)
    def configure_options(self):
        super(MRjoins, self).configure_options()
        self.add_passthrough_option('--join-type', type = 'string', default = 'left')      
       
    def mapper_init_leftjoin(self):
        self.country = {}
        with open('Countries.dat', 'r') as country:
            for line in country:
                tokens = line.split('|')
                # the entry is the page id => ( url : count )
                self.country[tokens[1].strip('\n')] = tokens[0]
            
    
        
    def mapper(self, _, line):
        self.increment_counter('Execution Counts', 'mapper calls', 1)

        fields = line.split("|")
        if fields[2].strip('\n') in self.country:
            sline = line + '|'+ self.country[fields[2].strip('\n')]
            yield None,sline
            
        else:
            yield None,line
    def mapper_innerjoin(self, _, line):
        self.increment_counter('Execution Counts', 'mapper calls', 1)

        fields = line.split("|")
        if fields[2].strip('\n') in self.country:
            sline = line + '|'+ self.country[fields[2].strip('\n')]
            yield None,sline
            
    def mapper_rightjoin(self, _, line):
        self.increment_counter('Execution Counts', 'mapper calls', 1)
        fields = line.split("|")
        keys =fields[2].strip('\n')
        if keys in self.country:
            sline = line + '|'+ self.country[keys]
            yield None,sline  
   

    def reducer_init(self):
        self.country = {}
        with open('Countries.dat', 'r') as f:
            for line in f:
                tokens = line.split('|')
                # the entry is the page id => ( url : count )
                self.country[tokens[1].strip('\n')] = tokens[0]
        
    def reducer(self,key, records):
        self.increment_counter('Execution Counts', 'reducer count', 1) 
        passedkeys = set()
        for rec in records:
            fields = rec.split("|")
            passedkeys.add(fields[2])
            yield None,[fields[0],fields[1],fields[2],fields[3]]
        for element in self.country.keys():
            if element not in passedkeys:
                yield None,[None,None,element,self.country[element]]
        
    def steps(self):  #pipeline of Map-Reduce jobs
        JOBCONF_STEP = {
            'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapred.lib.KeyFieldBasedComparator',
            'stream.map.output.field.separator':'\t',    
            'mapreduce.partition.keycomparator.options': '-k1,1nr -k2',
            'mapreduce.job.reduces': '1',
            
        }
        if self.options.join_type == 'left':
             step = MRStep( mapper_init=self.mapper_init_leftjoin,
                    mapper=self.mapper,       # STEP 1: word count step
                    )
        elif self.options.join_type == 'inner':
             step = MRStep( mapper_init=self.mapper_init_leftjoin,
                    mapper=self.mapper_innerjoin,       # STEP 1: word count step
                    )
        else:
             step =  MRStep( 
                    mapper_init=self.mapper_init_leftjoin,
                    mapper=self.mapper_rightjoin, 
                    reducer_init = self.reducer_init,
                    reducer=self.reducer
                    )
        return [step]
            
            

if __name__ == '__main__':
    MRjoins.run()


#END STUDENT CODE43