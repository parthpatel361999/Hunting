import random as rnd
import numpy as np
import copy 
import math
from common import Agent, Target, numActions, manhattanDistance


def ba3(agent, r, c, d = True): 
    #basicAgent 3 implementation. included d to stop scoring when not required.
    scale = 1.0 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
    agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability
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
            if d:
                dist = manhattanDistance((r,c), (i,j))
                agent.map[i][j].score = float(dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
                if ((minScore > agent.map[i][j].score)):
                    minScore = agent.map[i][j].score
                    new_r = i
                    new_c = j
            j = j + 1
        i = i + 1
    return (new_r, new_c)


def improvedAgent(agent, target,thresh):
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
            r,c = ba3(agent,r,c)
            if(agent.map[r][c].probability < thresh): #control thresh value
                agent2 = copy.deepcopy(agent) #create deep copy
                r,c = simulate(agent2,r,c)

            numActions((prevr, prevc), (r,c), agent)
    return agent.numMoves
def simulate(agent,r,c):
    #simulate failure of reality board's suggestion: 
    r1,c1 = ba3(agent,r,c,False)
    
    #pick representative cells for failures
    s = sample(agent.dim,agent.map)
    
    #induce failure across sample set
    for coords in s:
        ba3(agent,coords[0],coords[1],False)
    
    #score finder, can modularize further
    i = 0 
    minScore = -1
    new_r = new_c = 0
    while i < agent.dim:
        j = 0
        while j < agent.dim:
            if (i == r and j == c):
                j+=1
                continue
            dist = manhattanDistance((r1,c1), (i,j))
            agent.map[i][j].score = float(dist) / (agent.map[i][j].probability * (1 - agent.map[i][j].falseNegativeProbability))
            if ((minScore > agent.map[i][j].score) or minScore == -1):
                minScore = agent.map[i][j].score
                new_r = i
                new_c = j
            j += 1
        i += 1
    
    return (new_r,new_c)
def sample(dim,map):
    s = [] 
    reorg = [[],[],[],[]]
    
    #sort into different baskets
    for row in map:
        for item in row:
            if(item.falseNegativeProbability == 0.1):
                reorg[0].append((item.row,item.col))
            elif(item.falseNegativeProbability == 0.3):
                reorg[1].append((item.row,item.col))
            elif(item.falseNegativeProbability == 0.7):
                reorg[2].append((item.row,item.col))
            else:
                reorg[3].append((item.row,item.col))
    
    #random sampling. total size 0.2*dim^2 cells, with specified distribution in freq
    freq = [0.2,0.3,0.3,0.2] 
    cellfreq = []
    for i in freq:
        cellfreq.append(i*(dim**2)/5)
    i = 0 
    while i < ((dim**2)/5):
        if not cellfreq[0] and not cellfreq[1] and not cellfreq[2] and not cellfreq[3]:
            break
        rndterrain = rnd.randint(0,3)
        while cellfreq[rndterrain] == 0:
            rndterrain = rnd.randint(0,3)
        s.append(reorg[rndterrain].pop(rnd.randint(0,len(reorg[rndterrain])-1)))
        cellfreq[rndterrain] -= 1
        i += 1  
    return s

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



numTrials = 100
dim = 10
j = 0.1 #change j = 0 
while j <= 1:  #j <= 0 to quickly compare to BA3
    total = 0
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
        total += improvedAgent(agent, target,j)
    print("Average Moves Taken at threshold value " + str(j) + " : " + str(float(total / numTrials)))
    j+=0.1
