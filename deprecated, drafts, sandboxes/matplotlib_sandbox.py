import networkx as nx
import matplotlib # do not remove

# see what matplotlib backend is in use
print(matplotlib.get_backend())

# use TkAgg instead
matplotlib.use("TkAgg")
print(matplotlib.get_backend())

# gibs for drawing # here is where the error happens
import matplotlib.pyplot as plt

# matplotlib.use('agg') # a hack I found because I was having trouble witha module called tkinter


G = nx.petersen_graph()
plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')



plt.show()

# fucking does not work
# no module named _tkinter
