#!/usr/bin/env python
from operator import itemgetter
import sys

# START STUDENT CODE HW221REDUCER
import sys
import re
cur_key = None

docClass = 0

wordcount = {}

for line in sys.stdin:
    key, value ,docClass = line.split("\t")
    docClass = docClass.rstrip()
    if key == cur_key:
        wordcount[(docClass,cur_key)]+= int(value)
    else:
        #if cur_key:
        #    print '%s\t%s' % (cur_key, wordcount[(docClass,cur_key)])
        cur_key = key
        
        if docClass == '0':
            wordcount[('0',cur_key)] = int(value)
            wordcount[('1',cur_key)] = 0
        else:
            wordcount[('1',cur_key)] = int(value)
            wordcount[('0',cur_key)] = 0
        #cur_count = int(value)

count  = 0
#print wordcount
for w in sorted(wordcount, key=wordcount.get, reverse=True):
     if w[0] == "0" and count <11: 
        print '%s\t%s\t%s' %(w[0],w[1],wordcount[w])
        count = count +1
count  = 0
for w in sorted(wordcount, key=wordcount.get, reverse=True):
     if w[0] == "1" and count <11: 
        print '%s\t%s\t%s' % (w[0],w[1],wordcount[w])
        count = count +1
#print '%s\t%s' % (cur_key, cur_count)

       
# END STUDENT CODE HW222REDUCER