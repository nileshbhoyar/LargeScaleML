#!/usr/bin/env python
from operator import itemgetter
import sys, operator, math
import numpy as np

numberOfRecords = 0
NumberOfMisclassifications=0
classificationAccurary = 0

# START STUDENT CODE HW231REDUCER_CLASSIFY

# input comes from STDIN
print "%s\t%s\t%s"%("PREDICTION","LABEL","DOCID")
for line in sys.stdin:
    # remove leading and trailing whitespace
    #line = line.strip()
    # split the line into words
    parts = line.split("\t")
    docID, preds, label = parts[0:3]
    print "%s\t%s\t%s"%( preds, label,docID)
    if int(preds) != int(label):
        NumberOfMisclassifications +=1
    numberOfRecords+=1
classificationAccurary = float(float(numberOfRecords-NumberOfMisclassifications) / float(numberOfRecords)) * float(100)
print 'Multinomial Naive Bayes Classifier Results are Total Records: %d,Mis-classes: %d,Accuracy: %2.5f' % (numberOfRecords, NumberOfMisclassifications, classificationAccurary) 
# END STUDENT CODE HW231REDUCER_CLASSIFY