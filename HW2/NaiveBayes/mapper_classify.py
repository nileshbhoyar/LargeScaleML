#!/usr/bin/env python
from NaiveBayesModel import NaiveBayesModel
import sys, re, string, subprocess
import sys, operator, math 
import numpy as np
from math import log
from math import exp
# Init mapper phase 

# read the MODEL into memory
# The model file resides the local disk (make sure to ship it home from HDFS).
# In the Hadoop command linke be sure to add the follow the -files commmand line option
NBModel = NaiveBayesModel("NaiveBayes/SPAM_Model_MNB.tsv") 
worddict = NBModel.model
#NBModel.printModel()
# define regex for punctuation removal
regex = re.compile('[%s]' % re.escape(string.punctuation))

# inner loop mapper phase: process each record
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    parts = line.split("\t")
    docID, docClass, title = parts[0:3]
    if len(parts) == 4:
        body = parts[3]
    else:
        body = ""
    # use subject and body 
    # remove punctuations, only have white-space as delimiter
    emailStr = regex.sub(' ', title.lower() + " " +body.lower()) #replace each punctuation with a space
    emailStr = re.sub( '\s+', ' ', emailStr )            # replace multiple spaces with a space
    # split the line into words
    words = emailStr.split()
    nwords = []
    for i in words:
        if i in worddict:
            nwords.append(i)
# START STUDENT CODE HW251MAPPER_CLASSIFY
      


    #PrClass0GivenDoc, PrClass1GivenDoc = NBModel.classify(words)

    #print "Pr(Class=0| Doc=%s) is %6.5f" % (docID, PrClass0GivenDoc)
    #print "Pr(Class=1| Doc=%s) is %6.5f" % (docID, PrClass1GivenDoc)

    PrClass0GivenDoc, PrClass1GivenDoc = NBModel.classifyInLogs(nwords)
    if PrClass0GivenDoc > PrClass1GivenDoc:
        print "%s\t%s\t%s"%(docID,0,docClass)
    else:
        print "%s\t%s\t%s"%(docID,1,docClass)
    #print "Pr(Class=0| Doc=D5) = %6.5f, log(Pr(Class=0| Doc=D5)) = %f" % (exp(PrClass0GivenDoc), PrClass0GivenDoc)
    #print "Pr(Class=1| Doc=D5) = %6.5f, log(Pr(Class=1| Doc=D5)) = %f" % (exp(PrClass1GivenDoc), PrClass1GivenDoc) 
    
# END STUDENT CODE HW251MAPPER_CLASSIFY
