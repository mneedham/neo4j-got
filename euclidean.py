from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

def distances(a, b):
    return np.linalg.norm(a-b), cosine_similarity([a, b])[0][1]

def mixed(n_zeros, n_ones):
    return np.concatenate((np.repeat([1], n_ones), np.repeat([0], n_zeros)), axis=0)

def ones(n_ones):
    return np.repeat([1], n_ones)

# as we increase the dimensionality, the cosine similarity stays the same but euclidean distance increases

print distances(mixed(2, 2), ones(4))
print distances(mixed(3, 3), ones(6))
print distances(mixed(50, 50), ones(100))
print distances(mixed(300, 300), ones(600))
