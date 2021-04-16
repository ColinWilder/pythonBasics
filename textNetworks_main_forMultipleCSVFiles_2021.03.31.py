# October 20, 2017

# Notes: My purpose in upping to version 3 is to integrate NetworkX into the code. Specifically, after reading the data CSV files, this code should put those into NetworkX edges, find and report the adjacencies/neighbors of each node, and then find and report all triangles and their weights.

# To do in a future version: Figure out the best way to organize different functions into code. all in one block? separate modules which call one another?

############ gibs ######################################################

import os, csv
import pandas as pd
from glob import glob
from utilities_bigrams import *
from utilities_output_files import *
from utilities_prepForGephi import *

############ global variables: general #################################

desiredWordDistance=2 # 1 means that ngrams are contructed only of adjacent words, but keep in mind that customarily stop words will already have been removed. wd=2 would mean that a bigram could be constructed for instance from two words that are separated by another word (hence the first word in the bigram is 2 away from the second). 
print("word distance:\t\t\t" + str(desiredWordDistance))
allTokensInWholeExecution=[]
allNgramsInWholeExecution=[]
ngramsDictInWholeExecution={}
outputForWholeExecution="" # this string will hold all output for all files processed in a given execution of the module, for one-stop shopping
tokenDictInCurrentSession={}

############ global variables: folders and data ########################

cwd=os.getcwd()
operationsDirectoryName="textNetworks_operations"

# make output base path
basePath=os.path.join(cwd,operationsDirectoryName)
print("basePath: \t\t\t" + basePath)

# make index path
indexPath= basePath +'/index.txt'
print("indexPath: \t\t\t" + indexPath)

# find the index of the most recent output
currentIndex=findCurrentOutputIndex(indexPath)
print("currentIndex: \t\t\t" + str(currentIndex))

# make data folder path
dataFolder=os.path.join(basePath,"data") # this is where data file(s) must be put to be found!
print("data folder: \t\t\t" + dataFolder)

# make new output folder based on index
newOutputFolderName="output"+str(currentIndex)
outputFolderPath=basePath+'/'+newOutputFolderName
if not os.path.exists(outputFolderPath):
	os.makedirs(outputFolderPath)
print("new output folder: \t\t" + outputFolderPath + "\n")

############ read data #################################################

# look in data folder
g=glob(dataFolder + "/*")

# to do: here you should separately open, read, and copy the contents of each data file, then add it all together into one giant combined data file. at present, I have been doing this manually. 

