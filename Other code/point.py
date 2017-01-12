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
    def __init__(self, filename, kDensity, kGraph):
        self.cloud = self.readData(filename)
        self.neighbors = self.computeNeighbors(kGraph)
        self.density = self.computeDensity(kDensity)
        self.parent = self.computeForest(kDensity)
        self.label = self.computeLabels()

    def readData(self, filename):
        cloud = []
        with open(filename, 'rb') as f:
            for line in f:
                cloud.append(Point(line))
        f.close()
        return np.array(cloud)

    def computeNeighbors(self, k):
        neighbors = np.zeros((len(self.cloud), k), dtype=int)
        for i, point1 in enumerate(self.cloud):
            distances = [point1.sqDist(point2) for point2 in self.cloud]
            neighbors[i] = np.argsort(distances)[1: k+1]
        return neighbors

    def computeDensity(self, k):
        density = np.zeros(len(self.cloud))
        for i, point1 in enumerate(self.cloud):
            avg_dist = np.mean(
                [point1.sqDist(point2)
                 for point2 in self.cloud[self.neighbors[i]]])
            density[i] = 1/np.sqrt(avg_dist)
        return density

    def computeForest(self, k):
        parent = np.arange(len(self.cloud))
        for i, point1 in enumerate(self.cloud):
            max_neighbor = self.neighbors[
                np.argmax(self.density[self.neighbors[i]])]
            print(max_neighbor)
            if self.density[max_neighbor[0]] > self.density[i]:
                parent[i] = max_neighbor[0]
        return parent

    def computeLabels(self):
        labels = np.zeros(len(self.cloud), dtype=int)
        for i, point1 in enumerate(self.cloud):
            idx = i
            uphill = self.parent[idx]
            while idx != uphill:
                idx = uphill
                uphill = self.parent[idx]
            labels[i] = uphill
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
