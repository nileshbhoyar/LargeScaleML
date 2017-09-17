#!/usr/bin/env python
# START STUDENT CODE HW211REDUCER
import sys
import re
cur_key = None
total_count = 0

for line in sys.stdin:
    key, value = line.split()
    if key!= cur_key:
        cur_key = key
        total_count = total_count + 1
    

print '%s\t%s' % ('vocab_size',  total_count)


# END STUDENT CODE HW211REDUCER