import numpy as np
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
from n3GraphSolution import min_bipartite_graph_match


costEdges=np.random.randint(0,2,(3,3))
print("\n", costEdges)

algorithm=min_bipartite_graph_match(costEdges)
print("\nAnswer:", algorithm.__call__())

algorithm=AdjacencyMatrixHungarian(costEdges)
result=algorithm.calculate()
print("\nOptimal result")
print(result)
