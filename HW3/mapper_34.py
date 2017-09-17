#!/usr/bin/python
## mapper.py

import sys
from itertools import  combinations

# Increment mapper counter
sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")

# Initialize variables
total = 0

# Our input comes from STDIN (standard input)
for line in sys.stdin:
    # Split our line into products
    products = line.replace('\n','').split()
    
    # Get all combinations of products:
    #  - Use a set to remove duplicate products
    #  - Combinations finds tuples of length 2 with no repeats
    for pair in combinations(sorted(set(products)), 2):
                print '%s\t%s\t%s' % (pair[0], pair[1], 1)
    
    total += 1
# Print total words
print '%s\t%s\t%s' % ('*total', '*total', total)