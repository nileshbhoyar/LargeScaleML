#!/bin/bash
## pWordCount.sh
## Author: James G. Shanahan
## Usage: pWordCount.sh m wordlist testFile.txt
## Input:
##       m = number of processes (maps), e.g., 4
##       word = a word in quotes, e.g., "alice"
##       inputFile = a text input file
##
## Instructions: Read this script and its comments closely.
##               Do your best to understand the purpose of each command,
##               and focus on how arguments are supplied to mapper.py/reducer.py,
##               as this will determine how the python scripts take input.

###----------------------------------------------------------------------------------------
#
# For HW1.3:
# modify this script to include shuffle/sort/merge phase, 
# which will collate wordCount records with the same key (i.e., same word)
# run: man sort to learn more about the linux sort command
#
###----------------------------------------------------------------------------------------


usage()
{
    echo ERROR: No arguments supplied
    echo
    echo To run use
    echo "pWordCount.sh m word inputFile"
    echo Input:
    echo "number of processes/maps, EG, 4"
    echo "word = a word in quotes, e.g., 'alice'"
    echo "inputFile = a text input file"
}

if [ $# -eq 0 ]
  then
    usage  
    exit 1
fi
    
## collect user input
m=$1 ## the number of parallel processes (maps) to run

word=$2 ## if set to "*", then all words are used

## a text file 
data=$3

## 'wc' determines the number of lines in the data
## 'perl -pe' regex strips the piped wc output to a number
linesindata=`wc -l $data | perl -pe 's/^.*?(\d+).*?$/$1/'`

## determine the lines per chunk for the desired number of processes
linesinchunk=`echo "$linesindata/$m+1" | bc`

## split the original file into chunks by line
split -l $linesinchunk $data $data.chunk.

## assign python mappers (mapper.py) to the chunks of data
## and emit their output to temporary files
for datachunk in $data.chunk.*; do
    ## feed word list to the python mapper here and redirect STDOUT to a temporary file on disk
    ####
    ####
    ./mapper.py  "$word" < $datachunk > $datachunk.counts &
    ####
    ####
done
## wait for the mappers to finish their work
wait
    

    
## 'ls' makes a list of the temporary count files
## 'perl -pe' regex replaces line breaks with spaces
countfiles=`\ls $data.chunk.*.counts | perl -pe 's/\n/ /'`
## feed the list of countfiles to the python reducer and redirect STDOUT to disk
####
####
cat $countfiles |sort -k1,1| ./reducer.py  > $data.output
####
####

## clean up the data chunks and temporary count files
rm $data.chunk.*
    
## display the content of the output file:
cat $data.output