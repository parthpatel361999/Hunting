import random as rnd

from common import Agent, Cell, Target


def basicAgent2(agent, target):
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
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[r][c].falseNegativeProbability)
                    if agent.map[i][j].score > maxP:
                        maxP = agent.map[i][j].score
                        r = i
                        c = j
                    j += 1
                i += 1
        # displayProbabilities(agent)
        # print()
    return agent.numMoves


def displayProbabilities(agent):
    for r in agent.map:
        for cell in r:
            print("{:.5f}".format(cell.probability), end='  ')
        print()


total = 0
numTrials = 100
for i in range(numTrials):
    agent = Agent(10)
    target = Target(10)
    while agent.map[target.position[0]][target.position[1]].falseNegativeProbability == 0.9:
        target = Target(10)
    # for r in agent.map:
    #     for cell in r:
    #         print(cell.falseNegativeProbability, end='  ')
    #     print()
    # print(target.position)
    total += basicAgent2(agent, target)
print("Average Moves Taken: " + str(float(total / numTrials)))
