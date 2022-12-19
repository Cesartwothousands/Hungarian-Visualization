import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
# n^3 Graph implemenation of Hungarian algorithm

class min_bipartite_graph_match(object):

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
        self.slack = np.array([0] * self.n, dtype=int)
        self.match_history = [list(self.match)]
        self.visx = np.array([False] * self.n, dtype=bool)
        self.visy = np.array([False] * self.m, dtype=bool)
        self.G = nx.Graph()
        for i in range(self.n):
            for j in range(self.m):
                if graph[i][j] != -1:
                    self.G.add_edge(i, self.m + j, color='black', weight=0.1)

    def draw(self):
        colors = nx.get_edge_attributes(self.G, 'color').values()
        weights = nx.get_edge_attributes(self.G, 'weight').values()
        top = nx.bipartite.sets(self.G)[0]
        pos = nx.bipartite_layout(self.G, top)
        nx.draw(self.G, pos, edge_color=colors, width=list(weights), with_labels=True)
        for i in range(self.n):
            for j in range(self.m):
                self.G[i][self.m + j]['color'] = 'black'
                self.G[i][self.m + j]['weight'] = 0.1

    def update_match_graph(self):
        m = self.match
        prev = self.match_history[-1]
        for i in range(len(prev)):
            if prev[i] != -1:
                if m[i] != prev[i]:
                    self.G[prev[i]][self.m + i]['color'] = 'r'
                    self.G[prev[i]][self.m + i]['weight'] = 2
                    self.G[m[i]][self.m + i]['color'] = 'b'
                    self.G[m[i]][self.m + i]['weight'] = 8
                else:
                    self.G[prev[i]][self.m + i]['color'] = 'g'
                    self.G[prev[i]][self.m + i]['weight'] = 5
            else:
                if m[i] != -1:
                    self.G[m[i]][self.m + i]['color'] = 'b'
                    self.G[m[i]][self.m + i]['weight'] = 8
        self.match_history.append(list(m))

    def reset_slack(self):
        self.slack.fill(-1)

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

            elif self.slack[y] < tmp_delta:
                self.slack[y] = tmp_delta

        return False

    def KM(self):
        for x in range(self.n):
            self.reset_slack()
            while True:
                self.reset_vis()
                if self.find_path(x):
                    break

                else:
                    # update slack
                    delta = self.slack[~self.visy].min()
                    self.lx[self.visx] -= delta
                    self.ly[self.visy] += delta
                    self.slack[~self.visy] -= delta
            self.update_match_graph()
            self.draw()
            plt.show(block=False)
            plt.pause(1)
            plt.close()
            if x == self.n - 1:
                self.update_match_graph()
                self.draw()
                plt.show(block=False)
                plt.pause(1)
                plt.close()

        return np.sum(self.lx) + np.sum(self.ly)

    def __call__(self):
        return self.KM()


costEdges = np.array([
    [2, 3, 2, 4],
    [4, 1, 5, 1],
    [1, 3, 6, 2],
    [5, 6, 7, 8]
])
algorithm = min_bipartite_graph_match(costEdges)
print("\n", algorithm.__call__())