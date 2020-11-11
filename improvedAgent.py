import random as rnd
import numpy as np
import copy 
from common import Agent, Target, numActions, manhattanDistance

def simulateBA(agent,scale,r,c,it): 
    # current performance: iterating even 1 step into the future at every time step is causing failure.
    # this has to do with the fact that even when the probabilities are very high we still assume that there is a failure occuring
    # adding an addl conditional to check the prob value and skipping recursion if above thresh
    minScore = agent.dim**4
    new_r = r
    new_c = c
    i = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if i == r and j == c:
                j += 1
                continue
            agent.map[i][j].probability = agent.map[i][j].probability / scale
            dist = manhattanDistance((r,c), (i,j))
            agent.map[i][j].score = float(dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
            if ((minScore > agent.map[i][j].score)):
                minScore = agent.map[i][j].score
                new_r = i
                new_c = j
            j = j + 1
        i = i + 1
    
    if(it < 1 and agent.map[r][c].probability < 0.2): 
        '''
            TODO change conditional to following form: A - B*x (obviously if this makes sense)
            A = max iterations you allow on the first run through (ie we don't have enough info so we let the agent simulate several failures)
            B = how gradual we want the descent to be. 
            Other considerations: should B be a dynamic value? depending on the current performance, can we tweak this value? 
        '''
        nit = it
        nit+=1
        scale = 1.0 - agent.map[new_r][new_c].probability + agent.map[new_r][new_c].probability * agent.map[new_r][new_c].falseNegativeProbability
        agent2 = copy.deepcopy(agent) #is there any way to not use a deep copy here? 
        agent2.map[new_r][new_c].probability = agent2.map[new_r][new_c].falseNegativeProbability * agent2.map[new_r][new_c].probability
        return simulateBA(agent2,scale,new_r,new_c,nit)
    
    return (new_r, new_c)


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
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r,c, target)
        if searchResult == False:
            scale = 1.0 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability
            r,c = simulateBA(agent,scale,r,c,0)
            numActions((prevr, prevc), (r,c), agent)
    return agent.numMoves

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
numTrials = 50
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