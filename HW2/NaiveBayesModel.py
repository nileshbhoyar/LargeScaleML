#!/usr/bin/env python
from math import log
from math import exp

class NaiveBayesModel(object):

    def __init__(self, modelFile):
        self.model = {}
        recordStrs = [s.split('\n')[0].split('\t') for s in open(modelFile).readlines()]
        for word, statsStr in recordStrs:
            self.model[word] = map(float, statsStr.split(","))
        #Class priors: counts and probs (Pr(Class =0) and Pr(Class =1))
        self.c0, self.c1, self.prClass0, self.prClass1 = map(float, self.model["ClassPriors"])

        

    def classify(self, doc):
        # Posterior Probabilities Pr(Class=0| Doc) and Pr(Class=1| Doc) 
        # Naive Bayes inference Pr(Class=0| Doc)  ~ Pr(Class=0) * Pr(Class=0| word1) * Pr(Class=0| word2)...... 
        PrClass0GivenDoc = self.prClass0  
        PrClass1GivenDoc = self.prClass1
        for word in doc:
            PrClass0GivenDoc *= self.model[word][2]
            PrClass1GivenDoc *= self.model[word][3]
        return([PrClass0GivenDoc, PrClass1GivenDoc])
 
    # the natural log based version of this 
    # helps avoid underflow issues
    def classifyInLogs(self, doc):       
        # Posterior Probabilities Pr(Class=0| Doc) and Pr(Class=1| Doc) 
        # Naive Bayes inference Pr(Class=0| Doc)  ~ Pr(Class=0) * Pr(Class=0| word1) * Pr(Class=0| word2)...... 
        PrClass0GivenDoc = log(self.prClass0)  
        PrClass1GivenDoc = log(self.prClass1)
        for word in doc:  #NOTE: Improvement: on loading one should convert probs to log probs!
            c0 = self.model[word][2]
            c1 = self.model[word][3]
            if c0 != 0:
                PrClass0GivenDoc += log(c0)
            else:
                PrClass0GivenDoc = float("-inf")
            if c1 != 0:
                PrClass1GivenDoc += log(c1)
            else:
                PrClass1GivenDoc = float("-inf")
                
        return([PrClass0GivenDoc, PrClass1GivenDoc])

        
    def printModel(self):
        print "NaiveBayes Model starts here\n----------------"
        print "PRIORS: prClass0=%04.3f, prClass1=%04.3f" % (self.prClass0, self.prClass1)
        for word, stats in self.model.items():
            print "Pr(",word, "| Class)", stats  #Pr(Class=0| Doc)  all stats
        print "NaiveBayes Model ENDS here\n----------------"
 