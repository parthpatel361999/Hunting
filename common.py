import copy
import random as rnd

import numpy as np

'''
    Define a class Target that keeps track of the map dimension and position of the target
'''

class Target:
    def __init__(self, dim):
        self.dim = dim
        self.position = (rnd.randint(0, dim - 1), rnd.randint(0, dim - 1))

    # Return the location of the target
    def isAt(self, row, col):
        return (row, col) == self.position

    # Moves the target to the desired location
    def move(self, newLocation=None):
        if newLocation is None:
            neighbors = findNeighbors(
                self.position[0], self.position[1], self.dim)
            self.position = neighbors[rnd.randint(0, len(neighbors) - 1)]
        else:
            self.position = newLocation

'''
    Define a class Agent that handles the following information:
    1. The dimension of the map to be searched
    2. A status indicator for whether or not the target has been found
    3. A map of Cell objects which represent different landscapes
'''

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
        self.searches = 0
        self.movements = 0

    # Resets the Agent
    def reset(self, map=[]):
        self.map = copy.deepcopy(map)
        self.hasFoundTarget = False
        self.currentPosition = (-1, -1)
        self.numMoves = 0
        self.searches = 0
        self.movements = 0

    # Returns a true/false based on the result of searching a specific cell. Updates the number of moves by 1.
    def searchCell(self, row, col, target):
        self.currentPosition = (row, col)
        self.numMoves += 1
        self.searches += 1
        if not target.isAt(row, col):
            return False
        else:
            if rnd.random() < self.map[row][col].falseNegativeProbability:
                return False
            else:
                self.hasFoundTarget = True
                return True

    # Returns true if the target is within manhattan distance 5 from the target
    def getHint(self, target):
        return manhattanDistance(target.position, self.currentPosition) <= 5

    # Moves the Agent to the desired location
    def move(self, row, col):
        self.currentPosition = (row, col)
        self.numMoves += 1
        self.movements += 1

'''
    Define a class Cell that keeps track of the following information for each landscape cell:
    1. The position of the cell in the map
    2. The probability that the cell will contain the target or belief value
    3. The false negative rate for that specific cell
    4. The score of this cell
    5. The neighbors of this cell
'''

class Cell:
    def __init__(self, row, col, dim, falseNegativeProbability):
        self.row = row
        self.col = col
        self.probability = 1.0/dim**2
        self.falseNegativeProbability = falseNegativeProbability
        self.score = 0
        self.neighbors = findNeighbors(row=row, col=col, dim=dim)

'''
    Returns a list of all neighboring cells to the inputted cell
'''

def findNeighbors(row, col, dim):
    neighbors = []
    potentialNeighbors = [(row - 1, col), (row, col + 1),
                          (row + 1, col), (row, col - 1)]
    for potentialNeighbor in potentialNeighbors:
        r, c = potentialNeighbor
        if r < dim and r >= 0 and c < dim and c >= 0:
            neighbors.append(potentialNeighbor)
    return neighbors

'''
    Returns the manhattan distance between two positions on the map
'''

def manhattanDistance(position1, position2):
    y1, x1 = position1
    y2, x2 = position2
    return abs(y1 - y2) + abs(x1 - x2)

'''
    Update the number of moves to reflect the number of cells the agent has travelled
'''

def numActions(initCoords, destination, agent):
    numMoves = manhattanDistance(initCoords, destination)
    agent.movements += numMoves
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
        if not (r, c) in coordList:
            coordList.append((r, c))
    withinRange5(agent, r+1, c, coordList, manD + 1)
    withinRange5(agent, r-1, c, coordList, manD + 1)
    withinRange5(agent, r, c+1, coordList, manD + 1)
    withinRange5(agent, r, c-1, coordList, manD + 1)

    return coordList

'''
    Returns a list of cells within manhattan distance of 6 from the start cell
'''

def at6(agent, r, c, coordList=[], manD=0):
    if r >= agent.dim or c >= agent.dim or r < 0 or c < 0:
        return []
    elif manD > 6:
        return []
    else:
        if not (r, c) in coordList:
            coordList.append((r, c))

    at6(agent, r+1, c, coordList, manD + 1)
    at6(agent, r-1, c, coordList, manD + 1)
    at6(agent, r, c+1, coordList, manD + 1)
    at6(agent, r, c-1, coordList, manD + 1)

    return coordList


'''
    If the target is w/in 5, search those cells to find minProb to find next cell to search
'''


def minInRange(agent, r, c, f=withinRange5):
    minScore = np.inf

    coordList = f(agent, r, c)
    coordList.remove((r, c))
    for coord in coordList:
        (r, c) = coord
        if agent.map[r][c].score < minScore:
            minScore = agent.map[r][c].score
            minR = r
            minC = c

    return minScore, minR, minC


'''
    If the target is w/in 5, search those cells to find minProb to find next cell to search
'''


def maxInRange(agent, r, c):
    maxScore = np.NINF

    coordList = withinRange5(agent, r, c)
    coordList.remove((r, c))
    for coord in coordList:
        (r, c) = coord
        if agent.map[r][c].score > maxScore:
            maxScore = agent.map[r][c].score
            minR = r
            minC = c

    return maxScore, minR, minC

'''
    If the target is not w/in 5, search cells that are not in that distance to find next lowest cell
'''

def minOutRange(agent, r, c):
    minScore = np.inf
    coordList = withinRange5(agent, r, c)
    coordList.remove((r, c))
    i = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if (i, j) in coordList or (i, j) == (r, c):
                j += 1
                continue
            if agent.map[i][j].score < minScore:
                minScore = agent.map[i][j].score
                minR = i
                minC = j
            j += 1
        i += 1
    return minScore, minR, minC

'''
    If the target is not w/in 5, search cells that are not in that distance to find next lowest cell
'''

def maxOutRange(agent, r, c):
    maxScore = np.NINF
    coordList = withinRange5(agent, r, c)
    coordList.remove((r, c))
    i = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if (i, j) in coordList or (i, j) == (r, c):
                j += 1
                continue
            if agent.map[i][j].score > maxScore:
                maxScore = agent.map[i][j].score
                minR = i
                minC = j
            j += 1
        i += 1
    return maxScore, minR, minC

'''
    Returns whether the target is within Manhattan Distance 5 of start cell
'''

def targetInRange(agent, target, r, c):
    coordList = withinRange5(agent, r, c)
    for coord in coordList:
        r, c = coord
        if target.isAt(r, c):
            return True
    return False


''' In part 3 of our assignment, the target needs to move the opposite way that the agent came. in this case 
    that is max manhattan distance between all the potential neighbors of the target and the new location of 
    the agent 
'''

def theWay(r, c, neighbors):
    maxC = -1
    maxR = -1
    for i in neighbors:
        if(maxC == -1 and maxR == -1):
            maxR = i[0]
            maxC = i[1]
        else:
            if(manhattanDistance((r, c), (i[0], i[1])) > manhattanDistance((r, c), (maxC, maxR))):
                maxR = i[0]
                maxC = i[1]
    return (maxR, maxC)