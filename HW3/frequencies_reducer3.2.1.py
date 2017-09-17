#!/usr/bin/env python
import sys
import os
# Initialize variables
total = 0
cur_key = None
cur_count = 0
sys.stderr.write("reporter:counter:Reducer Counters,Calls,1\n")
dictcounts = {}
#totalrecs = int(os.environ.get('TOTAL_RECS', '980482')) 
for line in sys.stdin:
   
    fields = line.replace('\n','').split('\t')
    count = fields[2]
    word = fields[1]
    try:
        count = int(count)
    except ValueError:
        continue
    if word == '*total': #not required in multireducers
        total =  total + int(count)
    else:
        x = dictcounts.get(word,None)
        if x != None:
            dictcounts[word]+=count
        else:
            dictcounts[word]=count
for key in dictcounts:
   
        print '%s\t%d\t%2.3f' %(key,dictcounts[key] ,float(dictcounts[key])/total)

        #print '%s,%s\t%s\t%2.3f' % (fields[0],word, count, float(count)/total)  