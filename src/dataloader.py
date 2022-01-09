import numpy as np

# Read graph data at {path} and return an adjacent matrix of that graph.
def readGraph(path):
    lines = []
    max_node_id = 0

    # Read lines and find the max node id.
    with open(path, 'r') as fd:
        for line in fd.read().splitlines():
            lines.append(line)
            if max_node_id < max(int(line.split(',')[0]), int(line.split(',')[1])):
                max_node_id = max(int(line.split(',')[0]), int(line.split(',')[1]))
        fd.close()
    
    # Build the adjacent matrix.
    adj_matrix = np.zeros((max_node_id, max_node_id))
    for line in lines:
        adj_matrix[int(line.split(',')[0]) - 1][int(line.split(',')[1]) - 1] = 1
    
    return adj_matrix

# Read IBM data at {path}, form a graph which links each transaction id
# to each item id, and return an adjacent matrix of that graph.
def readIBM(path):
    lines = []
    max_node_id = 0

    # Read lines and find the max node id.
    with open(path, 'r') as fd:
        for line in fd.read().splitlines():
            temp = []
            for ele in line.split(" "):
                if ele:
                    temp.append(ele)
            temp.pop(0)
            lines.append(temp)
            if max_node_id < max(int(temp[0]), int(temp[1])):
                max_node_id = max(int(temp[0]), int(temp[1]))
        fd.close()
    
    # Build the adjacent matrix.
    adj_matrix = np.zeros((max_node_id, max_node_id))
    for line in lines:
        adj_matrix[int(line[0]) - 1][int(line[1]) - 1] = 1
    
    return adj_matrix
