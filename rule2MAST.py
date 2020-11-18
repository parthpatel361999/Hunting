import random as rnd
from common import Agent, Target, numActions

'''
Run Walking Basic Agent 2 on a Stationary Target
1. Determine the cell with the highest probability of finding the target.
2. Walk the agent over to the highest scored cell and search it.
3. Update the belief state and score of the searched cell.
4. Update the belief state and score of the remaining cells using the scaling factor.
5. Repeat at step 1 if the target was not found. 
'''

def rule2MAST(agent, target):
    highest = 0
    r = c = 0

    # Set the initial scores
    for row in agent.map:
        for cell in row:
            cell.score = cell.probability * (1 - cell.falseNegativeProbability)
            if cell.score > highest:
                highest = cell.score
                r, c = cell.row, cell.col

    while(agent.hasFoundTarget == False):
        maxP = 0
        prevr = r
        prevc = c
        searchResult = agent.searchCell(r, c, target)
        if searchResult == False:

            # Calculate the scaling factor
            scale = 1 - agent.map[r][c].probability + \
                agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability

            # Update the belief state of the searched cell
            agent.map[r][c].probability = agent.map[r][c].probability * \
                agent.map[r][c].falseNegativeProbability
            i = 0
            while i < agent.dim:
                j = 0
                while j < agent.dim:
                    if i == prevr and j == prevc:
                        j += 1
                        continue

                    # Update the beleif state and score of all cells
                    agent.map[i][j].probability = agent.map[i][j].probability / scale
                    agent.map[i][j].score = agent.map[i][j].probability * \
                        (1 - agent.map[i][j].falseNegativeProbability)
                    
                    # Keep strack of the highest scored cell for the next search
                    if agent.map[i][j].score > maxP:
                        maxP = agent.map[i][j].score
                        numActions((r, c), (i, j), agent)
                        r = i
                        c = j
                    j += 1
                i += 1
    return agent.numMoves