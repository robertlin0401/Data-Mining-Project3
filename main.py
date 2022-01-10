import numpy as np
from src import dataloader, HITS, PageRank, SimRank

# constant
path = {
    "input": "./data/",
    "output": "./output/"
}
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
    matrices.append(dataloader.readGraph(path["input"] + graph))
matrices.append(dataloader.readIBM(path["input"] + ibm))

# HITS
a = []
h = []
for matrix in matrices:
    result = HITS.run(np.array(matrix))
    a.append(result[0])
    h.append(result[1])

for i in range(7):
    if i != 6:
        np.savetxt(path["output"] + graphs[i].split('.')[0] + "_HITS_authority.txt", a[i], fmt="%.8f", newline=" ")
        np.savetxt(path["output"] + graphs[i].split('.')[0] + "_HITS_hub.txt", h[i], fmt="%.8f", newline=" ")
    else:
        np.savetxt(path["output"] + ibm.split('.')[0] + "_HITS_authority.txt", a[i], fmt="%.8f", newline=" ")
        np.savetxt(path["output"] + ibm.split('.')[0] + "_HITS_hub.txt", h[i], fmt="%.8f", newline=" ")

# PageRank
r = []
for matrix in matrices:
    r.append(PageRank.run(np.array(matrix)))

for i in range(7):
    if i != 6:
        np.savetxt(path["output"] + graphs[i].split('.')[0] + "_PageRank.txt", r[i], fmt="%.8f", newline=" ")
    else:
        np.savetxt(path["output"] + ibm.split('.')[0] + "_PageRank.txt", r[i], fmt="%.8f", newline=" ")

# SimRank
s = []
for matrix in matrices:
    s.append(SimRank.run(np.array(matrix)))

for i in range(7):
    if i != 6:
        np.savetxt(path["output"] + graphs[i].split('.')[0] + "_SimRank.txt", s[i], fmt="%.8f", delimiter=" ")
    else:
        np.savetxt(path["output"] + ibm.split('.')[0] + "_SimRank.txt", s[i], fmt="%.8f", delimiter=" ")
