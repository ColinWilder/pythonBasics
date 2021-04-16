# Latin Phrase Processor (LPP) version 5
# October 3, 2017

# Notes:
# Formerly called CTP (Catalog Title Processor). For story, see earlier versions. 
# Version 6: Adding log output function. Changing csv output column headings. Ugh. 

############ gibs ######################################################

import os, csv
import pandas as pd
import shutil
from cltk.lemmatize.latin.backoff import DefaultLemmatizer
from cltk.lemmatize.latin.backoff import TrainLemmatizer
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tokenize.word import WordTokenizer
from cltk.utils.file_operations import open_pickle
from glob import glob
from utilities_output_files import *
from utilities_preprocessing import *

############ global variables and universal machines: general ##########

customDictionary={} # a dictionary into which we will read the custom dictionary csv file for use during execution
customDictionaryCurrentLength=0 # we're going to walk through the customDictionary once but will later need to go to the last line so let's keep track of the length!
cwd=os.getcwd()
default = DefaultLemmatizer('UNK') # make default lemmatizer
failsList=[] # here will be recorded tokens which the two dictionaries have failed to recognize for that line
failsListForWholeExecution=[] # like failsList but will contain all fails in whole execution session, for use in console output
jv=JVReplacer()
lemmatizedTextList=[] # holds the versions of the title as we lemmatize them
lemmatizer = LemmaReplacer('latin')
lengthOfDataFile=0 # number of rows in data file
numberOfFails=0
numberOfSuccesses=0
outputForWholeExecution="" # this string will hold all output for all files processed in a given execution of the module, for one-stop shopping
outputRowsForWholeExecution=[]
preprocessedTitle="" # a temp string where we store the ongoing preprocessing work on a title
successfulHits=[]
word_tokenizer = WordTokenizer('latin')

# make a hole in the output
print()

# build standard dictionary/model # courtesy of Patrick Burns
print("building standard dictionary")
rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
path = os.path.expanduser(rel_path)
file = 'latin_lemmata_cltk.pickle'
old_model_path = os.path.join(path, file)
LATIN_OLD_MODEL = open_pickle(old_model_path)

# make standard lemmatizer # as an instance of TrainLemmatizer # courtesy of Patrick Burns
lemmatizer = TrainLemmatizer(model=LATIN_OLD_MODEL, backoff=default)

# import custom dictionary csv as python dictionary
print("building custom dictionary")
customDictionaryPath=os.path.join(cwd,'customDictionary.csv')
with open(customDictionaryPath,'r') as f: # this should close the file after the end of the with loop
	reader=csv.DictReader(f)
	for row in reader:
		customDictionaryCurrentLength+=1
		if row['lemma']=="":
			continue # in case a token has been added to custom dictionary but no lemma has yet been provided it
		customDictionary[row['token']]=row['lemma']

# make custom lemmatizer
lemmatizer2 = TrainLemmatizer(model=customDictionary, backoff=lemmatizer)

############ global variables: folders and data ########################

cwd=os.getcwd()
operationsDirectoryName="latinPhraseProcessor_operations"

# make output base path
basePath=os.path.join(cwd,operationsDirectoryName)
print("basePath: \t\t" + basePath)

# make index path
indexPath= basePath +'/index.txt'
print("indexPath: \t\t" + indexPath)

# find the index of the most recent output
currentIndex=findCurrentOutputIndex(indexPath)
print("currentIndex: \t\t" + str(currentIndex))

# make data folder path
dataFolder=os.path.join(basePath,"data") # this is where data file(s) must be put to be found!
print("data folder: \t\t" + dataFolder)

# make new output folder based on index
newOutputFolderName="output"+str(currentIndex)
outputFolderPath=basePath+'/'+newOutputFolderName
if not os.path.exists(outputFolderPath):
	os.makedirs(outputFolderPath)
print("new output folder: \t" + outputFolderPath)

# open csv file for writing data that results from processing all data in the whole execution
outputFileWholeExecutionPath=outputFolderPath+'/' + 'LPP_results_concatenated.csv'
outputFileWholeExecutionObject = open(outputFileWholeExecutionPath,"w") # open csv writer object for writing # in Python 2 it might be w instead of wb
wwe=csv.writer(outputFileWholeExecutionObject)

############ read data #################################################

# look in data folder
g=glob(dataFolder + "/*")

