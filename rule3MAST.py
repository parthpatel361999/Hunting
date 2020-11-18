import random as rnd
import time

from common import Agent, Target, manhattanDistance, numActions

'''
    This is Basic Agent 3 for the stationary target. We initialize all cells with their respective probabilities 
    in the first for loop and select the first cell that we want to explore. After exploring that first cell, we start to pick
    the next cells to explore by using the score of their Manhattan Distance divided by their probability. The minimum "score"
    cell is the one that we travel to from here on. 
'''
def rule3MAST(agent, target):
    highest = 0
    r = c = 0
    # the initializing of the first probabilities (no score here)
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    # while the target has not been found, keep searching cells
    while (agent.hasFoundTarget == False):
        minScore = agent.dim**4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:
            # update the probabilties of the cell we just searched
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
                agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    # if we reach the same cell that we already updated, skip, as the distance will be zero and this will always be the lowest scored cell
                    if i == prevr and j == prevc:
                        j += 1
                        continue
                    # update the probabilties of each of the other cells in the board
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    # update the score of each of the other cells in the board. 
                    dist = manhattanDistance((prevr, prevc), (i, j))
                    agent.map[i][j].score = (1 + float(dist)) / (
                        agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    if minScore > agent.map[i][j].score:
                        minScore = agent.map[i][j].score
                        r = i
                        c = j
                    j = j + 1
                i = i + 1
            # imcrement number of actions between the previous cell and the one we have just explored
            numActions((prevr, prevc), (r, c), agent)

    return agent.numMoves