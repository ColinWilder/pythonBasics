# Latin Phrase Processor (LPP) version 5
# October 3, 2017

# Notes:
# Formerly called CTP (Catalog Title Processor), named for its first application - the processing of titles in historic library catalogs. Also previously the file was just called LPP, short forLatin Phrase Processor. But I have come to mislike the brevity of Unix style, prefer instead the loquacity that Python has encouraged. So I write the full name. 
# This is version 5. The versions are just convenient stopping points in development, each representing a more or less stable, functioning code base. Version 5 is as I think mostly finished for the current vision of program functionality. With version 5, I changed the module name from LPP to Latin Phrase Processor. 

# Outstanding changes still planned:
# The LPP4 output csv files contain too much information. You don't need several of the columns. Just have them include the original title and the bestCurrentLemmatizedForm.

# gibs
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

# global variables
customDictionary={} # a dictionary into which we will read the custom dictionary csv file for use during execution
customDictionaryCurrentLength=0 # we're going to walk through the customDictionary once but will later need to go to the last line so let's keep track of the length!
cwd=os.getcwd()
default = DefaultLemmatizer('UNK') # make default lemmatizer
failsList=[] # here will be recorded tokens which the two dictionaries have failed to recognize for that line
failsListSession=[] # like failsList but will contain all fails in whole execution session, for use in console output
jv=JVReplacer()
lemmatizedTextList=[] # holds the versions of the title as we lemmatize them
lemmatizer = LemmaReplacer('latin')
lengthOfDataFile=0 # number of rows in data file
numberOfFails=0
numberOfSuccesses=0
preprocessedTitle="" # a temp string where we store the ongoing preprocessing work on a title
successfulHits=[]
word_tokenizer = WordTokenizer('latin')

# build standard dictionary/model # courtesy of Patrick Burns
rel_path = os.path.join('~/cltk_data/latin/model/latin_models_cltk/lemmata/backoff')
path = os.path.expanduser(rel_path)
file = 'latin_lemmata_cltk.pickle'
old_model_path = os.path.join(path, file)
LATIN_OLD_MODEL = open_pickle(old_model_path)

# make standard lemmatizer # as an instance of TrainLemmatizer # courtesy of Patrick Burns
lemmatizer = TrainLemmatizer(model=LATIN_OLD_MODEL, backoff=default)

# import custom dictionary csv as python dictionary
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

# make a hole in the output
print()

# find the current data file index and increment it
# make new output base path
bp=newOutputBasePath()
print("basePath: \t\t" + bp)
ci=currentIndex()

#construct new output folder based on index
newOutputFolder=makeNewOutputFolder(ci,bp)
print("new output folder: \t" + newOutputFolder)

# construct data folder path
dataFolder=os.path.join(bp,"data") # make data folder path; this is where data file(s) are to live
print("data folder: \t\t" + dataFolder)

# look in data folder
g=glob(dataFolder + "/*")

