#!/usr/bin/python
## mapper.py


import sys

# Increment mapper counter
sys.stderr.write("reporter:counter:Mapper Counters,Calls,1\n")

# Initialsys.stderr.write(ize variables
total = 0
basket_size = 0
largest_basket_size = 0

for line in sys.stdin:
    total = 0
    basket_size = 0
    # Split our line into products
    for product in line.replace('\n','').split():
        print '%s\t%s' % (product, 1)
        #print generateLongCountToken(product)
        basket_size += 1
        total += 1

        
    
    print '%s\t%s' % ('*largest_basket', total)
    #basket_size = 0


    