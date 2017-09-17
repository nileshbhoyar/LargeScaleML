#!/usr/bin/env python

import sys
#sys.stderr.write("reporter:counter:Tokens,Total,1") # NOTE missing the carriage return so wont work
# Set up counters to monitor/understand the number of times a mapper task is run
sys.stderr.write("reporter:counter:HW2.0.1 Mapper Counters,Calls,1\n")
sys.stderr.write("reporter:status:processing my message...how are  you\n")

for line in sys.stdin:
    for word in line.split():
        print '%s\t%s' % (word, 1)