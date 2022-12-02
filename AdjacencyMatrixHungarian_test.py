import numpy as np
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian


costEdges=np.array([
    [2,3,2,4],
    [4,1,5,1],
    [1,3,6,2],
    [5,6,7,8]
])
algorithm=AdjacencyMatrixHungarian(costEdges)
result=algorithm.calculate()
print("Optimal result")
print(result)
