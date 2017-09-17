#!/usr/bin/python
from __future__ import division
import math
import os
import sys
import re


count = 0
numReducers = int(os.environ.get('NUM_PARTITIONS', '4')) # default to 4

##################################### PARTITION THE DATA INTO N BUCKETS ####################################
# lowercase chars range from 97 -> 122.
# there are 26 chars. So let's partion by spliting at 26/n 
# ord('a') -> 97
# chr(97) -> 'a'
# ord(word[0])-96  --> get the number of the first letter between 1 and 26, such that a -> 1; z -> 26
############################################################################################################

def makeKey(word,n):
  divisor = 26/n
  return int(math.ceil((ord(word[0])-96)/divisor))


for line in sys.stdin:
  line = line.strip()
  for word in re.findall(r'[a-z]+', line.lower()):
    # prepend a key based on the number of reducers
    key = makeKey(word,numReducers)
    print key,"\t",word,"\t",1