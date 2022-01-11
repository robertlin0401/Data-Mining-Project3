import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from src import dataloader, HITS, PageRank

# constant
path = {
    "input": "./data/",
}
graphs = [
    "graph_1.txt",
    "graph_2.txt",
    "graph_3.txt",
]

# Read data.
matrices = []
for graph in graphs:
    matrices.append(dataloader.readGraph(path["input"] + graph))

# HITS
a = []
h = []
for matrix in matrices:
    result = HITS.run(np.array(matrix))
    a.append(result[0])
    h.append(result[1])
print(h[0][0], h[1][0], h[2][0])
print(a[0][0], a[1][0], a[2][0])

# PageRank
r = []
for matrix in matrices:
    r.append(PageRank.run(np.array(matrix)))
print(r[0][0], r[1][0], r[2][0])

# Draw Graph.
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
for index, graph in enumerate(graphs):
    G = nx.DiGraph()
    edges = []
    with open(path["input"] + graph, 'r') as fd:
        for line in fd.read().splitlines():
            edges.append((line.split(',')[0], line.split(',')[1]))
        fd.close()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size=500, ax=axs[index])
    nx.draw_networkx_labels(G, pos, ax=axs[index])
    nx.draw_networkx_edges(G, pos, node_size=500, arrowsize=14, arrows=True, ax=axs[index])
    axs[index].title.set_text(graph.split('.')[0])
fig.tight_layout()
plt.show()
