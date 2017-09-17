import re
import sys
from collections import defaultdict

word = sys.argv[1]
pathToFile = sys.argv[2]
adict = defaultdict(int)
def hw111(word,pathToFile):
  # takes a word and the path to the file as arguments
  # returns the line containing the word and count
  
  # START STUDENT CODE HW111
      with open(pathToFile) as f:
     
          for line in f.readlines():
            line = line.strip()
            key, count = line.split('\t')
            adict[key.rstrip()] = count
      return adict[word]
  
  # END STUDENT CODE HW111
  
print hw111(word,pathToFile)