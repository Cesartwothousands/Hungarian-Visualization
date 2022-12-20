import numpy as np


# n^4 Graph implemenation of Hungarian algorithm

class min(object):

    def __init__(self, graph):
        self.graph = graph
        # graph
        self.n, self.m = graph.shape
        assert self.n == self.m
        # number of n
        self.lx = self.graph.min(1)
        self.ly = np.array([0] * self.m, dtype=int)
        # if weight of edges is float, change dtype to float
        self.match = np.array([-1] * self.n, dtype=int)

        self.visx = np.array([False] * self.n, dtype=bool)
        self.visy = np.array([False] * self.m, dtype=bool)

    def reset_vis(self):
        self.visx.fill(False)
        self.visy.fill(False)

    def find_path(self, x):
        self.visx[x] = True

        for y in range(self.m):
            if self.visy[y]:
                continue

            tmp_delta = self.lx[x] + self.ly[y] - self.graph[x][y]

            if tmp_delta == 0:
                self.visy[y] = True
                if self.match[y] == -1 or self.find_path(self.match[y]):
                    self.match[y] = x
                    return True

        return False

    def KM(self):
        delta = -1
        for x in range(self.n):

            while True:
                self.reset_vis()

                if self.find_path(x):
                    break
                else:

                    for i in range(self.n):
                        for j in range(self.n):
                            if not self.visy[i] and delta > self.graph[i][j] - self.lx[i] - self.ly[j]:
                                delta = self.graph[i][j] - self.lx[i] - self.ly[j]

                    self.lx[self.visx] -= delta
                    self.ly[self.visy] += delta

        return np.sum(self.lx) + np.sum(self.ly)

    def __call__(self):
        return self.KM()

