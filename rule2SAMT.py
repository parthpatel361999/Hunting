import random as rnd
import numpy as np
from common import Agent, Target, maxInRange, maxOutRange, targetInRange

'''
Run Jumping Basic Agent 2 on a Moving Target with a Proximity Clue
1. Move the target.
2. Determine the cell with the highest probability of finding the target using the clue.
3. Search this cell.
4. Update the belief state and score of the searched cell.
5. Update the belief state and score of the remaining cells using the scaling factor.
6. Repeat at step 1 if the target was not found. 
'''

def rule2SAMTWithClue(agent, target):
    highest = 0
    r = c = 0

    # Set the initial scores
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while agent.hasFoundTarget == False:
        minScore = agent.dim ** 4
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)

        if searchResult == False:
            # Move the target
            target.move()

            # Generate a hint for the target
            withinFive = targetInRange(agent, target, prevr, prevc)

            # Calculate the scaling factor
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability

            # Update the probability of the searched cell
            agent.map[r][c].probability = agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # Update the probabilities and scores of all cells
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[i][j].falseNegativeProbability)
                    j = j + 1
                i = i + 1

            # Determine the next cell to search based on the proximity hint
            if withinFive:
                minScore, r, c = maxInRange(agent, prevr, prevc)
            else:
                minScore, r, c = maxOutRange(agent, prevr, prevc)

    return agent.numMoves

'''
Run Jumping Basic Agent 2 on a Moving Target without a Proximity Clue
1. Move the target.
2. Determine the cell with the highest probability of finding the target without using the clue.
3. Search this cell.
4. Update the belief state and score of the searched cell.
5. Update the belief state and score of the remaining cells using the scaling factor.
6. Repeat at step 1 if the target was not found. 
'''

def rule2SAMTWithoutClue(agent, target):
    highest = 0
    r = c = 0

    # Set the initial scores
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while agent.hasFoundTarget == False:
        maxP = 0
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)

        if searchResult == False:
            # Move the target
            target.move()

            # Calculate the scaling factor
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability

            # Update the probability of the searched cell
            agent.map[r][c].probability = agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if prevr == i and prevc == j:
                        j += 1
                        continue
                    # Update the probability and score of all cells
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[i][j].falseNegativeProbability)

                    # Keep track of the next cell to search
                    if agent.map[i][j].score > maxP:
                        maxP = agent.map[i][j].score
                        r = i
                        c = j
                    j = j + 1
                i = i + 1

    return agent.numMoves