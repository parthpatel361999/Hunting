from common import Agent, Target, numActions, manhattanDistance, findNeighbors,theWay,findNeighbors
import random as rnd
import numpy as np

'''
    to be compared to rule 2, so used the rule two probability updates
'''


def movingTarget3(agent, target):
    highest = 0
    r = c = 0

    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col
    
    while agent.hasFoundTarget == False:
        minScore = agent.dim ** 4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r,c,target)
        #print('searched cell: ', (prevr,prevc))
        #print('Target Position: ', target.position)
        
        if searchResult == False:
            withinFive = targetInRange(agent, target, prevr, prevc)
            #print('target in range? ', withinFive)
            scale = 1 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # probabilities/scores are updated here 
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability)
                    dist = manhattanDistance((prevr,prevc), (i,j))
                    agent.map[i][j].score = (1 + float(dist)) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    j = j + 1
                i = i + 1
            
            if withinFive: 
                minScore, r, c = minInRange(agent, prevr, prevc)
            else: 
                minScore, r, c = minOutRange(agent, prevr, prevc)
            target.move(theWay(r,c,findNeighbors(target.position[0],target.position[1],agent.dim))) #pain
    return agent.numMoves

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

'''
    If the target is w/in 5, search those cells to find minProb to find next cell to search
'''
def minInRange(agent, r, c):
    minScore = np.inf
    
    coordList = withinRange5(agent, r, c)
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

# agent = Agent(12)
# y = withinRange5(agent,5,5)
# print(len(y))

total = 0
numTrials = 10
dim = 10
for i in range(numTrials):
    agent = Agent(dim)
    target = Target(dim)
    while agent.map[target.position[0]][target.position[1]].falseNegativeProbability == 0.9:
        target = Target(dim)
    # for r in agent.map:
    #     for cell in r:
    #         print(cell.falseNegativeProbability, end='  ')
    #     print()
    # print(target.position)
    total += movingTarget3(agent, target)
print("Average Moves Taken: " + str(float(total / numTrials)))