import copy
import random as rnd
from queue import PriorityQueue

import numpy as np

from common import (Agent, Target, at6, manhattanDistance, minInRange,
                    minOutRange, numActions, targetInRange, withinRange5)

# from improvedMAST import improvementMAST

'''
    This Improved Agent is the same as our Improved Agent for the stationary target. It simply factors in the extra clue of whether 
    the target is within a distance of 5 by limiting its search scope to determine the next cell to search in the same way that 
    it did for the other agents. 
'''

def improvedMAMTWithClue(agent, target):
    highest = 0
    r = c = 0

    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * \
                (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while agent.hasFoundTarget == False:
        minScore = agent.dim ** 4
        prevr = r
        prevc = c

        numChecks = int(agent.map[r][c].falseNegativeProbability * 10.0)
        for check in range(numChecks):
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
                if check == numChecks - 1:
                    if withinFive:
                        minScore, r, c = minInRange(agent, prevr, prevc)
                    else:
                        minScore, r, c = minOutRange(agent, prevr, prevc)
                    numActions((prevr, prevc), (r, c), agent)
            else:
                break
    return agent.numMoves


def improvedMAMTWithoutClue(agent, target):
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
        numChecks = int(agent.map[r][c].falseNegativeProbability * 10.0)
        for check in range(0, numChecks):
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
                        if check == numChecks - 1 and minScore > agent.map[i][j].score:
                            minScore = agent.map[i][j].score
                            r = i
                            c = j
                        j = j + 1
                    i = i + 1
                if check == numChecks - 1:
                    numActions((prevr, prevc), (r, c), agent)
            else:
                break

    return agent.numMoves
