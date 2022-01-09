import numpy as np

def run(adj_matrix):
    length = len(adj_matrix)
    r = np.ones(length) / length
    d = 0.1

    for index, row in enumerate(adj_matrix):
        if sum(row) != 0:
            adj_matrix[index] = row / sum(row)

    while True:
        new_r = d / length + (1 - d) * np.dot(adj_matrix.T, r)

        new_r = new_r / sum(new_r)

        if (sum(abs(r - new_r)) < 0.001):
            break
        
        r = new_r

    return r