# open and process file(s) inside the data folder
for fileName in g:
	print("found in data folder: \t"+str(fileName))
	# make local variables for this file - we will print/output them when finished processing file
	outputHeader="" # the metadata that goes at the top of the output log file
	output="" # for each file processed, we will send all data to this output text and file, for easy perusal
	# open csv file for writing data that results from processing this file
	dataFileName=os.path.split(fileName)[1]
	outputFilePath=outputFolderPath+'/' + dataFileName[0:-4] + '_LPP_results.csv' # the 0:-4 index is to get rid of the .csv extension
	outputFileObject = open(outputFilePath,"w") # open csv writer object for writing # in Python 2 it might be w instead of wb
	w=csv.writer(outputFileObject)
	# open and read the file
	with open(fileName,'r+') as f: # this loop is for the whole data file
		lines = f.readlines()
		for i in range(0,len(lines)): # this for statement looks at one line at a time
			preprocessedTitle=lines[i]
	
			############ preprocess the line ###########################
			
			preprocessedTitle=removePunctuation(preprocessedTitle) # remove punctuation
			preprocessedTitle=removeNumbers(preprocessedTitle) # remove numbers
			preprocessedTitle=preprocessedTitle.lower() # change preprocessedTitle to lower case
			preprocessedTitle=removeStopWords(preprocessedTitle) # remove English, German, and French stop words before U-V I-J swaps
			preprocessedTitle=removeStopWordsFromSpecialList(preprocessedTitle, stopWordList=germanStopList)
			preprocessedTitle=removeStopWordsFromSpecialList(preprocessedTitle, stopWordList=frenchStopList)
			preprocessedTitle=removeStopWordsFromSpecialList(preprocessedTitle, stopWordList=latinStopList) # remove Latin stopwords (first time)
			preprocessedTitle=jv.replace(preprocessedTitle) # change js and vs
			preprocessedTitle=removeStopWordsFromSpecialList(preprocessedTitle, stopWordList=latinStopList) # remove Latin stopwords (second time - in case anything has change after U-V I-J subs)
			preprocessedTitle=removeExtraWhiteSpace(preprocessedTitle) # remove extra white space because material forces determine that whiteness will disappear
			
			############ tokenization and lemmatization ################

			# tokenize text # this gets rid of enclitics
			text_tokenized=word_tokenizer.tokenize(preprocessedTitle) # tokenization produces a list, which is what the lemmatizers need
			
			# repeat some of the low-level preprocessing
			swingList=[]
			for token in text_tokenized:
				token=token.strip()
				token=token.strip('-') # I think that tokenization produces "-ne" and "-que" from enclitic suffixes so these must be removed. 
				token=removePunctuation(token) # removePunctuation again because tokenizer leaves dashes on enclitics
				token=removeStopWordsFromSpecialList(token, stopWordList=latinStopList) # removeStopWordsFromSpecialList again to remove new arrivals like que or ne produced from separating enclitics
				if token in latinStopList:
					continue
				token=removeSingletons(token) # removeSingletons again
				if not token =="" and not token in swingList:
					swingList.append(token)
			text_tokenized=swingList

			# lemmatization
			finishedText = lemmatizer2.lemmatize(text_tokenized)
			
			# remove stop words yet again in case lemmatization has produced some stop words that we didn't catch before
			swingList=[] # since we used swingList already it is probably not empty, so empty it now
			for tup in finishedText:
				if tup[1] not in latinStopList and tup[1] not in germanStopList:
					swingList.append(tup)
			finishedText=swingList
			
			# write successes and fails to session lists successfulHits, failsList
			for j in range(0,len(finishedText)):
				if finishedText[j][1]=='UNK' and finishedText[j][0] not in latinStopList:
					# we check the fails against the stop words again just to catch the damned things like que 
					failsList.append(finishedText[j][0]) # records the fails of just this row in just this file
					failsListForWholeExecution.append(finishedText[j][0]) # record all fails in whole execution
				else:
					successfulHits.append(finishedText[j]) # record all successes in whole execution session
			
			# fashion a simple string version of finishedText and write it to column 4
			bestCurrentLemmatizedForm="" # a temp string for storing the best current form containing lemmas where possible and failing that the original tokens
			for tuple in finishedText:
				if tuple[1]=='UNK':
					bestCurrentLemmatizedForm+=tuple[0]+" "
				else:
					bestCurrentLemmatizedForm+=tuple[1]+" "
			bestCurrentLemmatizedForm=bestCurrentLemmatizedForm.strip().lower() # because the final for loop adds a space at the end of the string
			
			# output original title and best current lem form to csv file
			outputRow=[lines[i].strip(), len(lines[i].strip().split()), bestCurrentLemmatizedForm, len(bestCurrentLemmatizedForm.split())]
			w.writerow(outputRow) # write that to the csv writer object
			outputRowsForWholeExecution.append(outputRow) # collect all output for execution to later put into one big csv

			# count successes and fails
			for item in finishedText:
				if item[1]=='UNK' and item[0] not in latinStopList:
					print("\tfail:\t"+item[0]) # this reports things like que even though they don't make it into the final fails list for the session!
					numberOfFails+=1
				else:
					numberOfSuccesses+=1

			# here ends the for loop that is looking at each line

		# here ends the while loop that is looking at a given file in the data folder

	# After all data files have been processed, the big for loop stops

# now we are done with all processing of data files # time to wrap up

############ final housekeeping ########################################

# write all data from whole execution to csv
wwe.writerows(outputRowsForWholeExecution)

# to do: make new version of custom dictionary including failures and send to csv file # since we are not using pandas anymore, we probably have to do this via the csv module and zip
failsListForWholeExecution=sorted(list(set(failsListForWholeExecution))) # deduplicate the failsListForWholeExecution list

# tally results for whole execution to console
o="number of successes:\t"+str(numberOfSuccesses)
print(o)
outputForWholeExecution += o + "\n"
o="number of fails:\t"+str(numberOfFails)
print(o)
outputForWholeExecution += o + "\n"

# print failures to console
print("\nfailsListForWholeExecution:\t"+str(failsListForWholeExecution))

# send successfulHits list to output as own file
shfo=open(os.path.join(outputFolderPath,'successfulHits.csv'), 'w') # shfo means successful hits file object
wr=csv.writer(shfo)
successfulHits=sorted(list(set(successfulHits))) # deduplicate the successfulHits list to make it smaller and easier to read
wr.writerows(successfulHits)

# write output for whole execution to file
logFilePath=outputFolderPath+'/' + 'latinPhraseProcessor_output_wholeRun.txt'
logFileObject = open(logFilePath,"w")
logFileObject.write(outputForWholeExecution)
logFileObject.close

# increment index for next time and write it to the index file for next time
currentIndex+=1
f = open(indexPath, "w")
f.write(str(currentIndex)) # print to output
f.close

# add a space for the sake of clarity of output to screen
print()

