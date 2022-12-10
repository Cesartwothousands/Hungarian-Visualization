import numpy as np
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
from n4GraphSolution import min_bipartite_graph_match
from hungarian import Hungarian

#random test on different implementations

N3=0
N4=1
HUN=2

flags=[N4,HUN]
for flag in flags:
    for i in range(1000):

        costEdges=np.random.randint(5,15,(6,6))
        matrix=costEdges.copy()
        #print("\n", costEdges)
        #print(matrix)
        if flag==N4:
            algorithm=min_bipartite_graph_match(costEdges)
            val=algorithm.__call__()
        elif flag==HUN:
            algorithm=Hungarian(costEdges)
            result=algorithm.calculate()
            val=0
            for x,y in result:
                val+=int(matrix[x][y])
        #print("\nAnswer:", val)
        
        algorithm=AdjacencyMatrixHungarian(costEdges)
        result=algorithm.calculate()
        #print("\nOptimal result")
        #print(result)
        sum=0
        for x,y in result:
            sum+=int(matrix[x][y])
        #print(sum)
        if sum!=val:
            print("neq")
            print(sum)
            print(val)
            print(matrix)
        else: print("Right!")
