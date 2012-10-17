import cProfile
import sys
import lcs


lcsret = ''
cProfile.run(sys.argv[1])
print '#lcsret: ' + lcsret
print '#rcalls: ' + str(lcs.global_rcalls)
