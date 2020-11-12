import random as rnd
import numpy as np
import copy 
from common import Agent, Target, numActions, manhattanDistance

def simulateBA(agent,scale, r, c): 
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
    return (new_r, new_c,agent.map[new_r][new_c].probability)
    #return (new_r, new_c,agent.map[new_r][new_c].score)


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
            
            r1,c1,prob = simulateBA(agent,scale,r,c)
            #r1,c1,score1 = simulateBA(agent,scale,r,c)
            
            #assume r,c are going to prove to be false 
            agent2 = copy.deepcopy(agent) #create deep copy
            

            scale = 1.0 - agent.map[r1][c1].probability + agent.map[r1][c1].probability * agent.map[r1][c1].falseNegativeProbability
            agent2.map[r1][c1].probability = agent2.map[r1][c1].falseNegativeProbability * agent2.map[r1][c1].probability
            
            r2,c2,prob = simulateBA(agent2,scale,r1,c1) #run the deep copy through the simulation
            #r2,c2,score2 = simulateBA(agent2,scale,r1,c1)
            
            
            dist = manhattanDistance((r,c), (r2,c2))
            fnrc = 1.0 - agent.map[r2][c2].falseNegativeProbability
            agent.map[r2][c2].score = float(dist) / ((agent.map[r2][c2].probability * fnrc) + (1-(agent.map[r2][c2].probability*fnrc)*prob))
            
            #if(score1 < score2):
            if(agent.map[r1][c1].score < agent.map[r2][c2].score):
                r = r1
                c = c1
            else: 
                r = r2
                c = c2
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