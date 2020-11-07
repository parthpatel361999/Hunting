from common import Target, Agent, Cell
import random as rnd

def basicAgent1(agent, target):
    r, c = (rnd.randint(0, agent.dim - 1), rnd.randint(0, agent.dim - 1))
    while(agent.hasFoundTarget == False):
        maxBelief = 0
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:
            scale = 1 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    if agent.map[i][j].probability > maxBelief:
                        maxBelief = agent.map[i][j].probability
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

agent = Agent(5)
target = Target(5)
for r in agent.map:
    for cell in r:
        print(cell.falseNegativeProbability, end='  ')
    print()
print(target.position)
print("Moves Taken: " + str(basicAgent1(agent, target)))