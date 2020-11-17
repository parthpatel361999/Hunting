import copy
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from common import Agent, Target
from improvedMAMT import improvedMAMTWithClue, improvedMAMTWithoutClue
from improvedMAMTExtra import improvedMAMTExtra
from improvedMAST import improvedMAST
from rule1MAST import rule1MAST
from rule1SAMT import rule1SAMTWithClue, rule1SAMTWithoutClue
from rule1SAST import rule1SAST
from rule2MAST import rule2MAST
from rule2SAMT import rule2SAMTWithClue, rule2SAMTWithoutClue
from rule2SAST import rule2SAST
from rule3MAMT import rule3MAMTWithClue, rule3MAMTWithoutClue
from rule3MAMTExtra import rule3MAMTExtra
from rule3MAST import rule3MAST


def testRules(rules, dim=50, maps=30, iterationsPerMap=30):
    averageSearches = {}
    averageMovements = {}
    averageActions = {}
    actionMeans = {}
    actionVariances = {}
    for rule in rules:
        averageSearches[rule.__name__] = []
        averageMovements[rule.__name__] = []
        averageActions[rule.__name__] = []
        actionMeans[rule.__name__] = []
        actionVariances[rule.__name__] = []

    for i in range(0, maps):
        startTime = time.time()

        searchTotals = {}
        movementTotals = {}
        actionTotals = {}
        for rule in rules:
            searchTotals[rule.__name__] = 0
            movementTotals[rule.__name__] = 0
            actionTotals[rule.__name__] = []

        agent = Agent(dim)
        fixedMap = copy.deepcopy(agent.map)
        target = Target(dim)

        for j in range(0, iterationsPerMap):
            startTimeInner = time.time()

            for rule in rules:
                rule(agent, target)
                searchTotals[rule.__name__] += agent.searches
                movementTotals[rule.__name__] += agent.movements
                actionTotals[rule.__name__].append(
                    agent.searches + agent.movements)
                agent.reset(fixedMap)

            _target = Target(dim)
            while _target.position == target.position:
                _target = Target(dim)
            target = _target

            print("\tMap", str(i), "iteration", str(j), "took",
                  str(time.time() - startTimeInner), "seconds")

        for rule in rules:
            averageSearches[rule.__name__].append(
                searchTotals[rule.__name__] / iterationsPerMap)
            averageMovements[rule.__name__].append(
                movementTotals[rule.__name__] / iterationsPerMap)
            averageActions[rule.__name__].append(
                (searchTotals[rule.__name__] + movementTotals[rule.__name__]) / iterationsPerMap)
            actionMeans[rule.__name__].append(
                np.average(actionTotals[rule.__name__]))
            actionVariances[rule.__name__].append(
                np.var(actionTotals[rule.__name__]))

        print("Map", str(i), "took", str(time.time() - startTime), "seconds")

    return averageSearches, averageMovements, averageActions, actionMeans, actionVariances


def writeToFile(testNum, dataFile, rules, testMeans, testVariances, testActions):
    dataFile.write("\nTEST" + str(testNum) + "\n")
    for rule in rules:
        dataFile.write("\t" + rule.__name__ + "\n")
        for i in range(0, maps):
            dataFile.write("\t\t" + str(testMeans[rule.__name__][i]) + ", " + str(
                testVariances[rule.__name__][i]) + "\n")
        dataFile.write("\tOVERALL: " + str(np.average(testActions[rule.__name__])) +
                       ", " + str(np.var(testActions[rule.__name__])) + "\n")
    dataFile.write("\n")


