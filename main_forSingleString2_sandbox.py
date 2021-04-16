import utilities_preprocessing, utilities_bigrams, urllib, re, sys, time, os, csv # used to be urllib2 instead...
from collections import defaultdict

textString="beginning god created heaven earth earth form void darkness face deep spirit god moved face waters god said let light light god saw light good god divided light darkness god called light day darkness called night evening morning day god said let firmament midst waters let divide waters waters god firmament divided waters firmament waters firmament god called firmament heaven evening morning second day god said let waters heaven gathered unto place let dry land appear god called dry land earth gathering waters called seas god saw good god said let earth bring forth grass herb yielding seed fruit tree yielding fruit kind seed itself earth earth brought forth grass herb yielding seed kind tree yielding fruit seed itself kind god saw good evening morning day god said let lights firmament heaven divide day night let signs seasons days years let lights firmament heaven light earth god great lights greater light rule day lesser light rule night stars god set firmament heaven light earth rule day night divide light darkness god saw good evening morning fourth day god said let waters bring forth abundantly moving creature hath life fowl fly earth open firmament heaven god created great whales living creature moveth waters brought forth abundantly kind winged fowl kind god saw good god blessed saying fruitful multiply waters seas let fowl multiply earth evening morning fifth day god said let earth bring forth living creature kind cattle creeping thing beast earth kind god beast earth kind cattle kind thing creepeth earth kind god saw good god said let make man image likeness let dominion fish sea fowl air cattle earth creeping thing creepeth earth god created man image image god created male female created god blessed god said unto fruitful multiply replenish earth subdue dominion fish sea fowl air living thing moveth earth god said behold given herb bearing seed face earth tree fruit tree yielding seed shall meat beast earth fowl air thing creepeth earth life given green herb meat god saw thing behold good evening morning sixth day" 

# TO DO: textString is a shortcut. It needs to be replaced with the full set of steps to start with any text passage and reduce that to lowered, remove stop words, etc.


#####################################################################
############ tokens and bigrams #####################################
#####################################################################

# make token frequency dictionary
textStringSplit=textString.lower().split()
tokens=[] # will be list of all tokens incl duplicates
tokenFreqDict={} # will be a frequency dictionary/frequency distro for all token # hence the keys in the dictionary should actually be the types since there can be no duplicate keys
for token in textStringSplit:
	tokens.append(token)
	tokenFreqDict=utilities_bigrams.countTokens(token, tokenFreqDict)
# result: tokens is now a list of all tokens
# result: tokenFreqDict is a frequency dict of all tokens/types

# make list of all bigrams 
bigramsList=utilities_bigrams.makeBigrams(textString, 2)
#print(bigramsList) # successfully produces huge list of all bigrams

# put all bigrams into a frequency dictionary
bigramFreqDict = {}
for bigram in bigramsList:
    bigramFreqDict = utilities_bigrams.countNgram(bigram, bigramFreqDict)
#print(bigramFreqDict)


#####################################################################
############ send stuff to console, output data to files ############
#####################################################################

# console and output: tokens
tokens=sorted(tokens) # sort the big list of tokens
print("number of tokens:\t" + str(len(tokens))) # report number of tokens
# print(allTokensInFile)
print("number of types:\t" + str(len(tokenFreqDict.keys()))) # report number of types
# print(list(tokenDictForFile.keys()))

# console and output: ngrams
bigramsList=sorted(bigramsList)
print("number of bigram tokens (i.e. all including duplicates):\t" + str(len(bigramsList)))
print("number of bigram types (i.e. unique bigrams):\t" + str(len(bigramFreqDict.keys())))
# print(list(ngramsDictForFile.keys()))


#####################################################################
############ write edge list to csv #################################
#####################################################################

"""Using the frequency distribution, make a list of triples (i.e. list of 3-item lists)"""
outputList=[]
outputList.append(["Source","Target","Weight"]) # this adds first triple
for key in bigramFreqDict:
    sublist=[key[0],key[1],bigramFreqDict[key]]
    outputList.append(sublist) # adds a subsequent triple
#print(outputList)


"""Write the new output list into the new file and close it"""
csvEdgeFileObject=open("text_networks_output_edges2.csv", 'w') # note it's a w flag not a wb flag
w=csv.writer(csvEdgeFileObject)
# alt # path=os.path.join(os.getcwd(),"edges-CSV.csv") # and tell the writer to open path
w.writerows(outputList)


# TO DO: as is, the code creates extra lines between node-node-edge weights in the csv; don't know why yet (3/31/21)