# open and process file(s) inside the data folder
for f in g:
	# for a given data file in the folder, do...
	print("found in data folder: \t"+str(f))
	currentDF=pd.read_csv(f, na_values=['nan'], keep_default_na=False) # read file into a pandas data frame # the nan thing is an annoying CLTK data thingy # don't worry # just keep this as is
	lengthOfDataFile = len(currentDF['fails'])
	nextDF=currentDF # make copy of the data frame; we will write changes to nextDF then write nextDF to a new file
	
	# for each row in the file you're looking at, do...
	for i in range(0,lengthOfDataFile):
		##############################
		# preprocess any titles that have not yet been preprocessed
		preprocessedTitle=currentDF['preprocessed title'][i]
		# if any cell is blank, then preprocess the corresponding cell in the first column # the purpose of this is in case (1) this is the first run of a new data set or (2) new data has been added.
		# if the preprocessed title cell is *not blank*, do *not* break for loop, because cells have to be re-lemmatized anew with every run of program in case customDictionary has been improved
		if currentDF['preprocessed title'][i] == "":
			# assume that user will not manually edit preprocessed titles
			preprocessedTitle=currentDF["original title"][i]
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
			nextDF['preprocessed title'][i]=preprocessedTitle # write the temporary string to column 2

		##############################
		# tokenization and lemmatization

		# tokenize text # this gets rid of enclitics
		text_tokenized=word_tokenizer.tokenize(preprocessedTitle) # tokenization produces a list, which is what the lemmatizers need
		
		# do the following preprocessing again
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
				failsListSession.append(finishedText[j][0]) # record all fails in whole execution session
			else:
				successfulHits.append(finishedText[j]) # record all successes in whole execution session
		
		# write finishedText to the column 3, so that we retain all the success and failure information for a possible next run of the system after perhaps improving the custom dictionary. 
		nextDF['lemmatized text list'][i]=finishedText
		
		# fashion a simple string version of finishedText and write it to column 4
		bestCurrentLemmatizedForm="" # a temp string for storing the best current form containing lemmas where possible and failing that the original tokens
		for tuple in finishedText:
			if tuple[1]=='UNK':
				bestCurrentLemmatizedForm+=tuple[0]+" "
			else:
				bestCurrentLemmatizedForm+=tuple[1]+" "
		bestCurrentLemmatizedForm=bestCurrentLemmatizedForm.strip().lower() # because the final for loop adds a space at the end of the string
		nextDF['best current lemmatized form'][i]=bestCurrentLemmatizedForm
		print(bestCurrentLemmatizedForm)
		
		# count successes and fails
		for item in finishedText:
			if item[1]=='UNK' and item[0] not in latinStopList:
				print("\tfail:\t"+item[0]) # this reports things like que even though they don't make it into the final fails list for the session!
				numberOfFails+=1
			else:
				numberOfSuccesses+=1

		# write failsList to the cell in the fifth column in a prettyprint string form, just for mark one eyeball perusal. it is not important to save the failsList structure because if/when we next run the system, we need to look for fails in column 3 not column 5 anyway so as to maintain the integrity and sequence of tokens/lemmas in the titles.
		nextDF['fails'][i]=failsList
	
	# write the dataframe to a new csv file. 
	fPrime=os.path.split(f)[1]
	print(fPrime)
	nextDF.to_csv(os.path.join(newOutputFolder,fPrime),index=False)
	#nextDF.to_csv(os.path.join(newOutputFolder,'testData3.csv'),index=False)
	
	# This is the last action to take after the loading and full processing of each file in the data folder. 
	# After all data files have been processed, the for loop stops. 

# now we are done with all processing of data files # time to wrap up

# print failures to console and to custom dictionary file for next round
failsListSession=sorted(list(set(failsListSession))) # deduplicate the failsListSession list
print("all fails this session:\t"+str(failsListSession))
customDictionaryDF=pd.read_csv(customDictionaryPath, na_values=['nan'], keep_default_na=False)
failsDF=pd.DataFrame(failsListSession, columns=['token'])
newCustomDictionaryDF=customDictionaryDF.append(failsDF, ignore_index=True)
newCustomDictionaryDF=newCustomDictionaryDF.sort_values(by='token', ascending=1) # sort rows in new dataframe
#newCustomDictionaryDF.to_csv('customDictionary-NEW.csv',mode='w',index=False) # write to a new file
newCustomDictionaryDF.to_csv('customDictionary.csv',mode='w',index=False) # write to a new file

# tally results to console
print("number of successes:\t"+str(numberOfSuccesses))
print("number of fails:\t"+str(numberOfFails))

# copy old custom dictionary to output folder for archiving just in case
shutil.copy(customDictionaryPath, os.path.join(newOutputFolder,'customDictionary-OLD.csv'))

# send successfulHits list to output
# successfulHits is name of list
shfo=open('successfulHits.csv', 'w') # successful hits file object
wr=csv.writer(shfo)
successfulHits=sorted(list(set(successfulHits))) # deduplicate the successfulHits list to make it smaller and easier to read
wr.writerows(successfulHits)

# add a space for the sake of clarity of output to screen
print()
