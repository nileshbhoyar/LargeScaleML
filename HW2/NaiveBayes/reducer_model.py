#!/usr/bin/env python
from operator import itemgetter
import sys, operator
import numpy as np
from  collections import OrderedDict 

# START STUDENT CODE HW241REDUCER_MODEL

current_word = None
smooth_factor = 1 # add 1 smoothing
current_count = [smooth_factor, smooth_factor]
msgIDs = {}
word = None
wordcount = {}

# input comes from STDIN
# remove leading and trailing whitespace

# parse the input we got from mapper.py

# convert count and spam flag (currently a string) to int


# handle msgID - store all IDs as we don't have too much
# not the best way to get prior, a two-level MapReduce jobs (ID - word) would be optimal
    
# calculate NB parameters, and write the dictionary to a file for the classification job
# prior probabilities

# conditional probability
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count, isSpam, msgID = line.split('\t', 3)
   
   
    # convert count and spam flag (currently a string) to int
    try:
        count = int(count)
        isSpam = int(isSpam)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    
    # handle msgID - store all IDs as we don't have too much
    # not the best way to get prior, a two-level MapReduce jobs (ID - word) would be optimal
    if msgID not in msgIDs:
        msgIDs[msgID] = isSpam

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:        
        current_count[isSpam] += count
    else:
        if current_word:
            # count finish for one word, save it
            wordcount[current_word] = current_count
        # initialize new count for new word
        current_count = [smooth_factor, smooth_factor]
        current_count[isSpam] += count                
        current_word = word

# do not forget to save the last word count if needed!
if current_word == word:    
    wordcount[current_word] = current_count
    
# calculate NB parameters, and write the dictionary to a file for the classification job
# prior probabilities
n_msg = len(msgIDs)
n_spam = sum(msgIDs.values())
n_ham = n_msg - n_spam
print '%s\t%s,%s,%s,%s' %('ClassPriors',n_ham,n_spam ,1.0*n_ham/n_msg, 1.0*n_spam/n_msg)

# conditional probability
n_total = np.sum(wordcount.values(), 0)


wordcount =OrderedDict(sorted(wordcount.items(), key=lambda t: t[0]))
for (key,value) in zip(wordcount.keys(), wordcount.values()/(1.0*n_total)):
    if sum(wordcount[key]) > 3:
        print '%s\t%s,%s,%s,%s' %(key,wordcount[key][0] ,wordcount[key][1],value[0], value[1])