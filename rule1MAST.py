import random as rnd

from common import Agent, Cell, Target, manhattanDistance, numActions


def rule1MAST(agent, target):
    r, c = (rnd.randint(0, agent.dim - 1), rnd.randint(0, agent.dim - 1))
    while(agent.hasFoundTarget == False):
        maxBelief = 0
        searchResult = agent.searchCell(r, c, target)
        prevr = r
        prevc = c

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
                    if agent.map[i][j].probability > maxBelief:
                        maxBelief = agent.map[i][j].probability
                        r = i
                        c = j
                    j += 1
                i += 1
            numActions((prevr, prevc), (r, c), agent)

        # displayProbabilities(agent)
        # print()
    return agent.numMoves


# total = 0
# numTrials = 20
# dim = 50
# for i in range(numTrials):
#     agent = Agent(dim)
#     target = Target(dim)
#     # for r in agent.map:
#     #     for cell in r:
#     #         print(cell.falseNegativeProbability, end='  ')
#     #     print()
#     # print(target.position)
#     total += basicAgent1(agent, target)
# print("Average Moves Taken: " + str(float(total / numTrials)))
