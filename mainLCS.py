import sys
import StressTester as stress
import profilelcs as profiler
import lcs
import random

#the LCS methods avaiable
lcsMethods = {'n': (lcs.naiveGetLCS, 'Naive LCS'),\
              'm': (lcs.memoizedGetLCS, 'memoized LCS'),\
              'd': (lcs.dynamicGetLCS, 'dynamic LCS'),\
              'q': (lcs.hirshbergGetLCS, 'hirshberg LCS')}

#usage: python mainLCS {nmdq} {s|r|i S1 S2}
#nmdq are the args indicating the algorithm(s) to run on
#s indicates a stress test to check the max size string that can run in 10 sec
#r indicates to choose a random string to run on
#i indicates to run on the input strings S1 and S2

if len(sys.argv) >= 3:
    #Get the list of algorithms to run
    algList = list(sys.argv[1])
    #run the correct function
    if sys.argv[2] == 's':
        for lcsMethod in algList:
            print 'Finding length n strings to get close to ~10 seconds computation for algorithm ', lcsMethods[lcsMethod][1]
            stress.run(lcsMethods[lcsMethod][0])
    elif sys.argv[2] == 'r':
        #generate a random sequence of 0 and 1 characters
        choiceList = []
        if random.random() > 0.5:
            choiceList = ['0', '1']
        else:
            choiceList = ['A', 'C', 'G', 'T']
        first = ''.join(random.choice(choiceList) for x in range(random.randint(1, 20)))
        second = ''.join(random.choice(choiceList) for x in range(random.randint(1, 20)))
        for lcsMethod in algList:
            print 'Finding the LCS for Strings:"' + first + '" "' + second + '"\n\t with algorithm: ', lcsMethods[lcsMethod][1]
            print profiler.run(lcsMethods[lcsMethod][0], first, second)[1]
    elif sys.argv[2] == 'i':
        if len(sys.argv) >= 5:
            first = sys.argv[3]
            second = sys.argv[4]
            for lcsMethod in algList:
                print 'Finding the LCS for Strings:"' + first + '" "' + second + '"\n\t with algorithm: ', lcsMethods[lcsMethod][1]
                print profiler.run(lcsMethods[lcsMethod][0], first, second)[1]
        else:
            print 'usage: python mainLCS {nmdq} {s|r|i S1 S2}'
else:
    print 'usage: python mainLCS {nmdq} {s|r|i S1 S2}'
