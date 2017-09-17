#!/usr/bin/python
## mapper.py


import sys

# Increment mapper counter
sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")

# Initialsys.stderr.write(ize variables
total = 0
basket_size = 0
largest_basket_size = 0

# Our input comes from STDIN (standard input)
for line in sys.stdin:
    # Split our line into products
    for product in line.replace('\n','').split():
        print '%s\t%s' % (product, 1)
        basket_size += 1
        total += 1
    if basket_size > largest_basket_size:
        largest_basket_size = basket_size
    
    basket_size = 0

# Print total words
print '%s\t%s' % ('*total', total)
print '%s\t%s' % ('*largest_basket', largest_basket_size)