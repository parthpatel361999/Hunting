import random as rnd
import numpy as np
from common import Agent, Target, numActions, manhattanDistance



def improvedAgent(agent, target):
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
        searchResult = agent.searchCell(r,c, target)
        if searchResult == False:
            scale = 1 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if i == prevr and j == prevc:
                        j += 1
                        continue
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    dist = manhattanDistance((prevr,prevc), (i,j))
                    agent.map[i][j].score = float(dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                    if minScore > agent.map[i][j].score:
                        minScore = agent.map[i][j].score
                        r = i
                        c = j
                    j = j + 1
                i = i + 1
            (r,c) = improvementFunction()
            numActions((prevr, prevc), (r,c), agent)

    return agent.numMoves
'''
What we need: 
-minScore
-Standard deviation of set
go one st dev above the minscore
get all the coordinates of scores between, inclusive, of minscore and minscore+1stdev
rank all scores by distance (recalculate dist using coordinates and prevr and prevc)
select the highest score with the lowest manhattan distance, visit there

improvementFunction(agent.map, minScore, msr, msc, prevr, prevc) returns (nextr,nextc) 

'''

def improvementFunction(agent, minScore, msr, msc, prevr, prevc): 
    listProb = list(np.concatenate(agent.map).flat)
    approvedDict = {}
    std = np.std(listProb)
    for row in agent.map: 
        for i in row: 
            if(i.score <= minScore+std):
                approvedDict[(i.row,i.col)] = (manhattanDistance((prevr,prevc),(i.row,i.col)),i.score)
    
    return (nextr, nextc)

def displayScores(agent):
    for r in agent.map:
        for cell in r:
            print("{:.5f}".format(cell.score), end='  ')
        print()


def displayProbabilities(agent):
    for r in agent.map:
        for cell in r:
            print("{:.5f}".format(cell.probability), end='  ')
        print()


total = 0
numTrials = 100
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
    total += improvedAgent(agent, target)
print("Average Moves Taken: " + str(float(total / numTrials)))
