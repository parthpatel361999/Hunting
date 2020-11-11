from common import Agent, Target, numActions, manhattanDistance
import random as rnd
import numpy as np

def movingTarget1(agent, target):
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
        print('searched cell: ', (prevr,prevc))
        print('Target Position: ', target.position)
        
        if searchResult == False:
            withinFive = targetInRange(agent, target, prevr, prevc)
            print('target in range? ', withinFive)
            scale = 1 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # probabilities/scores are updated here 
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    dist = manhattanDistance((prevr,prevc), (i,j))
                    agent.map[i][j].score = (1 + float(dist)) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    # so here has to be the check for within5
                    # if within5, find minCell within these cells, else find minCell 
                    j = j + 1
                i = i + 1
            
            if withinFive: # if withinFive, find lowest prob among those cells
                minScore, r, c = minInRange(agent, prevr, prevc)
            else: # else find lowest prob in cells that are not withinFive
                minScore, r, c = minOutRange(agent, prevr, prevc)
            target.move()
    return agent.numMoves

# returns list of coords within Manhattan Distance of 5, including the original r,c
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

def minInRange(agent, r, c):
    minScore = np.inf
    
    coordList = withinRange5(agent, r, c)
    #print(coordList)
    for coord in coordList:
        #print(coord)
        (r, c) = coord
        if agent.map[r][c].score < minScore:
            minScore = agent.map[r][c].score
            minR = r
            minC = c


    return minScore, minR, minC

def minOutRange(agent, r, c):
    minScore = np.inf
    coordList = withinRange5(agent, r, c)
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
# returns whether the target is within Manhattan Distance 5
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
    total += movingTarget1(agent, target)
print("Average Moves Taken: " + str(float(total / numTrials)))