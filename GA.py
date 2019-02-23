from __future__ import division
import random as rand
import math
from itertools import permutations as perm
from sys import exit

D = 9
POPULATION_SIZE = 12
sqr = int(math.sqrt(D))
MUTATION_RATE = 0.2


def init():
    popList = []
    while len(popList) < POPULATION_SIZE:
        temp0 = []
        while len(temp0) < D:
            temp1 = []
            while len(temp1) < D:
                val = rand.randrange(1,D + 1)
                if(val not in temp1):
                    temp1.append(val)
            if temp1 not in temp0:
                temp0.append(temp1)
        if temp0 not in popList:
            popList.append(temp0)
    return popList


def weighted_random_choice(choices):
    max = sum(choices.values())
    pick = rand.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key


def split_first_part(parent, whichSquare, whichIndex):
    parentFirstPart = []
    #next completed squares
    for i in range(whichSquare):
        for value in parent[i]:
            parentFirstPart.append(value)

    #an uncompleted square
    for i in range(whichIndex):
        parentFirstPart.append(parent[whichSquare][i])
    return parentFirstPart


def split_second_part(parent, whichSquare, whichIndex):
    ##an uncompleted square
    parentScondPart = []
    for i in range(whichIndex, D):
        parentScondPart.append(parent[whichSquare][i])

    #next completed squares
    for i in range(whichSquare + 1, D):
        for value in parent[i]:
            parentScondPart.append(value)

    return parentScondPart


def rubuild_chromosome(chromoStr):
    temp = list(chromoStr)
    chromosome = []
    for val in temp:
        chromosome.append(int(val))
    result = []
    for i in range(D):
        result.append(chromosome[i*D: (i+1)*D])
    return result

def printSol(chromosome):
    cnt = 0
    for i in range(0, D, sqr):
        for k in range(0, D, sqr ):
            temp = []
            for j in range(i, i + sqr):
                for l in range(k, k + sqr):
                    temp.append(chromosome[j][l])
                cnt = cnt + 1
                if cnt % sqr == 0:
                    print temp

def split_choice(selectedParent0, selectedParent1):
    splitPoint = rand.randrange(0, D*D)
    # splitPoint = int(D*D/2)
    whichSquare = int(splitPoint/D)
    #its index in the last selected square
    whichIndex = splitPoint % D

    parent0FirstPart = split_first_part(selectedParent0, whichSquare, whichIndex)
    parent1FirstPart = split_first_part(selectedParent1, whichSquare, whichIndex)

    parent0SecondPart = split_second_part(selectedParent0, whichSquare, whichIndex)
    parent1SecondPart = split_second_part(selectedParent1, whichSquare, whichIndex)

    firstChild = parent0FirstPart + parent1SecondPart
    secondChild = parent1FirstPart + parent0SecondPart

    return firstChild, secondChild



def mutation(chromosome):
    listOfRands = []
    while len(listOfRands) < 4:
        temp = rand.randrange(0, D*D)
        if temp not in listOfRands:
            listOfRands.append(temp)
    whichSquare0 = int(listOfRands[0] / D)
    whichSquare1 = int(listOfRands[1] / D)
    whichIndex0 = int(listOfRands[0] % D)
    whichIndex1 = int(listOfRands[1] % D)

    whichSquare2 = int(listOfRands[2] / D)
    whichSquare3 = int(listOfRands[3] / D)
    whichIndex2 = int(listOfRands[2] % D)
    whichIndex3 = int(listOfRands[3] % D)

    temp = chromosome[whichSquare0][whichIndex0]
    chromosome[whichSquare0][whichIndex0] = chromosome[whichSquare1][whichIndex1]
    chromosome[whichSquare1][whichIndex1] = temp

    temp = chromosome[whichSquare2][whichIndex2]
    chromosome[whichSquare2][whichIndex2] = chromosome[whichSquare3][whichIndex3]
    chromosome[whichSquare3][whichIndex3] = temp

    return chromosome

def fitness_population(popList, popStrList):
    result = {}

    for idx, chromosome in enumerate(popList):
        cnt = 0
        result[popStrList[idx]] = fitness_chromosome(chromosome)

    return result


