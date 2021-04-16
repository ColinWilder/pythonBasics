"""
Some notes, 3/31/2021:
This is a new version of the triangle code. Prevoius version is at triangles_2017.py.
The functoins of this version should be to only find triangles and their weights.
So it's essentially going to be a utility file, that is, contain one or more tools. 
"""

# gibs
import csv, os
from glob import glob
import networkx as nx

# geyers
listOfTriangleEdges = []
listOfTriangleEdges.append(["Source","Target","Type","Weight"])
triangleEdge=[]

# make network
G = nx.Graph() # I gather this makes an empty network in networkx

# make base path
# cwd=os.getcwd()
# operationsDirectoryName="triangles_operations"
# basePath=os.path.join(cwd,operationsDirectoryName)

# get files
# g=glob(basePath + "/data/*")

# Expect that each CSV file contains rows that are just network edges: 2 cells, a node and a node (skip first line since it has column titles)
# For each file, for each row in the CSV, put edges into NetworkX and perform operations.  
"""
print("##################### reading CSV rows ################")
for file in g:
	print("reading " + str(file))
	# make csv writer object to write triangles to
	dataFileName=os.path.split(file)[1] # the list index 1 just gets the filename itself, leaving off all of the folder directory structure
	outputFilePath=basePath+'/results/' + 'triangles_' + dataFileName[0:-4] + '.csv' # the 0:-4 index is to get rid of the .csv extension
	outputFileObject = open(outputFilePath,"w", newline='') # open csv writer object for writing # in Python 2 it might be w instead of wb
	trianglesWriter=csv.writer(outputFileObject) # make csv writer object to write triangle ngrams to
	outputFilePath=basePath+'/results/' + 'triangleNgrams_' + dataFileName[0:-4] + '.csv' # the 0:-4 index is to get rid of the .csv extension
	outputFileObject = open(outputFilePath,"w", newline='') # open csv writer object for writing # in Python 2 it might be w instead of wb
	triangleNgramsWriter=csv.writer(outputFileObject)
	# read spam from so-called data file
	with open(file, newline='') as f:
		spamReader = csv.reader(f,delimiter=',')
		for row in spamReader:
			if spamReader.line_num == 1: # I think this means we are ignoring the first line since it is the column headings
				continue
			else:
				if int(row[3]) > 1:
					G.add_edge(row[0],row[1]) # insert ngram into networkX graph
					G[row[0]][row[1]]['weight']=row[3]
					print(row[0],row[1],": ",G[row[0]][row[1]]['weight'])
"""


# expect that we are going to feed this code a bgram dictionary
# recall that a bgram dictonary is a python dictionary showing the frequency of bgram types in a document.
if int(row[3]) > 1:
	G.add_edge(row[0],row[1]) # insert ngram into networkX graph
	G[row[0]][row[1]]['weight']=row[3]
	print(row[0],row[1],": ",G[row[0]][row[1]]['weight'])






# report adjacencies
print("##################### adjacencies #####################")
for node in G.nodes:
	# print(node) # prints node label
	# print(G[node]) # prints list of neighbors - in useless form
	# print(list(G[node])) # prints list of neighbors
	# print(G.adj[node]) # prints list of neighbors - in useless form
	print(node+": "+str(list(G.adj[node]))) # it's good to use list function before printing # list function turns native nx dictionary into more human-readable list

# find triangles 
print("##################### triangles #######################")
triangles=[] # all the triangles we find go here
for node in G.nodes:
	neighbors=list(G.adj[node])
	if len(neighbors)<2: # too few edges; cannot be part of a triangle; ignoring this one
		continue
	else:
		# print("candidate:",node)
		for neighbor in neighbors:
			non=list(G.adj[neighbor]) # non stands for neighbors of neighbors
			for someNon in non:
				if someNon in neighbors: # if the neigbor of a neighbor of the original node is itself a neighbor, then you have a triangle
					triangle=sorted([node,neighbor,someNon]) # triangle should be a list
					if triangle not in triangles: # check whether we already found this one; if so, don't report and count it again
						print(node,neighbor,someNon)
						triangles.append(triangle)
					# produce list of just those ngrams that are in the triangles - listOfTriangleEdges
					for i in range(0,3):
						j=i+1
						if j==3:
							j=0 # make it do last vertex with first first
						triangleEdge=sorted([triangle[i],triangle[j]])
						wt=int(G[triangle[i]][triangle[j]]['weight'])
						triangleEdge.append("Undirected")
						triangleEdge.append(wt)
						if triangleEdge not in listOfTriangleEdges:
							listOfTriangleEdges.append(triangleEdge)


# find triangle weights!
print("##################### triangle weight #################")
triangleWeight=0
for triangle in triangles:
	triangleWeight=int(G[triangle[0]][triangle[1]]['weight']) + int(G[triangle[1]][triangle[2]]['weight']) + int(G[triangle[0]][triangle[2]]['weight'])
	print(triangle[0], triangle[1], triangle[2],": ",str(triangleWeight))


############################ send results to CSV file ########
# use trianglesWriter
outputList=[]
outputList.append(["triangle","triangle weight"]) # this adds column titles
for triangle in triangles:
	triangleWeight=int(G[triangle[0]][triangle[1]]['weight']) + int(G[triangle[1]][triangle[2]]['weight']) + int(G[triangle[0]][triangle[2]]['weight'])
	L=[int(G[triangle[0]][triangle[1]]['weight']), int(G[triangle[1]][triangle[2]]['weight']), int(G[triangle[0]][triangle[2]]['weight'])]
	triangleAverageWeight=sum(L) / float(len(L))
	outputList.append([triangle, triangleWeight, triangleAverageWeight]) # adds information for each triangle
	# note we added the triangle's average weight on as another columnb
trianglesWriter.writerows(outputList)

triangleNgramsWriter.writerows(listOfTriangleEdges)

############################ create regular gephi csv output too
"""
for each triangle
add each of its edges to a list of edges to be graphed/added to a csv file
any time you encounter a dupe, it should be the same as what was already in there .
save to output file
let's not make a new node file since the nodes of the triangles are a subset of all the nodes of the graph
"""
