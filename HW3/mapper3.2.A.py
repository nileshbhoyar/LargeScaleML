#!/usr/bin/env python
# START STUDENT CODE HW32AMAPPER
import sys
import re

sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")
WORD_RE = re.compile(r"[\w']+")
for line in sys.stdin:
    for word  in [s.lower() for s in WORD_RE.findall(line)]:
        print '%s\t%s' % (word, 1)

# END STUDENT CODE HW32AMAPPER