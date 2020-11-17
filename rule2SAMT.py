import random as rnd

import numpy as np

from common import Agent, Target, maxInRange, maxOutRange, targetInRange

'''
    to be compared to rule 2, so used the rule two probability updates
'''


def rule2SAMTWithClue(agent, target):
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
                    # dist = manhattanDistance((prevr,prevc), (i,j))
                    # agent.map[i][j].score = (1 + float(dist)) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    j = j + 1
                i = i + 1

            if withinFive:
                minScore, r, c = maxInRange(agent, prevr, prevc)
            else:
                minScore, r, c = maxOutRange(agent, prevr, prevc)

    return agent.numMoves


def rule2SAMTWithoutClue(agent, target):
    highest = 0
    r = c = 0

    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while agent.hasFoundTarget == False:
        maxP = 0
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        #print('searched cell: ', (prevr,prevc))
        #print('Target Position: ', target.position)

        if searchResult == False:
            target.move()
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

                    if agent.map[i][j].score > maxP:
                        maxP = agent.map[i][j].score
                        r = i
                        c = j
                    # dist = manhattanDistance((prevr,prevc), (i,j))
                    # agent.map[i][j].score = (1 + float(dist)) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    j = j + 1
                i = i + 1

    return agent.numMoves
# total = 0
# numTrials = 10
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
#     total += movingTarget2(agent, target)
# print("Average Moves Taken: " + str(float(total / numTrials)))
