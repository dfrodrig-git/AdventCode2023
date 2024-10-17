# -*- coding: utf-8 -*-

MAX_ROWS = 0
MAX_COLS = 0


class Edge():
    def __init__(self, nodeA, nodeB, weight):
        # print(f"Creating Edge A:{nodeA}, B:{nodeB}")
        self.curNode = nodeA
        self.nextNode = nodeB
        self.weight = weight


class Node():
    def __init__(self, row, col, character):
        # print(f"Creating node row:{row}, col:{col}, {character}")
        self.row = row
        self.col = col
        self.character = character
        self.isGalaxy = False
        self.distanceRow = 1
        self.distanceCol = 1
        if character == "#":
            self.isGalaxy = True
        self.connectedEdges = []

    # def isGalaxy(self):
    #    return self.isGalaxy

    def multiplyDistance(self, row=1, col=1):
        if self.isGalaxy:
            raise Exception()
        self.distanceRow *= row
        self.distanceCol *= col

    def connectNodes(self, universeNodes):
        # print(f"Connecting Nodes on {self}, with MAX_ROWS = {MAX_ROWS}, MAX_COLS = {MAX_COLS}")
        if self.row < MAX_ROWS:
            self.connectedEdges.append(
                Edge(self, universeNodes[(self.row+1, self.col)], self.distanceRow))
        if self.col < MAX_COLS:
            self.connectedEdges.append(
                Edge(self, universeNodes[(self.row, self.col+1)], self.distanceCol))
        if self.row > 0:
            self.connectedEdges.append(
                Edge(self, universeNodes[(self.row-1, self.col)], self.distanceRow))
        if self.col > 0:
            self.connectedEdges.append(
                Edge(self, universeNodes[(self.row, self.col-1)], self.distanceCol))
        # print(f"Connected {len(self.connectedEdges)} edges to {self}")

    def __str__(self):
        return f"node:{self.character}:{self.row}, {self.col}, {self.distanceRow}, {self.distanceCol}"

    def __repr__(self):
        return f"node:{self.character}:{self.row}, {self.col}, {self.distanceRow}, {self.distanceCol} "


def getInput(test=True):
    if test:
        f = open('input11thTest.txt')
    else:
        f = open('input11th.txt')

    # p = re.compile('[\dA-Z]{3}')
    nodes = {}
    # path = ''
    lines = []
    for row, line in enumerate(f):
        line = line.replace("\n", "")
        data = tuple(line)
        lines.append(line)
        for col, character in enumerate(data):
            nodes[(row, col)] = Node(row, col, character)

    global MAX_ROWS
    global MAX_COLS
    MAX_ROWS = len(lines)-1
    MAX_COLS = len(lines[0])-1
    print(f"MAX_ROWS: {MAX_ROWS}, MAX_COLS: {MAX_COLS}")

    return expandUniverse(lines, nodes)


def expandUniverse(lines, nodes):

    addRows = []
    for i, line in enumerate(lines):
        if line.count("#") == 0:
            addRows.append(i)

    addColumns = []
    for j in range(len(lines[0])-1):
        column = [x[j] for x in lines]
        if column.count("#") == 0:
            addColumns.append(j)

    print(f"Adding weights to rows:{addRows}, cols:{addColumns} ")

    for i in addRows:
        [x.multiplyDistance(row=2) for x in nodes.values() if x.row == i]
    for j in addColumns:
        [x.multiplyDistance(col=2) for x in nodes.values() if x.col == j]

    return (lines, nodes)


def findShortestPath(startNode, endNode=None, universeNodes=None):
    print(f"Finding shortest Path between {startNode} and {endNode}")
    dist = {x: float('inf') for x in universeNodes.values()}

    shortestPath = {}

    unvisited = [x for x in universeNodes.values()]
    visited = []

    dist[startNode] = 0

    while len(visited) < len(unvisited):
        a = (x for x in dist.items() if x not in visited)
        # print(f"Len unvisited: {len(a)}")
        u = min(a, key=lambda x: x[1])[0]

        # unvisited.remove(u)
        if len(visited) % 100 == 0:
            print(f"removing {u} from list: lenvisited:{len(visited)} < {len(unvisited)}")
        visited.append(u)

        # print(f"Checking {u.connectedEdges}:")
        for x in u.connectedEdges:
            # print(f"Checking connectedEdge: {x}, {x.nextNode}")
            nextNode = x.nextNode
            '''
            if nextNode not in unvisited:
                print(f"{x.nextNode}  is not in unvisited")
                continue
            '''
            curDist = dist[u] + x.weight
            if curDist < dist[nextNode]:
                dist[nextNode] = curDist
                # shortestPath[nextNode] = u

            '''
            if nextNode == endNode:
                print(f"Got to endNode {endNode} ")
                return dist[nextNode] #, shortestPath# dist, shortestPath
            '''

    return dist  # , shortestPath


universeNodes = getInput(True)[1]
print(f"MAX_ROWS: {MAX_ROWS}, MAX_COLS: {MAX_COLS}")

[x.connectNodes(universeNodes) for x in universeNodes.values()]

galaxies = [x for x in universeNodes.values() if x.isGalaxy]

distMap = {}

for startGalaxy in galaxies:
    dist = findShortestPath(startGalaxy, universeNodes=universeNodes)
    for endGalaxy in galaxies:
        if (startGalaxy, endGalaxy) not in distMap.keys():
            distMap[(startGalaxy, endGalaxy)] = dist[endGalaxy]
            distMap[(endGalaxy, startGalaxy)] = dist[endGalaxy]
            print(f"Got distance between {startGalaxy} and {endGalaxy} : {dist[endGalaxy]}")

#distances, shortestPath = findShortestPath(galaxies[0], galaxies[1], universeNodes)

print(f"Result = {sum(distMap.values()) /2}")
