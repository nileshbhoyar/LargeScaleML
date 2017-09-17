#!/usr/bin/python

import sys
import re

for line in sys.stdin:
  line = line.strip()
  for word in re.findall(r'[a-z]+', line.lower()):
    print word,"\t",1