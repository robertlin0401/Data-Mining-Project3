import numpy as np

def run(adj_matrix):
    length = len(adj_matrix)
    a = np.ones(length)
    h = np.ones(length)

    while True:
        new_a = np.dot(adj_matrix.T, h)
        new_h = np.dot(adj_matrix, a)

        new_a = new_a / sum(new_a)
        new_h = new_h / sum(new_h)

        if (sum(abs(a - new_a)) + sum(abs(h - new_h)) < 0.001):
            break
        
        a = new_a
        h = new_h

    return a, h