if __name__ == "__main__":

    dim = 30
    maps = 30
    iterationsPerMap = 30
    ind = np.arange(maps)
    width = 0.2

    dataFile = open("graphs/data.txt", "a")
    dataFile.write("******************************\n")
    dataFile.write("START TEST " +
                   datetime.now().strftime("%m/%d/%Y %H:%M:%S") + "\n")
    dataFile.write("******************************\n")

    """
    Part 1-3
    """
    rules = [rule1SAST, rule2SAST]
    testSearches, testMovements, testActions, testMeans, testVariances = testRules(
        rules, dim, maps, iterationsPerMap)
    figure = plt.figure(figsize=((10., 6.)))
    plt.bar(
        ind, testSearches[rule1SAST.__name__], width, label="Rule 1 Searches", color="red")
    plt.bar(ind + width,
            testSearches[rule2SAST.__name__], width, label="Rule 2 Searches", color="gold")
    plt.ylabel("Searches")
    plt.xlabel("Map")
    plt.title("Stationary Agent, Stationary Target")
    plt.xticks(ind + width/2, list(range(1, maps + 1)))
    plt.legend(loc="best")
    plt.savefig("graphs/1.png")
    plt.close(figure)
    writeToFile(1, dataFile, rules, testMeans, testVariances, testActions)

    """
    Part 1-4
    """
    rules = [rule1MAST, rule2MAST, rule3MAST, improvedMAST]
    testSearches, testMovements, testActions, testMeans, testVariances = testRules(
        rules, dim, maps, iterationsPerMap)
    figure = plt.figure(figsize=((10., 6.)))
    plt.bar(
        ind, testSearches[rule1MAST.__name__], width, label="Rule 1 Searches", bottom=testMovements[rule1MAST.__name__], color="red")
    plt.bar(
        ind, testMovements[rule1MAST.__name__], width, label="Rule 1 Movements", color="darkred")
    plt.bar(ind + width,
            testSearches[rule2MAST.__name__], width, label="Rule 2 Searches", bottom=testMovements[rule2MAST.__name__], color="gold")
    plt.bar(ind + width,
            testMovements[rule2MAST.__name__], width, label="Rule 2 Movements", color="goldenrod")
    plt.bar(
        ind + width * 2, testSearches[rule3MAST.__name__], width, label="Rule 3 Searches", bottom=testMovements[rule3MAST.__name__], color="lightgreen")
    plt.bar(
        ind + width * 2, testMovements[rule3MAST.__name__], width, label="Rule 3 Movements", color="green")
    plt.bar(ind + width * 3,
            testSearches[improvedMAST.__name__], width, label="Improved Agent Searches", bottom=testMovements[improvedMAST.__name__], color="blue")
    plt.bar(ind + width * 3,
            testMovements[improvedMAST.__name__], width, label="Improved Agent Movements", color="darkblue")
    plt.ylabel("Actions")
    plt.xlabel("Map")
    plt.title("Moving Agent, Stationary Target")
    plt.xticks(ind + width * 1.5, list(range(1, maps + 1)))
    plt.legend(loc="best")
    plt.savefig("graphs/2.png")
    plt.close(figure)
    writeToFile(2, dataFile, rules, testMeans, testVariances, testActions)

    """
    Part 2-1
    """
    rules = [rule1SAMTWithoutClue, rule1SAMTWithClue,
             rule2SAMTWithoutClue, rule2SAMTWithClue]
    testSearches, testMovements, testActions, testMeans, testVariances = testRules(
        rules, dim, maps, iterationsPerMap)
    figure = plt.figure(figsize=((10., 6.)))
    plt.bar(
        ind, testSearches[rule1SAMTWithoutClue.__name__], width, label="Rule 1 Searches (No Clue)", color="red")
    plt.bar(ind + width,
            testSearches[rule1SAMTWithClue.__name__], width, label="Rule 1 Searches (w/ Clue)", color="gold")
    plt.bar(
        ind + width * 2, testSearches[rule2SAMTWithoutClue.__name__], width, label="Rule 2 Searches (No Clue)", color="lightgreen")
    plt.bar(ind + width * 3,
            testSearches[rule2SAMTWithClue.__name__], width, label="Rule 2 Searches (w/ Clue)", color="green")
    plt.ylabel("Actions")
    plt.xlabel("Map")
    plt.title("Stationary Agent, Moving Target")
    plt.xticks(ind + width * 1.5, list(range(1, maps + 1)))
    plt.legend(loc="best")
    plt.savefig("graphs/3.png")
    plt.close(figure)
    writeToFile(3, dataFile, rules, testMeans, testVariances, testActions)

    """
    Part 2-2
    """
    rules = [rule3MAMTWithoutClue, rule3MAMTWithClue,
             improvedMAMTWithoutClue, improvedMAMTWithClue]
    testSearches, testMovements, testActions, testMeans, testVariances = testRules(
        rules, dim, maps, iterationsPerMap)
    figure = plt.figure(figsize=((10., 6.)))
    plt.bar(
        ind, testSearches[rule3MAMTWithoutClue.__name__], width, label="Rule 3 Searches (No Clue)", bottom=testMovements[rule3MAMTWithoutClue.__name__], color="red")
    plt.bar(
        ind, testMovements[rule3MAMTWithoutClue.__name__], width, label="Rule 3 Movements (No Clue)", color="darkred")
    plt.bar(ind + width,
            testSearches[rule3MAMTWithClue.__name__], width, label="Rule 3 Searches (w/ Clue)", bottom=testMovements[rule3MAMTWithClue.__name__], color="gold")
    plt.bar(ind + width,
            testMovements[rule3MAMTWithClue.__name__], width, label="Rule 3 Movements (w/ Clue)", color="goldenrod")
    plt.bar(
        ind + width * 2, testSearches[improvedMAMTWithoutClue.__name__], width, label="Improved Agent Searches (No Clue)", bottom=testMovements[improvedMAMTWithoutClue.__name__], color="lightgreen")
    plt.bar(
        ind + width * 2, testMovements[improvedMAMTWithoutClue.__name__], width, label="Improved Agent Movements (No Clue)", color="green")
    plt.bar(ind + width * 3,
            testSearches[improvedMAMTWithClue.__name__], width, label="Improved Agent Searches (w/ Clue)", bottom=testMovements[improvedMAMTWithClue.__name__], color="blue")
    plt.bar(ind + width * 3,
            testMovements[improvedMAMTWithClue.__name__], width, label="Improved Agent Movements (w/ Clue)", color="darkblue")
    plt.ylabel("Actions")
    plt.xlabel("Map")
    plt.title("Moving Agent, Moving Target")
    plt.xticks(ind + width * 1.5, list(range(1, maps + 1)))
    plt.legend(loc="best")
    plt.savefig("graphs/4.png")
    plt.close(figure)
    writeToFile(4, dataFile, rules, testMeans, testVariances, testActions)

    """
    Part Extra
    """
    rules = [rule3MAMTWithClue, rule3MAMTExtra,
             improvedMAMTWithClue, improvedMAMTExtra]
    testSearches, testMovements, testActions, testMeans, testVariances = testRules(
        rules, dim, maps, iterationsPerMap)
    figure = plt.figure(figsize=((10., 6.)))
    plt.bar(
        ind, testSearches[rule3MAMTWithClue.__name__], width, label="Rule 3 Searches (w/ Clue)", bottom=testMovements[rule3MAMTWithClue.__name__], color="red")
    plt.bar(
        ind, testMovements[rule3MAMTWithClue.__name__], width, label="Rule 3 Movements (w/ Clue)", color="darkred")
    plt.bar(ind + width,
            testSearches[rule3MAMTExtra.__name__], width, label="Rule 3 Searches (Extra)", bottom=testMovements[rule3MAMTExtra.__name__], color="gold")
    plt.bar(ind + width,
            testMovements[rule3MAMTExtra.__name__], width, label="Rule 3 Movements (Extra)", color="goldenrod")
    plt.bar(
        ind + width * 2, testSearches[improvedMAMTWithClue.__name__], width, label="Improved Agent Searches (w/ Clue)", bottom=testMovements[improvedMAMTWithClue.__name__], color="lightgreen")
    plt.bar(
        ind + width * 2, testMovements[improvedMAMTWithClue.__name__], width, label="Improved Agent Movements (w/ Clue)", color="green")
    plt.bar(ind + width * 3,
            testSearches[improvedMAMTExtra.__name__], width, label="Improved Agent Searches (Extra)", bottom=testMovements[improvedMAMTExtra.__name__], color="blue")
    plt.bar(ind + width * 3,
            testMovements[improvedMAMTExtra.__name__], width, label="Improved Agent Movements (Extra)", color="darkblue")
    plt.ylabel("Actions")
    plt.xlabel("Map")
    plt.title("Moving Agent, Moving Target (Extra)")
    plt.xticks(ind + width * 1.5, list(range(1, maps + 1)))
    plt.legend(loc="best")
    plt.savefig("graphs/5.png")
    plt.close(figure)
    writeToFile(5, dataFile, rules, testMeans, testVariances, testActions)

    dataFile.write("\n\n")
    dataFile.close()
