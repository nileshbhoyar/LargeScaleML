#!/usr/bin/env python
# START STUDENT CODE HW32CFREQREDUCER
import sys

# Initialize variables
total = 0
cur_key = None
cur_count = 0
sys.stderr.write("reporter:counter:Reducer Counters,Calls,1\n")
for line in sys.stdin:
   
    fields = line.replace('\n','').split('\t')
    count = fields[1]
    word = fields[0]
    try:
        count = int(count)
    except ValueError:
        continue
    if word == '*total': 
        total =  total + float(count)
    else: 
        print '%s\t%s\t%2.3f' % (word, count, float(count)/total)  
        #print "{0:20}\t{1:10}\t{2}\n".format(word, count, float(count)/total) 
# END STUDENT CODE HW32CFREQREDUCER