# network analysis and graphing module
# The purpose of this module is to graph a network and to produce a set of basic useful reports.

# to do: modify textNetworks module to enable it to output list or dictionary of edges, which could be used directly in the present module. that output might include both a title for the data set and the data set itself in list or dictionary form. the title is important in case we want to send multiple data sets to the present module one after another.
# gibs
import networkx as nx

# make graph
G = nx.Graph()

# add edges
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

# reporting of basic node and edge stuff
print("nodes")
print(G.number_of_nodes())
print(list(G.nodes))
print("edges")
print(G.number_of_edges())
print(list(G.edges))

# report adjacencies
print("adjacencies")
for node in G.nodes:
	print(node+": "+str(list(G.adj[node]))) # it's good to use list function before printing # list function turns native nx dictionary into more human-readable list
print(list(G["jus"])) # list form
# print(G["jus"]) # dictionary form

# set (new) edge attributes
print("setting new edge attributes")
G["jus"]["civilis"]["status"]="super important"
# G.edges[1, 2]['color'] = "red" # another way to do it
print(G["jus"]["civilis"]["status"])
G["jus"]["civilis"]["weight"]=17
print(G["jus"]["civilis"]["weight"])

# graph

import matplotlib # do not remove
matplotlib.use('agg') # a hack I found because I was having trouble witha module called tkinter
import matplotlib.pyplot as plt

nx.draw(G)
plt.show()



# Betweenness centrality?


# Community detection
# (alt. use high word distance or collocation to find all words which basically are never around one another)
# I forget but clustering seems similar to community detection. Possible alternative? 


# triangles with the highest total edge weight # i.e. there are going to be lots of triangles # but the sum of the weights of the 3 edges of some triangles will be greater than the sum of the weights of the 3 edges of others.
