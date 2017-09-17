#!/usr/bin/env python
# START STUDENT CODE HW32CFREQMAPPER
from __future__ import division
import math
import os
import sys
import re

separator = ','
sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")
WORD_RE = re.compile(r"[\w']+")

#loop through each records
for line in sys.stdin:
    print line.strip()
            


# END STUDENT CODE HW32CFREQMAPPER