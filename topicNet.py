
# gibs
import csv, os
from glob import glob

# global variables
counter=0

# book words
bookWordsList=['abdruck', 'abhandlung', 'actum', 'anmerkung', 'annotatio', 'beitrage', 'bericht', 'blatt', 'buch', 'buchdruckerkun', 'b\xc3\xbcchlein', 'codex', 'commentaria', 'commentarius', 'commentatio', 'consilium', 'decretales', 'decretum', 'digestum', 'documentum', 'enchiridion', 'epistolicus', 'epistula', 'epitome', 'gegenbericht', 'geschichtsregister', 'handlung', 'kreutterbuch', 'lexicon', 'littera', 'manuscript', 'opus1', 'pandectae', 'register', 'rescript', 'schrift', 'tomus', 'tractatus'] # ambiguous cases include terms like argumentum assertio etc. (many such could be enumerated) # they are ambiguous to me because they essentially mean a human narrative act of forming an argument or account # such actions are closely akin to an actual book

# canon law words
canonLawList=['canon', 'canonicus', 'decretum', 'decretale', 'utriusque']

# history words
targetList=['chronick', 'chronicon', 'chronographica', 'chronologia', 'enarratio', 'erzähhlung', 'geschichte', 'geschichtsregister', 'histoire', 'historia', 'historicus', 'historischer']

# make base path
cwd=os.getcwd()
operationsDirectoryName="topicNet_operations"
basePath=os.path.join(cwd,operationsDirectoryName)

# get files
g=glob(basePath + "/data/*")

# For each file, for each title, if any of the words in the target list appear, then copy the bestCurrentLemmatizedForm into a temporary list. 

print("extracting titles that contain types " + str(targetList))

hits=[] # list to hold all those titles which are found to contain one or more terms from the target list

for file in g:
	print("\nreading " + str(file)+"\n")
	# make csv writer object to write local results to
	dataFileName=os.path.split(file)[1]
	outputFilePath=basePath+'/results/' + 'historyResults_' + dataFileName[0:-4] + '.csv' # the 0:-4 index is to get rid of the .csv extension
	outputFileObject = open(outputFilePath,"w") # open csv writer object for writing # in Python 2 it might be w instead of wb
	w=csv.writer(outputFileObject)

	with open(file,'r+') as f:
		titles = f.readlines()
		for i in range(0,len(titles)):
			title=titles[i].lower().split() # turn title into a list of tokens
			for token in title:
				if token in targetList:
					if title not in hits:
						hits.append(title)
						print(titles[i][0:-1])
						counter+=1
						w.writerow([titles[i][0:-1]]) # write that to the csv writer object
		hits=[] # empty the hits list so it can be used cleanly when examining the next file
		print(str(counter)+" results")
		counter=0 # reset the counter

# Remove all instances of words in [historia, historisch] from the strings in the temporary list. 
# Now for each string, make edge pairs out of all collocates in any given line. 
