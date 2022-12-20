import sys
import os
sys.path.insert(0, os.getcwd())
import numpy as np
import time
from algorithm.n4 import min as n4min
from algorithm.n3 import min as n3min

# Time test on different implementations

N3=0
N4=1

flags=[N4, N3]

for flag in flags:
    
    n = 100000
    time_start = time.time()
    for i in range(n):
        
        costEdges=np.random.randint(5,15,(16,16))
        matrix=costEdges.copy()
        #print("\n", costEdges)
        #print(matrix)
        if flag==N4:
            algorithm=n4min(costEdges)
            val=algorithm.__call__()
        elif flag==N3:
            algorithm=n3min(costEdges)
            val=algorithm.__call__()
        #print("\nAnswer:", val)
        
        if i == n-1:
            time_end = time.time()
            print(flag, " is: ",time_end - time_start)
