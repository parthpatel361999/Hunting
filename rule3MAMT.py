import random as rnd

import numpy as np

from common import Agent, Target, manhattanDistance, numActions

'''
    This is Basic Agent 3 for the moving target. It is the same as Basic Agent 3 for the stationary target, with the additional information
    of whether the target is within a Manhattan distance of 5 of the agent. We limit our search to only those cells on the board 
    that are within a distance of 5 or out of 5, depending on the clue. 
'''


def rule3MAMTWithClue(agent, target):
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
        searchResult = agent.searchCell(r, c, target)
        #print('searched cell: ', (prevr,prevc))
        #print('Target Position: ', target.position)

        if searchResult == False:
            target.move()
            withinFive = targetInRange(agent, target, prevr, prevc)
            #print('target in range? ', withinFive)
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # probabilities/scores are updated here
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[i][j].falseNegativeProbability)
                    dist = manhattanDistance((prevr, prevc), (i, j))
                    agent.map[i][j].score = (1 + float(dist)) / (
                        agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    j = j + 1
                i = i + 1
            # if the target is within five, find the minimum cell oout of those within five 
            if withinFive:
                minScore, r, c = minInRange(agent, prevr, prevc)
            else: # if the target is not within five, find the minimum cell out of those that are not within five
                minScore, r, c = minOutRange(agent, prevr, prevc)
            numActions((prevr, prevc), (r, c), agent)

    return agent.numMoves


def rule3MAMTWithoutClue(agent, target):
    highest = 0
    r = c = 0
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            # dist = float(manhattanDistance((r,c), (i,j)))
            # agent.map[i][j].score = dist / agent.map[i][j].score
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while (agent.hasFoundTarget == False):
        minScore = agent.dim**4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:
            target.move()
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
                agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if i == prevr and j == prevc:
                        j += 1
                        continue
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    dist = manhattanDistance((prevr, prevc), (i, j))
                    agent.map[i][j].score = (1 + float(dist)) / (
                        agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    if minScore > agent.map[i][j].score:
                        minScore = agent.map[i][j].score
                        r = i
                        c = j
                    j = j + 1
                i = i + 1
            numActions((prevr, prevc), (r, c), agent)

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
        if not (r, c) in coordList:
            coordList.append((r, c))
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
    coordList.remove((r, c))
    # print(coordList)
    for coord in coordList:
        # print(coord)
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
    Returns whether the target is within Manhattan Distance 5 of start cell
'''


def targetInRange(agent, target, r, c):
    coordList = withinRange5(agent, r, c)
    for coord in coordList:
        r, c = coord
        if target.isAt(r, c):
            return True
    return False

# agent = Agent(12)
# y = withinRange5(agent,5,5)
# print(len(y))


# total = 0
# numTrials = 100
# dim = 10
# for i in range(numTrials):
#     agent = Agent(dim)
#     target = Target(dim)
#     while agent.map[target.position[0]][target.position[1]].falseNegativeProbability == 0.9:
#         target = Target(dim)
#     # for r in agent.map:
#     #     for cell in r:
#     #         print(cell.falseNegativeProbability, end='  ')
#     #     print()
#     # print(target.position)
#     total += rule3MAMTWithClue(agent, target)
# print("Average Moves Taken: " + str(float(total / numTrials)))
