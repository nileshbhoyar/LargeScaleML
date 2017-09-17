#!/usr/bin/env python
# START STUDENT CODE HW212MAPPER
import sys
import re

for line in sys.stdin:
  line = line.strip()
  for word in re.findall(r'[a-z]+', line.lower()):
    print word,"\t",1


# END STUDENT CODE HW212MAPPER