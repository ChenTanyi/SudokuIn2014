#!/usr/bin/env python
#===============================================================================
#This is a sudoku-solver made by Chen Tanyi.
#===============================================================================
from itertools import *
from random import *

class Sudoku:
    originalBox = [[0,0,0,1,1,1,2,2,2],
                   [0,0,0,1,1,1,2,2,2],
                   [0,0,0,1,1,1,2,2,2],
                   [3,3,3,4,4,4,5,5,5],
                   [3,3,3,4,4,4,5,5,5],
                   [3,3,3,4,4,4,5,5,5],
                   [6,6,6,7,7,7,8,8,8],
                   [6,6,6,7,7,7,8,8,8],
                   [6,6,6,7,7,7,8,8,8]]
    def __init__(self,grid=[],box=[]):
        self.N = 9
        self.rating = [21,24,27,30]
        self.grid = grid
        if box == [] :
            self.box=Sudoku.originalBox
        else:
            self.box = box
        self.inverbox = {i: set() for i in xrange(9)}
        for i,row in enumerate(self.box):
            for j,flag in enumerate(row):
                self.inverbox[flag].add((i,j))
        self.X = ([("rc", rc) for rc in product(xrange(self.N), xrange(self.N))] +
                  [("rn", rn) for rn in product(xrange(self.N), xrange(1,self.N + 1))] +
                  [("cn", cn) for cn in product(xrange(self.N), xrange(1,self.N + 1))] +
                  [("bn", bn) for bn in product(xrange(self.N), xrange(1,self.N + 1))])
        self.CoverY = dict()
        for r,c,n in product(xrange(self.N),xrange(self.N),xrange(1,self.N+1)):
            b = self.box[r][c]
            self.CoverY[(r,c,n)] = [("rc",(r,c)),
                                    ("rn",(r,n)),
                                    ("cn",(c,n)),
                                    ("bn",(b,n))]
        self.check=[[False for i in xrange(9)]for j in xrange(9)]
        #-----------------------------------------------------------------------
    def solveSudoku(self,grid):
        self.CoverX = self.exactCover (self.X,self.CoverY)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    self.select(self.CoverX,self.CoverY,(i,j,n))
        tmpgrid=[[0 for i in xrange(9)] for j in xrange(9)]
        for i in xrange(9):
            for j in xrange(9):
                tmpgrid[i][j]=grid[i][j]
        for solution in self.solve(self.CoverX,self.CoverY,[]):
            for (r,c,n) in solution:
                tmpgrid[r][c] = n
            yield tmpgrid
        #-----------------------------------------------------------------------
    def exactCover(self,X,Y):
        CoverX = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                CoverX[j].add(i)
        return CoverX
        #-----------------------------------------------------------------------
    def solve(self,X,Y,solution=[]):
        if not X:
            yield list(solution)
        else:
            c = min(X,key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self.select(X,Y,r)
                for s in self.solve(X,Y,solution):
                    yield s
                self.deselect(X,Y,r,cols)
                solution.pop()
        #-----------------------------------------------------------------------
    def select(self,X,Y,r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols
        #-----------------------------------------------------------------------
    def deselect(self,X,Y,r,cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)
        #-----------------------------------------------------------------------
    def setBox(self,box):
        self.box = box
        self.inverbox = {i: set() for i in xrange(9)}
        for i,row in enumerate(self.box):
            for j,flag in enumerate(row):
                self.inverbox[flag].add((i,j))
        self.CoverY = dict()
        for r,c,n in product(xrange(self.N),xrange(self.N),xrange(1,self.N+1)):
            b = self.box[r][c]
            self.CoverY[(r,c,n)] = [("rc",(r,c)),
                                    ("rn",(r,n)),
                                    ("cn",(c,n)),
                                    ("bn",(b,n))]
        #-----------------------------------------------------------------------
    def createGrid(self):
        grid=[[0 for i in xrange(9)] for j in xrange(9)]
        row=[i for i in xrange(1,10)]
        shuffle(row)
        grid[0]=row
        n=randrange(20)
        for i,solution in enumerate(self.solveSudoku(grid)):
            if i == n :
                self.grid=solution
                return
        self.grid=solution
        #-----------------------------------------------------------------------
    def makeGrid(self,grade):
        self.Tblank = 81-randrange(3)-self.rating[grade]
        scoop=[[False for i in xrange(9)]for j in xrange(9)]
        blank = 0
        count=0
        grid=[[0 for i in xrange(9)]for j in xrange(9)]
        for i in xrange(9):
            for j in xrange(9):
                grid[i][j] = self.grid[i][j]
        while blank < self.Tblank :
            x=randrange(81)
            row=x/9
            col=x%9
            flag=False
            if not scoop[row][col]:
                number=grid[row][col]
                grid[row][col]=0
                for i in xrange(1,10):
                    if i != number:
                        if self.checkLegel(grid,row,col,i):
                          grid[row][col]=i
                          for solution in self.solveSudoku(grid):
                              flag=True
                              break
                          grid[row][col]=number
                if not flag:
                    grid[row][col]=0
                    blank+=1
                scoop[row][col]=True
                count+=1
            if count == 81:
                return False
        self.grid=grid
        return True
        #-----------------------------------------------------------------------
    def checkLegel(self,grid,row,col,num):
        for i in xrange(9):
            if grid[row][i] == num:
                return False
            if grid[i][col] == num:
                return False
        for i,j in self.inverbox[self.box[row][col]]:
            if grid[i][j] == num:
                return False
        return True
        #-----------------------------------------------------------------------
    def checkDifficulty(self,grid):
        freedom = 0
        for row in xrange(9):
            for col in xrange(9):
                if grid[row][col] == 0:
                    for i in xrange(9):
                        if i != row and grid[i][col] == 0:
                            freedom += 1
                        if i != col and grid[row][col] == 0:
                            freedom += 1
                    for i,j in self.inverbox[self.box[row][col]]:
                        if grid[i][j] == 0:
                            freedom += 1
        return freedom
        #-----------------------------------------------------------------------
    def setGrid(self,grid):
        self.grid=grid
        #-----------------------------------------------------------------------
    def updateCheck(self):
        rowC,colC,boxC=[0 for i in xrange(9)],[0 for i in xrange(9)],[0 for i in xrange(9)]
        for row in xrange(9):
            for col in xrange(9):
              if self.grid[row][col] != 0:
                number = 1 << (self.grid[row][col]*2 - 1 )
                if rowC[row] & number == 0:
                    rowC[row] += number >> 1
                if colC[col] & number == 0:
                    colC[col] += number >> 1
                if boxC[self.box[row][col]] & number ==0:
                    boxC[self.box[row][col]] += number >> 1
        for row in xrange(9):
            for col in xrange(9):
              if self.grid[row][col] != 0:
                number = 1<<(self.grid[row][col]*2-1)
                if rowC[row] & number != 0:
                    self.check[row][col] = True
                elif colC[col] & number != 0:
                    self.check[row][col] = True
                elif boxC[self.box[row][col]] & number != 0:
                    self.check[row][col] = True
                else:self.check[row][col] = False
            

if __name__ == "__main__":
    grid=[]
    print "Please enter a solving sudoku:"
    for i in xrange(9):
      row=raw_input()
      while row[-1] == ' ':
          row = row [:-1]
      row=row.split(" ")
      grid.append(map(int,row))
      '''[[0, 7, 0, 0, 0, 4, 3, 0, 0],
          [0, 0, 1, 0, 0, 0, 0, 0, 2],
          [4, 0, 9, 2, 6, 0, 0, 0, 0],
          [2, 0, 0, 6, 5, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0],
          [0, 0, 0, 3, 8, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 2, 0],
          [0, 0, 0, 0, 0, 0, 8, 3, 6],
          [0, 0, 3, 0, 0, 9, 0, 7, 4]]'''
    sudoku=Sudoku(grid)
    for solution in  sudoku.solveSudoku(grid):
        print "\nThe solution is :"
        for i in xrange(9):
            for j in xrange(9):
                print solution[i][j],
            print
    