# open and process file(s) inside the data folder
for fileName in g:
	# get our bearings
	print("found in data folder:\t\t"+str(fileName))
	# initialize variables which store new data - they must be empty at the start of each looping
	allNgramsInFile=[] # this is where all the ngrams from all lines of the file will be stored together
	allTokensInFile=[]
	ngramsDictForFile={} # the frequency dictionary for the ngrams
	tokenDictForFile={} # the frequency dictionary for the tokens
	outputHeader="" # the metadata that goes at the top of the output log file
	output="" # for each file processed, we will send all data to this output text and file, for easy perusal
	
	############ read and process each line ############################
	
	with open(fileName,'r+') as f:
		lines = f.readlines()
		for i in range(0,len(lines)):
			line=lines[i].lower()
			lineSplit=lines[i].lower().split()
			if len(line)==1 or len(lineSplit) == 0:
				# if nothing there, then continue i.e. do nothing
				print("empty line")
				continue
			else:
				allNgramsInFile.extend(makeBigrams(line,desiredWordDistance)) # makes ngrams; add to allNgramsInFile list
				allNgramsInWholeExecution.extend(makeBigrams(line,desiredWordDistance)) # makes ngrams; add to allNgramsInWholeExecution list
				for token in lineSplit:
					allTokensInFile.append(token)
					allTokensInWholeExecution.append(token)
					tokenDictForFile=countTokens(token, tokenDictForFile) # count each token into the token dictionary

	# put all ngrams into the ngram frequency dictionary
	for ngram in allNgramsInFile:
		ngramsDictForFile=countNgram(ngram, ngramsDictForFile)

	############ send stuff to console, output data to files ###########

	# console and output: tokens
	output += "\nTokens:"
	allTokensInFile=sorted(allTokensInFile)
	output += "\n" + "number of tokens:\t" + str(len(allTokensInFile))
	print("number of tokens:\t" + str(len(allTokensInFile)))
	# print(allTokensInFile)
	output += "\n" + "number of types:\t" + str(len(list(set(allTokensInFile))))
	print("number of types:\t" + str(len(tokenDictForFile.keys())))
	# print(list(tokenDictForFile.keys()))
	# output += "\n"+ str(allTokensInFile)

	# console and output: ngrams
	output += "\n\nNgrams:"
	allNgramsInFile=sorted(allNgramsInFile)
	output += "\n" + "number of ngrams (non-unique):\t" + str(len(allNgramsInFile))
	print("number of ngram tokens (i.e. all ngrams, including duplicates):\t" + str(len(allNgramsInFile)))
	# for ngram in allNgramsInFile:
		# output += "\n"+ str(ngram)
	output += "\n" + "number of ngrams (unique):\t" + str(len(ngramsDictForFile.keys()))
	print("number of ngram types (i.e. unique ngrams):\t" + str(len(ngramsDictForFile.keys())))
	# print(list(ngramsDictForFile.keys()))
		
	# console and output: token dictionary
	output += "\n\nToken frequency dictionary:"
	# output += "\n"+ str(tokenDictForFile)

	# console and output: ngrams dictionary
	output += "\n\nNgram frequency dictionary:"
	# output += "\n"+ str(ngramsDictForFile)
	
	# pass ngrams dictionary for file to larger ngrams dictionary for whole execution
	for k in ngramsDictForFile.keys():
		if k not in ngramsDictInWholeExecution.keys():
			ngramsDictInWholeExecution[k]=ngramsDictForFile[k]
		else:
			ngramsDictInWholeExecution[k]=ngramsDictInWholeExecution[k]+ngramsDictForFile[k]

	# send output to log file
	dataFileName=os.path.split(fileName)[1]
	logFilePath=outputFolderPath+'/' + dataFileName[0:-4] + '_textNetworks_output.txt' # the 0:-4 index is to get rid of the .csv extension
	logFileObject = open(logFilePath,"w") # open log file for writing
	
	# write stuff
	outputForWholeExecution += "logFile " + str(currentIndex) + " for data file\n"
	outputForWholeExecution += fileName + "\n\n"
	now = datetime.datetime.today().strftime("This log file was created on %m/%d/%Y, %H:%M:%S"+".\n")
	outputForWholeExecution += now
	outputForWholeExecution += "word distance:\t" + str(desiredWordDistance)
	logFileObject.write(outputHeader)
	logFileObject.write(output)
	logFileObject.close

	# write output for whole execution - all files
	outputForWholeExecution+=outputHeader+"\n"
	outputForWholeExecution+=output+"\n\n"

	# make the CSV files for graphing in Gephi
	makeEdgeListForGephi(ngramsDictForFile, dataFileName[0:-4], outputFolderPath)
	makeNodeListForGephi(tokenDictForFile, dataFileName[0:-4], outputFolderPath)
	print()

############ final housekeeping ########################################

# count up total number of u and non-u tokens and u and non-u ngrams and send to big output
# outputForWholeExecution+="number of non-unique tokens in all data examined in this execution:\t"+str(len(allTokensInWholeExecution))+"\n"
# outputForWholeExecution+="number of unique tokens in all data examined in this execution:\t"+str(len(list(set(allTokensInWholeExecution))))+"\n"
# outputForWholeExecution+="number of non-unique ngrams in all data examined in this execution:\t"+str(len(allNgramsInWholeExecution))+"\n"
# outputForWholeExecution+="number of unique ngrams in all data examined in this execution:\t"+str(len(ngramsDictInWholeExecution.keys()))
#### I've commented this out because at present it just gives back these four numbers. It doesn't make a composite CSV, or the actual node or edge lists. 

# write output for whole execution to file
logFilePath=outputFolderPath+'/' + 'textNetworks_output_wholeRun.txt'
logFileObject = open(logFilePath,"w")
logFileObject.write(outputForWholeExecution)
logFileObject.close

# increment index for next time and write it to the index file for next time
currentIndex+=1
f = open(indexPath, "w")
f.write(str(currentIndex)) # print to output
f.close
