#!~/anaconda2/bin/python
# -*- coding: utf-8 -*-
from __future__ import division 
import re
import random
import sys
import mrjob
from mrjob.job import MRJob 
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol

class MRbuildSample(MRJob):
   
    OUTPUT_PROTOCOL = RawValueProtocol
    INPUT_PROTOCOL = RawValueProtocol
    def configure_options(self):
        super(MRbuildSample, self).configure_options()

        self.add_passthrough_option(
            '--sampling-factor', type = 'float', default = 0.01)

    def mapper(self, _, line):
        if random.random() <= self.options.sampling_factor:
            yield None, line
    def steps(self): 
       
        return [MRStep( mapper=self.mapper)
               ]
   
if __name__ == '__main__' and sys.argv[0].find('ipykernel') == -1:
    MRbuildSample().run()