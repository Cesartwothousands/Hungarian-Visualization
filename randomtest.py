import numpy as np
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
from test import max_bipartite_graph_match


costEdges=np.random.randint(0,5,(2,2))
print("\n", costEdges)

algorithm=max_bipartite_graph_match(costEdges)
print("\nAnswer:", algorithm.__call__())

algorithm=AdjacencyMatrixHungarian(costEdges)
result=algorithm.calculate()
print("\nOptimal result")
print(result)
