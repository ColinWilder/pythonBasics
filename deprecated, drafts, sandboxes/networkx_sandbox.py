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
print(list(G["jus"])) # list form
# print(G["jus"]) # dictionary form

# density
density = nx.density(G)
print("########### density ###########")
print("Network density:", density)

# shortest path (demo)
print("########### shortest path (demo)")
sample_shortest_path = nx.shortest_path(G, source="jus", target="doctor")
print("Shortest path between jus and something:", sample_shortest_path)
print("Length of that shortest path: ", len(sample_shortest_path)-1)
# there are other shortest path methods; see Ladd et al tutorial
# diameter # only works on connected graphs

# connected components
print("########### connectedness #####")
print(nx.is_connected(G)) # learn if graph is connected
components = nx.connected_components(G) # get list of components
largest_component = max(components, key=len) # use max() command to find largest one
subgraph = G.subgraph(largest_component) # create subgraph of just the largest component
diameter = nx.diameter(subgraph) # then calculate diameter of subgraph
print("Network diameter of largest component:", diameter)

# triads
print("########### triads ############")
triadic_closure = nx.transitivity(G)
print("Triadic closure:", triadic_closure)
print("for each node, the number of triangles which include it")
for node in G.nodes:
	print(node,":",nx.triangles(G, node)) # gives the number of triangles which include node n as a vertex

# triangle weight
"""
pseudo code
for a given node
if there are 2+ edges
make a list of its neighbors
in turn look at the neighbors of each neighbor
if the neigbor of a neighbor of the original node is itself a neighbor, then you have a triangle

"""