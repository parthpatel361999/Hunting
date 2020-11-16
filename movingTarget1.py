from common import targetInRange, maxInRange, maxOutRange, Agent, Target
import random as rnd
import numpy as np

'''
    to be compared to rule 1, so used the rule one probability updates
'''
def movingTarget1(agent, target):
    highest = 0
    r = c = 0

    # for row in agent.map:
    #     for cell in row:
    #         cell.score = cell.probability * (1 - cell.falseNegativeProbability)
    #         if cell.score > highest:
    #             highest = cell.score
    #             r, c = cell.row, cell.col

    while agent.hasFoundTarget == False:
        minScore = agent.dim ** 4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r,c,target)
        #print('searched cell: ', (prevr,prevc))
        #print('Target Position: ', target.position)
        
        if searchResult == False:
            withinFive = targetInRange(agent, target, prevr, prevc)
            #print('target in range? ', withinFive)
            scale = 1 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability
            agent.map[r][c].score = agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability
                    j = j + 1
                i = i + 1
            
            if withinFive: 
                minScore, r, c = maxInRange(agent, prevr, prevc)
            else: 
                minScore, r, c = maxOutRange(agent, prevr, prevc)
            target.move()
    return agent.numMoves



# agent = Agent(12)
# y = withinRange5(agent,5,5)
# print(len(y))

total = 0
numTrials = 10
dim = 10
for i in range(numTrials):
    agent = Agent(dim)
    target = Target(dim)
    while agent.map[target.position[0]][target.position[1]].falseNegativeProbability == 0.9:
        target = Target(dim)
    # for r in agent.map:
    #     for cell in r:
    #         print(cell.falseNegativeProbability, end='  ')
    #     print()
    # print(target.position)
    total += movingTarget1(agent, target)
print("Average Moves Taken: " + str(float(total / numTrials)))