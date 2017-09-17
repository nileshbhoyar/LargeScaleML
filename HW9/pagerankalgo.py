#!/usr/bin/python
from mrjob.job import MRJob
from mrjob.step import MRStep

class pagerankalgo(MRJob):
    DEFAULT_PROTOCOL = 'json'

    def configure_options(self):
        super(pagerankalgo, self).configure_options()        
        self.add_passthrough_option(
            '--i', dest='init', default='0', type='int',
            help='i: run initialization iteration (default 0)')    

    # mapper of first pass of the file (initialization)
    def mapper_job_init(self, _, line):        
        # parse line
        nid, adj = line.strip().split('\t', 1)
        nid = nid.strip('"')
        adj=eval(adj)
        # initialize node struct        
        node = {'a':adj.keys(), 'p':0}
        rankMass = 1.0/len(adj)
        # emit graphs as it
        yield nid, node
        
        # emit pageRank mass    
        for m in node['a']:
            yield m, rankMass
          
    # after initialization
    def mapper_job_iter(self, _, line):             
        # parse line
        nid, node = line.strip().split('\t', 1)
        nid = nid.strip('"')
        node =eval(node)
        # distribute rank mass  
        n_adj = len(node['a'])
        if n_adj > 0:
            rankMass = 1.0*node['p'] / n_adj
            # emit pageRank mass        
            for m in node['a']:
                yield m, rankMass
        else:
            # track dangling mass with counter
            self.increment_counter('dangling_mass', 'mass', int(node['p']*1e10))
        # reset pageRank and emit node
        node['p'] = 0
        yield nid, node
 

    
    # reducer for initialization pass --> need to handle dangling nodes
    def reducer_job_init(self, nid, value):      
        # increase counter for node count
        self.increment_counter('node_count', 'nodes', 1)
        rankMass, node = 0.0, None
        # loop through all arrivals
        for v in value:            
            if isinstance(v, float):
                rankMass += v         
            else:
                node = v
        # dangling node additions
        if not node:            
            node = {'a':[], 'p':rankMass}            
            self.increment_counter('dangling_mass', 'mass', int(1e10))
        else:
            node['p'] += rankMass            
      
        yield nid, node
        
 
    def reducer_job_iter(self, nid, value):              
        rankMass, node = 0.0, None
        # loop through all arrivals
        for v in value:            
            if isinstance(v, float):
                rankMass += v         
            else:
                node = v
        # emit accumulative mass for nid       
        if node:
            node['p'] += rankMass
            yield nid, node
        else:
            yield nid, rankMass

    def steps(self):
     
        return [MRStep(mapper=self.mapper_job_init if self.options.init else self.mapper_job_iter,                       
                                           
                       reducer=self.reducer_job_init if self.options.init else self.reducer_job_iter,
                        jobconf = {
                        'mapred.map.tasks': 100,
                        'mapred.reduce.tasks':20,
                        'mapreduce.reduce.cpu.vcores':4,
                        }
                      
                      )
               ]

if __name__ == '__main__':
    pagerankalgo.run()