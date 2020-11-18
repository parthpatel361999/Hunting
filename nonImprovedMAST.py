import copy
import random as rnd
import time
from queue import PriorityQueue

import numpy as np

from common import Agent, Target, manhattanDistance, numActions

'''
    This was the initial improved agent for stationary target that we came up with that performed only marginally better than Basic Agent 3.
    The algorithm was to initially use the mechanics of basic agent 3 and simply build off of that. As we are moving to the new cell to search,
    we simply choose a small subset of cells along that path to search as we are traversing the board. The subset is based which cells 
    along the path have the minimum score based on basic agent 3. Note that because this algorithm was built off of the mechanics
    of basic agent 3, the scores of each cell are calculated the same as they were for basic agent 3. 
'''

# used to continually recalculate the scores and probabilities of each cell using the same mechanics as basic agent 3
def ba3(agent, r, c):
    scale = 1.0 - agent.map[r][c].probability + \
        agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
    agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
        agent.map[r][c].probability
    minScore = -1
    new_r = r
    new_c = c
    i = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if i == r and j == c:
                j += 1
                continue
            agent.map[i][j].probability = agent.map[i][j].probability / scale
            dist = manhattanDistance((r, c), (i, j))
            agent.map[i][j].score = float(
                dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
            if ((minScore > agent.map[i][j].score) or minScore == -1):
                minScore = agent.map[i][j].score
                new_r = i
                new_c = j
            j = j + 1
        i = i + 1
    return (new_r, new_c)

'''
    The actual improved agent
'''
def improvedMAST(agent, target, thresh=0.2):
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
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:
            r, c = ba3(agent, r, c)
            r, c = improvementMAST(agent, target, r, c, prevr, prevc, thresh)
            if(r == -1 and c == -1):
                break

    return agent.numMoves

'''
    This function implements the searching along the path as we are traveling to a new cell to search. Probabilities and scores 
    are recalculated each time we search a cell. 
'''
def improvementMAST(agent, target, r, c, prevr, prevc, thresh):

    # check if recommended same location
    if(r == prevr and c == prevc):
        agent.searchCell(r, c, target)
        ret_r, ret_c = ba3(agent, r, c)
        return ret_r, ret_c

    # generate path
    path = pathwalkMAST(prevr, prevc, r, c)

    # highest probability path
    pathHigh = findHighestinRoomMAST(agent, path, thresh)

    # walkthrough the path
    i = 0
    found = False  # indicator variable
    ret_r = r
    ret_c = c
    for item in path:  # walk through path
        if(item in pathHigh):  # check if in pathhigh
            if(not agent.searchCell(item[0], item[1], target)):  # search
                ret_r, ret_c = ba3(agent, item[0], item[1])
            else:
                found = True
                break
        i += 1
    numActions((prevr, prevc), path[i-1], agent)

    if(not found):
        return (ret_r, ret_c)
    else:
        return (-1, -1)

'''
    This function determines the path that the agent will take to reach the next cell that the algorithm.
    This function can be expanded to find the most weighted path to take as we arbitrarily decided a path each iteration. 
'''
def pathwalkMAST(prevr, prevc, r, c):
    # L-shaped trajectory
    path = []
    if(prevr <= r):
        ctr = prevr
        while ctr < r:
            path.append((ctr, prevc))
            ctr += 1
    else:
        ctr = prevr
        while ctr > r:
            path.append((ctr, prevc))
            ctr -= 1
    if(prevc <= c):
        ctr = prevc
        while ctr <= c:
            path.append((r, ctr))
            ctr += 1
    else:
        ctr = prevc
        while ctr >= c:
            path.append((r, ctr))
            ctr -= 1
    return path

'''
    This function finds the subset of cells along the path for the agent to search based on the best scores to search. 
'''
def findHighestinRoomMAST(agent, path, thresh):
    # path has following format: [coord1,coord2] where coord = (row,col)
    highestPath = []
    q = PriorityQueue()
    # loop through list and take the complement because its a minQ
    for p in path:
        q.put((1.0-agent.map[p[0]][p[1]].probability, p))

    # pop thresh*qsize values (ie top x% of probabilities)
    totalpop = int(thresh*q.qsize())
    while(totalpop > 0):
        highestPath.append(q.get()[1])
        totalpop -= 1

    return highestPath  # return list of tuples
