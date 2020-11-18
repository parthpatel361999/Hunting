import copy
import random as rnd
import time
from queue import PriorityQueue

import numpy as np

from common import Agent, Target, manhattanDistance, numActions

'''
    This is the remastered improved agent for the stationary target. The premise of this agent is to check a cell based on the terrain type of 
    the cell. The higher the false negative rate for a cell, the more times we search the cell in order to offset the chance that 
    the target is contained within the cell and our agent just could not find it in that cell. 
'''

def improvedMAST(agent, target):
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
        # calculate the number of times to check a cell based on its terrain type
        # the number of checks for a given cell is simply 10 x (false negative rate)
        numChecks = int(agent.map[r][c].falseNegativeProbability * 10.0)
        for check in range(0, numChecks):
            searchResult = agent.searchCell(r, c, target)
            if searchResult == False:
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


