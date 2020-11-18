import random as rnd
import time

from common import Agent, Target, manhattanDistance, numActions


def rule3MAST(agent, target):
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


# def displayScores(agent):
#     for r in agent.map:
#         for cell in r:
#             print("{:.5f}".format(cell.score), end='  ')
#         print()


# def displayProbabilities(agent):
#     for r in agent.map:
#         for cell in r:
#             print("{:.5f}".format(cell.probability), end='  ')
#         print()


total = 0
numTrials = 20
dim = 30
for i in range(numTrials):
    startTime = time.time()
    agent = Agent(dim)
    target = Target(dim)
    total += rule3MAST(agent, target)
    print("iteration", str(i) + ":", time.time() - startTime)
print("Average Moves Taken: " + str(float(total / numTrials)))
