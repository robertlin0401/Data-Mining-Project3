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
ibm = "ibm-5000.txt"

# Read data.
matrices = []
for graph in graphs:
    matrices.append(dataloader.readGraph(path + graph))
matrices.append(dataloader.readIBM(path + ibm))
