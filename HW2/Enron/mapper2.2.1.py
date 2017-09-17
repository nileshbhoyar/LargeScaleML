#!/usr/bin/env python
import sys, re, string

# START STUDENT CODE HW221MAPPER


# define regex for punctuation removal
#regex = re.compile('[%s]' % re.escape(string.punctuation))
# input comes from STDIN (standard input)

# use subject and body

# remove punctuations, only have white-space as delimiter

# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
#
# tab-delimited; the trivial word count is 1
for line in sys.stdin:
    docID, docClass,title,body = line.split("\t",3)   
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    emailStr = regex.sub(' ', title + " " +body.lower())
    emailStr = re.sub( '\s+', ' ', emailStr )
# split the line into words
    words = emailStr.split()
    for w in words: 
        
            print w, "\t", 1 #or yield(w, 1)
            
# END STUDENT CODE HW221MAPPER            