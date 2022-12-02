import numpy as np
"""
#1st input 
mat= np.array(([9,11,14,11,7],[6,15,13,13,10],[12,13,6,8,8],[11,9,10,12,9],[7,12,14,10,14]))
mat1= np.array(([9,11,14,11,7],[6,15,13,13,10],[12,13,6,8,8],[11,9,10,12,9],[7,12,14,10,14]))
n=m=5
"""
#2 nd input
mat=np.array(([82,	83,	69,	92],
           	[77,	37,	49,	92],
		[11,	69,	5,	86],
		[8,	9,	98,	23]
))
mat1=np.array(([82,	83,	69,	92],
           	[77,	37,	49,	92],
		[11,	69,	5,	86],
		[8,	9,	98,	23]
))

n=4
m=4
"""
#input 3
mat=np.array((
[250, 400, 350],
[400, 600, 350],
[200, 400, 250]
))
mat1=np.array((
[250, 400, 350],
[400, 600, 350],
[200, 400, 250]
))
n=3
m=3
"""
print(" Cost Matrix")
print(mat)
for i in range(n):
	temp=mat[i][:]
	mi=min(temp)
	for j in range(m):
		mat[i][j]-=mi
print("Updated cost matrix after row operation ")
print(mat)		

for j in range(m):
	mi=float("inf")
	for i in range(m):
		mi=min(mi,mat[i][j])
	for i in range(n):
		mat[i][j]-=mi
		
print("Updated cost matrix after col operation ")
print(mat)
tell=0
while(1):
	count=0
	visited=np.zeros((n,m)) 
	for i in range(n):
		c=0
		for j in range(m):
			if(mat[i][j]==0):
				c+=1
		if(c>1):
			for j in range(m):
				visited[i][j]+=1
			count+=1	
				
				
				
	for j in range(m):
		c=0
		for i in range(m):
			if(mat[i][j]==0 and visited[i][j]==0):
				c+=1
		if(c>1):
			for i in range(n):
				visited[i][j]+=1
			count+=1	
	
	for j in range(n):
		for i in range(n):
			if(mat[i][j]==0 and visited[i][j]==0):
				count+=1
				for k in range(n):
					visited[k][j]+=1
				
	for i in range(n):
		for j in range(n):
			if(mat[i][j]==0 and visited[i][j]==0):
				count+=1
				for k in range(n):
					visited[i][k]+=1				

	print("count of no of lines ",count)
	if(count>=n):
		print("Count of no of lines is greater equal to required ")
		print("Optimal condition reached ")
		break
	ma=float("inf")	
	for i in range(n):
		for j in range(n):
			if(visited[i][j]!=0):
				continue
			e=mat[i][j]
			ma=min(ma,e)
	print(" Minimum no to substract to the uncovered cost and to be added to intersected cost",ma)		
	for i in range(n):
		for j in range(m):
			if(visited[i][j]==0):
				mat[i][j]-=ma
			elif(visited[i][j]>1):
				mat[i][j]+=ma	
	
	print("Updated cost matrix",mat)
								
		
	
res=0
machine=np.zeros(n)
job=arr = np.zeros(m)	
for i in range(n):
		c=0
		for j in range(m):
			if(mat[i][j]==0):
				c+=1
	
		if(c==1):
			machine[i]=1
			for j in range(m):
				if(mat[i][j]==0):
					job[j]=1
					res+=mat1[i][j]
					print("Assigned worker ",i+1," to  job ",j+1) 
					break
					
for i in range(n):
	if(machine[i]==0):
		for j in range(n):
			if(mat[i][j]==0 and job[j]==0):
				res+=mat1[i][j]
				print("Assigned worker ",i+1," to  job ",j+1) 
				job[j]=1
				break					
		
			
print("The total cost of this optimal assignment is",res)	
