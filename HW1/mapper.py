#!/usr/bin/python
import sys
import re
from collections import defaultdict
 #for each document create dictionary of words
word_cnts = defaultdict(int)
# START STUDENT CODE HW13MAPPER
for line in sys.stdin:
     
  
    #Upper case letters
    for word in re.findall(r'\b[A-Z][a-z]*\b',line):
       
        word_cnts['upper'] += 1
    #lower case letters
    for word in re.findall(r'\b[a-z][a-z]*\b',line):
       
        word_cnts['lower'] += 1    
    # emit key-value pairs only for distinct words per document 
for w in word_cnts.keys():
    
        print '%s\t%s' % (w,word_cnts[w])
# END STUDENT CODE HW13MAPPER