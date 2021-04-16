# Subcreated first on Wednesday, June 7, 2017
# @author: Colin F. Wilder
# Intellectual Property statement: This code is based on lots of other freely available code on the internet, but the synthesis is mine. This relates to my broader metaphysics of creation and subcreation. I have gained a lot from Stack Overflow. The basic ngrams stuff I think is my own,but may also come from lessons from the Programming Historian by Adam Crymble and William Turkel. Parts of them were inspired by code written by Duncan Buell in his CSCE 500; Programming for Humanists course at the University of South Carolina in Autumn 2013. This module is therefore released under a CC-BY license i.e. Creative Commons Attribution 2.0 Generic license, which is explained at https://creativecommons.org/licenses/by/2.0/.#
# this is a set of utilities that takes an ngram frequency dictionary and produces a node list and an edge list suitable for graphing in Gephi

# gibs
import csv

# make list of edges in csv
def makeEdgeListForGephi(ngramsFrequencyDictionary, fileTitlePrefix="", filePath=""):
	# make list of triples (i.e. list of 3-item lists)
	outputList=[]
	outputList.append(["Source","Target","Type","Weight"]) # this adds column titles
	for key in ngramsFrequencyDictionary:
		outputList.append([key[0],key[1],"Undirected",ngramsFrequencyDictionary[key]]) # adds information for each ngram
	# write the new output list into the new file and close it
	if fileTitlePrefix=="":
		fileTitle+="text_networks_output_edges.csv"
	else:
		fileTitle=fileTitlePrefix+"_text_networks_output_edges.csv"
	if filePath=="":
		fileTitle=fileTitle
	else:
		fileTitle=filePath + "/" + fileTitle
	csvEdgeFileObject=open(fileTitle, 'w') # in Python 2 it might be w instead of wb
	w=csv.writer(csvEdgeFileObject)
	w.writerows(outputList)
	print("edge list has been generated")

# make list of nodes in csv # we need this because to graph a network, you need label names
def makeNodeListForGephi(tokensFrequencyDictionary, fileTitlePrefix="", filePath=""):
	# transform the token dictionary into a list of triples
	outputList=[]
	outputList.append(["Id","Label","Weight"]) # Id and Label are same (improve this later)
	for key in tokensFrequencyDictionary:
		outputList.append([key,key,tokensFrequencyDictionary[key]])
	# write the new output list into the new file and close it
	if fileTitlePrefix=="":
		fileTitle+="textNetworks_output_nodes.csv"
	else:
		fileTitle=fileTitlePrefix+"_textNetworks_output_nodes.csv"
	if filePath=="":
		fileTitle=fileTitle
	else:
		fileTitle=filePath + "/" + fileTitle
	csvNodeFileObject=open(fileTitle, 'w') # see similar above
	w2=csv.writer(csvNodeFileObject)
	w2.writerows(outputList)
	print("node list has been generated")
    