def fitness_chromosome(chromosome):
    cnt = 0
    for i in range(0, D, sqr):
        for k in range(0, D, sqr ):
            temp = []
            for j in range(i, i + sqr):
                for l in range(k, k + sqr):
                    temp.append(chromosome[j][l])
            for m in range(1, D + 1):
                if temp.count(m) >= 2:
                    cnt = cnt + temp.count(m) - 1
    #col
    for i in range(0, int(D/sqr)):
        for k in range(0, int(D/sqr) ):
            temp = []
            for j in range(i, D, sqr):
                for l in range(k, D, sqr):
                    temp.append(chromosome[j][l])
            for m in range(1, D + 1):
                if temp.count(m) >= 2:
                    cnt = cnt + temp.count(m) - 1
    for val in chromosome:
        for i in range(1, D+1):
            if val.count(i) >= 2:
                cnt = cnt + val.count(i) - 1
    return 1/(1+cnt)


# python does not recognize list as a candidate key -_-
def convert_list_to_string(popList):
    popStr = []
    for chromosome in popList:
        tempStr = ""
        for square in chromosome:
            for val in square:
                tempStr = tempStr + str(val)
        popStr.append(tempStr)

    return popStr


def main():
    solved = False
    popList = init()
    cnt = 0
    while(True):
        cnt = cnt + 1
        if cnt == 100000:
            popList = init()
        popStrList = convert_list_to_string(popList)
        fitnesses = fitness_population(popList, popStrList)
        print fitnesses
        sortedValues = []
        # lastBestFitness = 0
        for key, val in fitnesses.items():
            sortedValues.append(val)
            if val == 1:
                print "Solved!"
                printSol(key)
                break

        sortedValues.sort()
        worstFitnesses = []
        for key, val in fitnesses.items():
            if len(worstFitnesses) == 2: break
            if sortedValues[0] == val or sortedValues[1] == val:
                worstFitnesses.append(key)


        temp = worstFitnesses[0]
        worstFitnesses[0] = rubuild_chromosome(temp)
        temp = worstFitnesses[1]
        worstFitnesses[1] = rubuild_chromosome(temp)


        father = weighted_random_choice(fitnesses)
        temp = fitnesses
        del temp[father]
        mother = weighted_random_choice(temp)
        children = split_choice(rubuild_chromosome(father), rubuild_chromosome(mother))
        firstChild = rubuild_chromosome(children[0])
        secondChild = rubuild_chromosome(children[1])

        firstChildFit = fitness_chromosome(firstChild)
        print "first child fit is: ", firstChildFit
        secChildFit = fitness_chromosome(firstChild)
        print "second child fit is: ", secChildFit
        if firstChildFit == 1:
            print "Solved!"
            printSol(firstChild)
            break

        if secChildFit == 1:
            print "Solved!"
            printSol(secondChild)
            break

        for idx, val in enumerate(popList):
            if val == worstFitnesses[0]:
                if fitness_chromosome(worstFitnesses[0]) < firstChildFit and firstChild not in popList:
                    popList[idx] = firstChild
            elif val == worstFitnesses[1]:
                if fitness_chromosome(worstFitnesses[1]) < secChildFit and secondChild not in popList:
                    popList[idx] = secondChild

        rr = rand.randrange(0, 100)
        if MUTATION_RATE * 100 >= rr:
            firstChild = mutation(firstChild)
            secondChild = mutation(secondChild)

            firstChildFit = fitness_chromosome(firstChild)
            print "first child fit after mutation is: ", firstChildFit
            secChildFit = fitness_chromosome(firstChild)
            print "second child fit after mutation is: ", secChildFit

            if firstChildFit == 1:
                print "Solved"
                printSol(firstChild)
                break

            if secChildFit == 1:
                print "Solved"
                printSol(secondChild)
                break

            sortedValues = []
            for key, val in fitnesses.items():
                sortedValues.append(val)
                if val == 1:
                    print "Solved"
                    printSol(key)
                    break

            sortedValues.sort()
            worstFitnesses = []
            for key, val in fitnesses.items():
                if len(worstFitnesses) == 2: break
                if sortedValues[0] == val or sortedValues[1] == val:
                    worstFitnesses.append(key)

            temp = worstFitnesses[0]
            worstFitnesses[0] = rubuild_chromosome(temp)
            temp = worstFitnesses[1]
            worstFitnesses[1] = rubuild_chromosome(temp)


        for idx, val in enumerate(popList):
            if val == worstFitnesses[0]:
                if fitness_chromosome(worstFitnesses[0]) < firstChildFit and firstChild not in popList:
                    popList[idx] = firstChild
            elif val == worstFitnesses[1]:
                if fitness_chromosome(worstFitnesses[1]) < secChildFit and secondChild not in popList:
                    popList[idx] = secondChild


if __name__ == '__main__':
    main()
