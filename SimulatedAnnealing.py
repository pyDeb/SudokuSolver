from __future__ import division
import random as rand
import math

D = 9
sqr = int(math.sqrt(D))
ALPHA = 0.2

def init():
    firstState = []
    while len(firstState) < D:
        temp1 = []
        while len(temp1) < D:
            val = rand.randrange(1,D + 1)
            if(val not in temp1):
                temp1.append(val)
        if temp1 not in firstState:
            firstState.append(temp1)

    return firstState



def randomMove(state):
    randVals = []
    while len(randVals) < 2:
        r = rand.randrange(0, D*D)
        if r not in randVals:
            randVals.append(r)
    whichSquare0 = int(randVals[0] / D)
    whichSquare1 = int(randVals[1] / D)
    whichIndex0 = int(randVals[0] % D)
    whichIndex1 = int(randVals[1] % D)

    temp = state[whichSquare0][whichIndex0]
    state[whichSquare0][whichIndex0] = state[whichSquare1][whichIndex1]
    state[whichSquare1][whichIndex1] = temp

    return state


def calcScore(state):
    cnt = 0
    for i in range(0, D, sqr):
        for k in range(0, D, sqr ):
            temp = []
            for j in range(i, i + sqr):
                for l in range(k, k + sqr):
                    temp.append(state[j][l])
            for m in range(1, D + 1):
                if temp.count(m) >= 2:
                    cnt = cnt + temp.count(m) - 1
    #col
    for i in range(0, int(D/sqr)):
        for k in range(0, int(D/sqr) ):
            temp = []
            for j in range(i, D, sqr):
                for l in range(k, D, sqr):
                    temp.append(state[j][l])
            for m in range(1, D + 1):
                if temp.count(m) >= 2:
                    cnt = cnt + temp.count(m) - 1
    for val in state:
        for i in range(1, D+1):
            if val.count(i) >= 2:
                cnt = cnt + val.count(i) - 1
    return 1/(1+cnt)


def rubuild_chromosome(chromoStr):
    temp = list(chromoStr)
    chromosome = []
    for val in temp:
        chromosome.append(int(val))
    result = []
    for i in range(D):
        result.append(chromosome[i*D: (i+1)*D])
    return result


def printSol(state):
    cnt = 0
    for i in range(0, D, sqr):
        for k in range(0, D, sqr ):
            temp = []
            for j in range(i, i + sqr):
                for l in range(k, k + sqr):
                    temp.append(state[j][l])
                cnt = cnt + 1
                if cnt % sqr == 0:
                    print temp
def main():
    cnt = 0
    state = init()
    while(True):
        if cnt == 1000000:
            cnt = 1
            state = init()
        currentScore = calcScore(state)
        if currentScore == 1:
            print "solved\n\n"
            printSol(state)
            break

        tempStr = ""
        for square in state:
            for val in square:
                tempStr = tempStr + str(val)
        newState = randomMove(state)
        state = rubuild_chromosome(tempStr)
        newScore = calcScore(newState)


        if newScore == 1:
            print "solved\n\n"
            printSol(newState)
            break

        if newScore > currentScore:
            cnt = cnt + 1
            state = newState


        else:##e^(alpha * abs(F(x0) - F(x1)) * n)
            randomScore = math.pow(math.e, -1*ALPHA * (abs(newScore - currentScore) * cnt))
            r = rand.uniform(0, 1)
            if r < randomScore:
                cnt = cnt + 1
                state = newState




if __name__ == '__main__':
    main()
