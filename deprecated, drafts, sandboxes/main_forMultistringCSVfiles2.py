# Subcreated first on Wednesday, June 7, 2017

# @author: Colin F. Wilder

# Intellectual Property statement: This code is based on lots of other freely available code on the internet, but the synthesis is mine. This relates to my broader metaphysics of creation and subcreation. I have gained a lot from Stack Overflow. The basic ngrams stuff I think is my own,but may also come from lessons from the Programming Historian by Adam Crymble and William Turkel. Parts of them were inspired by code written by Duncan Buell in his CSCE 500; Programming for Humanists course at the University of South Carolina in Autumn 2013. This module is therefore released under a CC-BY license i.e. Creative Commons Attribution 2.0 Generic license, which is explained at https://creativecommons.org/licenses/by/2.0/.#

# what this file does (in brief): perform text analysis separately on multiple strings in a CSV file

# what this file does (in full):
# read each line in a file
# turn each line into a normalized, simplified etc. list of words
# make k-skip n-grams ("skip grams") from that list of words
# make frequency dictionary from those ngram lists
# produce node and edge lists from that frequency dictionary for use in Gephi

# other notes: this is a main file so it is what you execute. it depends on several utilities files. 

# gibs
from utilities_bigrams import *
from utilities_prepForGephi import *
from utilities_logging import *

# declare global variables
fileName="Hanau_copy3_PREPPED.csv"
desiredWordDistance=1 # 1 means that ngrams are contructed only of adjacent words 
allNgrams=[] # this is where all the ngrams from all lines of the file will be stored together
allTokens=[]
ngramsDict={} # the frequency dictionary for the ngrams
tokenDict={} # the frequency dictionary for the tokens
output="" # this is what we will send to the output file at the end

########################################## to do: wrap more or less everything below here in a fo loop, going through all files in a folder...
########################################## to do: with each loop through the for, re-empty most of the global variables











# open, read, and process the file with the multiple string lines
with open(fileName,'r+') as f:
    lines = f.readlines()
    for i in range(0,len(lines)):
        line=lines[i].lower()
        #print len(line)
        if len(line)==1: # something weird but I think it is counting the carriage return as a character
            print("processing empty line")
            continue
        elif len(line)<=100:
            print("processing line: " + line[0:-1]) # -1 because carriage return again? 
        else:
            print("processing line: " + line[0:100])
        # here we insert a flow of control statement to address cases of varying number of tokens
        lineSplit=lines[i].lower().split()
        # case 1: nothing there: continue.
        if len(lineSplit) == 0:
            print("empty line")
            continue
        # case 2: # tokens < desiredWordDistance: count tokens but do not make ngrams
        elif len(lineSplit) < desiredWordDistance:
            for token in lineSplit:
                allTokens.append(token)
                tokenDict=countTokens(token, tokenDict) # count each token into the token dictionary
        # case 3: # tokens >= desiredWordDistance: count tokens and make ngrams
        else:
            allNgrams.extend(makeSpreadBigrams(line,desiredWordDistance)) # makes ngrams; add to allNgrams list
            for token in lineSplit:
                allTokens.append(token)
                tokenDict=countTokens(token, tokenDict) # count each token into the token dictionary

# put all ngrams into the ngram frequency dictionary
for ngram in allNgrams:
    ngramsDict=countNgram(ngram, ngramsDict)

# console and output: tokens
output += "\n\nTokens:"
output += "\n" + "number of tokens:\t" + str(len(allTokens))
output += "\n"+ str(allTokens)
# print summary to console
print("number of tokens:\t"+str(len(allTokens)))

# console and output: ngrams
output += "\n\nNgrams:"
output += "\n" + "number of ngrams:\t" + str(len(allNgrams))
for ngram in allNgrams:
    output += "\n"+ str(ngram)
# print summary to console
print("number of ngrams:\t"+str(len(allNgrams)))
    
# console and output: token dictionary
output += "\n\nToken frequency dictionary:"
output += "\n"+ str(tokenDict)

# console and output: ngrams dictionary
output += "\n\nNgram frequency dictionary:"
output += "\n"+ str(ngramsDict)

# make the CSV files for graphing in Gephi
########################################## to do: these have to be put in the special output folder too
makeEdgeListForGephi(ngramsDict)
makeNodeListForGephi(tokenDict)

# send output to log file
########################################## to do: this will have to be changed to create and write to a custom-named output data or log file
# cannot use old output logging system since each time it is called, it iterates to a new index
sendToOutput(output)

