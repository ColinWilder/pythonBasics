# mainComprehensiveNew.2021.04.14.py

# foundations
import urllib.request, urllib.error, urllib.parse, utilities_for_PH, utilities_kSkipNgrams20210414, csv
import networkx as nx

###########################################################################
########################## take input text ################################
###########################################################################

# overview: for time being (until you wre ready to set up the code to take and process a config file, probably wth JSON), let's just use a simple comment system: there would be one version of this section in whcih the user pastes in a url. there is one version in which the user pastes in a string of text. there will be a third and final version in which the user can give the name of a file in the working directory. if more than one entry is given for any of these, or more than one of the three is given, etc., it will be declared an input error and the process broken. 

# User provides URL
# url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
# # get info and read from internet
# response = urllib.request.urlopen(url)   
# HTML = response.read()
# # remove XML tags
# HTML=HTML.decode('utf-8') # gets rid of r/n/ ugliness
# primarySourceTextItself = utilities_for_PH.stripTags(HTML)

# User pastes in a string
primarySourceTextItself="In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. And God said, Let there be light: and there was light. And God saw the light, that it was good: and God divided the light from the darkness. And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day. And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters. And God made the firmament, and divided the waters which were under the firmament from the waters which were above the firmament: and it was so. And God called the firmament Heaven. And the evening and the morning were the second day. And God said, Let the waters under the heaven be gathered together unto one place, and let the dry land appear: and it was so. And God called the dry land Earth; and the gathering together of the waters called he Seas: and God saw that it was good. And God said, Let the earth bring forth grass, the herb yielding seed, and the fruit tree yielding fruit after his kind, whose seed is in itself, upon the earth: and it was so. And the earth brought forth grass, and herb yielding seed after his kind, and the tree yielding fruit, whose seed was in itself, after his kind: and God saw that it was good. And the evening and the morning were the third day. And God said, Let there be lights in the firmament of the heaven to divide the day from the night; and let them be for signs, and for seasons, and for days, and years: and let them be for lights in the firmament of the heaven to give light upon the earth: and it was so."

# TO DO: User gives name of a file on which to run subsequent code

###########################################################################
########################### preprocessing #################################
###########################################################################

# make lowercase
primarySourceTextItself=primarySourceTextItself.lower()

# strip all non-alphanumeric characters
fullWordList = utilities_for_PH.stripNonAlphaNum(primarySourceTextItself)

# remove stop words
wordList = utilities_for_PH.removeStopwords(fullWordList)
tokens = wordList # giving this a better name
# this produces word list format output

# TO DO: export wordList to a .txt file so it can be modularly used for KWIC as a separate process. 
# open a new empty file and write the full, original HTML to it
# f = open('obo-t17800628-33.html', 'wb') # note difference between w and wb
# f.write(HTML) # this is writing the full HTML, incl all tags
# f.close

###########################################################################
############## produce and count word types and bigram types ##############
###########################################################################

# overview: produce and count word types and bigram types. export everything to console, html browser page, and csv. the word-type frequency dictionary can be used in a spreadsheet for counting and graphing etc. the bigram-type frequency dictionary can be graphed in Gephi as I did recently for the first section of Genesis.

# produce and count word types - put into frequency dictionary
tokenFreqDict = utilities_for_PH.wordListToFreqDict(tokens)
sortedDict = utilities_for_PH.sortFreqDict(tokenFreqDict)

# print to console
# print(sortedDict[0:10])

# export to html in browser tab
# produce an output file (.html) of the word-type frequency dictionary
# outstring = ""
# for s in sortedDict:
#     outstring += str(s) # write each dictionary entry
#     outstring += "<br />" # adding a line break
# utilities_for_PH.wrapStringInHTMLWindows ("word-type-frequency-dictionary", url, outstring)

# TO DO: write the word-type frequency dictionary out as a .csv as well, for easy subsequent analysis, graphing, etc. Keep in mind though that Voyant does this pretty well already and I believe has an export feature, so this is really not something you need to do yourself here.

