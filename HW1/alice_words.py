import re
import sys
from collections import defaultdict

pathToFile = sys.argv[1]
wordCounts = defaultdict(int)


def hw11(pathToFile):
  # takes the path to the file as command line argument
  # prints sorted tab separated list of words and counts
  # ex) print word,'\t',count
  # returns sorted list of tuples of words and counts: wordList
  # ex) wordList = [('a', 690),('abide', 2),...]
  
  wordList = []

  # START STUDENT CODE HW11
  file=open(pathToFile,"r+")


  template = "{0:17}{1:3}"
  for word in re.findall(r'[a-z]+', file.read().lower()):
    wordCounts[word] += 1
  for key in sorted(wordCounts):
        #print template.format(key, wordCounts[key])
        print key ,'\t' ,wordCounts[key]

  # END STUDENT CODE HW11
  
  #print wordList

hw11(pathToFile)