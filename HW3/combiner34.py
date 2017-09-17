#!/usr/bin/env python
# START STUDENT CODE HW32CCOMBINER
import sys

cur_key = None
cur_count = 0
mydict = {}
sys.stderr.write("reporter:counter:Combiner Counters,Calls,1\n")
for line in sys.stdin:
    key1,key2, value = line.split()
    key = (key1,key2)
    if key == cur_key:
        cur_count += int(value)
    else:
        if cur_key and cur_count >=100:
            print '%s\t%s\t%s' % (cur_key[0],cur_key[1], cur_count)
        cur_key = key
        cur_count = int(value)

print '%s\t%s\t%s'% (cur_key[0],cur_key[1], cur_count)