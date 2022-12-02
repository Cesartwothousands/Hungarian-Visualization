import numpy as np

class hungarian_graph:
    def __init__(self, costEdges):
        self.costEdges=costEdges
        
        if costEdges.shape[0]!=costEdges.shape[1]:
            raise Exception("Cost Edges must be n X n")
        
        self.n=costEdges.shape[0]

    def calculate(self):
        # init labels and matches
        self.labels_X=np.zeros((self.n,1))
        self.labels_Y=np.zeros((self.n,1))
        
        for i in range(self.n):
            self.labels_Y[i]=(self.costEdges.min(0))[i]
        
        equalityGraph=self.getEqualityGraph()
        
        matches=[]

        iter=1
        while True:
            print("\n################## "+str(iter)+" #################")
            iter+=1
            
            print("Searching augmenting path...")
            (existAugPath, path, S, T)=self.searchAugPath(matches,equalityGraph)
            
            if existAugPath: 
            #If there's augment path, we can extend the matches
                print("Find augmenting path, extending matches")
                
                matches=self.invert(path,matches)
                print("Current matches :")
                print(matches)
                
                if len(matches)==self.n:
                #Judge whether it's a perfect matching
                    break
                
            else:
                print("Can't find augmenting path, updating labels")
                print("\nCurrent matches :")
                print(matches)
                theta=self.getLabelTheta(S,T)
                self.updateLabels(theta,S,T)
                equalityGraph=self.getEqualityGraph()
        
        return matches
                
    def updateLabels(self, theta, S, T):
        for i in range(self.n):
            if i in S:
                self.labels_X[i]=self.labels_X[i]+theta
        for j in range(self.n):
            if j in T:
                self.labels_Y[j]=self.labels_Y[j]-theta

    def getLabelTheta(self, S, T):
        theta=float('inf')
        for i in range(self.n):
            for j in range(self.n):
                if (i in S) and (j not in T):
                    delta=self.costEdges[i,j]-self.labels_X[i]-self.labels_Y[j]
                    
                    if theta>delta:
                        theta=delta
        return theta

    def getEqualityGraph(self):
        # equalityGraph just descrip whether x and y exist edge
        equalityGraph=np.zeros((self.n,self.n))
        for i in range(self.n):
            for j in range(self.n):
                if self.labels_X[i]+self.labels_Y[j]==self.costEdges[i,j]:
                    equalityGraph[i,j]=1
                else:
                    equalityGraph[i,j]=0
        return equalityGraph

    def searchAugPath(self,matches,equalityGraph):
        #Create direct graph
        #directMatrix[i,j]=1 : x_i -> y_j
        totalVertexN=self.n+self.n+2 # node_0 is start node , node_totalVertexN-1 is end node
        directMatrix=np.zeros((totalVertexN,totalVertexN))
        
        for i in range(0,totalVertexN-1):
            for j in range(0,totalVertexN):
                if i==0 and j>=1 and j<=self.n:
                    directMatrix[i,j]=1
                    continue
                
                if j==totalVertexN-1 and i>self.n:
                    directMatrix[i,j]=1
                    continue
                
                if i==j or i==0 or j==0 or j==totalVertexN-1:
                    continue
                
                iIsX=False
                jIsX=False
                
                if i>0 and i<=self.n:
                    iIsX=True
                elif i>self.n and i<=totalVertexN-2:
                    iIsX=False
                    
                if j>0 and j<=self.n:
                    jIsX=True    
                elif j>self.n and j<=totalVertexN-2:
                    jIsX=False
                    
                if iIsX and jIsX==False:
                    directMatrix[i,j]=equalityGraph[i-1,j-1-self.n]
                    
        for (x,y) in matches:
            directMatrix[x+1,y+1+self.n]=0
            directMatrix[y+1+self.n,x+1]=1
            
        for j in range(1, self.n+1):
            isMatched=False
            for k in range(self.n, totalVertexN-1):
                if directMatrix[k][j]==1:
                    isMatched=True
                    break
            if isMatched:
                directMatrix[0][j]=0
                
        for i in range(self.n, totalVertexN-1):
            isMatched=False
            for k in range(1, self.n+1):
                if directMatrix[i][k]==1:
                    isMatched=True
                    break
            if isMatched:
                directMatrix[i][totalVertexN-1]=0

        (shortestRoute, longestRoute)=self.findRoute(directMatrix,[0],[],[])
        # shortestRoute represents augmenting path
        # If shortestRoute doesn't exist, longestRoute represents the max alternating path
        if len(shortestRoute)>0:
            augmentPath=[]
            for i in range(1,len(shortestRoute)-2):
                vertexIndex_A=shortestRoute[i]
                actualIndex_A=0
                vertexIsX_A=False
                if vertexIndex_A>=1 and vertexIndex_A<=self.n:
                    actualIndex_A=vertexIndex_A-1
                    vertexIsX_A=True
                else:
                    actualIndex_A=vertexIndex_A-1-self.n

                vertexIndex_B=shortestRoute[i+1]
                actualIndex_B=0
                vertexIsX_B=False
                
                if vertexIndex_B>=1 and vertexIndex_B<=self.n:
                    actualIndex_B=vertexIndex_B-1
                    vertexIsX_B=True
                else:
                    actualIndex_B=vertexIndex_B-1-self.n
                
                augmentPath.append((actualIndex_A,actualIndex_B,vertexIsX_A))
            return (True, augmentPath, None, None)
        
        else: 
            S=[]
            T=[]
            alternatingPath=[]
            for i in range(1,len(longestRoute)):
                vertexIndex=longestRoute[i]
                actualIndex=0
                vertexIsX=False
                if vertexIndex>=1 and vertexIndex<=self.n:
                    actualIndex=vertexIndex-1
                    vertexIsX=True
                else:
                    actualIndex=vertexIndex-1-self.n
                if vertexIsX:
                    S.append(actualIndex)
                else:
                    T.append(actualIndex)
            return (False, None, S, T)
            
    def findRoute(self, directMatrix, currentRoute, currentShortestRoute, currentLongestRoute):
        if len(currentLongestRoute)==0 or len(currentLongestRoute)<len(currentRoute):
            currentLongestRoute=currentRoute.copy()
        if currentRoute[-1]==directMatrix.shape[0]-1:
            if len(currentShortestRoute)==0 or len(currentShortestRoute)>len(currentRoute):
                currentShortestRoute=currentRoute.copy()
            return (currentShortestRoute, currentLongestRoute)
        for i in range(0,directMatrix.shape[0]):
            if directMatrix[currentRoute[-1],i]==1:
                nextRoute=currentRoute.copy()
                nextRoute.append(i)
                (route1, route2)=self.findRoute(directMatrix, nextRoute,currentShortestRoute, currentLongestRoute)
                if len(currentShortestRoute)==0 or len(currentShortestRoute)>len(route1):
                    currentShortestRoute=route1.copy()
                if len(currentLongestRoute)==0 or len(currentLongestRoute)<len(route2):
                    currentLongestRoute=route2.copy()
        return (currentShortestRoute, currentLongestRoute)

    def invert(self, augPath, matches):
        for i in range(len(augPath)):
            if i%2==0:
                if augPath[i][2]:
                    matches.append((augPath[i][0],augPath[i][1]))
                else:
                    matches.append((augPath[i][1],augPath[i][0]))
            else:
                removeIndex=-1
                for index in range(len(matches)):
                    if (matches[index][0]==augPath[i][0] and matches[index][1]==augPath[i][1]) or (matches[index][0]==augPath[i][1] and matches[index][1]==augPath[i][0]):
                        removeIndex=index
                        break
                matches.pop(removeIndex)
        return matches
    
