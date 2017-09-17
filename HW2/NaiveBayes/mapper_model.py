#!/usr/bin/env python
import sys, re, string

# Init mapper phase 
# define regex for punctuation removal
regex = re.compile('[%s]' % re.escape(string.punctuation))

# inner loop mapper phase: process each record
# input comes from STDIN (standard input)

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    # use subject and body 
    
    parts = line.split("\t")
    docID, docClass, title = parts[0:3]
    if len(parts) == 4:
        body = parts[3]
    else:
        body = ""
    
    # remove punctuations, only have white-space as delimiter
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    emailStr = regex.sub(' ', title.lower() + " " +body.lower()) #replace each punctuation with a space
    emailStr = re.sub( '\s+', ' ', emailStr )            # replace multiple spaces with a space
    # split the line into words
    words = emailStr.split()
    
# START STUDENT CODE HW241MAPPER_MODEL

# define regex for punctuation removal

# increase counters
# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
#
# tab-delimited; the trivial word count is 1
    
    for w in words: 
        print "%s\t%d\t%d\t%s"%(w,1,int(docClass),docID)# w, "\
                
# END STUDENT CODE HW241MAPPER_MODEL    