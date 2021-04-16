
# gibs
import csv, os
from glob import glob

# make base path
cwd=os.getcwd()
operationsDirectoryName="topicModeling_operations"
basePath=os.path.join(cwd,operationsDirectoryName)

# get files
g=glob(basePath + "/data/*")

# geyers
doc_clean = [] # a list of lists # each list herein will be just the important, normalized words in the string

# read and process each data file
for file in g:
	print("\nreading " + str(file)+"\n")
	"""# make csv writer object to write local results to
	dataFileName=os.path.split(file)[1]
	outputFilePath=basePath+'/results/' + 'historyResults_' + dataFileName[0:-4] + '.csv' # the 0:-4 index is to get rid of the .csv extension
	outputFileObject = open(outputFilePath,"w") # open csv writer object for writing # in Python 2 it might be w instead of wb
	w=csv.writer(outputFileObject)"""
	
	with open(file,'r+') as f:
		titles = f.readlines()
		for i in range(0,len(titles)):
			# title=titles[i].lower().split() # turn title into a list of tokens
			title=titles[i]
			# print(title[:-1]) # there seems to be an extra carriage return at the end of the lines
			doc_clean.append(title[:-1].split()) # a list of lists # each list herein is just the important, normalized words in the string
	
	# print(doc_clean)

# Importing Gensim
import gensim
from gensim import corpora

# Creating the term dictionary of our corpus, where every unique term is assigned an index.
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=5, num_words=10))
