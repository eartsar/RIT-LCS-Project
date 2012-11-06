import sys
import StressTester as stress
import profilelcs as profiler
import lcs
import random
import string

#the LCS methods avaiable
lcsMethods = {'n': (lcs.naiveGetLCS, 'Naive LCS'),\
              'm': (lcs.memoizedGetLCS, 'memoized LCS'),\
              'd': (lcs.dynamicGetLCS, 'dynamic LCS'),\
              'q': (lcs.hirshbergGetLCS, 'hirshberg LCS')}

#usage: python mainLCS {nmdq} {s [SL ][v ] | r [maxS1L ][maxS2L ][minS1L ][minS2L] | i S1 S2 | a SL AL}
#nmdq are the args indicating the algorithm(s) to run on
#s indicates a stress test to check the max size string that can run in 10 sec
#r indicates to choose a random string to run on
#i indicates to run on the input strings S1 and S2
#a indicates to test avg time to find LCS of random string of length SL generated from an alphabet of length AL

if len(sys.argv) >= 3:
    #Get the list of algorithms to run
    algList = list(sys.argv[1])

    sys.setrecursionlimit(10000) #Allow for deeper recursion
    #run the correct function
    if sys.argv[2] == 's':
	verbose = False
	fixedLength = -1
	if len(sys.argv) >= 4 and sys.argv[3] != 'v':
		fixedLength =int(sys.argv[3])
        if sys.argv[-1]=='v':
		verbose =True
        for lcsMethod in algList:
            if fixedLength <= -1:
                print 'Finding length n strings to get close to ~10 seconds computation for algorithm ', lcsMethods[lcsMethod][1]
                stress.run(lcsMethods[lcsMethod][0],verbose)
            else:
                first = '0' * fixedLength
                second = '1' * fixedLength
                print 'Using length',fixedLength,'strings to stress test for algorithm ', lcsMethods[lcsMethod][1]
                print profiler.run(lcsMethods[lcsMethod][0], first, second)[1]

    elif sys.argv[2] == 'r':
	maxLengthFirst = 20
	minLengthFirst = 1
	maxLengthSecond = 20
	minLengthSecond = 1
	if len(sys.argv) >= 4:
		maxLengthFirst = int(sys.argv[3])
	if len(sys.argv) >= 5:
		maxLengthSecond = int(sys.argv[4])
	if len(sys.argv) >= 6:
		minLengthFirst = int(sys.argv[5])
	if len(sys.argv) >= 7:
		minLengthSecond = int(sys.argv[6])
        #generate a random sequence of 0 and 1 characters
        choiceList = []
        if random.random() > 0.5:
            choiceList = ['0', '1']
        else:
            choiceList = ['A', 'C', 'G', 'T']
	if len(sys.argv) >= 8:
		choiceList = [str(x) for x in range(int(sys.argv[7]))]
        first = ''.join(random.choice(choiceList) for x in range(random.randint(minLengthFirst, maxLengthFirst)))
        second = ''.join(random.choice(choiceList) for x in range(random.randint(minLengthSecond, maxLengthSecond)))
        for lcsMethod in algList:
            print 'Finding the LCS for Strings:"' + first + '" "' + second + '"\n\t with algorithm: ', lcsMethods[lcsMethod][1]
            print profiler.run(lcsMethods[lcsMethod][0], first, second)[1] 
    elif sys.argv[2] == 'a':
	length = 20
        alphabetLength = 5
	if len(sys.argv) >= 4:
		length = int(sys.argv[3])
	if len(sys.argv) >= 5:
		alphabetLength = int(sys.argv[4])
        choiceList = [string.printable[x] for x in range(alphabetLength)]
        for lcsMethod in algList:
            print 'Finding avg time for alphabet ',choiceList,' with algorithm: ', lcsMethods[lcsMethod][1]
            i = 0
            total = 0
            while i < 10:
                first = ''.join(random.choice(choiceList) for x in range(random.randint(length, length)))
                second = ''.join(random.choice(choiceList) for x in range(random.randint(length, length)))
                total += float(profiler.run(lcsMethods[lcsMethod][0], first, second)[0])
                i+=1
            avg = total/10.0
            print 'Average CPU time: ',avg
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
    print 'usage: python mainLCS {nmdq} {s [SL ][v ] | r [maxS1L ][maxS2L ][minS1L ][minS2L] | i S1 S2 | a SL AL}'
