import numpy as np

def run(adj_matrix):
    length = len(adj_matrix)
    C = 0.5

    W = np.array(adj_matrix.T)
    for index, row in enumerate(W):
        W[index] = [(1 / sum(row)) if i == 1 else 0 for i in row]
    W = W.T

    s = np.dot(W.T, W) * C
    np.fill_diagonal(s, 1)

    while True:
        new_s = np.dot(np.dot(W.T, s), W) * C
        np.fill_diagonal(new_s, 1)
        
        if (sum(sum(abs(s - new_s))) < 0.001):
            break

        s = new_s

    return s
