#!/usr/bin/python
from mrjob.job import MRJob
from mrjob.step import MRStep

class distweight(MRJob):
    DEFAULT_PROTOCOL = 'json'

    def configure_options(self):
        super(distweight, self).configure_options()        
        self.add_passthrough_option(
            '--s', dest='size', default=0, type='int',
            help='size: node number (default 0)')    
        self.add_passthrough_option(
            '--j', dest='alpha', default=0.15, type='float',
            help='jump: random jump factor (default 0.15)') 
        self.add_passthrough_option(
            '--m', dest='m', default=0, type='float',
            help='m: rank mass from dangling nodes (default 0)') 
    
    def mapper_init(self):
        self.damping = 1 - self.options.alpha        
        self.p_dangling = self.options.m / self.options.size        
    

            
    def mapper(self, _, line):             
        # parse line
        nid, node = line.strip().split('\t', 1)
        nid = nid.strip('"')
        node =eval(node)     
        node['p'] = (self.p_dangling + node['p']) * self.damping + self.options.alpha
        yield nid, node

    def steps(self):
     
        return [MRStep(mapper_init=self.mapper_init
                       , mapper= self.mapper ,                      
                     jobconf = {
                        'mapred.map.tasks': 100,
                        'mapred.reduce.tasks':20,
                        'mapreduce.reduce.cpu.vcores':4,
                        }
                      )
               ]

if __name__ == '__main__':
    distweight.run()