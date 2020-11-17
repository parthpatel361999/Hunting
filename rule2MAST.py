import random as rnd

from common import Agent, Target, numActions


def rule2MAST(agent, target):
    highest = 0
    r = c = 0
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while(agent.hasFoundTarget == False):
        maxP = 0
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if i == prevr and j == prevc:
                        j += 1
                        continue
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[i][j].falseNegativeProbability)
                    if agent.map[i][j].score > maxP:
                        maxP = agent.map[i][j].score
                        numActions((r, c), (i, j), agent)
                        r = i
                        c = j
                    j += 1
                i += 1
            #numActions((prevr, prevc), (r,c), agent)
        # print("probs:")
        # displayProbabilities(agent)
        # print("scores:")
        # displayScores(agent)
        # input()
        # print()
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


# total = 0
# numTrials = 1
# dim = 50
# for i in range(numTrials):
#     agent = Agent(dim)
#     target = Target(dim)
#     # for r in agent.map:
#     #     for cell in r:
#     #         print(cell.falseNegativeProbability, end='  ')
#     #     print()
#     # print(target.position)
#     total += rule2MAST(agent, target)
# print("Average Moves Taken: " + str(float(total / numTrials)))