import random as rnd
import numpy as np
from common import Agent, Target, maxInRange, maxOutRange, targetInRange

'''
Run Jumping Basic Agent 1 on a Moving Target with Proximity Clue
1. Move the target to a new location.
2. Determine the cell with the highest probability of containing the target with the clue.
3. Create the scale factor based on the probability of the searched cell.
4. Update the probability of the searched cell using the scaling factor.
5. Update the probability of the remaining cells using the scaling factor.
6. Repeat at step 1 if the target was not found. 
'''

def rule1SAMTWithClue(agent, target):
    highest = 0
    r = c = 0

    while agent.hasFoundTarget == False:
        minScore = agent.dim ** 4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)

        if searchResult == False:
            target.move()
            withinFive = targetInRange(agent, target, prevr, prevc)

            # Calculate the scaling factor
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability

            # Update the probability of the searched cell
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
                agent.map[r][c].probability
            agent.map[r][c].score = agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue

                    # Update the probability of the remaining cells
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability
                    j = j + 1
                i = i + 1
            
            # Find the best cell to search next
            if withinFive:
                minScore, r, c = maxInRange(agent, prevr, prevc)
            else:
                minScore, r, c = maxOutRange(agent, prevr, prevc)

    return agent.numMoves

'''
Run Jumping Basic Agent 1 on a Moving Target without Proximity Clue
1. Move the target to a new location.
2. Determine the cell with the highest probability of containing the target.
3. Create the scale factor based on the probability of the searched cell.
4. Update the probability of the searched cell using the scaling factor.
5. Update the probability of the remaining cells using the scaling factor.
6. Repeat at step 1 if the target was not found. 
'''

def rule1SAMTWithoutClue(agent, target):
    highest = 0
    r = c = 0

    while agent.hasFoundTarget == False:
        maxBelief = 0
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)

        if searchResult == False:
            target.move()

            # Calculate the scaling factor
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            
            # Update the probability of the searched cell
            agent.map[r][c].probability = agent.map[r][c].falseNegativeProbability * \
                agent.map[r][c].probability
            agent.map[r][c].score = agent.map[r][c].probability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # Update the probability of the remaining cells 
                    agent.map[i][j].probability = agent.map[i][j].probability / scale

                    # Keep track of the highest probability cell
                    if agent.map[i][j].probability > maxBelief:
                        maxBelief = agent.map[i][j].probability
                        r = i
                        c = j
                    j = j + 1
                i = i + 1

    return agent.numMoves