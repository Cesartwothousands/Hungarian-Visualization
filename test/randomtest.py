import sys
import os
sys.path.insert(0, os.getcwd())
import numpy as np
from algorithm import AdjacencyMatrixHungarian
from algorithm.AdjacencyMatrixHungarian import AdjacencyMatrixHungarian
from algorithm.N4Review import min
from algorithm.hungarian import Hungarian

# random test on different implementations

N3 = 0
N4 = 1
HUN = 2

flags = [N4, HUN]
erro_count=0
for flag in flags:
    for i in range(1000):

        costEdges = np.random.randint(5, 15, (6, 6))
        matrix = costEdges.copy()
        # print("\n", costEdges)
        # print(matrix)
        if flag == N4:
            algorithm = min(costEdges)
            val = algorithm.__call__()
        elif flag == HUN:
            algorithm = Hungarian(costEdges)
            result = algorithm.calculate()
            val = 0
            for x, y in result:
                val += int(matrix[x][y])
        # print("\nAnswer:", val)

        algorithm = AdjacencyMatrixHungarian(costEdges)
        result = algorithm.calculate()
        # print("\nOptimal result")
        # print(result)
        sum = 0
        for x, y in result:
            sum += int(matrix[x][y])
        # print(sum)
        if sum != val:
            erro_count+=1
            print("neq")
            print(sum)
            print(val)
            print(matrix)
print(f"finish with {erro_count} errors.")
