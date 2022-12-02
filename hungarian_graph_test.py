import numpy as np
from hungarian_graph import hungarian_graph

costEdges=np.array([
    [2,3,2,4],
    [4,1,5,1],
    [1,3,6,2],
    [5,6,7,8]
])
algorithm=hungarian_graph(costEdges)
print("\n", algorithm.calculate())
