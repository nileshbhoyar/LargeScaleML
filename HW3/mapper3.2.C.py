#!/usr/bin/env python
# START STUDENT CODE HW32CMAPPER
from __future__ import division
import math
import os
import sys
import re

separator = ','
sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")
WORD_RE = re.compile(r"[\w']+")
#numReducers = int(os.environ.get('NUM_PARTITIONS', '4')) 

total = 0

def makeKey(word,n):
  divisor = 26/n
  return int(math.ceil((ord(word[0])-96)/divisor))

#loop through each records
for line in (sys.stdin):
#get 3rd column
        fields = line.split(separator)
        if 'Complaint ID' != fields[0] :
           
            # we have a real record, so do some mapping
            counter_name = None
            for word  in [s.lower() for s in WORD_RE.findall(fields[3])]:
                #key = makeKey(word,numReducers)
                print '%s\t%s' % (word, 1)
                total = total + 1
print '%s\t%s' % ("*total", total)
            


# END STUDENT CODE HW32CMAPPER