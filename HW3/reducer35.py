#!/usr/bin/env python
# START STUDENT CODE HW32AREDUCER
import sys
from collections import OrderedDict
#from collections import collections
#import collections
prev_key = None
cur_count = 0
prev_stripe = {}
largest = []
dictcounts = {}
sys.stderr.write("reporter:counter:Reducer Counters,Calls,1\n")

for line in sys.stdin:
    
    fields = line.replace('\n','').split('\t')
    key = fields[0]
    
    stripe = eval(fields[1])
    
    
    if prev_key == key:
        # We need to move through the dictionary and update counts
        for item in stripe:
            if item in prev_stripe:
                prev_stripe[item] += stripe[item]
            else:
                prev_stripe[item] = stripe[item]
        
    else:
        if len(prev_stripe) > 0:
            # We are at a new pair, need to print previous pair sum
            #print '%s\t%s' % (prev_key, prev_stripe)
            for word in prev_stripe:
                dictcounts[(prev_key,word)] = prev_stripe[word]
        prev_stripe = stripe
        prev_key = key

# Output the last line
if prev_stripe == stripe:
    for word in prev_stripe:
        dictcounts[(prev_key,word)] = prev_stripe[word]
totals = dictcounts[('*total','*total')]
dictcounts =OrderedDict(sorted(dictcounts.items(), key=lambda t: t[1], reverse=True))
count  = 0
print "*****Top 50 Products*************"
for key in dictcounts:
    if count <= 100 and count%2 == 0:
        print '%s\t%s\t%d\t%2.3f' %(key[0],key[1],dictcounts[key] ,float(dictcounts[key])/totals )
    count += 1