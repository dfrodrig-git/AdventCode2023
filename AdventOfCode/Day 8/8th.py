# -*- coding: utf-8 -*-
import re

def getInput(test = False) :
    if test :
        f=open('input8thTest')
    else :
        f=open('input8th')

    p = re.compile('[\dA-Z]{3}')
    nodes={}
    path = ''
    for line in f :
        if '(' in line :
            nodeInput = p.findall(line)
            nodes[nodeInput[0]] = [nodeInput[1], nodeInput[2]]
            continue
        
        if 'L' in line :
            path=line.strip()
        
    return (path, nodes)



class Node() :
    def __init__(self, nodeRef) :
        print(f'creating node: {nodeRef}')
        self.nodeRef = nodeRef
        self.endNode = True if nodeRef[2] =='Z' else False

    def addLeftRight(self, leftNode, rightNode) : 
        self.leftNode = leftNode
        self.rightNode = rightNode
                
    def getNodeRef(self) :
        return self.nodeRef 
    
    def left(self) :
        return self.leftNode
    
    def right(self) :
        return self.rightNode
    
    def __str__(self) :
        return f'{self.nodeRef}'

    def __repr__(self) :
        return f'{self.nodeRef}'


def traverse(path, fromNode, toNode=None) :
    print(f'traversing "{fromNode} {fromNode.nodeRef}" on path {path}')
    i = 0
    steps = 0
    curNode = fromNode
    
    while curNode.nodeRef != "ZZZ" :
        if path[i] == 'L' :
            curNode = curNode.left()
        if path[i] == 'R' :
            curNode = curNode.right()
        
        steps +=1
        
        if i < len(path)-1 :
            i += 1
        else :
            i = 0
    
    
    return steps


import time
def traverse2(path, fromNodes) :
    i = 0
    steps = 0
    curNodes = fromNodes
    
    
    start = time.time()
    while True :
        #map( lambda x.left  , path)
        if steps%1000000 == 0 :
            print(f'Step {steps} , in {time.time()-start}sec')
            start = time.time()
        #print(f'curNodes: {[x.nodeRef for x in curNodes]}')
        #print(f'Checking: {[(x, x.nodeRef) for x in curNodes]} ')
        if path[i] == 'L' :
            curNodes = [x.leftNode for x in curNodes]
        if path[i] == 'R' :
            curNodes = [x.rightNode for x in curNodes]

        #print(f'curNodes: {[x.nodeRef for x in curNodes]}')
                    
        #print(f'Checking: {[(x, x.nodeRef) for x in curNodes]} ')
        steps +=1
        if i< len(path)-1 :
            i+=1
        else :
            i=0
        if sum([x.endNode for x in curNodes]) == 6:
            break
        #start = time.time()
    return steps


def distances(path, fromNode, toNode) :
    print(f"=================================================================")
    print(f"Checking from {fromNode.nodeRef} => to {toNode.nodeRef}")
    i = 0
    steps = 0
    curNode = fromNode
    visitedOnStep = []
    
    while True:
        steps +=1
        if path[i] == 'L' :
            curNode = curNode.leftNode
        if path[i] == 'R' :
            curNode = curNode.rightNode
            
        #break conditions    
        if curNode.nodeRef == toNode.nodeRef :
            break 
        
        if (curNode, i % len(path) ) in visitedOnStep :
            steps = -1
            break
        visitedOnStep.append((curNode, i%len(path)))
           
        if i < len(path)-1 :
            i+=1
        else :
            i=0
 
    print(f'Visited on step: {[(x[0].nodeRef, x[1]) for x in visitedOnStep]}')
    print(f"-----------------------------------------------------------------")
    print("")
    
    return steps




path, nodes = getInput(False)
path = tuple(path)

for k in nodes.keys() :
    newNode = Node(k)
    nodes[k].append(newNode)

for k, v in nodes.items() :
    v[2].addLeftRight(nodes[v[0]][2],nodes[v[1]][2])    

begin = [v[2] for k, v in nodes.items() if k[2] == 'A']
print(f'Starting on nodes {begin} ')

#begin = nodes[startNode][2]
#result = traverse(path, begin)

#result = traverse2(path, begin)
#print(f'traverse Result: {result}')




    
    
zNodes = [x[2] for x in nodes.values() if x[2].endNode]


distancesMatrix = []
for a in begin :
    for b in zNodes :
        distancesMatrix.append((a, b)) 

minPathTo = []        
for x in distancesMatrix :
        print(f'Finding distance for {x} ')
        minPathTo.append( [x[0], x[1], distances(path, x[0], x[1])] )
        print(f'got {minPathTo} ')
    
print([(x[0].nodeRef, x[1].nodeRef, x[2]) for x in minPathTo])


