#!/usr/bin/env python
from __future__ import division
import math
import os
import sys
import re


count = 0


separator = ','
#create partition key
def makeKeyn(word):
  if ord(word[0]) in range(ord('a'), ord('m')):
     return 'A'
  else:
     return 'B'
#regex for word extraction
WORD_RE = re.compile(r"[\w']+")
for line in sys.stdin:
    fields = line.split(separator)
    if 'Complaint ID' != fields[0]:
        for word  in [s.lower() for s in WORD_RE.findall(fields[3])]:
    # prepend a key based on the number of reducers
            key = makeKeyn(word)
            count = count + 1
            print key,"\t",word,"\t",1
print 'A',"\t","*total","\t",count #to get total in all combiners
print 'B',"\t","*total","\t",count
 