# -*- coding: utf-8 -*-
import re

#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
# part ii optimized
#-----------------------------------------------------------------------------#

test = True
steps = 6

if test:
    with open("input6thtest.txt", "r") as file :
        lines = file.readlines()

else : 
    with open("input6th.txt", 'r') as file :
        lines = file.readlines()
    steps = 64
    
ROWLEN=len(lines)
COLLEN=len(lines[0])-1

#find rocks
pr=re.compile('#')
rocksLoc=[]

#find start
ps=re.compile('S')
startLoc=[]

#find gear symbol
pg=re.compile('\.')
gardenLoc=[]

def checkRock(a) :
    return 0 if a == '#' else 1
def checkStart(a) :
    return 1 if a == 'S' else 0


gardenMatrixFilter = []
for i, line in enumerate(lines) :
    mappedLine = list(map(checkRock, line))
    gardenMatrixFilter.append(mappedLine[:-1])
MAX_ROWS = len(gardenMatrixFilter)-1
MAX_COLUMNS = len(gardenMatrixFilter[0])-1


''' 
        
gardenMatrixTransform = []
for y, row in enumerate(gardenMatrixFilter) :
    print(f'Checking {y}, {row}')
    matrixTransformRow = []
    for x, column in enumerate(row) :
        print(f'Checking ({x}, {y}), {column}')
        nextX = x+1 if x < MAX_COLUMNS else 0
        nextY = y+1 if y < MAX_ROWS else 0
        transformXY = [gardenMatrix[x-1][y], gardenMatrix[nextX][y], gardenMatrix[x][y-1], gardenMatrix[x][nextY]]
        matrixTransformRow.append(transformXY)
    gardenMatrixTransform.append(matrixTransformRow)
''' 
''' def shiftLeft(a) :
    return a[1:]+[False]

def shiftRight(a) :
    return [False] + a[:-1]

def shiftUp(a) :
    return a[1:] + [[False]*len(a[0])]
    
def shiftDown(a) :
    return [[False]*len(a[0])] + a[:-1] 
'''

import numpy as np

matrixDict = {}
cursorMatrix=[]
for i, line in enumerate(lines) :
    mappedLine = list(map(checkStart, line))
    cursorMatrix.append(mappedLine[:-1])


cursorMatrix = np.array(cursorMatrix)
matrixDict[(0,0)] = cursorMatrix

cursorCache={} 

steps = 500
for step in range(steps) :
    #print(f'-------------------------------------------------------------------')
    print(f"Running step {step+1}")


    curItems = list(matrixDict.items())
    for key, cursorMatrix in curItems :
        #print(f'Processing {cursorMatrix} on map {key}')
        hcm = hash(str(cursorMatrix))
        if hcm in cursorCache :
            print(f'Cache hit: {key}')
            newCursorMatrix = cursorCache[hcm]
        else :    
            newCursorMatrix = (np.roll(cursorMatrix, 1, axis=1) +
                                           np.roll(cursorMatrix, -1, axis=1) + 
                                           np.roll(cursorMatrix, 1, axis=0) +  
                                           np.roll(cursorMatrix, -1, axis=0))
        
            #removing roll effect
            newCursorMatrix[MAX_ROWS] -= cursorMatrix[0]
            newCursorMatrix[0] -= cursorMatrix[MAX_ROWS]
            newCursorMatrix[:,0] -= cursorMatrix[:,MAX_COLUMNS]
            newCursorMatrix[:,MAX_COLUMNS] -= cursorMatrix[:,0]
            
            newCursorMatrix = 1*np.logical_and(gardenMatrixFilter, newCursorMatrix)
            cursorCache[hcm] = newCursorMatrix
        cursorMatrix = newCursorMatrix
        matrixDict[key] = cursorMatrix

    for key, cursorMatrix in curItems :
        #Processing step towards other maps
        if sum(cursorMatrix[0]) > 0 :
            northBound = matrixDict.setdefault((key[0], key[1]+1), np.zeros([MAX_ROWS+1,MAX_COLUMNS+1], dtype=int))    
            northBound[MAX_ROWS] += cursorMatrix[0]
            northBound = 1*np.logical_and(gardenMatrixFilter, northBound)
            matrixDict[(key[0], key[1]+1)] = northBound
            #
        
        if sum(cursorMatrix[MAX_ROWS]) > 0 :
            southBound = matrixDict.setdefault((key[0], key[1]-1), np.zeros([MAX_ROWS+1,MAX_COLUMNS+1], dtype=int))    
            southBound[0] += cursorMatrix[MAX_ROWS]    
            southBound = 1*np.logical_and(gardenMatrixFilter, southBound)
            matrixDict[(key[0], key[1]-1)] = southBound
            
        if np.sum(cursorMatrix, axis=0)[0] > 0 :
            #print("\n\nGetting WestBound!")
            westBound = matrixDict.setdefault((key[0]-1, key[1]), np.zeros([MAX_ROWS+1,MAX_COLUMNS+1], dtype=int))    
            westBound[:,MAX_COLUMNS] += cursorMatrix[:,0]
            #print(f'\n\nwestBound: {westBound}')
            #print(f'\n\ncursorMatrix[0]: {cursorMatrix[:,0]}')
            #print(f'\n\ncursorMatrix[MaX]: {cursorMatrix[:,MAX_COLUMNS]}')
            westBound = 1*np.logical_and(gardenMatrixFilter, westBound)
            matrixDict[(key[0]-1, key[1])] = westBound
        
        if np.sum(cursorMatrix, axis=0)[MAX_COLUMNS] > 0 :
            eastBound = matrixDict.setdefault((key[0]+1, key[1]), np.zeros([MAX_ROWS+1,MAX_COLUMNS+1], dtype=int))    
            eastBound[:,0] += cursorMatrix[:,MAX_COLUMNS]
            eastBound = 1*np.logical_and(gardenMatrixFilter, eastBound)
            matrixDict[(key[0]+1, key[1])] = eastBound
            #

        #print(f'updated: {key} : {cursorMatrix}')
        #print(f'Sum for processed:  {np.sum(cursorMatrix)}')    
        #print(f'matrices keys: {matrixDict.keys()}')
    #print(f'\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    if step+1 in [6, 10, 50, 100, 500, 1000] :
        print(f'all matrices sum after {step+1}: {sum(np.sum(x) for x in matrixDict.values())}')
    #print(f'{matrixDict}')
    
    