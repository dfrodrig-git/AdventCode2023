''' 
algorithm


nodeList [] (threads)

nodeQueue

node; 
    reachable Nodes; current maps;
    currentStep


nodeAsThread

step, map

NodeThread.run()
- while currentStep < steps
- for reachableNode, mapDir in reachableNodes 
  changeQueue.notify(reachableNode, step, mapList + mapDir)
  
  checkLatestStep():
      getLock(queue[node])
          if queue[node].getLatestStep() < currentStep :
               continue
          else :
              self.currentStep = queue[node].step+1
              self.mapList = mapList+mapDir
      
  

NodeQueue
  {node: [ step, mapList+mapDir] }
'''

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
#===============================================================================



import threading
class GardenNode(threading.Thread):
    def __init__(self, x, y):
        threading.Thread.__init__(self) 
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
        self.reachableMapNodes = {} #key = (mapDir)
        self.maps = []
        self.currentStep =0
        self.steps = []

    def run(self):
        
        for reachableNode in reachableNodes :
            getLock(changeQueue[reachableNode])
            if changeQueue[reachableNode][-1][0] <= self.currentStep :
                changeQueue[reachableNode].append((self.currentStep+1, self.maps))
            releaseLock(changeQueue[reachableNode])
            
        
        self.checkLatestStep() :
            
            
            
        ''' 
        getLock(queue[node])
            if queue[node].getLatestStep() < currentStep :
                 continue
            else :
                self.currentStep = queue[node].step+1
                self.mapList = mapList+mapDir
        '''
            
    def checkLastestStep(self) :
        getLock(changeQueue[self])
        if changeQueue[self][-1][0] > self.currentStep :
            changeQueue[self]
        
        
        
    def visit(self):
        return self

    def __str__(self):
        return f"l:{self.location}, {id(self)}"

    def __repr__(self):
        return f"l:{self.location}"
    



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
                

nodeThreadList = list()

