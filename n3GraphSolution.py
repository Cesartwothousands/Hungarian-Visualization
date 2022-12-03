import numpy as np

class min_bipartite_graph_match(object):
 
    def __init__(self,graph):
        self.graph = graph
        # graph
        self.n,self.m = graph.shape
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
            
            if  tmp_delta == 0:
                self.visy[y] = True
                if  self.match[y] == -1 or self.find_path(self.match[y]):
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
 
        return np.sum(self.lx) + np.sum(self.ly)
 
    def __call__(self):
        return self.KM()
    
costEdges=np.array([
        [2,3,2,4],
        [4,1,5,1],
        [1,3,6,2],
        [5,6,7,8]    
])
algorithm=min_bipartite_graph_match(costEdges)
print("\n", algorithm.__call__())