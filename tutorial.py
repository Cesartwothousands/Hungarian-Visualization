"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np
from pointset import PointSet


def full_covered(matrix,rows,columns):
    for x in len(matrix):
        for y in len(matrix[0]):
            if matrix[x][y]==0:
                if x not in rows or y not in columns:
                    return False
    return True


matrix=np.array([
    [2,3,2,4],
    [4,1,5,1],
    [1,3,6,2],
    [5,6,7,8]
])

cost=0
n=len(matrix)
#Step 1 & 2
min_rows = np.amin(matrix, axis=1,keepdims=True)
matrix-=min_rows
min_cols = np.amin(matrix, axis=0,keepdims=True)
matrix-=min_cols
print(matrix)
##!! check the covered column and covered rows, should they use x or y?

#Step 3
#All zeros in the matrix must be covered by marking as few rows and/or columns as possible

#assign as many as possible
assigned_rows=set()
assigned_colums=set()
# hashmap x->y
starred_point=PointSet()
covered_colums=set()
covered_row=set()
primed_point=PointSet()
find=False
while not find:
    for x in range(n):
        for y in range(n):
            if matrix[x][y]==0 and x not in assigned_rows and y not in assigned_colums:
                assigned_rows.add(x)
                assigned_colums.add(y)
                starred_point.add_point((x,y))
                covered_colums.add(y)
                break
    #check if it is full covered
    if full_covered(matrix,covered_row,covered_colums):
        break
    #find a non-converted zero and prime it 
    # if the zero is on the same row as the starred zero,cover the corresponding row and uncover the column of
    # the starred zero
    for x in range(n):
        for y in range(n):
            if matrix[x][y]==0 and x not in covered_row and y not in covered_colums:
                #prime it
                primed_point.add_point((x,y))
                if x in starred_point:
                    #uncover the column
                    covered_colums.remove(starred_point[x])
                    #cover the row
                    covered_row.add(x)
                    #check if it is full covered
                    if full_covered(matrix,covered_row,covered_colums):
                        ## change the flag to break
                        find=True
                        break
                else:
                    px=x
                    py=y
                    primed_on_path=PointSet()
                    starred_on_path=PointSet()
                    primed_on_path.add_point((px,py))
                    while True:
                        #step1
                        #find a starred zero on column
                        if starred_point.contains_y(py):
                            px,_=starred_point.get_by_y(py)
                            starred_on_path.add_point((px,py))
                        else:        
                            break
                        #step2
                        #find a primed zero on row
                        _,py=primed_point.get_by_x(px)
                        primed_on_path.add_point((px,py))
                    #star all prime zero and remove all covered lines and prime zeros
                    covered_row=set()
                    covered_colums=set()
                    starred_point=primed_on_path()
                    #cover the columns of all prime zero
                    for px,py in starred_point:
                        covered_colums.add(y)

#Step 4
# for the left values, find the lowest , subtract from every unmarked element and add to every 
# element covered by two lines
if len(covered_row)+len(covered_colums)==n:
    #find the result
    pass
min=matrix.max()
for x in range(n):
    for y in range(n):
        if x not in covered_row and y not in covered_colums:
            min=min(min,matrix[x][y])

for x in range(n):
    for y in range(n):
        if x not in covered_row and y not in covered_colums:
            matrix[x][y]-=min
        if x in covered_row and y in covered_colums:
            matrix[x][y]+=min
