import numpy as np
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
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
        self.slack = np.array([0] * self.m, dtype=int)
        self.visx = np.array([False] * self.n, dtype=bool)
        self.visy = np.array([False] * self.m, dtype=bool)

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
            print("tmp",tmp_delta)

            if tmp_delta == 0:
                self.visy[y] = True
                print("bool:",self.match[y], self.find_path(self.match[y]))
                if self.match[y] == -1 or self.find_path(self.match[y]):
                    print("xxxxxxxxxxxxxxxxxxxxxxxx",x)
                    self.match[y] = x
                    return True

            elif self.slack[y] < tmp_delta:
                self.slack[y] = tmp_delta

        return False

    def KM(self):
        for x in range(self.n):
            print("x",self.lx,"y", self.ly,"match", self.match,"slack", self.slack,"vx", self.visx,"vy", self.visy)
            for j in range(self.n): self.slack[j]
            while True:
                print(j,1)
                self.reset_vis()
                print(2)
                
                if self.find_path(x):
                    print(3)
                    break
                else:
                    print(4)
                    # update slack
                    delta = self.slack[~self.visy].min()
                    self.lx[self.visx] -= delta
                    self.ly[self.visy] += delta
                    self.slack[~self.visy] -= delta

        return np.sum(self.lx) + np.sum(self.ly)

    def __call__(self):
        return self.KM()


#costEdges = np.random.randint(5, 15, (2, 2))
costEdges =np.array([
        [5,10],
        [11,12]    
])
matrix = costEdges.copy()
print(costEdges)

algorithm = AdjacencyMatrixHungarian(matrix)
result = algorithm.calculate()
sum = 0
for x, y in result:
    sum += int(costEdges[x][y])
print(matrix)

algorithm = min_bipartite_graph_match(costEdges)
val = algorithm.__call__()

if sum != val:
    print("neq")
    print(sum)
    print(val)
    print(costEdges)
else: print("Right!")
