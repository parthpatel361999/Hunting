import random as rnd
import numpy as np
import copy 
from queue import PriorityQueue 
from common import Agent, Target, numActions, manhattanDistance, targetInRange, minInRange, minOutRange, withinRange5, at6

def ba3(agent, r, c): 
    scale = 1.0 - agent.map[r][c].probability + agent.map[r][c].probability * agent.map[r][c].falseNegativeProbability
    agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * agent.map[r][c].probability        
    minScore = -1
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
            if ((minScore > agent.map[i][j].score) or minScore == -1):
                minScore = agent.map[i][j].score
                new_r = i
                new_c = j
            j = j + 1
        i = i + 1
    return (new_r, new_c)


def improvedAgent(agent, target,thresh=0.2):
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
        searchResult = agent.searchCell(r,c, target) # search cell
        withinFive = targetInRange(agent, target, r, c) # check if within 5
        if searchResult == False: # if not found
            r,c = ba3(agent,r,c) #normalize board
            if not withinFive: # if outside
                minScore, r, c = minOutRange(agent, prevr, prevc) # find best score in cells outside
                numActions((prevr, prevc), (r,c), agent) # increment actions
                continue 
            else: # if within 5 
                minScore, r, c = minInRange(agent, prevr, prevc) # find best score in cells within 5
                r,c = improvement(agent,target,r,c,prevr,prevc) # run improvement
           
            if(r == -1 and c == -1): 
                break

    return agent.numMoves

def improvement(agent,target,r,c,prevr,prevc,thresh=0.2):
    pathHighs = []
    #check if recommended same location
    if(r == prevr and c ==prevc):
        agent.searchCell(r,c,target)
        ret_r,ret_c = ba3(agent,r,c)
        return ret_r,ret_c
    
    #generate path
    path1, path2 = pathwalk(prevr,prevc,r,c)
    if path1 == path2:
        path = path1
        pathHighs = findHighestinRoom(agent, path, thresh)
    else:
    #highest probability path
        path1probs, pathHigh1 = findHighestinRoom(agent,path1,thresh)
        path2probs, pathHigh2 = findHighestinRoom(agent, path2, thresh)
        if path1probs[0] <= path2probs[0]: # check this conditional because of the whole 1 - prob thing for the queue
            path = path1 
            pathHighs = pathHigh1
        else:
            path = path2
            pathHighs = pathHigh2
        
    #walkthrough the path
    i = 0
    found = False #indicator variable
    ret_r = r
    ret_c = c

    inMH = True

    for item in path: #walk through path
        if(item in pathHighs): #check if in pathhigh
            if(not agent.searchCell(item[0],item[1],target)): #search
                ret_r, ret_c = ba3(agent,item[0],item[1])
                inMH = targetInRange(agent, target, r, c) # boolean if target is on in range
                if not inMH:
                    # we know that it is within 6 of the original spot, so pick out of those
                    minScore, ret_r, ret_c = minInRange(agent,prevr,prevc, f=at6)
                    i+=1
                    break
            else:
                found = True
                break
        i += 1
    numActions((prevr,prevc),path[i-1],agent)

    if(not found):
        return (ret_r,ret_c)
    else:
        return (-1,-1)
def pathwalk(prevr,prevc,r,c):
    #L-shaped trajectory
    path1 = []
    path2 = []
    
    if(prevr <= r): # up to down 
        ctr = prevr
        while ctr < r: 
            path1.append((ctr,prevc))
            ctr += 1
    else:   # down to up
        ctr = prevr
        while ctr > r:
            path1.append((ctr,prevc))
            ctr -= 1
    if(prevc <= c): # left to right
        ctr = prevc
        while ctr <= c: 
            path1.append((r,ctr))
            ctr += 1
    else:   # right to left
        ctr = prevc
        while ctr >= c:
            path1.append((r,ctr))
            ctr -= 1
     # path 2
    if(prevc <= c): # left to right
        ctr = prevc
        while ctr < c: 
            path2.append((prevr,ctr))
            ctr += 1
    else:   #  right to left
        ctr = prevc
        while ctr > c:
            path2.append((prevr,ctr))
            ctr -= 1
    if(prevr <= r): # up to down
        ctr = prevr
        while ctr <= r: 
            path2.append((ctr,c))
            ctr += 1
    else:   # left to right
        ctr = prevr
        while ctr >= r:
            path2.append((ctr,c))
            ctr -= 1
   # path2 = reverseTuples(path1)

    return path1,path2

def findHighestinRoom(agent,path,thresh=0.2):
    #path has following format: [coord1,coord2] where coord = (row,col)
    highestPath = []
    probHighs = []
    q = PriorityQueue()
    #loop through list and take the complement because its a minQ
    for p in path: 
        q.put((1.0-agent.map[p[0]][p[1]].probability,p))
    
    #pop thresh*qsize values (ie top x% of probabilities)
    totalpop = 1
    while(totalpop > 0):
        temp = q.get()
        probHighs.append(temp[0])
        highestPath.append(temp[1])
        totalpop-=1
    # print(probHighs)
    # print(highestPath)
    return probHighs,highestPath # return list of tuples

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
total = 0
j = 0.1
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
print("Average Moves Taken at threshold value " + str(0.2) + " : " + str(float(total / numTrials)))