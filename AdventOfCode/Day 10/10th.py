#.....
#.S-7.
#.|.|.
#.L-J.
#.....

class Node() :
    def __init__(self, row,col, character) :
        self.inside = False
        self.location = (row,col)
        self.row = row
        self.col = col
        self.character = character
        self.connectedNodesLoc = []
        if character == '|':
            self.connectedNodesLoc = [(row-1,col), (row+1,col)] 
        if character == '-' :
            self.connectedNodesLoc = [(row, col-1), (row, col+1)]
        if character == 'L': 
            self.connectedNodesLoc = [(row-1,col), (row,col+1)]
        if character == 'J': 
            self.connectedNodesLoc = [(row-1,col), (row, col-1)]
        if character == '7': 
            self.connectedNodesLoc = [(row, col-1), (row+1, col)]
        if character == 'F':
            self.connectedNodesLoc = [(row, col+1), (row+1, col)]
        if character == 'S':
            self.connectedNodesLoc = []
    
    def __str__(self) :
        return f"node:{self.character}:{self.location}"

    def __repr__(self) :
        return f"node:{self.character}:{self.location}"
        

def getInput(test = True) :
    if test :
        f=open('input10thTest')
    else :
        f=open('input10th')

    #p = re.compile('[\dA-Z]{3}')
    #nodes={}
    #path = ''
    nodes = {}
    startNode=None
    row = 0
    lines = []
    for i, line in enumerate(f) :
        lines.append(line)
        data=tuple(line)
        print(f"got data # {i} # {data}")
        for col, x in enumerate(data) :
            if x in ['\n'] :
                continue
            nodes[(row,col)] = Node(row, col, x)
        row +=1
        
    for node in nodes.values() :
        node.connectedNodes = [nodes.get((x,y)) for x,y in node.connectedNodesLoc]
        if node.character == 'S' :
            startNode = node
    
    addNodesToStartNode = [y
                           for y in nodes.values() 
                           for x in y.connectedNodes 
                           if (x is not None 
                               and x.location==startNode.location) 
                           ]
    startNode.connectedNodes = addNodesToStartNode

    return (startNode, nodes, lines)


visitedNodes = {}
def stepDfs(curNode, distance) :
    print(f'Visited nodes: {visitedNodes} ')
    print(f'Visiting {curNode}. ')
    if curNode in visitedNodes :
        return
    else :
        visitedNodes[curNode] = distance
    for node in curNode.connectedNodes :
        stepDfs(node, distance+1)
    
    
def stepBfs(curNodes, distance) :
    #print(f'-----------------------------------------------------------------')
    #print(f'checking {curNodes}, {distance} ')
    #print(f'alreadyVisited: {visitedNodes}')
    
    for x in curNodes :
        visitedNodes[x] = distance
    
    return [x for y in curNodes for x in y.connectedNodes if x not in visitedNodes]

def doBfs(startNode) :
    distance = 0
    curNodes = [startNode]
    while True :
        curNodes = stepBfs(curNodes, distance)
        distance += 1
        if len(curNodes) == 0:
            break
    
    

    
startNode, allNodes, lines = getInput(False)
doBfs(startNode)
#printData(allNodes)

        
border = visitedNodes.keys()

borderLocations = [x.location for x in border]
matrix = {}
for x in borderLocations:
    if x[0] not in matrix :
        matrix[x[0]] = [x[1]]   
    else :
        matrix[x[0]].append(x[1])

for x in matrix.values() :
    x.sort()
        
dotNodes = [x for x in allNodes.values() if x.character=='.']

from itertools import chain

reducedLines = {}
''' 
print("Building reduced Lines")
for key, line in matrix.items() :
    print(f"Key: {key} : {line}")
    a=list(zip(line[:-1], line[1:]))
    print(f"a: {a}")
    b=[x for x in a if (x[1]-x[0])>1]
    print(f"b: {b}")
    c=list(chain(*b)) 
    print(f"c:{c}")
    reducedLines[key] = set(c)
''' 
    
for i in range(len(border)):
    reducedLine = [x for x in border if x.row == i and x.character not in ('-')]
    
    reducedLine.sort(key=lambda x:x.col)

    previousCharVertix = False
    newReducedLine = []
    for node in reducedLine :
        if node.character in ['|'] :
            newReducedLine.append(node)
            continue
        if previousCharVertix == True :
            previousCharVertix = False
            continue
        previousCharVertix = True
        newReducedLine.append(node)

    reducedLines[i] = newReducedLine

for dotNode in dotNodes :
    nodex=dotNode.col
    nodey=dotNode.row
    
    if nodey not in reducedLines :
        continue
    
    
    checkLine = [x.col for x in reducedLines[nodey]] 
    #print(f"Line Check: {checkLine}")
    
    if (len([x for x in checkLine if x < nodex])%2 == 0) :
        dotNode.inside = False
    else :
        print(f"found one:  location: {dotNode.location}, line at:{nodey}:{checkLine} ")
        dotNode.inside = True
    
    

newLines = []
for y, line in enumerate(lines) :
    newLine=""
    for x, l in enumerate(line) :
        if (y,x) in borderLocations :
            print(f'{x},{y},{l}')
            newLine += l
        else :
            print(f'({x},{y}) is not in border!')
            l = '.'
            newLine += l
    newLines += [newLine]


def reduceLine(line) :
    newLine = ""
    
    newLine = line.replace("-", "")
    newLine = newLine.replace("L7", "|")
    newLine = newLine.replace("LJ", "||")
    newLine = newLine.replace("F7", "||")
    newLine = newLine.replace("FJ", "|")
    newLine = newLine.replace("SJ", "||")    
    newLine = newLine.replace("S7", "||")    
    ''' 
    b= ""
    newLine = ""
    for a in line : 
        if a == "." :
            newLine += b
            b=""
            newLine += a
            continue
        if len(b) == 2 :
            continue
        b += a
    ''' 
    return newLine

def checkLine(line) :
    current = "O"
    newLine = ""
    for i, l in enumerate(line) :
        if l == "." :
            l = current
        if l in ('|', 'F', 'J', '7', 'L', 'S' ) :
            current = "I" if current == "O" else "O"
        newLine += l
    
    iOccurrences = newLine.count("I")
        
    return (newLine, iOccurrences)
''' 
def checkLine(line) :
    numberSpecialChars = 0
    inside = 0
    for i in line :
        if i==".":
            if numberSpecialChars%2 == 1 :
                inside +=1
        else :
            numberSpecialChars += 1
    return inside''' 
list(map(reduceLine, lines))
list(map(checkLine, map(reduceLine, lines)))

list(map(checkLine, map(reduceLine, newLines)))
