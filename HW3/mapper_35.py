#!/usr/bin/python
## mapper.py

import sys
from itertools import  combinations
#import collections

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
   
    for i, term in enumerate(products):
                # Create a new stripe for each term
                stripe = {}

                for j, token in enumerate(products):
                    # Don't count the term's co-occurrence with itself
                    if i != j:
                        x = stripe.get(token,None)
                        if x == None:
                            stripe[token] = 1
                        else:
                            stripe[token] += 1

                # Emit the term and the stripe
                print '%s\t%s' % (term, stripe)
# Increment total number of baskets
    total += 1           
stripe = {}
stripe['*total'] = total
print '%s\t%s' % ('*total', stripe)
