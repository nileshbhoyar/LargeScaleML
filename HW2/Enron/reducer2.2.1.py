#!/usr/bin/env python
from operator import itemgetter
import sys

# START STUDENT CODE HW221REDUCER
import sys
import re
cur_key = None
cur_count = 0

for line in sys.stdin:
    key, value = line.split()
    if key == cur_key:
        cur_count += int(value)
    else:
        if cur_key:
            print '%s\t%s' % (cur_key, cur_count)
        cur_key = key
        cur_count = int(value)

print '%s\t%s' % (cur_key, cur_count)

       
# END STUDENT CODE HW221REDUCER