import random as rnd
from common import Agent, Cell, Target, manhattanDistance, numActions

'''
Run Walking Basic Agent 1 on a Stationary Target
1. Determine the cell with the highest probability of containing the target.
2. Walk the agent over to the highest probability cell and search it.
3. Create the scale factor based on the probability of the searched cell.
4. Update the probability of the searched cell using the scaling factor.
5. Update the probability of the remaining cells using the scaling factor.
6. Repeat at step 1 if the target was not found. 
'''

def rule1MAST(agent, target):
    r, c = (rnd.randint(0, agent.dim - 1), rnd.randint(0, agent.dim - 1))
    while(agent.hasFoundTarget == False):
        maxBelief = 0
        searchResult = agent.searchCell(r, c, target)
        prevr = r
        prevc = c

        if searchResult == False:

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
                    if i == prevr and j == prevc:
                        j += 1
                        continue

                    # Update the probabilities for the rest of the cells in the map
                    agent.map[i][j].probability = agent.map[i][j].probability / scale

                    # Keep track of the highest probability cell in the map
                    if agent.map[i][j].probability > maxBelief:
                        maxBelief = agent.map[i][j].probability
                        r = i
                        c = j
                    j += 1
                i += 1
            # Update the number of moves taken based on the distance to the searched cell
            numActions((prevr, prevc), (r, c), agent)

    return agent.numMoves