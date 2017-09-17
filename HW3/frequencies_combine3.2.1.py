#!/usr/bin/env python
import sys
import os
# Initialize variables
total = 0
cur_key = ("key1","key2")
cur_count = 0
sys.stderr.write("reporter:counter:combiner Counters,Calls,1\n")

for line in sys.stdin:
   
        partkey,key1, value = line.split()
        partkey = partkey
        key = (partkey,key1)
        if key1 == cur_key[1]:
            cur_count += int(value)
        else:
            if cur_key!= ("key1","key2"):
                print '%s\t%s\t%d' % (cur_key[0],cur_key[1], cur_count)
            cur_key = key
            cur_count = int(value)

print '%s\t%s\t%d' % (cur_key[0],cur_key[1], cur_count)  