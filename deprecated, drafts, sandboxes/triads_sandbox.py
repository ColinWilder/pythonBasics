# gibs
import networkx as nx
from operator import itemgetter
import community #This is the python-louvain package we installed.

# make network
G = nx.Graph()
G.add_edge("A","B")
G.add_edge("B","C")
G.add_edge("A","D")
G.add_edge("B","D")

# report
print(nx.info(G)) # reports basic info about network
print("########### nodes #############")
# print(G.number_of_nodes())
print(G.nodes())
print("########### edges #############")
# print(G.number_of_edges())
print(G.edges())

# report adjacencies
print("########### adjacenies ########")
for node in G.nodes:
	print(node+": "+str(list(G.adj[node]))) # it's good to use list function before printing # list function turns native nx dictionary into more human-readable list
print(list(G["A"])) # list form
# print(G["jus"]) # dictionary form

# density
density = nx.density(G)
print("########### density ###########")
print("Network density:", density)

# triads
print("########### triads ############")
triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)

# I don't know how transitivity is calculated here. 