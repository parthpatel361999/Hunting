import copy
import random as rnd
import time
from queue import PriorityQueue

import numpy as np

from common import Agent, Target, manhattanDistance, numActions


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


# def ba3(agent, r, c):
#     scale = 1.0 - agent.map[r][c].probability + \
#         agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
#     agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
#         agent.map[r][c].probability
#     minScore = -1
#     new_r = r
#     new_c = c
#     i = 0
#     while i < agent.dim:
#         j = 0
#         while j < agent.dim:
#             if i == r and j == c:
#                 j += 1
#                 continue
#             agent.map[i][j].probability = agent.map[i][j].probability / scale
#             dist = manhattanDistance((r, c), (i, j))
#             agent.map[i][j].score = float(
#                 dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
#             if ((minScore > agent.map[i][j].score) or minScore == -1):
#                 minScore = agent.map[i][j].score
#                 new_r = i
#                 new_c = j
#             j = j + 1
#         i = i + 1
#     return (new_r, new_c)


# def improvedMAST(agent, target, thresh=0.2):
#     highest = 0
#     r = c = 0
#     for row in agent.map:
#         for cell in row:
#             cell.score = cell.probability * (1 - cell.falseNegativeProbability)
#             # dist = float(manhattanDistance((r,c), (i,j)))
#             # agent.map[i][j].score = dist / agent.map[i][j].score
#             if cell.score > highest:
#                 highest = cell.score
#                 r, c = cell.row, cell.col

#     while (agent.hasFoundTarget == False):
#         prevr = r
#         prevc = c
#         searchResult = agent.searchCell(r, c, target)
#         if searchResult == False:
#             r, c = ba3(agent, r, c)
#             r, c = improvementMAST(agent, target, r, c, prevr, prevc, thresh)
#             if(r == -1 and c == -1):
#                 break

#     return agent.numMoves


# def improvementMAST(agent, target, r, c, prevr, prevc, thresh):

#     # check if recommended same location
#     if(r == prevr and c == prevc):
#         agent.searchCell(r, c, target)
#         ret_r, ret_c = ba3(agent, r, c)
#         return ret_r, ret_c

#     # generate path
#     path = pathwalkMAST(prevr, prevc, r, c)

#     # highest probability path
#     pathHigh = findHighestinRoomMAST(agent, path, thresh)

#     # walkthrough the path
#     i = 0
#     found = False  # indicator variable
#     ret_r = r
#     ret_c = c
#     for item in path:  # walk through path
#         if(item in pathHigh):  # check if in pathhigh
#             if(not agent.searchCell(item[0], item[1], target)):  # search
#                 ret_r, ret_c = ba3(agent, item[0], item[1])
#             else:
#                 found = True
#                 break
#         i += 1
#     numActions((prevr, prevc), path[i-1], agent)

#     if(not found):
#         return (ret_r, ret_c)
#     else:
#         return (-1, -1)


# def pathwalkMAST(prevr, prevc, r, c):
#     # L-shaped trajectory
#     path = []
#     if(prevr <= r):
#         ctr = prevr
#         while ctr < r:
#             path.append((ctr, prevc))
#             ctr += 1
#     else:
#         ctr = prevr
#         while ctr > r:
#             path.append((ctr, prevc))
#             ctr -= 1
#     if(prevc <= c):
#         ctr = prevc
#         while ctr <= c:
#             path.append((r, ctr))
#             ctr += 1
#     else:
#         ctr = prevc
#         while ctr >= c:
#             path.append((r, ctr))
#             ctr -= 1
#     return path


# def findHighestinRoomMAST(agent, path, thresh):
#     # path has following format: [coord1,coord2] where coord = (row,col)
#     highestPath = []
#     q = PriorityQueue()
#     # loop through list and take the complement because its a minQ
#     for p in path:
#         q.put((1.0-agent.map[p[0]][p[1]].probability, p))

#     # pop thresh*qsize values (ie top x% of probabilities)
#     totalpop = int(thresh*q.qsize())
#     while(totalpop > 0):
#         highestPath.append(q.get()[1])
#         totalpop -= 1

#     return highestPath  # return list of tuples


# # def displayScores(agent):
# #     for r in agent.map:
# #         for cell in r:
# #             print("{:.5f}".format(cell.score), end='  ')
# #         print()


# # def displayProbabilities(agent):
# #     for r in agent.map:
# #         for cell in r:
# #             print("{:.5f}".format(cell.probability), end='  ')
# #         print()


# total = 0
# numTrials = 20
# dim = 30
# for i in range(numTrials):
#     startTime = time.time()
#     agent = Agent(dim)
#     target = Target(dim)
#     total += improvedMAST(agent, target)
#     print("iteration", str(i) + ":", time.time() - startTime)
# print("Average Moves Taken: " + str(float(total / numTrials)))
