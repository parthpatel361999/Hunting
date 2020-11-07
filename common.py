import random as rnd


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
