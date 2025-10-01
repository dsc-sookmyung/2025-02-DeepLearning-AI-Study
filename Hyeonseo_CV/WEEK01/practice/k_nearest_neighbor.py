from builtins import range
from builtins import object
import numpy as np
from past.builtins import xrange

class KNearestNeighbor(object):
    """ a kNN classifier with L2 distance """

    def __init__(self):
        pass

    def train(self, X, y):
        """
        Train the classifier. For k-nearest neighbors this is just
        memorizing the training data.
        """
        self.X_train = X
        self.y_train = y

    def predict(self, X, k=1, num_loops=0):
        """
        Predict labels for test data using this classifier.
        """
        if num_loops == 0:
            dists = self.compute_distances_no_loops(X)
        elif num_loops == 1:
            dists = self.compute_distances_one_loop(X)
        elif num_loops == 2:
            dists = self.compute_distances_two_loops(X)
        else:
            raise ValueError("Invalid value %d for num_loops" % num_loops)

        return self.predict_labels(dists, k=k)

    def compute_distances_two_loops(self, X):
        """
        Compute the L2 distance using two nested loops.
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            for j in range(num_train):
                diff = X[i] - self.X_train[j]
                dists[i, j] = np.sqrt(np.sum(diff**2))
        return dists

    def compute_distances_one_loop(self, X):
        """
        Compute the L2 distance using a single loop over test data.
        """
        num_test = X.shape[0]
        num_train = self.X_train.shape[0]
        dists = np.zeros((num_test, num_train))
        for i in range(num_test):
            diff = self.X_train - X[i]        # shape (num_train, D)
            dists[i, :] = np.sqrt(np.sum(diff**2, axis=1))
        return dists

    def compute_distances_no_loops(self, X):
        """
        Compute the L2 distance without any explicit loops.
        """
        X_square = np.sum(X**2, axis=1, keepdims=True)           # shape (num_test, 1)
        X_train_square = np.sum(self.X_train**2, axis=1)         # shape (num_train,)
        cross_term = X.dot(self.X_train.T)                       # shape (num_test, num_train)
        dists = np.sqrt(X_square - 2*cross_term + X_train_square)
        return dists

    def predict_labels(self, dists, k=1):
        """
        Predict labels based on the distance matrix.
        """
        num_test = dists.shape[0]
        y_pred = np.zeros(num_test, dtype=int)
        for i in range(num_test):
            # Get indices of k nearest neighbors
            closest_y_indices = np.argsort(dists[i])[:k]
            closest_y = self.y_train[closest_y_indices]

            # Select the most common label; tie broken by smaller label
            y_pred[i] = np.bincount(closest_y).argmax()
        return y_pred
