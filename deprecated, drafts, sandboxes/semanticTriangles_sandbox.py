# gibs
import networkx as nx
from operator import itemgetter
import community #This is the python-louvain package we installed.

# make network
G = nx.Graph()
G.add_edge("jus","civilis")
G.add_edge("civilis","judicium")
G.add_edge("judicium","decisio")
G.add_edge("decisio","doctor")
G.add_edge("doctor","utriusque")
G.add_edge("utriusque","jus")
G.add_edge("jus","corpus")
G.add_edge("jus","canonicus")
G.add_edge("canonicus","corpus")
G.add_edge("canonicus","decretum")
G.add_edge("civilis","corpus")

# report adjacencies
print("########### adjacencies ########")
for node in G.nodes:
	print(node+": "+str(list(G.adj[node]))) # it's good to use list function before printing # list function turns native nx dictionary into more human-readable list
print(list(G["jus"])) # list form
# print(G["jus"]) # dictionary form

# triangle weight
print("########### triangle weight ###")
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
					triangle=sorted([node,neighbor,someNon])
					if triangle not in triangles: # check whether we already found this one; if so, don't report and count it again
						print(node,neighbor,someNon)
						triangles.append(triangle)
print(triangles)					
