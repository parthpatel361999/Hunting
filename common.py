import random as rnd
import numpy as np


class Target:
    def __init__(self, dim):
        self.dim = dim
        self.position = (rnd.randint(0, dim - 1), rnd.randint(0, dim - 1))

    def isAt(self, row, col):
        return (row, col) == self.position

    def move(self, newLocation=None):
        if newLocation is None:
            neighbors = findNeighbors(
                self.position[0], self.position[1], self.dim)
            self.position = neighbors[rnd.randint(0, len(neighbors) - 1)]
        else:
            self.position = newLocation


class Agent:
    def __init__(self, dim):
        self.dim = dim
        self.hasFoundTarget = False
        self.map = []
        for i in range(0, dim):
            mapRow = []
            for j in range(0, dim):
                falseNegativeProbability = 0.0
                landscape = rnd.randint(0, 9)
                if landscape < 2:
                    falseNegativeProbability = 0.1
                elif landscape < 5:
                    falseNegativeProbability = 0.3
                elif landscape < 8:
                    falseNegativeProbability = 0.7
                else:
                    falseNegativeProbability = 0.9
                cell = Cell(row=i, col=j, dim=dim,
                            falseNegativeProbability=falseNegativeProbability)
                mapRow.append(cell)
            self.map.append(mapRow)
        self.currentPosition = (-1, -1)
        self.numMoves = 0

    def searchCell(self, row, col, target):
        self.currentPosition = (row, col)
        self.numMoves += 1
        if not target.isAt(row, col):
            return False
        else:
            if rnd.random() < self.map[row][col].falseNegativeProbability:
                return False
            else:
                self.hasFoundTarget = True
                return True

    def getHint(self, target):
        return manhattanDistance(target.position, self.currentPosition) <= 5

    def move(self, row, col):
        self.currentPosition = (row, col)
        self.numMoves += 1


class Cell:
    def __init__(self, row, col, dim, falseNegativeProbability):
        self.row = row
        self.col = col
        self.probability = 1.0/dim**2
        self.falseNegativeProbability = falseNegativeProbability
        self.score = 0
        self.neighbors = findNeighbors(row=row, col=col, dim=dim)


def findNeighbors(row, col, dim):
    neighbors = []
    potentialNeighbors = [(row - 1, col), (row, col + 1),
                          (row + 1, col), (row, col - 1)]
    for potentialNeighbor in potentialNeighbors:
        r, c = potentialNeighbor
        if r < dim and r >= 0 and c < dim and c >= 0:
            neighbors.append(potentialNeighbor)
    return neighbors


def manhattanDistance(position1, position2):
    y1, x1 = position1
    y2, x2 = position2
    return abs(y1 - y2) + abs(x1 - x2)

def numActions(initCoords, destination, agent):
    numMoves = manhattanDistance(initCoords, destination)
    agent.numMoves += numMoves

'''
    Returns list of cells that are within manhattan distance of five away from start cell
'''
def withinRange5(agent, r, c, coordList=[], manD=0): 
    if r >= agent.dim or c >= agent.dim or r < 0 or c < 0:
        return []
    elif manD > 5:
        return []
    else:
        if not (r,c) in coordList:
            coordList.append((r,c))
    withinRange5(agent, r+1, c, coordList, manD + 1)
    withinRange5(agent, r-1, c, coordList, manD + 1)
    withinRange5(agent, r, c+1, coordList, manD + 1)
    withinRange5(agent, r, c-1, coordList, manD + 1)
    
    return coordList

def at6(agent, r, c, coordList=[], manD=0): # we are not sure if this function should be all cells within 6 or just the border cells of distance 6
    if r >= agent.dim or c >= agent.dim or r < 0 or c < 0:
        return []
    elif manD > 6:
        return []
    else:
        if not (r,c) in coordList:
            coordList.append((r,c))

    at6(agent, r+1, c, coordList, manD + 1)
    at6(agent, r-1, c, coordList, manD + 1)
    at6(agent, r, c+1, coordList, manD + 1)
    at6(agent, r, c-1, coordList, manD + 1)

    return coordList

'''
    If the target is w/in 5, search those cells to find minProb to find next cell to search
'''
def minInRange(agent, r, c, f = withinRange5):
    minScore = np.inf
    
    coordList = f(agent, r, c)
    coordList.remove((r,c))
    #print(coordList)
    for coord in coordList:
        #print(coord)
        (r, c) = coord
        if agent.map[r][c].score < minScore:
            minScore = agent.map[r][c].score
            minR = r
            minC = c


    return minScore, minR, minC

'''
    If the target is not w/in 5, search cells that are not in that distance to find next lowest cell
'''
def minOutRange(agent, r, c):
    minScore = np.inf
    coordList = withinRange5(agent, r, c)
    coordList.remove((r,c))
    i = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if (i,j) in coordList or (i,j) == (r,c):
                j+=1
                continue
            if agent.map[i][j].score < minScore :
                minScore = agent.map[i][j].score
                minR = i
                minC = j
            j+=1
        i+=1 
    return minScore, minR, minC
'''
    Returns whether the target is within Manhattan Distance 5 of start cell
'''
def targetInRange(agent, target, r, c):
    coordList = withinRange5(agent, r, c)
    for coord in coordList:
        r, c = coord
        if target.isAt(r,c):
            return True
    return False


''' In part 3 of our assignment, the target needs to move the opposite way that the agent came. in this case 
    that is max manhattan distance between all the potential neighbors of the target and the new location of 
    the agent '''

def theWay(r,c,neighbors): 
    maxC = -1
    maxR = -1
    for i in neighbors:
        if(maxC == -1 and maxR == -1):
            maxR = i[0]
            maxC = i[1]
        else:
            if(manhattanDistance((r,c),(i[0],i[1])) > manhattanDistance((r,c),(maxC,maxR))):
                maxR = i[0]
                maxC = i[1]
    return (maxR,maxC)
    