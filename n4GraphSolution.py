import numpy as np

# n^4 Graph implemenation of Hungarian algorithm

class min_bipartite_graph_match(object):
 
    def __init__(self,graph):
        self.delta = -1 
        
        self.graph = graph
        # graph
        self.n,self.m = graph.shape
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
            
            if  tmp_delta == 0:
                self.visy[y] = True
                if  self.match[y] == -1 or self.find_path(self.match[y]):
                    self.match[y] = x
                    return True
 
        return False
 
    def KM(self):
        for x in range(self.n):
            
            while True:
                self.reset_vis()
                
                if self.find_path(x): 
                    break
                
                else: 
                # update slack
                    for i in range(self.n):
                        if self.visx[i]:
                            for j in range(self.m):
                                if self.visy[j]:
                                    self.delta = min(self.delta, self.graph[i][j] - self.lx[i] - self.ly[j])

                    self.lx[self.visx] -= self.delta
                    self.ly[self.visy] += self.delta
 
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