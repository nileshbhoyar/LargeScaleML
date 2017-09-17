#!/usr/bin/env python

import sys
#sys.stderr.write("reporter:counter:Tokens,Total,1") # NOTE missing the carriage return so wont work
# Set up counters to monitor/understand the number of times a mapper task is run
sys.stderr.write("reporter:counter:HW2.1 Mapper Counters,Calls,1\n")
sys.stderr.write("reporter:status:processing my message...how are  you\n")

# START STUDENT CODE HW21MAPPER

import re
from collections import defaultdict
 #for each document create dictionary of words

# START STUDENT CODE HW13MAPPER
for line in sys.stdin:
     
  
    #Upper case letters
    for word in re.findall(r'\b[A-Z][a-z]*\b',line):
       
        print '%s\t%s' % ('upper', 1)
    #lower case letters
    for word in re.findall(r'\b[a-z][a-z]*\b',line):
       
        print '%s\t%s' % ('lower', 1)    

# END STUDENT CODE HW21MAPPER