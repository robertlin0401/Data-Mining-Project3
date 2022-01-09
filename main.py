from src import dataloader, HITS

# constant
path = "./data/"
graphs = [
    "graph_1.txt",
    "graph_2.txt",
    "graph_3.txt",
    "graph_4.txt",
    "graph_5.txt",
    "graph_6.txt"
]

# read graph data
graph_matrices = []
for graph in graphs:
    graph_matrices.append(dataloader.readGraph(path + graph))
