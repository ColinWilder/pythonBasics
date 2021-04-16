# Subcreated in period 2013 to 2017. 
# @author: Colin F. Wilder
# IP statement: This code is based on lots of other freely available code on the internet, especially lessons from the Programming Historian by Adam Crymble and William Turkel. The utilities to make bigrams are, I believe, fairly original to me, though not rocket science anyway.  Parts of them were inspired by code written by Duncan Buell in his CSCE 500; Programming for Humanists course at the University of South Carolina in Autumn 2013. This module is therefore released under a CC-BY license i.e. Creative Commons Attribution 2.0 Generic license, which is explained at https://creativecommons.org/licenses/by/2.0/.#

def makeBigrams(textString, wordDistance):
	# arguments: the string and the number of words in the n-grams 
	# takes string and returns list of bigrams in it
	outputBigramsList=[] # the final result
	list=textString.split() # turn string into list
	for i in range(0,len(list)-1):
		outerLimit=min(len(list),i+wordDistance+2)
		for j in range(i+1,outerLimit):
			# print(list[i]+" "+list[j])
			outputBigramsList.append((list[i], list[j])) # add a bigram to outputBigramsList
	return outputBigramsList

def countNgram(ngram, ngramDictionary):
# takes a list of bigrams as argument
# returns a dictionary with bigrams as keys, their frequencies as values
    pairTuple=ngram[0], ngram[1]
    if pairTuple in ngramDictionary.keys():
        ngramDictionary[pairTuple]=ngramDictionary[pairTuple]+1
    else:
        ngramDictionary[pairTuple]=1
    return ngramDictionary

def countTokens(token, tokenDictionary): # takes as arguments a token and a token dictionary
# use this while making ngrams, in the middle of the process, to also make a frequency dictionary of the tokens themselves
    if token in tokenDictionary.keys():
        tokenDictionary[token]=tokenDictionary[token]+1
    else:
        tokenDictionary[token]=1
    return tokenDictionary # a dictionary


def mostFrequentBigrams(bigramsFreqsDict, numberToShow):
# Takes bigram frequency dictionary. Returns sorted list of most frequent bigrams
# First loop over the dictionary to find the highest value (frequency). 
    highestFreqValue=0    
    for key in bigramsFreqsDict:
        if bigramsFreqsDict[key]>highestFreqValue:
            highestFreqValue=bigramsFreqsDict[key]
# Then loop through and for each key whose value is that high value, print key and value. Then go down one unit to next lowest value and print all those keys and values. Do this until you reach the number of frequencies requested to be shown. 
    counter=0
    for i in range(highestFreqValue,0,-1):
        for key in bigramsFreqsDict:
            if bigramsFreqsDict[key]==i:
                print(key,":",bigramsFreqsDict[key],"occurence(s)")
                counter +=1
            if counter==numberToShow: 
                break
        if counter==numberToShow: 
                break
