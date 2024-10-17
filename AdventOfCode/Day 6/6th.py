# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:00:21 2024

@author: CTW00905
"""

# -*- coding: utf-8 -*-
import re

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



for i, line in enumerate(lines) :
    for m in pr.finditer(line) :
        rocksLoc.append((m.start(),i))
    for m in ps.finditer(line) :
        startLoc.append((m.start(),i))
    for m in pg.finditer(line) :
        gardenLoc.append((m.start(), i))

if len(startLoc) > 1 :
    print(f'Whattt? startLoc with more than one location: {startLoc} ')

    
def moveCursor(cursors) :
    newPositions = []

    for cursor in cursors :
        x, y, z = cursor        
        north = (x, y+1)
        if north not in rocksLoc and y+1 < ROWLEN : newPositions.append(north) 
        south = (x, y-1)
        if south not in rocksLoc and y-1 >= 0 : newPositions.append(south)
        west = (x-1, y)
        if west not in rocksLoc and x-1 >= 0 : newPositions.append(west) 
        east = (x+1, y)
        if east not in rocksLoc and x+1 < COLLEN : newPositions.append(east)
        
    return set(newPositions)
        
def printPositions(cursors) :    
    for y in range(ROWLEN) :
        row = ""
        for x in range(COLLEN) :
            if (x,y) in rocksLoc :
                row += "#"
                continue
            if (x,y) in cursors :
                row += "O"
                continue
            row += "."
        print(row)


    
''' 
cursors = startLoc + [0,0,0,0]
for i in range(steps) :
    cursors = moveCursor(cursors)
    print(f"On step {i} we reached : {len(cursors)}")
    #printPositions(cursors)
    
''' 

#----------------------------------------------------------------------------#
# Part ii
# 
#----------------------------------------------------------------------------#            
class Garden :
    def __init__(self, position) :
        self.x, self.y = position
        self.position = position
        self.north = None
        self.east = None
        self.west = None
        self.south = None
        self.northNewMap = False
        self.eastNewMap = False
        self.westNewMap = False
        self.southNewMap = False
        
    def getGardenLoc(self) :
        return tuple(self.position)
    def getPosition(self) :
        return tuple(self.position)
    
    def getDirection(self,direction) :
        if direction == 'south' :
            return self.getSouth()
        if direction == 'north' :
            return self.getNorth()
        if direction == 'west' :
            return self.getWest()
        if direction == 'east' :
            return self.getEast()
        
    
    def addNorth(self,garden) :
        self.north = garden
        if abs(self.y - self.north.y) > 1 :
            self.northNewMap = True
    def addEast(self,garden) :
        self.east = garden
        if abs(self.x - self.east.x) > 1 :
            self.eastNewMap = True
    def addWest(self,garden) :
        self.west = garden
        if abs(self.x - self.west.x) > 1 :
            self.westNewMap = True
    def addSouth(self,garden) :
        self.south = garden
        if abs(self.y - self.south.y) > 1 :
            self.southNewMap = True
    def getNorth(self) :
        if self.north is not None:
            return (self.north, self.northNewMap)
        return (None, None)
    def getSouth(self) :
        if self.south is not None:
            return (self.south, self.southNewMap)
        return (None, None)
    def getEast(self) :
        if self.east is not None:
            return (self.east, self.eastNewMap)
        return (None, None)
    def getWest(self) :
        if self.west is not None:
            return (self.west, self.westNewMap)
        return (None, None)
    
   #def __str__(self) :
        return (f'Garden in: ({self.position})')
        
    def __repr__(self) :
        return (f'Garden in: ({self.position})')
        
        
gardenMap = {}        
def buildMap() :    
    for y in range(ROWLEN) :
        for x in range(COLLEN) :
            if (x,y) not in rocksLoc :
                gardenMap[(x,y)] = Garden((x,y))
    
    for y in range(ROWLEN) :
        for x in range(COLLEN) :
            if (x,y) in rocksLoc :
                continue
            north = (x, y+1) if y+1 < ROWLEN else (x,0)                
            east = (x+1, y) if x+1 < COLLEN else (0, y)
            south = (x, y-1) if y-1 >= 0 else (x, ROWLEN-1)
            west = (x-1, y) if x-1 >= 0 else ( COLLEN-1, y)
            if north in gardenMap :
                gardenMap[(x,y)].addNorth(gardenMap[north])
            if south in gardenMap :
                gardenMap[(x,y)].addSouth(gardenMap[south])
            if east in gardenMap :
                gardenMap[(x,y)].addEast(gardenMap[east])
            if west in gardenMap :
                gardenMap[(x,y)].addWest(gardenMap[west])


def transverseMap(cursorList) :
    nextCursors = []
    #print(f'Current Cursors: {cursors}')
    for cursor in cursorList :
        south = cursor.goDirection('south')
        east = cursor.goDirection('east')
        north = cursor.goDirection('north')
        west = cursor.goDirection('west')
        
        
        nextCursors += [south] if south is not None  else []
        nextCursors += [west] if west is not None else []
        nextCursors += [east] if east is not None  else []
        nextCursors += [north] if north is not None   else []

    return set(nextCursors) 

maps = {}
class CursorMap() :
    def __init__(self, x=0, y=0) : #north=0, south=0, east=0, west=0) :
        #self.pos = [north, south, east, west]
        self.pos = [x, y]
    
    def getPosition(self) :
        return tuple(self.pos)
        
    def getMap(self,direction=None) :
        x = self.pos[0]
        y = self.pos[1]
        #east = self.pos[2]
        #west = self.pos[3]
        if direction == 'north' :
            y = self.pos[1] + 1
        if direction == 'south' :
            y = self.pos[1] - 1
        if direction == 'east' :
            x = self.pos[0] + 1
        if direction == 'west' :
            x = self.pos[0] - 1
        
        key = (x,y)
        if key in maps :
            return maps[key]
        else :
            newMap = CursorMap(*key)            
            maps[key] = newMap
            return newMap
    
    def getMapLoc(self) :
        return self.position
    
    def __repr__(self) :
        return f'| Cursor map: [{self.pos}]'
    
    def __hash__(self) :
        return hash(self.__repr_())

cursors = {}
class Cursor() :
    def __init__(self, garden, cursorMap) :
        self.cursorMap = cursorMap
        self.cursorGarden = garden
    
    def getGardenPosition(self) :
        return tuple(self.cursorGarden.getPosition())

    def getMapPosition(self) :
        return tuple(self.cursorMap.getPosition())
    
    ''' 
    def step(self) :
        nextCursors = []
        for direction in ['south', 'north', 'east', 'west'] :
            nextCursors.append(self.goDirection(direction))
        return nextCursors
    ''' 
    
    def goDirection(self, direction) :
        #print(f'Going in direction {direction} from garden {self.cursorGarden}')
        nextGarden, z = self.cursorGarden.getDirection(direction)
        if nextGarden == None:
            #print(f'No Garden in that direction :( {nextGarden}')
            return None
        
        nextMap = self.cursorMap
        if z == True :
            nextMap = self.cursorMap.getMap(direction)
        
            
        if nextMap.getPosition() not in cursors :
            cursors[nextMap.getPosition()] = {}
                
        
        if nextGarden.getPosition() not in cursors[nextMap.getPosition()]:
            newCursor = Cursor(nextGarden, nextMap)
            cursors[newCursor.getMapPosition()][newCursor.getGardenPosition()] = newCursor
        
        #print(f'Returning Cursor for {direction} from {self.getGardenPosition()} to {self.newCursor.getGardenPosition()}') 
        return cursors[nextMap.getPosition()][nextGarden.getPosition()]
    
    def __eq__(self, other):
        if isinstance(other, Cursor):
            return ((self.getGardenPosition() == other.getGardenPosition()) 
                    and (self.getMapPosition() == other.getMapPosition()))
        else:
            return False
        
    def __hash__(self):
        return hash(self.__repr__())
    
    def __repr__(self) :
        return f'{self.getGardenPosition()}| {self.getMapPosition()}'
    
    
buildMap()

import time

curMap = CursorMap()
maps[curMap.getPosition()] = curMap
initialGarden = gardenMap[startLoc[0]]
curCursor = Cursor(initialGarden, curMap)

cursors[curMap.getPosition()]={}
cursors[curCursor.getMapPosition()][curCursor.getGardenPosition()] = curCursor
curCursors = [curCursor]
start_time = time.time()
for i in range(500) :
    curCursors = set(transverseMap(curCursors))
    if i+1 in [6, 10, 50, 100, 500, 1000, 5000] : 
        print(f'in step {i+1}, got {len(curCursors)} gardens')    
        print(f'In: current: {time.time()}--- {(time.time() - start_time)}  seconds ---' )



    
    