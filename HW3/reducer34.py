#!/usr/bin/env python
# START STUDENT CODE HW32AREDUCER
import sys
from collections import OrderedDict

cur_key = None
cur_count = 0
dictcounts = {}
largest = []
sys.stderr.write("reporter:counter:Reducer Counters,Calls,1\n")
for line in sys.stdin:
    key1,key2, value = line.split()
    key = (key1,key2)
    if key1 != '*total':    
        if key == cur_key:
            cur_count += int(value)
        else:
            if cur_key:
                dictcounts[cur_key] = cur_count
            #print '%s\t%s' % (cur_key, cur_count)
            cur_key = key
            cur_count = int(value)
    else:
        if key1 == '*total':
            largest.append(int(value))

totals = sum(largest)
dictcounts =OrderedDict(sorted(dictcounts.items(), key=lambda t: t[1], reverse=True))
count  = 0
print "*****Top 50 Products*************"
for key in dictcounts:
    if count <= 49:
        print '%s\t%s\t%d\t%2.3f' %(key[0],key[1],dictcounts[key] ,float(dictcounts[key])/totals )
    count += 1