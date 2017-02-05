import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Point:
    def __init__(self, line):
        stringarray = line.split(' ')
        self.coords = np.array([float(string) for string in stringarray
                                if string != ''])

    def sqDist(self, point):
        return np.linalg.norm(self.coords - point.coords) ** 2

    def toString(self):
        np.set_printoptions(precision=3)
        print("Point coordinates:\n", self.coords)


class HillClimbing:
    def __init__(self, filename, kDensity, kGraph, persistence=False, tau=0):
        self.cloud = self.readData(filename)
        self.neighbors = self.computeNeighbors(kGraph)
        self.density = self.computeDensity(persistence, kDensity, kGraph)
        self.parent = self.computeForest()
        if persistence:
            self.label = self.computePersistence(tau)
        else:
            self.label = self.computeLabels()

    def readData(self, filename):
        # Read the textfile data, with each line representing a point in the
        # dataset
        cloud = []
        with open(filename, 'rb') as f:
            for line in f:
                cloud.append(Point(line))
        f.close()
        return np.array(cloud)

    def computeNeighbors(self, k):
        # Compute k-nearest neighbors
        neighbors = np.zeros((len(self.cloud), k), dtype=int)
        for i, point1 in enumerate(self.cloud):
            distances = [point1.sqDist(point2) for point2 in self.cloud]
            neighbors[i] = np.argsort(distances)[1: k+1]
        return neighbors

    def computeDensity(self, persistence, kDensity, kGraph):
        # Compute the density neighbors
        density_neighbors = self.computeNeighbors(kDensity)

        # Compute a pointwise density estimation
        density = np.zeros(len(self.cloud))
        for i, point1 in enumerate(self.cloud):
            avg_dist = np.mean(
                [point1.sqDist(point2)
                 for point2 in self.cloud[density_neighbors[i]]])
            density[i] = 1/np.sqrt(avg_dist)

        # If we're calculating persistence, it's useful to sort the points by
        # decreasing order of density
        if persistence:
            new_idx = np.argsort(density)[::-1]
            density = density[new_idx]
            self.cloud = self.cloud[new_idx]
            self.neighbors = self.computeNeighbors(kGraph)

        return density

    def computeForest(self):
        # Compute the parent (maximum density neighbor) forest
        parent = np.arange(len(self.cloud))
        for i, point1 in enumerate(self.cloud):
            max_neighbor = self.neighbors[
                i,
                np.argmax(self.density[self.neighbors[i]])]
            if self.density[max_neighbor] > self.density[i]:
                parent[i] = max_neighbor
        return parent

    def computeLabels(self):
        # Perform clustering using the parent forest, through the hill-climbing
        # algorithm
        labels = np.zeros(len(self.cloud), dtype=int)
        for i in range(len(self.cloud)):
            idx = i
            uphill = self.parent[idx]
            while idx != uphill:
                idx = uphill
                uphill = self.parent[idx]
            labels[i] = uphill
        return labels

    def computePersistence(self, tau):
        # Initiate component labels
        labels = np.arange(len(self.cloud))
        for point, neighbors in enumerate(self.neighbors):
            # Get list of neighbors that were already processed (the ones with
            # higher density than the current point)
            proc_neighbors = neighbors[
                self.density[neighbors] > self.density[point]]

            # Get label of the max density neighbor (the parent), whose cluster
            # will integrate the others
            max_label = labels[self.parent[point]]
            neighbor_labels = labels[proc_neighbors]

            # Get only clusters with prominence peaks less than tau for merging
            neighbor_labels = neighbor_labels[
                self.density[neighbor_labels] >= self.density[max_label] + tau]

            # Integrate the clusters
            labels = np.array(
                [max_label if label in neighbor_labels or label == point
                 else label for label in labels])

        return labels

    def plotClusters(self):
        n_labels = len(np.unique(self.label))
        cmap = sns.color_palette("hls", n_labels)
        points = np.array([point.coords for point in self.cloud])
        fig, ax = plt.subplots()
        for i, label in enumerate(np.unique(self.label)):
            sub_points = points[np.where(self.label == label)]
            ax.scatter(sub_points[:, 0], sub_points[:, 1], c=cmap[i])
        plt.show()
