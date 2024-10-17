# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 18:54:59 2024

@author: CTW00905
"""
import time
import networkx as nx
import re
import numpy as np
import pprint
import threading
import queue

''' 
from colorama import init, Fore, Back, Style
init(autoreset= True)
x="blah"
print(Style.BRIGHT + Back.YELLOW + Fore.RED + f"CHEESY {x}")
'''

# -------------------------------------------------
# Inputs
# -------------------------------------------------
test = True
steps = 6

if test:
    with open("input6thtest.txt", "r") as file:
        lines = file.readlines()

else:
    with open("input6th.txt", 'r') as file:
        lines = file.readlines()
    steps = 64


def printPositions(cursors):
    for y in range(MAX_ROWS):
        row = ""
        for x in range(MAX_COLUMNS):
            if gardenMatrixFilter[y][x] == 0:
                row += "# "
                continue
            if (y, x) in [x.location for x in cursors]:
                row += "O "
                continue
            row += ". "
        print(row)

''' lines = ["####\n"]
lines += ["..S.\n"]
lines += ["####\n"]
lines += ["####\n"]
# lines += [".....\n"]
'''


# find gear symbol
pg = re.compile('\.')
gardenLoc = []


def checkRock(a):
    return 0 if a == '#' else 1


def checkStart(a):
    return True if a == 'S' else False


gardenMatrixFilter = []
for i, line in enumerate(lines):
    mappedLine = list(map(checkRock, line))
    gardenMatrixFilter.append(mappedLine[:-1])

MAX_ROWS = len(gardenMatrixFilter)
MAX_COLUMNS = len(gardenMatrixFilter[0])

startNode = (0, 0)
for i, line in enumerate(lines):
    mappedLine = list(map(checkStart, line))
    if sum(mappedLine) == 1:
        startNode = (i, mappedLine.index(1))
        break
print(f'{startNode}')
start = np.zeros([MAX_ROWS, MAX_COLUMNS])
start[startNode] = True
# gmf=numpy.matrix(gardenMatrixFilter)




class GardenNode():
    def __init__(self, x, y):
        self.location = (x, y)
        self.isBorder = True if (x == 0) or (y == 0) \
            or (x == MAX_COLUMNS - 1) or (y == MAX_ROWS - 1) \
            else False
        self.isCorner = True if (x == 0 and y == 0) \
            or (x == 0 and y == MAX_ROWS - 1) \
            or (x == MAX_COLUMNS - 1 and y == 0) \
            or (x == MAX_COLUMNS - 1 and y == MAX_COLUMNS - 1) \
            else False
        self.reachableNodes = []
        self.reachableMapNodes = {}
        self.maps = []

    def visit(self):
        return self

    def __str__(self):
        return f"l:{self.location}, {id(self)}"

    def __repr__(self):
        return f"l:{self.location}"
    

class GardenMap() :
    def __init__(self, x, y) :
        self.location = (x,y)
        self.curNodes = []
        self.isSteadyState = False
        self.nodeCache = {} #{tuple: (step, #items, edgeCursors)}
    
    def patternFound(self, t, step, size) :
        previousNode = self.nodeCache[t]
        self.patternFrequency = step-previousNode[0] 
        
        #step/Mod numberItems edgeCursors
        self.patternMap = {x-previousNode[0]: ( x[1], x[2]) for x in nodeCache.values() if x[0] > previousNode[0]}
         
        self.isSteadyState = True
    
    def getPattern(step) :
        
        patternKey = step % self.patternFrequency
        
        return self.patternMap[patternKey]
        
    
    def nextStep(self,step) :
        if self.isSteadyState :
            
        else:   
            
            

    
    def step(self, step) :
        if self.steadyState :
            return self.nextNodes()
            
        
        
        selfNodes = set([(self.location, node)
                             for cursor in self.curNodes
                             for node in cursor.reachableNodes])        


        edgeCursors = [((mapDir[0]+mapId[0], mapDir[1]+mapId[1]), node)
                       for cursor in self.curNodes
                       for mapDir, node in cursor.reachableMapNodes.items()]
    
        t=tuple(selfNodes)
        if t in self.nodeCache.keys():
            self.patternFound(t, step, len(selfNodes))
        else :
            self.nodeCache[t] = (step, len(selfNodes), edgeCursors)
            
        return nodesList
    
    def updateMap(self, newNodes) :
        self.curNodes += newNodes
    




    # def visitNewMap(self):

###############################################################################
##              Build Nodes                                                  ##
###############################################################################


gardenNodesDict = {}
for x in range(MAX_COLUMNS):
    for y in range(MAX_ROWS):
        if gardenMatrixFilter[x][y] == 1:
            node = GardenNode(x, y)
            gardenNodesDict[(x, y)] = node

for x in range(MAX_COLUMNS):
    for y in range(MAX_ROWS):
        node = gardenNodesDict.get((x, y), None)
        if node is None:
            continue
        for key in [(x, y+1), (x, y-1), (x-1, y), (x+1, y)]:
            neighbourNode = gardenNodesDict.get(key, None)
            if neighbourNode is not None:
                node.reachableNodes.append(neighbourNode)
        if x == 0:
            neighbourNode = gardenNodesDict.get((MAX_COLUMNS-1, y), None)
            if neighbourNode is not None:
                node.reachableMapNodes.setdefault(
                    (-1, 0), []).append(neighbourNode)
        if y == 0:
            neighbourNode = gardenNodesDict.get((x, MAX_ROWS-1), None)
            if neighbourNode is not None:
                node.reachableMapNodes.setdefault(
                    (0, -1), []).append(neighbourNode)
        if x == MAX_COLUMNS-1:
            neighbourNode = gardenNodesDict.get((0, y), None)
            if neighbourNode is not None:
                node.reachableMapNodes.setdefault(
                    (1, 0), []).append(neighbourNode)
        if y == MAX_ROWS-1:
            neighbourNode = gardenNodesDict.get((x, 0), None)
            if neighbourNode is not None:
                node.reachableMapNodes.setdefault(
                    (0, 1), []).append(neighbourNode)


# steps = 6

sourceNode = gardenNodesDict[startNode]
cursors = [sourceNode]
''' 
for step in range(steps):
    # print(f'step:{step+1}')
    cursors = set([x.visit() for y in cursors for x in y.reachableNodes])
    cursors = set([x.visitNewMap()
                  for y in cursors for x in y.reachableMapNodes])

    # print(f'Reached {len(cursors)} gardens')
'''


class GardenGraph():
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.maps = {}  # all nodes reached at a given step
        self.hashmaps = {}
        self.G = nx.Graph()
        self.distanceMaps = {}
        self.previousMapCursors = {}
        return None

    def addNode(self, node):
        self.G.add_node(node)
        self.nodes[node.location] = node

    def addEdges(self, edgeList):
        self.G.add_edges_from(edgeList)
        for a in edgeList:
            self.edges.setdefault(a[0], []).append(a[1])
            self.edges.setdefault(a[1], []).append(a[0])

    ''' 
    def computeDescendantsAt(self, steps, sourceNode):
        a = []
        for i in range(steps+1) :
            distLen=self.distanceMaps.setdefault(i, len(nx.descendants_at_distance(self.G, sourceNode, i)))
            a.append(distLen)
    
        return sum(a[1::2])
    '''

    def traverse(self, sourceNode, steps):
        cursors = [sourceNode]

        for step in range(steps):
            cursors = set([x.visit()
                          for y in cursors for x in y.reachableNodes])

        key = hash(tuple(cursors))
        self.hashmaps[steps] = key
        self.maps[key] = tuple(cursors)

        return len(cursors)
        

    def extendedTraverse(self, sourceNode, steps):
        cursors = [sourceNode]

        mapCursors = {}
        mapCursors[(0, 0)] = set(cursors)
        profile1=0 
        profile2=0
        profile3=0
        for step in range(steps):
            # print(f"mapCursors: {mapCursors}")

            delayedExecution = []
            for mapId, cursors in list(mapCursors.items()):
                #print(f'processing map: {mapId}, currentCursors:{cursors} ')
                #getting all reachable nodes within existing map
                
                
                start_time = time.time()
                mapCursors[mapId] = set([node
                                         for cursor in cursors
                                         for node in cursor.reachableNodes])
                profile1 += time.time()-start_time
                
                #getting reachable nodes in other maps
                
                start_time = time.time()
                edgeCursors = (((mapDir[0]+mapId[0], mapDir[1]+mapId[1]), node)
                               for cursor in cursors
                               for mapDir, node in cursor.reachableMapNodes.items())
                profile2 += time.time()-start_time
                
                
                start_time = time.time()
                delayedExecution += (#mapCursors.setdefault(edgeCursor[0], set([])).add(node)
                                  (edgeCursor[0], node)
                                  for edgeCursor in edgeCursors
                                  for node in edgeCursor[1])
                profile3 += time.time()-start_time
                
                #print(f"\n\n\nedgeCursors at step {step+1} on {mapId}:")
                #pprint.pp(sorted(edgeCursors, key=lambda x:x[0]))

            addEdgeNodes= [mapCursors.setdefault(x,set([])).add(y) for x,y in delayedExecution]
            #print(f"resulting Edgenodes : {delayedExecution}")

            #print(f"\n\n========================= step : {step+1}")
            totalAcross = 0
            for x, y in mapCursors.items():
                # print(f"Map: {x}, len: {len(y)} ")
                # print(f"Map: {x}, cursors: {y} ")
                totalAcross += len(y)
        
            if (step + 1) in [10,50,100,500,1000,5000] :
                print(f"Step {step+1} === total across:{totalAcross}. profiling: {profile1}, {profile2}, {profile3}")
            #self.visualize(mapCursors)

            # print(f"on {mapId}, adding {edgeCursors}")
            # edgeMapKeys = set(map(lambda x:x[1], edgeCursors))
            #print(f"Next step::::::::::::::::::::::::::::::::::::::::::::::::")

        return mapCursors

    def visualize(self, mapCursors):
        newMap = []
        mapLen = len(lines[0])+1
        for i in range(3*mapLen):
            line = []
            [line.append(" ") for x in range(3*mapLen)]
            line = ''.join(line)
            newMap.append(list(line))

        '''for a in [(-1,-1), (-1,0), (-1,1), (0,-1),(0,0), (0,1), (1,-1), (1,0), (1,1)]:
            for y in range(MAX_ROWS):
                for x in range(MAX_COLUMNS):
                    if gardenMatrixFilter[y][x] == 0:
                        newMap[x+(1+a[0])*11][y+(1+a[1])*11]=Fore.WHITE+"\u00A4"+Style.RESET_ALL 
                        continue
        '''

        for a in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
            locations = mapCursors.get(a)
            if locations == None:
                continue
            for l in locations:
                # print(f'adding {l.location} in {a}')
                x = l.location[0] + (1+a[0])*mapLen
                y = l.location[1] + (1+a[1])*mapLen
                # print(f'adding {x} in {y} :{newMap[x][y]}:')
                newMap[x][y] = "+"

        for a in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
            locations = self.previousMapCursors.get(a)
            if locations == None:
                continue
            for l in locations:
                # print(f'adding {l.location} in {a}')
                x = l.location[0] + (1+a[0])*mapLen
                y = l.location[1] + (1+a[1])*mapLen
                # print(f'adding {x} in {y} :{newMap[x][y]}:')
                newMap[x][y] = "O"

        for i, line in enumerate(newMap):
            # print(line)
            start = line[0:mapLen]
            start.extend(["|"])
            start.extend(line[mapLen:2*mapLen])
            start.extend(["|"])
            start.extend(line[2*mapLen:3*mapLen])
            s = ''.join(str(x) for x in start)

            print(s)
            if i in (mapLen-1, 2*mapLen-1):
                print("---------------------------------")

        print("=================================")
        self.previousMapCursors = dict(mapCursors)


G = nx.Graph()
G.add_nodes_from([x for x in gardenNodesDict.values()])
G.add_edges_from([(y, x) for y in gardenNodesDict.values()
                 for x in y.reachableNodes])

# Some Analytics:
# nx.shortest_path_length(G,source=0)
nx.shortest_path_length(G, gardenNodesDict[startNode])

a = list(nx.dfs_successors(G, source=sourceNode, depth_limit=steps))
print(f"Result dfs: {len(a)}")

a = list(nx.bfs_successors(G, source=sourceNode, depth_limit=steps))
print(f"Result bfs: {len(a)}")

a = list(nx.descendants_at_distance(G, source=sourceNode, distance=steps))
print(f"Result bfs: {len(a)}")

allGraphDistances = nx.all_pairs_shortest_path_length(G)


''' 
transform: from location i can reach location j (#count reachable locations)

in x steps can reach x locations

        
    '''
GG = GardenGraph()
a = [GG.addNode(x) for x in gardenNodesDict.values()]
a = [(y, x) for y in gardenNodesDict.values() for x in y.reachableNodes]
GG.addEdges(a)
sourceNode = GG.nodes[startNode]

start_time = time.time()
# for i in range(10):
steps = 1001
x = GG.extendedTraverse(sourceNode, steps)
# if i % 10 == 0 or i == 64:
#    print(f"step:{i}, {x}, numberMaps:{len(GG.maps)}")
print("In: --- %s seconds ---" % (time.time() - start_time))


''' 
start_time = time.time()
for i in range(150):
    x = GG.computeDescendantsAt(i, sourceNode)
    if i % 10 == 0 :
        print(f"step:{i}, {x}, numberMaps:{len(GG.maps)}")
print("In: --- %s seconds ---" % (time.time() - start_time))
'''