# produce k-skip bigrams (i.e. actually list of all k-skip bigram tokens)
kSkipBigramsList=utilities_kSkipNgrams20210414.makeKSkipBigrams(wordList, 2)
# TO DO: Add some way to eliminate self-referrals / tautologies happen - e.g. "god god 4" - where god shows up close to god 4x. 
# print(kSkipBigramsList[0:30])

# count bigrams - put into frequency dictionary
# returns a dictionary with bigrams as keys, their frequencies as values
kSkipBigramFrequencyDictionary={}
for item in kSkipBigramsList:
    pairTuple=item[0], item[1]
    if pairTuple in kSkipBigramFrequencyDictionary.keys():
        kSkipBigramFrequencyDictionary[pairTuple]=kSkipBigramFrequencyDictionary[pairTuple]+1
    else:
        kSkipBigramFrequencyDictionary[pairTuple]=1

# print to console
# print(kSkipBigramFrequencyDictionary)
for key in kSkipBigramFrequencyDictionary:
    if kSkipBigramFrequencyDictionary[key]>3:
        print(str(key) + ", " + str(kSkipBigramFrequencyDictionary[key]))

# TO DO: export to html in browser tab

# Write to CSV

# Using the frequency distribution, make a list of triples (i.e. list of 3-item lists)
outputList=[]
outputList.append(["Source","Target","Weight"]) # this adds first triple
for key in kSkipBigramFrequencyDictionary:
    sublist=[key[0],key[1],kSkipBigramFrequencyDictionary[key]]
    outputList.append(sublist) # adds a subsequent triple
#print(outputList)

# Write the new output list into the new file and close it
csvEdgeFileObject=open("kSkipBigramsAsEdges.csv", 'w') # note it's a w flag not a wb flag
w=csv.writer(csvEdgeFileObject)
# alt # path=os.path.join(os.getcwd(),"edges-CSV.csv") # and tell the writer to open path
w.writerows(outputList)

# TO DO: as is, the code creates extra lines between node-node-edge weights in the csv; don't know why yet (3/31/21)

#####################################################################
############ send stuff to console, output data to files ############
#####################################################################

# console output: tokens
tokens=sorted(tokens) # sort the big list of tokens
print("number of tokens:\t" + str(len(tokens))) # report number of tokens
# print(allTokensInFile)
print("number of types:\t" + str(len(tokenFreqDict.keys()))) # report number of types
# print(list(tokenDictForFile.keys()))

# console output: ngrams
bigramsList=sorted(kSkipBigramsList)
print("number of k-skip bigram tokens (i.e. all including duplicates):\t" + str(len(bigramsList)))
print("number of k-skip bigram types (i.e. unique k-skip bigram):\t" + str(len(kSkipBigramFrequencyDictionary.keys())))
# print(list(ngramsDictForFile.keys()))

###########################################################################
############################## triangles ##################################
###########################################################################

# read bigrams CSV
# load and run networkx
# make network of bigrams

# global variables
listOfTriangleEdges = []
listOfTriangleEdges.append(["Source","Target","Type","Weight"])
triangleEdge=[]

# make empty network graph itself
G = nx.Graph() # I gather this makes an empty network in networkx
print("created networkx graph")

for kSkipBigram in outputList[1:]:
    if int(kSkipBigram[2]) > 1: # if k-skip bigram appears 2+ times (so it is not quite so insignficant)
        G.add_edge(kSkipBigram[0],kSkipBigram[1]) # insert ngram into networkX graph
        G[kSkipBigram[0]][kSkipBigram[1]]['weight']=kSkipBigram[2]
        print(kSkipBigram[0],kSkipBigram[1],": ",G[kSkipBigram[0]][kSkipBigram[1]]['weight'])
print("added all k-skip bigrams to networkx graph")


# report adjacencies
print("##################### adjacencies #####################")
for node in G.nodes:
	# print(node) # prints node label
	# print(G[node]) # prints list of neighbors - in useless form
	# print(list(G[node])) # prints list of neighbors
	# print(G.adj[node]) # prints list of neighbors - in useless form
	print(node+": "+str(list(G.adj[node]))) # it's good to use list function before printing # list function turns native nx dictionary into more human-readable list



