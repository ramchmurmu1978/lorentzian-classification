import numpy as np

def lorentzian_distance(x, y):
    """
    Calculate lorentzian_distance between two feature vectors.
    Parameters:
        x: array-like 
           first feature vector.
        y: array-like
           second feature vector.
    Returns:
        float:
            Lorentzian distance.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    distance = np.sum(np.log1p(np.abs(x - y)))

    return distance
def find_nearest_neighbour(
        current_vector,
        historical_vectors,
        k=8
):
    """
    Find the k nearest historical observations using lorentzian distance. 
    
    Parameters:
        current_vectors: array-like
        Current feature vectors.

        historical_vectors: array-like
        Historical feature vectors.

        k: int
           Number of nearest neighbours

        Returns:
            list
        List of (index, distance) tuples.
        """
    distances = []

    for index, historical_vector in enumerate(historical_vectors):
        distance = lorentzian_distance(current_vector, historical_vector)
        distances.append((index, distance))

    distances.sort(key=lambda x: x[1])

    return distances[:k]

def predict_from_neighbors(neighbor_indices, labels):
    """
    Predict class using majority vote from nearest neighbors.
    
    Parameter
    ---------
    neighbor_indices: list
        Indices of nearest neighbors.
    labels: panda Series
        Classification labels.

    Return
    ------
    int
        Predicted class: 1 or -1
    """
    neighbor_labels = [
        labels.loc[index]
        for index in neighbor_indices
    ]
    positive_count = neighbor_labels.count(1.0)
    negative_count = neighbor_labels.count(-1.0)

    if positive_count > negative_count:
        return 1
    else:
        return -1