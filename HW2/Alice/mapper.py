#!/usr/bin/env python
# START STUDENT CODE HW213MAPPER

import sys
import re

for line in sys.stdin:
  line = line.strip()
  for word in re.findall(r'[a-z]+', line.lower()):
    if word  == 'alice':
        print word,"\t",1

# END STUDENT CODE HW213MAPPER