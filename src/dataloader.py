import numpy as np

# read graph data at {path} and return an adjacent matrix of that graph
def readGraph(path):
    lines = []
    max_node_id = 0

    # read lines and find the max node id
    with open(path, 'r') as fd:
        for line in fd.read().splitlines():
            lines.append(line)
            if max_node_id < max(int(line.split(',')[0]), int(line.split(',')[1])):
                max_node_id = max(int(line.split(',')[0]), int(line.split(',')[1]))
        fd.close()
    
    # build the adjacent matrix
    adj_matrix = np.zeros((max_node_id, max_node_id))
    for line in lines:
        adj_matrix[int(line.split(',')[0]) - 1][int(line.split(',')[1]) - 1] = 1
    
    return adj_matrix
