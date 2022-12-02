import numpy as np

class AdjacencyMatrixHungarian:
    def __init__(self, costEdges):
        self.costEdges=costEdges
        if costEdges.shape[0]!=costEdges.shape[1]:
            self.handleUnbalance()
        self.n=self.costEdges.shape[0]
    
    def handleUnbalance(self):
        m=self.costEdges.shape[0]
        n=self.costEdges.shape[1]
        if(m<n):
                dummy_row=np.zeros((1,n))
                self.costEdges=np.vstack((self.costEdges,dummy_row))
        elif(m>n):
                dummy_column=np.zeros((m,1))
                self.costEdges=np.hstack((self.costEdges,dummy_column))

    def calculate(self):
        self.rowReduction()
        self.columnReduction()
        print("Cost matrix after row and column reduction")
        print(self.costEdges)
        (coverRows,coverColumns,independentZeros)=self.findMinCoverLines()
        n1=len(coverRows)+len(coverColumns)
        while n1!=self.n:
            print("Haven't reach optimal, start iterate reduction")
            self.costEdges=self.iterateReduction(coverRows,coverColumns)
            print("Cost matrix after iterate reduction")
            print(self.costEdges)
            (coverRows,coverColumns,independentZeros)=self.findMinCoverLines()
            n1=len(coverRows)+len(coverColumns)
        return independentZeros

    def rowReduction(self):
        for i in range(self.n):
            minValue=self.costEdges[i].min()
            for j in range(self.n):
                self.costEdges[i,j]=self.costEdges[i,j]-minValue

    def columnReduction(self):
        for j in range(self.n):
            minValue=self.costEdges[:,j].min()
            for i in range(self.n):
                self.costEdges[i,j]=self.costEdges[i,j]-minValue
    
    def iterateReduction(self, coverRows, coverColumns):
        minValue=float('inf')
        for i in range(self.n):
            for j in range(self.n):
                if i in coverRows or j in coverColumns:
                    continue
                if self.costEdges[i,j]<minValue:
                    minValue=self.costEdges[i,j]
        for i in range(self.n):
            if i in coverRows:
                continue
            for j in range(self.n):
                self.costEdges[i,j]-=minValue
        for j in range(self.n):
            if j in coverColumns:
                for i in range(self.n):
                    self.costEdges[i,j]+=minValue
        return self.costEdges

    def findMinCoverLines(self):
        starMarks=np.zeros((self.n,self.n))
        primeMarks=np.zeros((self.n,self.n))
        coverRows=[]
        coverColumns=[]
        for i in range(self.n):
            for j in range(self.n):
                if self.costEdges[i,j]!=0:
                    continue
                existStarZeroThisRow=False
                for k in range(self.n):
                    if starMarks[i,k]==1:
                        existStarZeroThisRow=True
                        break
                existStarZeroThisColumn=False
                for l in range(self.n):
                    if starMarks[l,j]==1:
                        existStarZeroThisColumn=True
                        break
                if not existStarZeroThisRow and not existStarZeroThisColumn:
                    starMarks[i,j]=1
                    coverColumns.append(j)

        while True:
            uncoverZeroCounter=0
            for i in range(self.n):
                for j in range(self.n):
                    if self.costEdges[i,j]!=0:
                        continue
                    if i in coverRows or j in coverColumns:
                        continue
                    uncoverZeroCounter+=1
                    primeMarks[i,j]=1
                    noStarZeroThisRow=True
                    for k in range(self.n):
                        if starMarks[i,k]==1:
                            coverColumns.remove(k)
                            coverRows.append(i)
                            noStarZeroThisRow=False
                            break
                    if not noStarZeroThisRow:
                        continue
                    else:
                        sequence=self.findAugmentSequence(starMarks, primeMarks, [(i,j)])
                        for k in range(len(sequence)):
                            if k%2==0:
                                primeMarks[sequence[k][0],sequence[k][1]]=0
                                starMarks[sequence[k][0],sequence[k][1]]=1
                            else:
                                starMarks[sequence[k][0],sequence[k][1]]=0
                        primeMarks[:,:]=0
                        coverRows=[]
                        coverColumns=[]
                        for j in range(self.n):
                            for i in range(self.n):
                                if starMarks[i,j]==1:
                                    coverColumns.append(j)
                                    continue

            if uncoverZeroCounter==0:
                break
        independentZeros=[]
        for i in range(self.n):
            for j in range(self.n):
                if starMarks[i,j]==1:
                    independentZeros.append((i,j))
        return (coverRows,coverColumns,independentZeros)

    def findAugmentSequence(self, starMarks, primeMarks, sequence):
        if primeMarks[sequence[-1][0],sequence[-1][1]]==1:
            for i in range(self.n):
                if starMarks[i,sequence[-1][1]]==1:
                    sequence.append((i,sequence[-1][1]))
                    return self.findAugmentSequence(starMarks,primeMarks,sequence)
            return sequence
        elif starMarks[sequence[-1][0],sequence[-1][1]]==1:
            for j in range(self.n):
                if primeMarks[sequence[-1][0],j]==1:
                    sequence.append((sequence[-1][0],j))
                    return self.findAugmentSequence(starMarks,primeMarks,sequence)
            return sequence
                