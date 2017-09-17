#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-

# START STUDENT CODE 7.0
# (ADD CELLS AS NEEDED)


from __future__ import division 
import re
import random
import sys
import mrjob
from mrjob.job import MRJob 
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

class MRSSSP_INIT(MRJob):
   
    
    def configure_options(self):
        super(MRSSSP_INIT, self).configure_options()
        self.add_passthrough_option('--firstnode', default='1')

    def mapper(self, _, line):
         fields = line.strip().split('\t')
         name = fields[0]
         neighbors = eval(fields[1])
         if name == self.options.firstnode:
            yield name, [neighbors, 0, 'Q']
         else:
            yield name, [neighbors, sys.maxint, 'U']    
    def steps(self): 
       
        return [MRStep( mapper=self.mapper)
               ]
   
if __name__ == '__main__' and sys.argv[0].find('ipykernel') == -1:
    MRSSSP_INIT().run()
# END STUDENT CODE 7.0