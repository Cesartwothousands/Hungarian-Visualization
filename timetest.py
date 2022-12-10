import numpy as np
import time
from AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
from n4GraphSolution import min_bipartite_graph_match
#from n3GraphSolution import min_bipartite_graph_match
from N4Review import min
from hungarian import Hungarian

#time test on different implementations
'''RESULT:
1  is:  63.371477365493774
2  is:  247.23789238929749
'''

N3=0
N4=1
HUN=2

flags=[N3, N4, HUN]

for flag in flags:
    
        
    n = 1000
    time_start = time.time()
    for i in range(n):
        
        costEdges=np.random.randint(5,15,(16,16))
        matrix=costEdges.copy()
        #print("\n", costEdges)
        #print(matrix)
        if flag==N4:
            algorithm=min(costEdges)
            val=algorithm.__call__()
        elif flag==N3:
            algorithm=min_bipartite_graph_match(costEdges)
            val=algorithm.__call__()
        elif flag==HUN:
            algorithm=AdjacencyMatrixHungarian(costEdges)
            result=algorithm.calculate()
        #print("\nAnswer:", val)
        '''
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
            print(matrix)'''
        
        if i == n-1:
            time_end = time.time()
            print(flag, " is: ",time_end - time_start)
